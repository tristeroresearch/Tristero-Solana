import asyncio
import binascii
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.account import Account
from solders.bankrun import ProgramTestContext
from solders.message import Message
from solders.token.associated import get_associated_token_address
from solders.bankrun import start_anchor
from solders.transaction import TransactionError, VersionedTransaction
from anchorpy import Provider, Program, WorkspaceType, workspace, Idl, Context, create_workspace, close_workspace, Wallet
from solders.system_program import ID as SYS_PROGRAM_ID
from pathlib import Path
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.instruction import Instruction, AccountMeta
from solders.message import Message
from solders.compute_budget import set_compute_unit_limit
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed
from tristero.instructions.create_match import create_match, CreateMatchAccounts
from tristero.instructions.place_order import place_order, PlaceOrderAccounts
from tristero.instructions.challenge import challenge, ChallengeAccounts
from tristero.types.create_match_params import CreateMatchParams, CreateMatchParamsJSON
from tristero.types.place_order_params import PlaceOrderParams, PlaceOrderParamsJSON
from tristero.types.challenge_params import ChallengeParams, ChallengeParamsJSON
from tristero.accounts.admin_panel import AdminPanel
import time
import json
import struct

tristero_program_id = Pubkey.from_string("APob25xoaC1Zz2FKePPCRfRBgJ5nhrjg7dUfV68ZNobP")
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

# # Set up the provider for AnchorPy
# provider = Provider(client, user.secret())

# # Initialize the program
# program = Program("./target/idl/tristero.json", tristero_program_id, provider)

LAMPORTS_PER_SOL = 1_000_000_000
ARBITRUM_EID = 40231

# RECEIVER_PUBKEY = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 237, 167, 180, 19, 229, 37, 204, 255, 159, 251, 166, 16, 245, 196, 184, 225, 137, 235, 83]
RECEIVER_PUBKEY = bytearray(32)

# Hexadecimal string to be converted to bytes
hex_string = '644DFf7307Bb76187f559CDC8aC926D827158E4B'

# Convert the hexadecimal string to bytes
padded_buffer = binascii.unhexlify(hex_string)

# Copy the bytes to the RECEIVER_PUBKEY bytearray starting at position 12
RECEIVER_PUBKEY[12:12 + len(padded_buffer)] = padded_buffer

# Print the result
print("receiverPubKey =>", RECEIVER_PUBKEY)

def get_order_pda(order_id):
    # Convert the order ID to a buffer
    order_id_buffer = order_id.to_bytes(8, byteorder="big")

    # Create the seeds
    seeds = [
        b"order",
        order_id_buffer
    ]

    # Find the program address
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_refund_token_account_pda(pubkey):
    # Create the seeds
    seeds = [
        b"refund_account",
        bytes(pubkey)
    ]

    # Find the program address
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_sol_panel():
    # Create the seeds
    seeds = [
        b"sol_panel"
    ]

    # Find the program address
    return Pubkey.find_program_address(seeds, tristero_program_id)[0]

def get_nonce_pda(sender_key, eid, receiver):
    # Convert the eid to a buffer
    eid_buffer = eid.to_bytes(4, byteorder="big")

    # Create the seeds
    seeds = [
        b"Nonce",
        bytes(sender_key),
        eid_buffer,
        bytes(receiver)
    ]
    
    return Pubkey.find_program_address(seeds, endpoint_program_id)[0]

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
    eid_bytes = eid.to_bytes(4, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"SendLibraryConfig", bytes(pubkey), eid_bytes],
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

# def get_send_library_info_pda(send_library_config, default_send_library_config): #have to fix this part
#     eid_bytes = struct.pack(">I", eid)
#     (distributor, bump) = Pubkey.find_program_address(
#         [b"SendLibraryConfig", eid_bytes],
#         endpoint_program_id,
#     )
#     return distributor

def get_endpoint_pda():
    return Pubkey.find_program_address(
        [b"Endpoint"],
        endpoint_program_id,
    )[0]

def get_price_feed_pda():
    (distributor, bump) = Pubkey.find_program_address(
        [b"PriceFeed"],
        price_fee_program_id,
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

def get_trade_match_pda(match_count):
    match_count_bytes = match_count.to_bytes(8, byteorder="big")
    (distributor, bump) = Pubkey.find_program_address(
        [b"trade_match", match_count_bytes],
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
    client = AsyncClient("https://api.testnet.solana.com")
    provider = Provider(client, Wallet.local())
    # Address of the deployed program.
    program_id = Pubkey.from_string("APob25xoaC1Zz2FKePPCRfRBgJ5nhrjg7dUfV68ZNobP")
    
    async with Program(idl, program_id, provider) as program:
        print(f"program: ", program)
        admin_panel_account = await program.account["AdminPanel"].fetch(get_admin_panel())
        print(f"admin_panel_account: {admin_panel_account}")
    
        register_tristero_oapp_params = {
            "delegate": user.pubkey()
        }
        tristero_oapp_pubkey = get_tristero_oapp()
        
        send_library_config = get_send_library_config_pda(tristero_oapp_pubkey, ARBITRUM_EID)
        default_send_library_config = get_default_send_library_config(ARBITRUM_EID)
        #send_library_info = get_send_library_info_pda(send_library_config, default_send_library_config) # should fix
        #uln_pda_deriver = 
        #send_config = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];
        #default_send_config = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0]; //until here
        
        send_instruction_remaining_accounts = [
            AccountMeta( #0
                pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #1
                pubkey = get_tristero_oapp(),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #2
                pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #3
                pubkey = Pubkey.from_string("141X4oNUhGaSKnva8LecEYNgjtFBjvMwZg258hFtQRJP"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #4
                pubkey = Pubkey.from_string("9wgwtfS2NbYariF6kFCV4ifj4fVYQ5bNtQ7pj4jWrE2T"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #5
                pubkey = Pubkey.from_string("526PeNZfw8kSnDU4nmzJFVJzJWNhwmZykEyJr5XWz5Fv"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #6
                pubkey = get_endpoint_pda(),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #7
                pubkey = get_nonce_pda(get_tristero_oapp(), ARBITRUM_EID, RECEIVER_PUBKEY),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #8
                pubkey = Pubkey.from_string("F8E8QGhKmHEx2esh5LpVizzcP4cHYhzXdXTwg9w3YYY2"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #9
                pubkey = Pubkey.from_string("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #10
                pubkey = Pubkey.from_string("2XgGZG4oP29U3w5h4nTk1V2LFHL23zKDPJjs3psGzLKQ"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #11
                pubkey = Pubkey.from_string("3ZZXoLURkHz7RuK11xnxDCHkz1sPPDomqaFNAKxaC1fS"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #12
                pubkey = Pubkey.from_string("3y4LwxWFPhMNc4w8P4CfH5WVqwUnAm21PA4Pf7UMoxej"),
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
                pubkey = Pubkey.from_string("7n1YeBMVEUCJ4DscKAcpVQd6KXU7VpcEcc15ZuMcL4U3"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #17
                pubkey = Pubkey.from_string("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #18
                pubkey = Pubkey.from_string("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #19
                pubkey = Pubkey.from_string("AwrbHeCyniXaQhiJZkLhgWdUCteeWSGaSN1sTfLiY7xK"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #20
                pubkey = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #21
                pubkey = Pubkey.from_string("CSFsUupvJEQQd1F4SsXGACJaxQX4eropQMkGV2696eeQ"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #22
                pubkey = Pubkey.from_string("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #23
                pubkey = Pubkey.from_string("4VDjp6XQaxoZf5RGwiPU9NR1EXSZn2TP4ATMmiSzLfhb"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #24
                pubkey = Pubkey.from_string("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP"),
                is_signer = False,
                is_writable =  True
            ),
            AccountMeta( #25
                pubkey = Pubkey.from_string("CSFsUupvJEQQd1F4SsXGACJaxQX4eropQMkGV2696eeQ"),
                is_signer = False,
                is_writable =  True
            )
        ]
        
        mint_addr = Pubkey.from_string("96dYLgk5D6rHm2V8Bi3djA3QXrAJrhENWuHC9m4kCmDq")
        
        admin_panel_pda = get_admin_panel()
        
        order_id = admin_panel_account.order_count
        trade_match_id = admin_panel_account.match_count
        
        erc20_addr = binascii.unhexlify('75faf114eafb1bdbe2f0316df893fd58ce46aa4d')
        arb_wallet_addr = binascii.unhexlify('De7014167c36c39aAfb56aA0Bd87776d8911369A')
        
        print(f"-----------------------Place Order--------------------------")
        place_order_accounts: PlaceOrderAccounts = {
            "authority": user.pubkey(),
            "admin_panel": admin_panel_pda,
            "sol_panel": get_sol_panel(),
            "token_mint": mint_addr,
            "token_account": Pubkey.from_string("CqVTHuqiBKuygw5UXiGmyinAaJzgyrcV5wxubK8C8fDQ"),
            "staking_account": get_staking_panel(mint_addr),
            "order": get_order_pda(order_id)
        }
        
        place_order_params_json : PlaceOrderParamsJSON = {
            "source_sell_amount": 100,
            "min_sell_amount": 10,
            "dest_token_mint": erc20_addr,
            "dest_buy_amount": 100,
            "order_id": order_id,
            "eid": ARBITRUM_EID
        }
        
        place_order_params = PlaceOrderParams.from_json(place_order_params_json)
        
        place_order_ix = place_order(
            {
                "params": place_order_params
            },
            place_order_accounts,
            program_id
        )
        
        latest_blockhash = solana_client.get_latest_blockhash()
        blockhash = latest_blockhash.value.blockhash
        signers = [user]
        
        txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
        txn.add(set_compute_unit_limit(2000000))
        txn.add(place_order_ix)
        
        place_order_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
        print(f"place_order_tx: {place_order_tx}")
        
        # calling create_match instruction
        print(f"-----------------------Create Match--------------------------")
        create_match_accounts : CreateMatchAccounts = {
            "authority": user.pubkey(),
            "admin_panel": get_admin_panel(),
            "order": get_order_pda(order_id),
            "trade_match": get_trade_match_pda(trade_match_id)
        }
        
        create_match_params_json : CreateMatchParamsJSON = {
            "src_index": order_id,
            "dst_index": 60,
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
            program_id
        )
        latest_blockhash = solana_client.get_latest_blockhash()
        blockhash = latest_blockhash.value.blockhash
        signers = [user]
        
        txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
        txn.add(set_compute_unit_limit(2000000))
        txn.add(create_match_ix)
        
        create_match_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
        print(f"create_match_tx: {create_match_tx}")
        
        
        print(f"-------------------------Challenge----------------------------")
        challenge_accounts : ChallengeAccounts = {
            "authority": user.pubkey(),
            "admin_panel": get_admin_panel(),
            "trade_match": get_trade_match_pda(trade_match_id)
        }
        
        challenge_params_json : ChallengeParamsJSON = {
            "trade_match_id": trade_match_id,
            "tristero_oapp_bump": get_tristero_oapp_bump(),
            "source_token_address_in_arbitrum_chain": arb_wallet_addr,
            "receiver": RECEIVER_PUBKEY
        }
        
        challenge_params = ChallengeParams.from_json(challenge_params_json)
        
        challenge_ix = challenge(
            {
                "params": challenge_params
            },
            challenge_accounts,
            program_id,
            send_instruction_remaining_accounts
        )
        latest_blockhash = solana_client.get_latest_blockhash()
        blockhash = latest_blockhash.value.blockhash
        signers = [user]
        
        txn = Transaction(recent_blockhash=blockhash, fee_payer=user.pubkey())
        txn.add(set_compute_unit_limit(2000000))
        txn.add(challenge_ix)
        
        challenge_tx = solana_client.send_transaction(txn, *signers, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)).value
        print(f"challenge_tx: {challenge_tx}")

asyncio.run(main())