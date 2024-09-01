from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.compute_budget import set_compute_unit_limit
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from solders.instruction import AccountMeta
from solders.system_program import ID as SYS_PROGRAM_ID
from config import solana_contract_addr

from tristero.instructions.create_match import create_match, CreateMatchAccounts
from tristero.instructions.execute_match import execute_match, ExecuteMatchAccounts
from tristero.instructions.confirm_match import confirm_match, ConfirmMatchAccounts
from tristero.instructions.place_order import place_order, PlaceOrderAccounts
from tristero.instructions.start_challenge import start_challenge, StartChallengeAccounts
from tristero.instructions.finish_challenge import finish_challenge, FinishChallengeAccounts
from tristero.instructions.register_tristero_oapp import register_tristero_oapp, RegisterTristeroOappAccounts
from endpoint.instructions.init_nonce import init_nonce, InitNonceAccounts
from endpoint.instructions.init_send_library import init_send_library, InitSendLibraryAccounts
from endpoint.instructions.init_receive_library import init_receive_library, InitReceiveLibraryAccounts
from endpoint.instructions.init_config import init_config, InitConfigAccounts

from tristero.instructions.register_config import register_config, RegisterConfigAccounts

from tristero.types.create_match_params import CreateMatchParams, CreateMatchParamsJSON
from tristero.types.execute_match_params import ExecuteMatchParams, ExecuteMatchParamsJSON
from tristero.types.confirm_match_params import ConfirmMatchParams, ConfirmMatchParamsJSON
from tristero.types.place_order_params import PlaceOrderParams, PlaceOrderParamsJSON
from tristero.types.challenge_params import ChallengeParams, ChallengeParamsJSON
from tristero.types.finish_challenge_params import FinishChallengeParams, FinishChallengeParamsJSON
from tristero.types.register_tristero_o_app_params import RegisterTristeroOAppParams, RegisterTristeroOAppParamsJSON
from endpoint.types.init_nonce_params import InitNonceParams, InitNonceParamsJSON
from endpoint.types.init_send_library_params import InitSendLibraryParams, InitSendLibraryParamsJSON
from endpoint.types.init_receive_library_params import InitReceiveLibraryParams, InitReceiveLibraryParamsJSON
from endpoint.types.init_config_params import InitConfigParams, InitConfigParamsJSON

from tristero.accounts.admin_panel import AdminPanel
from endpoint.accounts.send_library_config import SendLibraryConfig

tristero_program_id = Pubkey.from_string(solana_contract_addr)
endpoint_program_id = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6")
executor_program_id = Pubkey.from_string("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn")
send_library_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")
price_fee_program_id = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP")
dvn_program_id = Pubkey.from_string("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW")
uln_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")

# Utils functions
def get_order_pda(order_id):
    order_id_buffer = order_id.to_bytes(8, byteorder="big")
    seeds = [
        b"order",
        order_id_buffer
    ]
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_refund_token_account_pda(pubkey):
    seeds = [
        b"refund_account",
        bytes(pubkey)
    ]
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_admin_panel():
    seeds = [
        b"admin_panel"
    ]
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_oapp_pda(authority):
    (distributor, bump) = Pubkey.find_program_address(
        [b"OApp", bytes(authority)],
        endpoint_program_id,
    )
    return distributor

def get_uln_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib"],
        uln_program_id,
    )
    return distributor

def get_tristero_oapp():
    (distributor, bump) = Pubkey.find_program_address(
        [b"TristeroOapp"],
        tristero_program_id,
    )
    return distributor

def get_tristero_oapp_bump():
    (distributor, bump) = Pubkey.find_program_address(
        [b"TristeroOapp"],
        tristero_program_id,
    )
    return bump

def get_message_lib_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib"],
        endpoint_program_id,
    )
    return distributor

def get_message_lib_info_pda(pubkey):
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib", bytes(pubkey)],
        endpoint_program_id,
    )
    return distributor

def get_oapp_registry_pda(pubkey):
    (distributor, bump) = Pubkey.find_program_address(
        [b"OApp", bytes(pubkey)],
        endpoint_program_id,
    )
    return distributor

def get_receive_library_config_pda(pubkey, eid):
    eid_bytes = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"ReceiveLibraryConfig", bytes(pubkey), eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_default_send_library_config(eid):
    eid_bytes = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_price_feed_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"PriceFeed"],
        price_fee_program_id,
    )
    return distributor

def get_staking_panel(mint):
    (distributor, bump) = Pubkey.find_program_address(
        [b"staking_account", bytes(mint)],
        tristero_program_id,
    )
    return distributor

def get_user_pda(authority):
    (distributor, bump) = Pubkey.find_program_address(
        [b"user", bytes(authority)],
        tristero_program_id,
    )
    return distributor

def get_trade_match_pda(match_count):
    match_count_bytes = match_count.to_bytes(8, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"trade_match", match_count_bytes],
        tristero_program_id,
    )
    return distributor

def get_send_library_config_pda(tristero_oapp, eid):
    eid_bytes = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", bytes(tristero_oapp), eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_default_send_library_config_pda(eid):
    eid_bytes = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_send_library_info_pda(send_library_info_pubkey):
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib", bytes(send_library_info_pubkey)],
        endpoint_program_id,
    )
    return distributor

def get_endpoint_pda():
    return Pubkey.find_program_address(
        [b"Endpoint"],
        endpoint_program_id,
    )[0]
    
def get_nonce_pda(sender_key, eid, receiver):
    eid_buffer = eid.to_bytes(4, byteorder="big")
    seeds = [
        b"Nonce",
        bytes(sender_key),
        eid_buffer,
        bytes(receiver)
    ]
    
    return Pubkey.find_program_address(seeds, endpoint_program_id)[0]

def get_pending_inbound_nonce_pda(sender_key, eid, receiver):
    eid_buffer = eid.to_bytes(4, byteorder="big")
    seeds = [
        b"PendingNonce",
        bytes(sender_key),
        eid_buffer,
        bytes(receiver)
    ]
    
    return Pubkey.find_program_address(seeds, endpoint_program_id)[0]

def get_event_authority_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"__event_authority"],
        endpoint_program_id,
    )
    return distributor

def get_uln_program_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib"],
        uln_program_id,
    )
    return distributor

def get_send_config_pda(eid, sender_addr):
    eid_buffer = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendConfig", eid_buffer, bytes(sender_addr)],
        uln_program_id,
    )
    return distributor

def get_receive_config_pda(eid, sender_addr):
    eid_buffer = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"ReceiveConfig", eid_buffer, bytes(sender_addr)],
        uln_program_id,
    )
    return distributor

def get_default_send_config_pda(eid):
    eid_buffer = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendConfig", eid_buffer],
        uln_program_id,
    )
    return distributor

def get_uln_event_authority_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"__event_authority"],
        uln_program_id,
    )
    return distributor

def get_executor_pda_deriver():
    (distributor, bump) = Pubkey.find_program_address(
        [b"ExecutorConfig"],
        executor_program_id,
    )
    return distributor

def get_price_fee_program_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"PriceFeed"],
        price_fee_program_id,
    )
    return distributor

def get_dvn_derive_config_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"DvnConfig"],
        dvn_program_id,
    )
    return distributor

def get_lz_receive_types_pda(oapp_config):
    (distributor, bump) = Pubkey.find_program_address(
        [b"LzReceiveTypes", bytes(oapp_config)],
        tristero_program_id,
    )
    return distributor

def get_receipt_pda(receiver, ind):
    ind_bytes = ind.to_bytes(8, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"receipt", bytes(receiver), ind_bytes],
        tristero_program_id,
    )
    return distributor

# Configuration functions
async def sol_register_new_oapp(solana_url, admin: Keypair):
    solana_client = Client(solana_url)
    admin_panel_pda = get_admin_panel()
    tristero_oapp_pubkey = get_tristero_oapp()
    
    print(f"--------------------------Register New Oapp------------------------------")
    register_oapp_accounts: RegisterTristeroOappAccounts = {
        "payer": admin.pubkey(),
        "oapp": tristero_oapp_pubkey,
        "admin_panel": admin_panel_pda,
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "event_authority": get_event_authority_pda(),
        "endpoint_program": endpoint_program_id
    }
    
    register_tristero_oapp_params_json : RegisterTristeroOAppParamsJSON = {
        "delegate": str(admin.pubkey()),
        "admin_wallet": str(admin.pubkey()),
        "payment_wallet": str(admin.pubkey())
    }
    
    register_tristero_oapp_params = RegisterTristeroOAppParams.from_json(register_tristero_oapp_params_json)
    register_tristero_oapp_ix = register_tristero_oapp(
        {
            "params": register_tristero_oapp_params
        },
        register_oapp_accounts,
        tristero_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(register_tristero_oapp_ix)
    
    register_tristero_oapp_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"register_tristero_oapp_tx: {register_tristero_oapp_tx}")
    print(f"tristero_oapp: ", tristero_oapp_pubkey)

async def sol_init_send_library(solana_url, admin: Keypair, dest_eid: int):
    solana_client = Client(solana_url)
    tristero_oapp_pubkey = get_tristero_oapp()
    print(f"-----------------------Init Send Library---------------------------")
    init_send_library_accounts: InitSendLibraryAccounts = {
        "delegate": admin.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "send_library_config": get_send_library_config_pda(tristero_oapp_pubkey, dest_eid),
    }
    
    init_send_library_params_json : InitSendLibraryParamsJSON = {
        "sender":  str(tristero_oapp_pubkey),
        "eid": dest_eid,
    }
    
    init_send_library_params = InitSendLibraryParams.from_json(init_send_library_params_json)
    
    init_send_library_ix = init_send_library(
        {
            "params": init_send_library_params
        },
        init_send_library_accounts,
        endpoint_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(init_send_library_ix)
    
    init_send_library_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"init_send_library_tx: {init_send_library_tx}")
    
async def sol_init_receive_library(solana_url, admin: Keypair, dest_eid: int):
    solana_client = Client(solana_url)
    tristero_oapp_pubkey = get_tristero_oapp()
    
    print(f"-----------------------Init Receive Library---------------------------")
    init_receive_library_accounts: InitReceiveLibraryAccounts = {
        "delegate": admin.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "receive_library_config": get_receive_library_config_pda(tristero_oapp_pubkey, dest_eid),
    }
    
    init_receive_library_params_json : InitReceiveLibraryParamsJSON = {
        "receiver": str(tristero_oapp_pubkey),
        "eid": dest_eid,
    }
    
    init_receive_library_params = InitReceiveLibraryParams.from_json(init_receive_library_params_json)
    
    init_receive_library_ix = init_receive_library(
        {
            "params": init_receive_library_params
        },
        init_receive_library_accounts,
        endpoint_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(init_receive_library_ix)
    
    init_receive_library_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"init_receive_library_tx: {init_receive_library_tx}")   

async def sol_init_nonce(solana_url, admin: Keypair, dest_eid: int, dest_oapp_addr):
    solana_client = Client(solana_url)
    tristero_oapp_pubkey = get_tristero_oapp()
    
    print(f"-----------------------Init Nonce---------------------------")
    print(f"get_nonce_pda(tristero_oapp_pubkey, ARBITRUM_EID, RECEIVER_PUBKEY) => {get_nonce_pda(tristero_oapp_pubkey, dest_eid, dest_oapp_addr)}")
    init_nonce_accounts: InitNonceAccounts = {
        "delegate": admin.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "nonce": get_nonce_pda(tristero_oapp_pubkey, dest_eid, dest_oapp_addr),
        "pending_inbound_nonce": get_pending_inbound_nonce_pda(tristero_oapp_pubkey, dest_eid, dest_oapp_addr)
    }
    
    init_nonce_params_json : InitNonceParamsJSON = {
        "local_oapp": str(tristero_oapp_pubkey),
        "remote_eid": dest_eid,
        "remote_oapp": dest_oapp_addr
    }
    
    init_nonce_params = InitNonceParams.from_json(init_nonce_params_json)
    
    init_nonce_ix = init_nonce(
        {
            "params": init_nonce_params
        },
        init_nonce_accounts,
        endpoint_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(init_nonce_ix)
    
    init_nonce_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"init_nonce_tx: {init_nonce_tx}")

async def sol_init_oft_config(solana_url, admin: Keypair, dest_eid: int):
    tristero_oapp_pubkey = get_tristero_oapp()
    solana_client = Client(solana_url)
    client = AsyncClient(solana_url)
    send_library_config = get_send_library_config_pda(tristero_oapp_pubkey, dest_eid)
    default_send_library_config = get_default_send_library_config(dest_eid)
    
    send_library_info_account = await SendLibraryConfig.fetch(client, default_send_library_config, program_id = endpoint_program_id)
    
    send_library_info_pubkey = send_library_info_account.message_lib
        
    print(f"---------------------Init Oft-Config------------------------")
    print(f"get_send_library_info_pda(send_library_info_pubkey) => {get_send_library_info_pda(send_library_info_pubkey)}")
    register_config_accounts: RegisterConfigAccounts = {
        "payer": admin.pubkey(),
        "oapp_config": tristero_oapp_pubkey,
        "lz_receive_types_accounts": get_lz_receive_types_pda(tristero_oapp_pubkey)
    }
    
    register_config_ix = register_config(
        {
            "param_pubkey": get_send_library_info_pda(send_library_info_pubkey)
        },
        register_config_accounts,
        tristero_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(register_config_ix)
    
    register_config_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"register_config_tx: {register_config_tx}")

async def sol_init_config(solana_url, admin: Keypair, dest_eid: int, dest_oapp_addr):
    solana_client = Client(solana_url)
    tristero_oapp_pubkey = get_tristero_oapp()
    message_lib_pubkey = get_message_lib_pda()
    
    print(f"-----------------------Init Config---------------------------")
    init_config_accounts: InitConfigAccounts = {
        "delegate": admin.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "message_lib_info": get_message_lib_info_pda(message_lib_pubkey),
        "message_lib": message_lib_pubkey,
        "message_lib_program": uln_program_id
    }
    
    init_config_remaining_accounts = [
        AccountMeta( #0
            pubkey = admin.pubkey(),
            is_signer = True,
            is_writable =  True
        ),
        AccountMeta( #1
            pubkey = message_lib_pubkey,
            is_signer = False,
            is_writable =  False
        ),
        AccountMeta( #2
            pubkey = get_send_config_pda(dest_eid, tristero_oapp_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #3
            pubkey = get_receive_config_pda(dest_eid, tristero_oapp_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #4
            pubkey = SYS_PROGRAM_ID,
            is_signer = False,
            is_writable =  True
        )
    ]
    
    init_config_params_json : InitConfigParamsJSON = {
        "oapp": str(tristero_oapp_pubkey),
        "eid": dest_eid
    }
    
    init_config_params = InitConfigParams.from_json(init_config_params_json)
    
    init_config_ix = init_config(
        {
            "params": init_config_params
        },
        init_config_accounts,
        endpoint_program_id,
        init_config_remaining_accounts
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [admin]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=admin.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(init_config_ix)
    
    init_config_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"init_config_tx: {init_config_tx}")


# Main Functions
async def sol_place_order(solana_url, user: Keypair, order_id: int, dest_eid: int, mint_addr: Pubkey, token_account: Pubkey, erc20_addr, src_quantity: int, dst_quantity: int, min_quantity: int):
    solana_client = Client(solana_url)
    admin_panel_pda = get_admin_panel()
    tristero_oapp_pubkey = get_tristero_oapp()
    
    print(f"-----------------------Place Order--------------------------")
    place_order_accounts: PlaceOrderAccounts = {
        "authority": user.pubkey(),
        "oapp": tristero_oapp_pubkey,
        "admin_panel": admin_panel_pda,
        "token_mint": mint_addr,
        "token_account": token_account,
        "staking_account": get_staking_panel(mint_addr),
        "order": get_order_pda(order_id)
    }
    
    place_order_params_json : PlaceOrderParamsJSON = {
        "source_sell_amount": src_quantity,
        "min_sell_amount": min_quantity,
        "dest_token_mint": erc20_addr,
        "dest_buy_amount": dst_quantity,
        "order_id": order_id,
        "eid": dest_eid
    }
    
    place_order_params = PlaceOrderParams.from_json(place_order_params_json)
    
    place_order_ix = place_order(
        {
            "params": place_order_params
        },
        place_order_accounts,
        tristero_program_id
    )
    
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(place_order_ix)
    
    place_order_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"place_order_tx: {place_order_tx}")
    print(f"order_id: :{order_id}")

async def sol_create_match(solana_url, user: Keypair, order_id: int, trade_match_id: int, arb_wallet_addr):
    solana_client = Client(solana_url)
    admin_panel_pda = get_admin_panel()
    
    # calling create_match instruction
    print(f"-----------------------Create Match--------------------------")
    create_match_accounts : CreateMatchAccounts = {
        "authority": user.pubkey(),
        "admin_panel": admin_panel_pda,
        "order": get_order_pda(order_id),
        "trade_match": get_trade_match_pda(trade_match_id)
    }
    
    create_match_params_json : CreateMatchParamsJSON = {
        "src_index": order_id,
        "dst_index": 7,
        "src_quantity": 100,
        "dst_quantity": 100,
        "trade_match_id": trade_match_id,
        "arb_source_token_addr": arb_wallet_addr
    }
    
    create_match_params = CreateMatchParams.from_json(create_match_params_json)
    
    create_match_ix = create_match(
        {
            "params": create_match_params
        },
        create_match_accounts,
        tristero_program_id
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(create_match_ix)
    
    create_match_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"create_match_tx: {create_match_tx}")
    print(f"match_id: {trade_match_id}")

async def sol_execute_match(solana_url, user: Keypair, src_token_addr: Pubkey, dst_token_addr: Pubkey, dst_eid: int, trade_match_id: int, quantity: int, dest_oapp_addr):
    solana_client = Client(solana_url)
    print(f"-----------------------Execute Match--------------------------")
    execute_match_accounts : ExecuteMatchAccounts = {
        "authority": user.pubkey(),
        "token_account": src_token_addr,
        "arb_user_token_account": dst_token_addr,
        "receipt": get_receipt_pda(dest_oapp_addr, trade_match_id)
    }
    
    execute_match_params_json : ExecuteMatchParamsJSON = {
        "dst_eid": dst_eid,
        "trade_match_id": trade_match_id,
        "source_sell_amount": quantity,
        "sender": dest_oapp_addr
    }
    
    execute_match_params = ExecuteMatchParams.from_json(execute_match_params_json)
    
    execute_match_ix = execute_match(
        {
            "params": execute_match_params
        },
        execute_match_accounts,
        tristero_program_id
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(execute_match_ix)
    
    execute_match_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"execute_match_tx: {execute_match_tx}")
    print(f"match_id: {trade_match_id}")

async def sol_confirm_match(solana_url, user: Keypair, token_account: Pubkey, token_mint_addr: Pubkey, order_id, trade_match_id):
    solana_client = Client(solana_url)
    tristero_oapp_pubkey = get_tristero_oapp()
    print(f"-----------------------Confirm Match--------------------------")
    confirm_match_accounts : ConfirmMatchAccounts = {
        "signer": user.pubkey(),
        "oapp": tristero_oapp_pubkey,
        "order": get_order_pda(order_id),
        "trade_match": get_trade_match_pda(trade_match_id),
        "token_account": token_account,
        "staking_account": get_staking_panel(token_mint_addr)
    }
    
    confirm_match_params_json : ConfirmMatchParamsJSON = {
        "trade_match_id": trade_match_id
    }
    
    confirm_match_params = ConfirmMatchParams.from_json(confirm_match_params_json)
    
    confirm_match_ix = confirm_match(
        {
            "params": confirm_match_params
        },
        confirm_match_accounts,
        tristero_program_id
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(confirm_match_ix)
    
    confirm_match_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"confirm_match_tx: {confirm_match_tx}")
    print(f"match_id: {trade_match_id}") 

async def sol_start_challenge(solana_url, user: Keypair, trade_match_id: int, dest_eid: int, taker, dest_oapp_addr):
    tristero_oapp_pubkey = get_tristero_oapp()
    solana_client = Client(solana_url)
    client = AsyncClient(solana_url)
    
    send_library_config = get_send_library_config_pda(tristero_oapp_pubkey, dest_eid)
    default_send_library_config = get_default_send_library_config(dest_eid)
    send_library_info_account = await SendLibraryConfig.fetch(client, default_send_library_config, program_id = endpoint_program_id)
    send_library_info_pubkey = send_library_info_account.message_lib
    send_instruction_remaining_accounts = [
        AccountMeta( #0
            pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #1
            pubkey = tristero_oapp_pubkey,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #2
            pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #3
            pubkey = send_library_config,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #4
            pubkey = default_send_library_config,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #5
            pubkey = get_send_library_info_pda(send_library_info_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #6
            pubkey = get_endpoint_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #7
            pubkey = get_nonce_pda(tristero_oapp_pubkey, dest_eid, dest_oapp_addr),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #8
            pubkey = get_event_authority_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #9
            pubkey = endpoint_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #10
            pubkey = get_uln_program_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #11
            pubkey = get_send_config_pda(dest_eid, tristero_oapp_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #12
            pubkey = get_default_send_config_pda(dest_eid),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #13
            pubkey = user.pubkey(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #14
            pubkey = user.pubkey(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #15
            pubkey = SYS_PROGRAM_ID,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #16
            pubkey = get_uln_event_authority_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #17
            pubkey = uln_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #18
            pubkey = executor_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #19
            pubkey = get_executor_pda_deriver(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #20
            pubkey = price_fee_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #21
            pubkey = get_price_fee_program_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #22
            pubkey = dvn_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #23
            pubkey = get_dvn_derive_config_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #24
            pubkey = price_fee_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #25
            pubkey = get_price_fee_program_pda(),
            is_signer = False,
            is_writable =  True
        )
    ]
    
    print(f"-------------------------Start Challenge----------------------------")
    
    start_challenge_accounts : StartChallengeAccounts = {
        "authority": user.pubkey(),
        "trade_match": get_trade_match_pda(trade_match_id)
    }
    
    start_challenge_params_json : ChallengeParamsJSON = {
        "trade_match_id": trade_match_id,
        "tristero_oapp_bump": get_tristero_oapp_bump(),
        "taker": taker,
        "receiver": dest_oapp_addr
    }
    
    start_challenge_params = ChallengeParams.from_json(start_challenge_params_json)
    
    start_challenge_ix = start_challenge(
        {
            "params": start_challenge_params
        },
        start_challenge_accounts,
        tristero_program_id,
        send_instruction_remaining_accounts
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(start_challenge_ix)
    
    start_challenge_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"challenge_tx: {start_challenge_tx}")

async def sol_finish_challenge(solana_url, user: Keypair, trade_match_id: int, dest_eid: int, spltoken, erc20token, dest_oapp_addr):
    tristero_oapp_pubkey = get_tristero_oapp()
    solana_client = Client(solana_url)
    client = AsyncClient(solana_url)
    send_library_config = get_send_library_config_pda(tristero_oapp_pubkey, dest_eid)
    default_send_library_config = get_default_send_library_config(dest_eid)
    send_library_info_account = await SendLibraryConfig.fetch(client, default_send_library_config, program_id = endpoint_program_id)
    send_library_info_pubkey = send_library_info_account.message_lib
    send_instruction_remaining_accounts = [
        AccountMeta( #0
            pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #1
            pubkey = tristero_oapp_pubkey,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #2
            pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #3
            pubkey = send_library_config,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #4
            pubkey = default_send_library_config,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #5
            pubkey = get_send_library_info_pda(send_library_info_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #6
            pubkey = get_endpoint_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #7
            pubkey = get_nonce_pda(tristero_oapp_pubkey, dest_eid, dest_oapp_addr),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #8
            pubkey = get_event_authority_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #9
            pubkey = endpoint_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #10
            pubkey = get_uln_program_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #11
            pubkey = get_send_config_pda(dest_eid, tristero_oapp_pubkey),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #12
            pubkey = get_default_send_config_pda(dest_eid),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #13
            pubkey = user.pubkey(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #14
            pubkey = user.pubkey(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #15
            pubkey = SYS_PROGRAM_ID,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #16
            pubkey = get_uln_event_authority_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #17
            pubkey = uln_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #18
            pubkey = executor_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #19
            pubkey = get_executor_pda_deriver(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #20
            pubkey = price_fee_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #21
            pubkey = get_price_fee_program_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #22
            pubkey = dvn_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #23
            pubkey = get_dvn_derive_config_pda(),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #24
            pubkey = price_fee_program_id,
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta( #25
            pubkey = get_price_fee_program_pda(),
            is_signer = False,
            is_writable =  True
        )
    ]
    
    print(f"-------------------------Finish Challenge----------------------------")
    finish_challenge_accounts : FinishChallengeAccounts = {
        "authority": user.pubkey(),
        "oapp": tristero_oapp_pubkey,
    }
    
    finish_challenge_params_json : FinishChallengeParamsJSON = {
        "arb_eid": dest_eid,
        "trade_match_id": trade_match_id,
        "spl_token": str(spltoken),
        "erc20token": erc20token,
        "receiver": dest_oapp_addr
    }
    
    finish_challenge_params = FinishChallengeParams.from_json(finish_challenge_params_json)
    
    finish_challenge_ix = finish_challenge(
        {
            "params": finish_challenge_params
        },
        finish_challenge_accounts,
        tristero_program_id,
        send_instruction_remaining_accounts
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(finish_challenge_ix)
    
    finish_challenge_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
    print(f"finish_challenge_tx: {finish_challenge_tx}")
