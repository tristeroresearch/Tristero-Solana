import asyncio
import binascii
from web3 import Web3
from solders.pubkey import Pubkey
import base58
from pathlib import Path
from lib_arb import arb_set_peer, arb_set_enforced_options, arb_place_order, arb_create_match, arb_execute_match, arb_confirm_match, arb_start_challenge, arb_finish_challenge
from lib_sol import sol_register_new_oapp, sol_init_send_library, sol_init_receive_library, sol_init_nonce, sol_init_oft_config
from lib_sol import sol_place_order, sol_create_match, sol_execute_match, sol_confirm_match, sol_start_challenge, sol_finish_challenge, get_tristero_oapp
import config
from script_tx_handler import ensure_approval
import json

class SimpleTradeTest:
    def __init__(self, mode): # mode:true(Mainnet), false(Testnet)
        if mode == False:
            self.arb_eid = 40231 # Arbitrum Sepolia Testnet
            self.sol_eid = 40168 # Solana Devnet
            self.arb_url = "https://sepolia-rollup.arbitrum.io/rpc"
            self.sol_url = "https://api.devnet.solana.com"
        else:
            self.arb_eid = 30110 # Arbitrum Mainnet
            self.sol_eid = 30168 # Solana Mainnet
            self.arb_url = "https://arb1.arbitrum.io/rpc"
            self.sol_url = "https://api.mainnet-beta.solana.com"
        
    async def define_trade_token(self, str_spl_token_addr, str_erc20_token_addr):
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        self.arb_spl_token_addr = base58.b58decode(str_spl_token_addr)
        self.arb_erc20_token_addr = web3.to_checksum_address(str_erc20_token_addr)
        
        self.sol_spl_token_addr = Pubkey.from_string(str_spl_token_addr)
        self.sol_erc20_token_addr = binascii.unhexlify(str_erc20_token_addr)
        
    async def set_configuration(self, is_first):
        with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
            file_str = f.read()
        json_object = json.loads(file_str)
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        deployed_contract = web3.eth.contract(
            address=config.arbitrum_contract_addr, abi=json_object["abi"]
        )
        
        sol_oapp_addr = base58.b58decode(str(get_tristero_oapp()))
        print(f"sol_oapp_addr: {get_tristero_oapp()}")
        arb_oapp_addr_bytesarry = bytearray(32)
        padded_buffer = binascii.unhexlify(config.arbitrum_contract_addr[2:])
        arb_oapp_addr_bytesarry[12:12 + len(padded_buffer)] = padded_buffer
        
        if is_first == True:
            # Solana OApp Configuration
            await sol_register_new_oapp(self.sol_url, config.admin_sol_wallet_pair)
            await sol_init_send_library(self.sol_url, config.admin_sol_wallet_pair, self.arb_eid)
            await sol_init_receive_library(self.sol_url, config.admin_sol_wallet_pair, self.arb_eid)
            await sol_init_nonce(self.sol_url, config.admin_sol_wallet_pair, self.arb_eid, arb_oapp_addr_bytesarry)
            await sol_init_oft_config(self.sol_url, config.admin_sol_wallet_pair, self.arb_eid)
            
            # Arbitrum OApp Configuration
            await arb_set_peer(web3, deployed_contract, self.sol_eid, sol_oapp_addr, config.a_user_arb_secret)
            await arb_set_enforced_options(web3, deployed_contract, self.sol_eid, config.a_user_arb_secret)
        else:
            await sol_init_nonce(self.sol_url, config.admin_sol_wallet_pair, self.arb_eid, arb_oapp_addr_bytesarry)
            await arb_set_peer(web3, deployed_contract, self.sol_eid, sol_oapp_addr, config.b_user_arb_secret)

    async def test_case1(self, a_user_token_account_addr, b_user_token_account_addr):
        with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
            file_str = f.read()
        json_object = json.loads(file_str)
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        deployed_contract = web3.eth.contract(
            address=config.arbitrum_contract_addr, abi=json_object["abi"]
        )
        imported_account = web3.eth.account.from_key(config.b_user_arb_secret)
        b_user_arb_pubkey_str = str(web3.to_checksum_address(imported_account.address))
        
        await sol_place_order(self.sol_url, config.a_user_sol_wallet_pair, 21, self.arb_eid, self.sol_spl_token_addr, a_user_token_account_addr, self.sol_erc20_token_addr, 1000, 1000, 10)
        await sol_create_match(self.sol_url, config.b_user_sol_wallet_pair, 21, 21, binascii.unhexlify(b_user_arb_pubkey_str[2:]))
        await ensure_approval(web3, imported_account.address, config.arbitrum_contract_addr, self.arb_erc20_token_addr, 1000, config.b_user_arb_secret)
        await arb_execute_match(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 21, config.b_user_arb_secret)
        await sol_confirm_match(self.sol_url, config.b_user_sol_wallet_pair, b_user_token_account_addr, self.sol_spl_token_addr, 21, 21)
    
    async def test_case2(self, a_user_token_account_addr_str, b_user_token_account_addr_str):
        with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
            file_str = f.read()
        json_object = json.loads(file_str)
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        deployed_contract = web3.eth.contract(
            address=config.arbitrum_contract_addr, abi=json_object["abi"]
        )
        imported_account = web3.eth.account.from_key(config.a_user_arb_secret)
        b_user_arb_pubkey_str = str(web3.to_checksum_address(web3.eth.account.from_key(config.b_user_arb_secret).address))
        
        await arb_place_order(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 1000, 1000, 10, 100, config.a_user_arb_secret)
        await ensure_approval(web3, imported_account.address, config.arbitrum_contract_addr, self.arb_erc20_token_addr, 1000, config.a_user_arb_secret)
        await arb_create_match(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, base58.b58decode(b_user_token_account_addr_str), config.b_user_arb_secret, 21)
        await sol_execute_match(self.sol_url, config.b_user_sol_wallet_pair, Pubkey.from_string(b_user_token_account_addr_str), Pubkey.from_string(a_user_token_account_addr_str), self.arb_eid, 21, 1000, binascii.unhexlify(b_user_arb_pubkey_str[2:]))
        await arb_confirm_match(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 21, config.b_user_arb_secret)
        
    async def test_case3(self, a_user_token_account_addr, b_user_token_account_addr):
        with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
            file_str = f.read()
        json_object = json.loads(file_str)
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        deployed_contract = web3.eth.contract(
            address=config.arbitrum_contract_addr, abi=json_object["abi"]
        )
        arb_oapp_addr_bytesarry = bytearray(32)
        padded_buffer = binascii.unhexlify(config.arbitrum_contract_addr[2:])
        arb_oapp_addr_bytesarry[12:12 + len(padded_buffer)] = padded_buffer
        imported_account = web3.eth.account.from_key(config.b_user_arb_secret)
        b_user_arb_pubkey_str = str(web3.to_checksum_address(imported_account.address))
        
        await sol_place_order(self.sol_url, config.a_user_sol_wallet_pair, 25, self.arb_eid, self.sol_spl_token_addr, a_user_token_account_addr, self.sol_erc20_token_addr, 1000, 1000, 10)
        await sol_create_match(self.sol_url, config.b_user_sol_wallet_pair, 25, 25, binascii.unhexlify(b_user_arb_pubkey_str[2:]))
        await ensure_approval(web3, imported_account.address, config.arbitrum_contract_addr, self.arb_erc20_token_addr, 1000, config.b_user_arb_secret)
        await arb_execute_match(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 25, config.b_user_arb_secret)
        await arb_start_challenge(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 1, config.b_user_arb_secret)
        await sol_finish_challenge(self.sol_url, config.b_user_sol_wallet_pair, 1, self.arb_eid, self.sol_spl_token_addr, self.sol_erc20_token_addr, arb_oapp_addr_bytesarry)
    
    async def test_case4(self, a_user_token_account_addr_str, b_user_token_account_addr_str):
        with Path("./test-python/arb-contract/SimpleTradeContract.json").open() as f:
            file_str = f.read()
        json_object = json.loads(file_str)
        web3 = Web3(Web3.HTTPProvider(self.arb_url))
        deployed_contract = web3.eth.contract(
            address=config.arbitrum_contract_addr, abi=json_object["abi"]
        )
        arb_oapp_addr_bytesarry = bytearray(32)
        padded_buffer = binascii.unhexlify(config.arbitrum_contract_addr[2:])
        arb_oapp_addr_bytesarry[12:12 + len(padded_buffer)] = padded_buffer
        imported_account = web3.eth.account.from_key(config.a_user_arb_secret)
        b_user_arb_pubkey_str = str(web3.to_checksum_address(web3.eth.account.from_key(config.b_user_arb_secret).address))
        
        await arb_place_order(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 1000, 1000, 10, 100, config.a_user_arb_secret)
        await ensure_approval(web3, imported_account.address, config.arbitrum_contract_addr, self.arb_erc20_token_addr, 1000, config.a_user_arb_secret)
        await arb_create_match(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, base58.b58decode(b_user_token_account_addr_str), config.b_user_arb_secret, 8)
        await sol_execute_match(self.sol_url, config.b_user_sol_wallet_pair, Pubkey.from_string(b_user_token_account_addr_str), Pubkey.from_string(a_user_token_account_addr_str), self.arb_eid, 8, 1000, binascii.unhexlify(b_user_arb_pubkey_str[2:]))
        await arb_start_challenge(web3, deployed_contract, self.arb_erc20_token_addr, self.arb_spl_token_addr, self.sol_eid, 8, config.a_user_arb_secret)
        await sol_finish_challenge(self.sol_url, config.b_user_sol_wallet_pair, 8, self.arb_eid, self.sol_spl_token_addr, self.sol_erc20_token_addr, arb_oapp_addr_bytesarry)
    
async def main():
    simple_trade_test = SimpleTradeTest(False)
    # await simple_trade_test.set_configuration(True)
    await simple_trade_test.define_trade_token("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU", "75faf114eafb1bdbe2f0316df893fd58ce46aa4d")
    await simple_trade_test.test_case1(Pubkey.from_string("6RzJ96TziaKHitum3KW5524D6GbvqqYJAeaNfQyicmEx"), Pubkey.from_string("9pveBsMdpg8EjBgap9LWWDSfMdY5B8x4yvxk4ZvfobLC"))
    await simple_trade_test.test_case2("6RzJ96TziaKHitum3KW5524D6GbvqqYJAeaNfQyicmEx", "9pveBsMdpg8EjBgap9LWWDSfMdY5B8x4yvxk4ZvfobLC")
    await simple_trade_test.test_case3(Pubkey.from_string("6RzJ96TziaKHitum3KW5524D6GbvqqYJAeaNfQyicmEx"), Pubkey.from_string("9pveBsMdpg8EjBgap9LWWDSfMdY5B8x4yvxk4ZvfobLC"))
    await simple_trade_test.test_case4("6RzJ96TziaKHitum3KW5524D6GbvqqYJAeaNfQyicmEx", "9pveBsMdpg8EjBgap9LWWDSfMdY5B8x4yvxk4ZvfobLC")

asyncio.run(main())