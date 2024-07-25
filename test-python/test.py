import asyncio
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.account import Account
from solders.bankrun import ProgramTestContext
from solders.message import Message
from solders.token.associated import get_associated_token_address
from solders.bankrun import start_anchor
from solders.transaction import TransactionError, VersionedTransaction
from anchorpy import Provider, Program, WorkspaceType, workspace, Idl, Context, create_workspace, close_workspace
from solders.system_program import ID as SYS_PROGRAM_ID
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.instruction import Instruction, AccountMeta
from solders.message import Message
from solders.compute_budget import set_compute_unit_limit
from tristero.instructions.create_match import create_match, CreateMatchAccounts
from tristero.types.create_match_params import CreateMatchParams
from tristero.types.create_match_params import CreateMatchParamsJSON
from tristero.accounts.admin_panel import AdminPanel
import json
import struct

tristero_program_id = Pubkey.from_string("5wrxGvTGkUCAusBSpkgGjW7N4G1xvWA2Aw1Pk1fAmuMf")
endpoint_program_id = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6")
executor_program_id = Pubkey.from_string("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn")
send_library_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")
price_fee_program_id = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP")
dvn_program_id = Pubkey.from_string("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW")
uln_program_id = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")

rpc_url = "https://api.testnet.solana.com"

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
RECEIVER_PUBKEY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 237, 167, 180, 19, 229, 37, 204, 255, 159, 251, 166, 16, 245, 196, 184, 225, 137, 235, 83]

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
    # Connect to the Solana testnet
    solana_client = Client("https://api.testnet.solana.com")
    ##context = await start_anchor(Path("../"))
    
    # Read the generated IDL.
    with Path("./target/idl/tristero.json").open() as f:
        raw_idl = f.read()
    idl = Idl.from_json(raw_idl)
    # Address of the deployed program.
    program_id = Pubkey.from_string("5wrxGvTGkUCAusBSpkgGjW7N4G1xvWA2Aw1Pk1fAmuMf")
    
    register_tristero_oapp_params = {
        "delegate": user.pubkey()
    }
    tristero_oapp_pubkey = get_tristero_oapp()
    
    
    send_instruction_remaining_accounts = [
        AccountMeta(
            pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("4qd1mSmxeBFqbsUDnDywj1bZD7UbxPn4nZwNoQWQ77im"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("141X4oNUhGaSKnva8LecEYNgjtFBjvMwZg258hFtQRJP"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("9wgwtfS2NbYariF6kFCV4ifj4fVYQ5bNtQ7pj4jWrE2T"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("526PeNZfw8kSnDU4nmzJFVJzJWNhwmZykEyJr5XWz5Fv"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("2uk9pQh3tB5ErV7LGQJcbWjb4KeJ2UJki5qJZ8QG56G3"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("5uUTpCkgpz9CofViozMKtRvKfJTez9UfjoFX1DinEhS1"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("F8E8QGhKmHEx2esh5LpVizzcP4cHYhzXdXTwg9w3YYY2"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("2XgGZG4oP29U3w5h4nTk1V2LFHL23zKDPJjs3psGzLKQ"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("3ZZXoLURkHz7RuK11xnxDCHkz1sPPDomqaFNAKxaC1fS"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("3y4LwxWFPhMNc4w8P4CfH5WVqwUnAm21PA4Pf7UMoxej"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("8oUck8bkDE1BnmfELXreAe8HS8cFR2FTqoFXA8daRNQ6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("8oUck8bkDE1BnmfELXreAe8HS8cFR2FTqoFXA8daRNQ6"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("11111111111111111111111111111111"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("7n1YeBMVEUCJ4DscKAcpVQd6KXU7VpcEcc15ZuMcL4U3"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("AwrbHeCyniXaQhiJZkLhgWdUCteeWSGaSN1sTfLiY7xK"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("CSFsUupvJEQQd1F4SsXGACJaxQX4eropQMkGV2696eeQ"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("4VDjp6XQaxoZf5RGwiPU9NR1EXSZn2TP4ATMmiSzLfhb"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP"),
            is_signer = False,
            is_writable =  True
        ),
        AccountMeta(
            pubkey = Pubkey.from_string("CSFsUupvJEQQd1F4SsXGACJaxQX4eropQMkGV2696eeQ"),
            is_signer = False,
            is_writable =  True
        )
    ]
    
    
    
    mint_addr = Pubkey.from_string("96dYLgk5D6rHm2V8Bi3djA3QXrAJrhENWuHC9m4kCmDq")
    
    admin_panel_pda = get_admin_panel()
    
    admin_panel = AdminPanel.fetch(solana_client, admin_panel_pda, program_id = program_id)
    
    # calling create_match instruction
    
    create_match_accounts : CreateMatchAccounts = {
        "authority": user.pubkey(),
        "admin_panel": admin_panel_pda,
        "token_mint": mint_addr,
        "token_account": Pubkey.from_string("CqVTHuqiBKuygw5UXiGmyinAaJzgyrcV5wxubK8C8fDQ"),
        "staking_account": get_staking_panel(mint_addr),
        "trade_match": get_trade_match_pda(mint_addr, admin_panel.match_count),
        "token_program": Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
        "system_program": SYS_PROGRAM_ID
    }
    
    create_match_params_json : CreateMatchParamsJSON = {
        "source_sell_amount": 100000,
        "dest_token_mint": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "dest_buy_amount": 10000,
        "eid": 40231,
    }
    
    create_match_params = CreateMatchParams.from_json(create_match_params_json)
    
    create_match_ix = create_match(
        {
            "params": create_match_params
        },
        create_match_accounts,
        program_id
    )
    latest_blockhash = solana_client.get_latest_blockhash()
    blockhash = latest_blockhash.value.blockhash
    signers = [user]
    
    txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
    txn.add(set_compute_unit_limit(2000000))
    txn.add(create_match_ix)
    
    create_match_tx = solana_client.send_transaction(txn, *signers).value
    print(f"create_match_tx: {create_match_tx}")

asyncio.run(main())