import asyncio
import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Optional

from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3
from web3.contract.contract import ContractFunction
from web3.datastructures import AttributeDict
from web3.types import TxReceipt

mutexes = defaultdict(asyncio.Lock)
mutex_dict_mutex = asyncio.Lock()
nonce_mutexes = defaultdict(asyncio.Lock)
nm_dict_mutex = asyncio.Lock()
current_nonce = defaultdict(int)

async def ensure_approval(w3: Web3, public_address, spender_address, src_usdc_address, usdc_amount: int, private_key):
    with Path("./test-python/arb-contract/ApproveAllowABI.json").open() as f:
        file_str = f.read()
    
    json_object = json.loads(file_str)
    
    contract = w3.eth.contract(
        address=src_usdc_address, abi=json_object
    )
    try:
        allowance_func = contract.functions.allowance(
            public_address, 
            spender_address,
        )
    except Exception as e:
        raise ValueError(f"failed to build allowance function: {e}") from e
    
    try:
        allowance = await asyncio.to_thread(allowance_func.call)
    except Exception as e:
        raise ConnectionError(f"failed to get allowance: {e}") from e
    
    if allowance >= usdc_amount:
        return
    
    try:
        approve_func = contract.functions.approve(
            spender_address,
            usdc_amount,
        )
    except Exception as e:
        raise ValueError(f"failed to build approve function: {e}") from e
    
    try: 
        tx_hash = await safe_build_and_send_tx(
            w3,
            private_key,
            public_address,
            approve_func,
        )
        print("f{tx_hash}")
    except Exception as e:
        raise ValueError(f"failed to send approve tx: {e}") from e
    
    return tx_hash

async def _get_mutex(chain_id: int, public_address: ChecksumAddress):
    checksummed_address = Web3.to_checksum_address(public_address)
    key = (chain_id, checksummed_address)
    async with mutex_dict_mutex:
        if key not in mutexes:
            mutexes[key] = asyncio.Lock()
        return mutexes[key]


async def _get_nonce_mutex(chain_id: int, public_address: ChecksumAddress):
    checksummed_address = Web3.to_checksum_address(public_address)
    key = (chain_id, checksummed_address)
    async with nm_dict_mutex:
        if key not in nonce_mutexes:
            nonce_mutexes[key] = asyncio.Lock()
        return nonce_mutexes[key]


async def _get_current_nonce(web3: Web3, public_address: ChecksumAddress, increment: bool = True):
    chain_id = web3.eth.chain_id
    mutex = await _get_nonce_mutex(chain_id, public_address)
    async with mutex:
        checksummed_address = Web3.to_checksum_address(public_address)
        key = (chain_id, checksummed_address)
        remote_nonce = await asyncio.to_thread(web3.eth.get_transaction_count, public_address, "pending")
        local_nonce = 0

        if key in current_nonce:
            local_nonce = current_nonce[key]

        if local_nonce is None or local_nonce < remote_nonce:
            current_nonce[key] = remote_nonce
            local_nonce = remote_nonce

        if increment:
            current_nonce[key] += 1

        return local_nonce


async def _increment_nonce(web3: Web3, public_address: ChecksumAddress, increment: int = 1):
    chain_id = web3.eth.chain_id
    mutex = await _get_nonce_mutex(chain_id, public_address)
    async with mutex:
        checksummed_address = Web3.to_checksum_address(public_address)
        key = (chain_id, checksummed_address)
        if key in current_nonce:
            current_nonce[key] += increment


class _HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        if isinstance(obj, AttributeDict):
            return {key: (self.default(value) if isinstance(value, (HexBytes, AttributeDict)) else value) for key, value in obj.items()}
        if isinstance(obj, dict):
            return {key: (self.default(value) if isinstance(value, (HexBytes, AttributeDict)) else value) for key, value in obj.items()}
        return super().default(obj)


async def wait_for_tx_receipt(web3: Web3, tx_hash: HexBytes, timeout: int = 120) -> TxReceipt:
    # wait for the tx receipt
    try:
        tx_receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=timeout)
    except Exception as e:
        raise ConnectionError(f"failed to get tx receipt: {e}") from e

    return tx_receipt


def legacy_tx_params(
    from_address: ChecksumAddress,
    nonce: int,
    gas_price: int,
    chain_id: int,
    gas: int = 1500000,
    value: int = 0,
):
    return {
        "from": from_address,
        "gas": gas,
        "nonce": nonce,
        "value": value,
        "gasPrice": gas_price,
        "chainId": chain_id,
    }


async def unsafe_build_tx_params(
    web3: Web3,
    public_address: ChecksumAddress,
    func: ContractFunction,
    nonce=None,
    gas_buffer: int = 0,
    gas: Optional[int] = None,
):
    # get the nonce
    if nonce is None:
        try:
            nonce = asyncio.to_thread(web3.eth.get_transaction_count, public_address, "pending")
        except Exception as e:
            raise ConnectionError(f"failed to fetch nonce: {e}") from e

    # estimate gas
    if gas is None:
        try:
            gas_estimate = await asyncio.to_thread(func.estimate_gas, {"from": public_address, "value": 0})
        except Exception as e:
            logging.error(f"failed to estimate gas, falling back to 2,000,000 gas: {e}")
            gas_estimate = 2000000
            # raise ValueError(f"failed to estimate gas: {e}")
    else:
        gas_estimate = gas

    # fetch gas price
    try:
        gas_price = web3.eth.gas_price + gas_buffer
    except Exception as e:
        raise ConnectionError(f"failed to fetch gas price: {e}") from e

    gas_price = int(gas_price * 1.2)

    # create params
    chain_id = web3.eth.chain_id
    params = legacy_tx_params(public_address, nonce, gas_price, chain_id, gas_estimate)

    return params


async def unsafe_send_transaction(web3: Web3, private_key: str, func: ContractFunction, params) -> HexBytes:
    # build the transaction
    if func is None:
        unsigned_tx = params
    else:
        try:
            unsigned_tx = func.build_transaction(params)
        except Exception as e:
            raise ValueError(f"failed to build transaction: {e}") from e

    # sign the transaction
    try:
        signed_tx = web3.eth.account.sign_transaction(unsigned_tx, private_key=private_key)
    except Exception as e:
        raise ValueError(f"failed to sign transaction: {e}") from e

    # send the transaction
    try:
        sent_tx = await asyncio.to_thread(web3.eth.send_raw_transaction, signed_tx.rawTransaction)
        return sent_tx
    except Exception as e:
        raise ConnectionError(f"failed to send raw transaction: {e}") from e


async def unsafe_build_and_send_tx(
    web3: Web3,
    private_key: str,
    public_address: ChecksumAddress,
    func: ContractFunction,
    nonce: Optional[int] = None,
    gas_buffer: int = 0,
    gas: Optional[int] = None,
):
    # build tx params
    try:
        tx_params = await unsafe_build_tx_params(web3, public_address, func, nonce=nonce, gas_buffer=gas_buffer, gas=gas)
    except Exception as e:
        raise ConnectionError(f"failed to build tx params: {e}") from e

    # send transaction
    try:
        tx_hash = await unsafe_send_transaction(web3, private_key, func, tx_params)
    except Exception as e:
        raise ConnectionError(f"failed to send transaction: {e}") from e

    # return transaction hash
    return tx_hash


async def safe_build_and_send_tx(
    web3: Web3,
    private_key: str,
    public_address: ChecksumAddress,
    func: ContractFunction,
    gas_buffer: int = 0,
    gas: Optional[int] = None,
    force_execute=False,
    value: int = 0,
) -> HexBytes:
    # get the mutex
    address_mutex = await _get_mutex(web3.eth.chain_id, public_address)

    # acquire the mutex
    async with address_mutex:
        # get the nonce
        try:
            nonce = await _get_current_nonce(web3, public_address)
        except Exception as e:
            raise ConnectionError(f"failed to fetch nonce: {e}") from e

        # estimate gas
        if gas is None:
            try:
                gas_estimate = await asyncio.to_thread(
                    func.estimate_gas,
                    {
                        "from": public_address,
                        "value": value,
                        "chainId": web3.eth.chain_id,
                        "nonce": nonce,
                    },
                )
                gas_estimate = int(gas_estimate * 1.15)
            except Exception as e:
                if force_execute and "Slippage" not in str(e):
                    gas_estimate = 2000000
                else:
                    await _increment_nonce(web3, public_address, increment=-1)
                    raise ValueError(f"failed to estimate gas, execution is expected to fail: {e}") from e
        else:
            gas_estimate = gas

        # fetch gas price
        try:
            gas_price = web3.eth.gas_price + gas_buffer
        except Exception as e:
            await _increment_nonce(web3, public_address, increment=-1)
            raise ConnectionError(f"failed to fetch gas price: {e}") from e

        gas_price = int(gas_price * 1.15)

        # create params
        chain_id = web3.eth.chain_id
        params = legacy_tx_params(public_address, nonce, gas_price, chain_id, gas_estimate, value=value)

        # send the transaction
        try:
            tx_hash = await unsafe_send_transaction(web3, private_key, func, params)
        except Exception as e:
            await _increment_nonce(web3, public_address, increment=-1)
            raise ConnectionError(f"failed to send transaction: {e}") from e

    # return transaction hash
    return tx_hash


async def safe_send_value(
    web3: Web3,
    private_key: str,
    public_address: ChecksumAddress,
    target_address: ChecksumAddress,
    gas_buffer: Optional[int] = 0,
    gas: Optional[int] = None,
    force_execute=False,
    value: int = 0,
) -> HexBytes:
    # get the mutex
    address_mutex = await _get_mutex(web3.eth.chain_id, public_address)

    # acquire the mutex
    async with address_mutex:
        # get the nonce
        try:
            nonce = await _get_current_nonce(web3, public_address)
        except Exception as e:
            raise ConnectionError(f"failed to fetch nonce: {e}") from e

        # estimate gas
        if gas is None:
            try:
                gas_estimate = await asyncio.to_thread(
                    web3.eth.estimate_gas,
                    {
                        "from": public_address,
                        "to": target_address,
                        "value": value,
                        "nonce": nonce,
                    },
                )
                gas_estimate = int(gas_estimate * 1.3)
            except Exception as e:
                if force_execute and "Slippage" not in str(e):
                    gas_estimate = 2000000
                else:
                    await _increment_nonce(web3, public_address, increment=-1)
                    raise ValueError(f"failed to estimate gas, execution is expected to fail: {e}") from e
        else:
            gas_estimate = gas

        # fetch gas price
        try:
            gas_price = web3.eth.gas_price + gas_buffer
        except Exception as e:
            await _increment_nonce(web3, public_address, increment=-1)
            raise ConnectionError(f"failed to fetch gas price: {e}") from e

        gas_price = int(gas_price * 1.15)

        # create params
        chain_id = web3.eth.chain_id
        params = legacy_tx_params(public_address, nonce, gas_price, chain_id, gas_estimate, value=value)
        params["to"] = target_address

        # send the transaction
        try:
            tx_hash = await unsafe_send_transaction(web3, private_key, None, params)
        except Exception as e:
            await _increment_nonce(web3, public_address, increment=-1)
            raise ConnectionError(f"failed to send transaction: {e}") from e

    # return transaction hash
    return tx_hash


async def receipt_to_json(tx_receipt: TxReceipt):
    receipt_dict = dict(tx_receipt)
    return json.dumps(receipt_dict, cls=_HexJsonEncoder)


async def _sql_value(value):
    if value is None:
        return "NULL"

    if isinstance(value, str):
        return f"'{value}'"

    if isinstance(value, HexBytes):
        return f"'{value.hex()}'"

    return value


async def receipt_to_sql_struct(receipt: TxReceipt):
    json_receipt_str = await receipt_to_json(receipt)
    json_receipt = json.loads(json_receipt_str)

    log_structs = []

    for log in json_receipt.get("logs", []):
        address = await _sql_value(log.get("address", "NULL"))
        topics = await _sql_value(log.get("topics", "NULL"))
        data = await _sql_value(log.get("data", "NULL"))
        block_number = await _sql_value(log.get("blockNumber", "NULL"))
        transaction_hash = await _sql_value(log.get("transactionHash", "NULL"))
        transaction_index = await _sql_value(log.get("transactionIndex", "NULL"))
        block_hash = await _sql_value(log.get("blockHash", "NULL"))
        log_index = await _sql_value(log.get("logIndex", "NULL"))
        removed = await _sql_value(log.get("removed", "NULL"))

        log_struct = f"STRUCT(\n" f"    {address} AS address," f"    {topics} AS topics," f"    {data} AS data," f"    {block_number} AS blockNumber," f"    {transaction_hash} AS transactionHash," f"    {transaction_index} AS transactionIndex," f"    {block_hash} AS blockHash," f"    {log_index} AS logIndex," f"    {removed} AS removed" f")"

        log_structs.append(log_struct)

    log_array = f"[{', '.join(log_structs)}]"

    loaded_receipt = f"STRUCT(" f"    {await _sql_value(json_receipt.get('blockHash', 'NULL'))} AS blockHash," f"    {await _sql_value(json_receipt.get('blockNumber', 'NULL'))} AS blockNumber," f"    {await _sql_value(json_receipt.get('contractAddress', 'NULL'))} AS contractAddress," f"    {await _sql_value(json_receipt.get('cumulativeGasUsed', 'NULL'))} AS cumulativeGasUsed," f"    {await _sql_value(json_receipt.get('effectiveGasPrice', 'NULL'))} AS effectiveGasPrice," f"    {await _sql_value(json_receipt.get('from', 'NULL'))} AS fromAddress," f"    {await _sql_value(json_receipt.get('gasUsed', 'NULL'))} AS gasUsed," f"    {await _sql_value(json_receipt.get('l1Fee', 'NULL'))} AS l1Fee," f"    {await _sql_value(json_receipt.get('l1GasPrice', 'NULL'))} AS l1GasPrice," f"    {await _sql_value(json_receipt.get('l1GasUsed', 'NULL'))} AS l1GasUsed," f"    {log_array} AS logs, \n" f"    {await _sql_value(json_receipt.get('logsBloom', 'NULL'))} AS logsBloom," f"    {await _sql_value(json_receipt.get('status', 'NULL'))} AS status," f"    {await _sql_value(json_receipt.get('to', 'NULL'))} AS toAddress," f"    {await _sql_value(json_receipt.get('transactionHash', 'NULL'))} AS transactionHash," f"    {await _sql_value(json_receipt.get('transactionIndex', 'NULL'))} AS transactionIndex," f"    {await _sql_value(json_receipt.get('type', 'NULL'))} AS type" f")"

    return loaded_receipt


# receipt_sql_struct STRUCT<
#     blockHash STRING,
#     blockNumber INT64,
#     contractAddress STRING,
#     cumulativeGasUsed INT64,
#     effectiveGasPrice INT64,
#     fromAddress STRING,
#     gasUsed INT64,
#     l1Fee STRING,
#     l1GasPrice STRING,
#     l1GasUsed STRING,
#     logs ARRAY<STRUCT<
#         address STRING,
#         topics ARRAY<STRING>,
#         data STRING,
#         blockNumber INT64,
#         transactionHash STRING,
#         transactionIndex INT64,
#         blockHash STRING,
#         logIndex INT64,
#         removed BOOL
#     >>,
#     logsBloom STRING,
#     status INT64,
#     toAddress STRING,
#     transactionHash STRING,
#     transactionIndex INT64,
#     type INT64
# >,
