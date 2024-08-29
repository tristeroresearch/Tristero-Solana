import asyncio
from web3 import Web3
import os
import json
import time
import requests
from pathlib import Path
from script_tx_handler import safe_build_and_send_tx, unsafe_build_and_send_tx, unsafe_send_transaction
import binascii
import base58

def base58_to_uint8_array(base58_str: str) -> bytes:
    return base58.b58decode(base58_str)

contract_address = "0x587Cf236D1fbebb8FC4243F2c763F63Fa0dE801e"
private_key = "edf47a7dbe67be7960c6aba3606830bf19e0334cdb26a18e6d4715997c271445"
sol_test_eid = 40168
sol_oapp_addr = "C8SxWZ5eHRTyRUp5tLvq45BEfRybLQgnHS7t8RGbVGcK"
spl_token_mint_addr = base58_to_uint8_array("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")
erc20_token_mint_addr = "0x75faf114eafb1bdbe2f0316df893fd58ce46aa4d"


async def main():
        
    with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
        file_str = f.read()
    
    json_object = json.loads(file_str)
    
    rpc_url = "https://sepolia-rollup.arbitrum.io/rpc"
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    print(f"web3 is_connected: {web3.is_connected()}")
    
    deployed_contract = web3.eth.contract(
        address=contract_address, abi=json_object["abi"]
    )
    
    oapp_addr_uint8_array = base58_to_uint8_array(sol_oapp_addr)
    
    imported_account = web3.eth.account.from_key(private_key)
    web3.eth.default_account = imported_account.address
    erc20_token_mint = web3.to_checksum_address(erc20_token_mint_addr)
    
    
    print("---------------------------setPeer----------------------------------")
    set_peer = deployed_contract.functions.setPeer(sol_test_eid, oapp_addr_uint8_array)

    set_peer_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        web3.eth.default_account,
        set_peer,
    )
    set_peer_receipt = web3.eth.wait_for_transaction_receipt(set_peer_hash, timeout=60)
    
    print(f"set_peer_receipt: ", set_peer_receipt)
    
    print("---------------------------placeOrder----------------------------------")
    place_order = deployed_contract.functions.placeOrder(
        (erc20_token_mint, spl_token_mint_addr, sol_test_eid),
        (1000, 1000, 10, erc20_token_mint, int(100)),
        (int(time.time()) + 3600, 20, 40),
        False
    )

    place_order_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        web3.eth.default_account,
        place_order,
    )
    place_order_receipt = web3.eth.wait_for_transaction_receipt(place_order_hash, timeout=60)
    
    print(f"place_order_receipt: ", place_order_receipt)
    
    print("---------------------------startChallenge----------------------------------")
    start_challenge = deployed_contract.functions.startChallenge(
        (erc20_token_mint, spl_token_mint_addr, sol_test_eid),
        0
    )

    start_challenge_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        web3.eth.default_account,
        start_challenge,
    )
    start_challenge_receipt = web3.eth.wait_for_transaction_receipt(start_challenge_hash, timeout=60)
    
    print(f"start_challenge_receipt: ", start_challenge_receipt)
    
asyncio.run(main())