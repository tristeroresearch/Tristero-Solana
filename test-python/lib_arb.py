
from script_tx_handler import safe_build_and_send_tx, ensure_approval
from web3 import Web3
import time

# Configuration functions
async def arb_set_peer(web3: Web3, deployed_contract, dest_eid, oapp_addr, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    
    print("---------------------------ArbSetPeer----------------------------------")
    set_peer = deployed_contract.functions.setPeer(dest_eid, oapp_addr)

    set_peer_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        set_peer,
    )
    set_peer_receipt = web3.eth.wait_for_transaction_receipt(set_peer_hash, timeout=60)
    
    print(f"set_peer_receipt: ", set_peer_receipt)

async def arb_set_enforced_options(web3: Web3, deployed_contract, dest_eid, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    
    print("---------------------------ArbSetEnforcedOptions----------------------------------")
    set_enforced_options = deployed_contract.functions.setEnforcedOptions([
        (dest_eid, 1, bytes([0, 3, 1, 0, 17, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 161, 32]))
    ])

    set_enforced_options_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        set_enforced_options,
    )
    set_enforced_options_receipt = web3.eth.wait_for_transaction_receipt(set_enforced_options_hash, timeout=60)
    
    print(f"set_enforced_options_receipt: ", set_enforced_options_receipt)
    
async def arb_place_order(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, src_quantity, dst_quantity, bond_fee, bond_amount, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    print("---------------------------ArbPlaceOrder----------------------------------")
    place_order = deployed_contract.functions.placeOrder(
        (erc20_token_addr, spl_token_addr, dest_eid),
        (src_quantity, dst_quantity, bond_fee, erc20_token_addr, int(bond_amount)),
        (int(time.time()) + 3600, 20, 40),
        False
    )

    place_order_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        place_order,
    )
    place_order_receipt = web3.eth.wait_for_transaction_receipt(place_order_hash, timeout=60)
    
    print(f"place_order_receipt: ", place_order_receipt)
    
async def arb_create_match(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, dest_account_addr, private_key,  match_id):
    imported_account = web3.eth.account.from_key(private_key)
    
    print("----------------------------ArbCreateMatch----------------------------------")
    create_match = deployed_contract.functions.createMatch(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id, match_id, dest_account_addr, 1000, 1000
    )
    
    create_match_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        create_match,
    )
    create_match_receipt = web3.eth.wait_for_transaction_receipt(create_match_hash, timeout=60)
    
    print(f"create_match_receipt: ", create_match_receipt)
    
async def arb_execute_match(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, match_id, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    
    print("----------------------------ArbExecuteMatch----------------------------------")
    execute_match = deployed_contract.functions.executeMatch(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id, web3.to_checksum_address("0xDe7014167c36c39aAfb56aA0Bd87776d8911369A"), 1000
    )
    
    execute_match_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        execute_match,
    )
    execute_match_receipt = web3.eth.wait_for_transaction_receipt(execute_match_hash, timeout=60)
    
    print(f"execute_match_receipt: ", execute_match_receipt)

async def arb_confirm_match(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, match_id, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    
    print("----------------------------ArbConfirmMatch----------------------------------")
    confirm_match = deployed_contract.functions.confirmMatch(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id
    )
    
    confirm_match_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        confirm_match,
    )
    confirm_match_receipt = web3.eth.wait_for_transaction_receipt(confirm_match_hash, timeout=60)
    
    print(f"confirm_match_receipt: ", confirm_match_receipt)

async def arb_start_challenge(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, match_id, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    
    get_quote = deployed_contract.functions.getQuote(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id
    ).call()
    
    print(f"get_quote: {get_quote}")
    
    print("----------------------------ArbStartChallenge----------------------------------")
    start_challenge = deployed_contract.functions.startChallenge(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id
    )
    
    start_challenge_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        start_challenge,
        0,
        None,
        False,
        get_quote
    )
    start_challenge_receipt = web3.eth.wait_for_transaction_receipt(start_challenge_hash, timeout=60)
    
    print(f"start_challenge_receipt: ", start_challenge_receipt)

async def arb_finish_challenge(web3: Web3, deployed_contract, erc20_token_addr, spl_token_addr, dest_eid, match_id, private_key):
    imported_account = web3.eth.account.from_key(private_key)
    get_quote = deployed_contract.functions.getQuote(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id
    ).call()
    
    print(f"get_quote: {get_quote}")
    
    print("----------------------------ArbFinishChallenge----------------------------------")
    finish_challenge = deployed_contract.functions.finishChallenge(
        (erc20_token_addr, spl_token_addr, dest_eid),
        match_id
    )
    
    finish_challenge_hash = await safe_build_and_send_tx(
        web3,
        private_key,
        imported_account.address,
        finish_challenge,
        0,
        None,
        False,
        get_quote
    )
    finish_challenge_receipt = web3.eth.wait_for_transaction_receipt(finish_challenge_hash, timeout=60)
    
    print(f"finish_challenge_receipt: ", finish_challenge_receipt)
