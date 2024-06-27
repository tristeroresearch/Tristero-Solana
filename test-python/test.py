import asyncio
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.account import Account
from solders.bankrun import ProgramTestContext
from solders.instruction import Instruction
from solders.message import Message
from solders.token.associated import get_associated_token_address
from solders.bankrun import start_anchor
from anchorpy import Provider, Program, WorkspaceType, workspace, Idl, Context, create_workspace, close_workspace
from solders.system_program import ID as SYS_PROGRAM_ID
from pathlib import Path
from solana.rpc.async_api import AsyncClient
import json
import struct

tristero_program_id = Pubkey.from_string("7rcYP7cn1KFSrPF6Py4FtaTBRy8fkkAkJpEnirvPdmu8")
endpoint_program_id = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6")
executor_program_id = Pubkey.from_string("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn")
send_library_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")
price_fee_program_id = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP")
dvn_program_id = Pubkey.from_string("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW")
uln_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")

rpc_url = "http://localhost:8899"

# Load JSON files
with open(Path("./tests/user.json"), "r") as user_file:
    user_json = json.load(user_file)

with open(Path("./tests/other.json"), "r") as other_file:
    other_json = json.load(other_file)

with open(Path("./tests/adminJson.json"), "r") as admin_file:
    admin_json = json.load(admin_file)

# Create Keypair instances from secret keys
user = Keypair.from_bytes(bytes(user_json))
other_user = Keypair.from_bytes(bytes(other_json))
admin = Keypair.from_bytes(bytes(admin_json))

LAMPORTS_PER_SOL = 1_000_000_000
ARBITRUM_EID = 40231
RECEIVER_PUBKEY = bytes([1] * 32)

def get_oapp_pda(authority):
    (distributor, bump) = Pubkey.find_program_address(
        [b"OApp", bytes(authority)],
        endpoint_program_id,
    )
    return distributor

def get_executor_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"ExecutorConfig"],
        executor_program_id,
    )
    return distributor

def get_uln_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"MessageLib"],
        uln_program_id,
    )
    return distributor

def get_send_config_pda():
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

def get_send_library_config_pda(pubkey, eid):
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", bytes(pubkey), eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_receive_library_config_pda(pubkey, eid):
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"ReceiveLibraryConfig", bytes(pubkey), eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_default_send_library_config(eid):
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_send_library_info_pda(send_library_config, default_send_library_config): #have to fix this part
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", eid_bytes],
        endpoint_program_id,
    )
    return distributor

def get_endpoint_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"Endpoint"],
        endpoint_program_id,
    )
    return distributor

def get_price_feed_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"PriceFeed"],
        price_fee_program_id,
    )
    return distributor

def get_nonce_pda(sender_key, eid, receiver):
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"Nonce", bytes(sender_key), eid_bytes, bytes(receiver)],
        endpoint_program_id,
    )
    return distributor

def get_pending_inbound_nonce_pda(sender_key, eid, receiver):
    eid_bytes = struct.pack(">I", eid)
    (distributor, bump) = Pubkey.find_program_address(
        [b"PendingNonce", bytes(sender_key), eid_bytes, bytes(receiver)],
        endpoint_program_id,
    )
    return distributor

def get_admin_panel():
    (distributor, bump) = Pubkey.find_program_address(
        [b"admin_panel"],
        tristero_program_id,
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

def get_trade_match_pda(authority, match_count):
    match_count_bytes = struct.pack(">B", match_count)
    (distributor, bump) = Pubkey.find_program_address(
        [b"trade_match", bytes(authority), match_count_bytes],
        tristero_program_id,
    )
    return distributor

def get_payload_hash_pda(receiver, src_eid, sender, nonce):
    src_eid_bytes = struct.pack(">I", src_eid)  # ">I" for big-endian, unsigned int (4 bytes)
    nonce_bytes = struct.pack(">Q", nonce)
    (distributor, bump) = Pubkey.find_program_address(
        [b"PayloadHash", bytes(receiver), src_eid_bytes, bytes(nonce), nonce_bytes],
        tristero_program_id,
    )
    return distributor

async def main():
    client = AsyncClient("http://127.0.0.1:8899")
    
    # Close the client connection
    await client.close()
    
    # Read the generated IDL.
    with Path("./target/idl/tristero.json").open() as f:
        raw_idl = f.read()
    idl = Idl.from_json(raw_idl)
    # Address of the deployed program.
    program_id = Pubkey.from_string("7rcYP7cn1KFSrPF6Py4FtaTBRy8fkkAkJpEnirvPdmu8")
    # Create an Anchor workspace
    workspace = create_workspace()
    program = workspace["tristero"]
    endpoint_program = workspace["endpoint"]
    
    accounts = {
        "admin_wallet": admin.pubkey(),
        "admin_panel": get_admin_panel(),
        "system_program": SYS_PROGRAM_ID
    }
    params = {
        "admin_wallet": admin.pubkey(),
        "payment_wallet": admin.pubkey(),
    }
    admin_panel_update_tx = await program.rpc["admin_panel_update"](params, ctx=Context(accounts = accounts, signers = [admin]))
    print("admin_panel_update_tx ", admin_panel_update_tx)
    
    # create_user_params = {}
    # create_user_accounts = {
    #     "authority": user.pubkey(),
    #     "user": get_user_pda(user.pubkey()),
    #     "system_program": SYS_PROGRAM_ID
    # }
    # create_user_account_tx = await program.rpc["create_user"](ctx = Context(accounts = create_user_accounts, signers=[user]))
    # print("create_user_tx: ", create_user_account_tx)
    
    register_tristero_oapp_params = {
        "delegate": user.pubkey()
    }
    tristero_oapp_pubkey = get_tristero_oapp()
    register_tristero_oapp_accounts = {
        "payer": user.pubkey(),
        "oapp": tristero_oapp_pubkey,
        "oapp_registry": get_oapp_pda(tristero_oapp_pubkey),
        "endpoint_program": endpoint_program_id,
        "system_program": SYS_PROGRAM_ID,
        "event_authority": endpoint_program_id
    }
    register_tristero_oapp_tx = await program.rpc["register_tristero_oapp"](register_tristero_oapp_params, ctx = Context(accounts = register_tristero_oapp_accounts, signers = [user]))
    print("register_tristero_oapp_tx: ", register_tristero_oapp_tx)
    
    init_send_library_accounts = {
        "delegate": user.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "send_library_config": get_send_library_config_pda(tristero_oapp_pubkey, ARBITRUM_EID)
    }
    init_send_library_params = {
        "oapp": tristero_oapp_pubkey,
        "sender": tristero_oapp_pubkey,
        "eid": ARBITRUM_EID
    }
    send_library_tx = await endpoint_program.rpc["init_send_library"](init_send_library_params, ctx = Context(accounts = init_send_library_accounts, signers = [user]))
    print("send_library_tx: ", send_library_tx)
    
    init_receive_library_accounts = {
        "delegate": user.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "receive_library_config": get_receive_library_config_pda(tristero_oapp_pubkey, ARBITRUM_EID)
    }
    init_receive_library_params = {
        "receiver": tristero_oapp_pubkey,
        "eid": ARBITRUM_EID
    }
    receive_library_tx = await endpoint_program.rpc["init_receive_library"](init_receive_library_params, ctx = Context(accounts = init_receive_library_accounts, signers = [user]))
    print("receive_library_tx: ", receive_library_tx)
    
    init_nonce_accounts = {
        "delegate": user.pubkey(),
        "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
        "nonce": get_nonce_pda(tristero_oapp_pubkey, ARBITRUM_EID, RECEIVER_PUBKEY)
    }
    init_nonce_params = {
        "local_oapp": tristero_oapp_pubkey,
        "remote_eid": ARBITRUM_EID,
        "remote_oapp": list(RECEIVER_PUBKEY)
    }
    init_nonce_tx = await endpoint_program.rpc["init_nonce"](init_nonce_params, ctx = Context(accounts = init_nonce_accounts, signers = [user]))
    print("init_nonce_tx: ", init_nonce_tx)
    

asyncio.run(main())