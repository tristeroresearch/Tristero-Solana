import json
import base64
import struct
import solana
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.transaction import Transaction
from solders.system_program import ID as SYS_PROGRAM_ID
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import TxOpts
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.async_client import AsyncToken
from spl.token.instructions import get_associated_token_address
from solders.pubkey import Pubkey
from solders.keypair import Keypair

# Load keypair from file
def load_keypair(file_path):
    with open(file_path, 'r') as f:
        secret_key = json.load(f)
    return Keypair.from_secret_key(bytes(secret_key))

# Constants and Configurations
# DEFAULT_MESSAGE_LIB = PublicKey(0)

client = AsyncClient("https://api.mainnet-beta.solana.com", commitment=Confirmed)
provider = Client("https://api.mainnet-beta.solana.com")
connection = provider
program_id = Pubkey("58nEPFCuebJsxjcyg6p6q2fXNLY2ApMiSQ619wZHe88h")
endpoint_id = Pubkey("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6")
dvn_id = Pubkey("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW")
executor_id = Pubkey("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn")
price_fee_id = Pubkey("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP")
uln_id = Pubkey("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")
LAMPORTS_PER_SOL = 1000000000

user_json = load_keypair("../tests/user.json")
other_json = load_keypair("../tests/other.json")
admin_json = load_keypair("../tests/adminJson.json")

user = Keypair.from_secret_key(bytes(user_json))
other_user = Keypair.from_secret_key(bytes(other_json))
admin = Keypair.from_secret_key(bytes(admin_json))
receiver_pubkey = other_user.public_key
arbitrum_eid = 40231

async def main():
    try:
        
        user_air_drop_tx = await connection.request_airdrop(user.public_key, 5 * LAMPORTS_PER_SOL)
        await connection.confirm_transaction(user_air_drop_tx)
        print("User Airdrop successful: ", user_air_drop_tx)

        admin_air_drop_tx = await connection.request_airdrop(admin.publicKey, 5 * LAMPORTS_PER_SOL)
        await connection.confirm_transaction(admin_air_drop_tx)
        print("User Airdrop successful: ", admin_air_drop_tx)

        print("balance(User): ", await connection.get_balance(user.public_key), "balance(Admin): ", await connection.getBalance(admin.publicKey))

        print("Balance:", await connection.get_balance(user.public_key))
        
        print("------------------------Create admin panel------------------------")
        

        print("------------------------Register New Oapp(Sender)------------------------")
        register_tristero_oapp_params = {"delegate": user.public_key}
        tristero_oapp_pubkey = get_tristero_oapp()
        endpoint_event_pda_deriver = EventPDADeriver(endpoint)
        uld_event_pda_deriver = EventPDADeriver(send_library_program)

        tx1 = Transaction()
        tx1.add(register_tristero_oapp(register_tristero_oapp_params, user.public_key, tristero_oapp_pubkey, get_oapp_pda(tristero_oapp_pubkey), endpoint, endpoint_event_pda_deriver.event_authority()[0]))
        await client.send_transaction(tx1, user)
        print("tx1 complete")

        print("-------------------Init Send Library-----------------------------")
        init_send_library_instruction_accounts = {
            "delegate": user.public_key,
            "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
            "send_library_config": get_send_library_config_pda(tristero_oapp_pubkey, arbitrum_eid)
        }
        init_send_library_params = {
            "params": {
                "oapp": tristero_oapp_pubkey,
                "sender": tristero_oapp_pubkey,
                "eid": arbitrum_eid
            }
        }

        send_library_instruction = create_init_send_library_instruction(init_send_library_instruction_accounts, init_send_library_params)
        tx2 = Transaction().add(send_library_instruction)
        await client.send_transaction(tx2, user)
        print("tx2 complete")

        print("----------------------------Init Receive Library-------------------------------")
        init_receive_library_instruction_accounts = {
            "delegate": user.public_key,
            "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
            "receive_library_config": get_receive_library_config_pda(tristero_oapp_pubkey, arbitrum_eid)
        }
        init_receive_library_params = {
            "params": {
                "receiver": tristero_oapp_pubkey,
                "eid": arbitrum_eid
            }
        }
        receive_library_instruction = create_init_receive_library_instruction(init_receive_library_instruction_accounts, init_receive_library_params)
        tx3 = Transaction().add(receive_library_instruction)
        await client.send_transaction(tx3, user)
        print("tx3 complete")

        print("-------------------Init Nonce-----------------------------")
        init_nonce_accounts = {
            "delegate": user.public_key,
            "oapp_registry": get_oapp_registry_pda(tristero_oapp_pubkey),
            "nonce": get_nonce_pda(tristero_oapp_pubkey, arbitrum_eid, receiver_pubkey),
            "pending_inbound_nonce": get_pending_inbound_nonce_pda(tristero_oapp_pubkey, arbitrum_eid, receiver_pubkey),
            "system_program": SYS_PROGRAM_ID
        }
        init_nonce_params = {
            "params": {
                "local_oapp": tristero_oapp_pubkey,
                "remote_eid": arbitrum_eid,
                "remote_oapp": list(receiver_pubkey.to_bytes())
            }
        }
        init_nonce_instruction = create_init_nonce_instruction(init_nonce_accounts, init_nonce_params)
        tx4 = Transaction().add(init_nonce_instruction)
        await client.send_transaction(tx4, user)
        print("tx4 complete")

        # Sending
        print("Sending")
        send_library_config = get_send_library_config_pda(tristero_oapp_pubkey, arbitrum_eid)
        default_send_library_config = get_default_send_library_config(arbitrum_eid)
        send_library_info = await get_send_library_info_pda(send_library_config, default_send_library_config)

        uln_pda_deriver = UlnPDADeriver(send_library_program)
        send_config = uln_pda_deriver.send_config(arbitrum_eid, tristero_oapp_pubkey)[0]
        default_send_config = uln_pda_deriver.default_send_config(arbitrum_eid)[0]

        treasury = user.public_key

        send_instruction_accounts = {
            "sender": tristero_oapp_pubkey,
            "endpoint_program": endpoint,
        }
        send_instruction_remaining_accounts = [
            {"pubkey": endpoint, "is_signer": False, "is_writable": True},
            {"pubkey": tristero_oapp_pubkey, "is_signer": False, "is_writable": True},
            {"pubkey": send_library_program, "is_signer": False, "is_writable": True},
            {"pubkey": send_library_config, "is_signer": False, "is_writable": True},
            {"pubkey": default_send_library_config, "is_signer": False, "is_writable": True},
            {"pubkey": send_library_info, "is_signer": False, "is_writable": True},
            {"pubkey": get_endpoint_pda(arbitrum_eid), "is_signer": False, "is_writable": True},
            {"pubkey": get_nonce_pda(tristero_oapp_pubkey, arbitrum_eid, receiver_pubkey), "is_signer": False, "is_writable": True},
            {"pubkey": endpoint_event_pda_deriver.event_authority()[0], "is_signer": False, "is_writable": True},
            {"pubkey": get_uln_pda(), "is_signer": False, "is_writable": True},
            {"pubkey": send_config, "is_signer": False, "is_writable": True},
            {"pubkey": default_send_config, "is_signer": False, "is_writable": True},
            {"pubkey": user.public_key, "is_signer": False, "is_writable": True},
            {"pubkey": SYS_PROGRAM_ID, "is_signer": False, "is_writable": True},
            {"pubkey": uld_event_pda_deriver.event_authority()[0], "is_signer": False, "is_writable": True},
            {"pubkey": executor_program_id, "is_signer": False, "is_writable": True},
            {"pubkey": new ExecutorPDADeriver(executor_program_id).config()[0], "is_signer": False, "is_writable": True},
            {"pubkey": price_fee_program_id, "is_signer": False, "is_writable": True},
            {"pubkey": new PriceFeedPDADeriver(price_fee_program_id).price_feed()[0], "is_signer": False, "is_writable": True},
            {"pubkey": dvn_program_id, "is_signer": False, "is_writable": True},
            {"pubkey": new DVNDeriver(dvn_program_id).config()[0], "is_signer": False, "is_writable": True}
        ]

        send_params = {
            "dst_eid": arbitrum_eid,
            "receiver": list(receiver_pubkey.to_bytes()),
            "message": b"Hello World",
            "options": Options.new_options().add_executor_lz_receive_option(100, 0).to_bytes(),
            "native_fee": 3 * LAMPORTS_PER_SOL,
            "lz_token_fee": 0
        }

        tx5 = Transaction()
        tx5.add(ComputeBudgetProgram.set_compute_unit_limit(90000000))
        tristero_send_instruction = await create_tristero_send_instruction(send_params, send_instruction_accounts, send_instruction_remaining_accounts)
        tx5.add(tristero_send_instruction)
        await client.send_transaction(tx5, user)
        print("tx5 complete")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
