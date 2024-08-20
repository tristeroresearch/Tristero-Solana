use std::str::FromStr;

use crate::*;
use anchor_lang::solana_program;
use anchor_spl::token::TokenAccount;
use anchor_spl::associated_token::get_associated_token_address;
use spl_token::ID as TOKEN_PROGRAM_ID;
use solana_program::system_program;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use endpoint::state::SendLibraryConfig;

#[derive(Accounts)]
pub struct LzReceiveTypes<'info> {
    /// CHECK:
    pub oft_config: UncheckedAccount<'info>,
    /// CHECK:
    pub token_mint: UncheckedAccount<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzReceiveTypeParams {
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
}

impl LzReceiveTypes<'_> {
    pub fn apply(
        ctx: &Context<LzReceiveTypes>,
        params: &LzReceiveTypeParams,
    ) -> Result<Vec<LzAccount>> {
        let program_id = ctx.program_id;

        let (sol_treasury, _) = Pubkey::find_program_address(
            &[b"sol_treasury"],
            &program_id,
        );

        let (tristero_oapp, _) = Pubkey::find_program_address(
            &[b"TristeroOapp"], 
            &program_id
        );

        /* analyze msg from arb, msg consists of trade_match_id, to_token_address
        0: msgType
        1: tradeMatchID,
        2: destAddr
        3: destMint
        4: sender_eid,
        5: sender
        */
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        msg!("==> {:#?}", msg_vec.len());
        let mix_id_msg_type = msg_vec[0];
        let mut temp:Vec<u8> = vec![0];
        temp.extend_from_slice(mix_id_msg_type[1..].as_ref());
        let temp_arr = temp.try_into().expect("Vec has wrong length");
        let trade_match_id =  vec_to_u64(temp_arr);
        let to_token_addr = Pubkey::new_from_array(msg_vec[1]);
        let token_mint = Pubkey::new_from_array(msg_vec[2]);
        // let sender_eid = vec_to_u32(msg_vec[4]);
        let sender_eid: u32 = 40231;
        let sender_addr = msg_vec[3];

        // account 5
        let (staking_account, _) = Pubkey::find_program_address(
            &[b"staking_account", &token_mint.to_bytes()],
            &program_id
        );

        let (trade_match, _) = Pubkey::find_program_address(
            &[b"trade_match", &trade_match_id.to_be_bytes()],
            &program_id
        );

        let mut accounts = vec![
            // LzAccount { pubkey: sol_treasury, is_signer: true, is_writable: true },      // 0
            LzAccount { pubkey: tristero_oapp, is_signer: false, is_writable: true }, //1
            LzAccount { pubkey: to_token_addr, is_signer: false, is_writable: true }, // 2
            LzAccount { pubkey: staking_account, is_signer: false, is_writable: true }, // 3
            LzAccount { pubkey: trade_match, is_signer: false, is_writable: true }, // 4
            LzAccount { pubkey: TOKEN_PROGRAM_ID, is_signer: false, is_writable: false } // 5
        ];

        // From here, handle remaining accounts
        let endpoint_program_id = Pubkey::from_str("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6").unwrap(); //ok 0
        
        let send_library_program = Pubkey::from_str("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH").unwrap(); //ok 2
        let (send_library_config, _) = Pubkey::find_program_address( //ok 3
            &[b"SendLibraryConfig", tristero_oapp.key().as_ref(), &sender_eid.to_be_bytes()],
            &endpoint_program_id
        );
        let (default_send_library_config, _) = Pubkey::find_program_address( //ok 4
            &[b"SendLibraryConfig", &sender_eid.to_be_bytes()],
            &endpoint_program_id
        );
        
        
        let (send_library_info, _) = Pubkey::find_program_address( // ok 5
            &[b"MessageLib", ctx.accounts.token_mint.key().as_ref()],
            &endpoint_program_id
        );



        let (endpoint_pda, _) = Pubkey::find_program_address( // ok 6
            &[b"Endpoint"],
            &endpoint_program_id
        );
        let (nonce_pda, _) = Pubkey::find_program_address( // ok 7
            &[b"Nonce", tristero_oapp.key().as_ref(), &sender_eid.to_be_bytes(), sender_addr.as_ref()],
            &endpoint_program_id
        );
        let (event_authority, _) = Pubkey::find_program_address( // ok 8
            &[b"__event_authority"],
            &endpoint_program_id
        );
        let (uln_program_pda, _) = Pubkey::find_program_address( // ok 10
            &[b"MessageLib"], 
            &send_library_program
        );
        let (send_config, _) = Pubkey::find_program_address( // ok 11
            &[b"SendConfig", &sender_eid.to_be_bytes(), tristero_oapp.key().as_ref()], 
            &send_library_program
        );
        let (default_send_config, _) = Pubkey::find_program_address( // ok 12
            &[b"SendConfig", &sender_eid.to_be_bytes()], 
            &send_library_program
        );
        let signer1 = Pubkey::default(); // ok 13
        let signer2 = Pubkey::default(); // ok 14
        let system_program_id = SYSTEM_ID; // ok 15
        let (uln_authority, _) = Pubkey::find_program_address( // ok 16
            &[b"__event_authority"],
            &send_library_program
        );
        // let send_library_program ok 17
        let executor_program_id = Pubkey::from_str("6doghB248px58JSSwG4qejQ46kFMW4AMj7vzJnWZHNZn").unwrap(); // ok 18
        let (executor_pda_deriver, _) = Pubkey::find_program_address( // ok 19
            &[b"ExecutorConfig"],
            &executor_program_id
        );
        let price_fee_program_id = Pubkey::from_str("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP").unwrap(); // ok 20
        let (price_fee_program_pda, _) = Pubkey::find_program_address( // ok 21
            &[b"PriceFeed"],
            &price_fee_program_id
        );
        let dvn_program_id = Pubkey::from_str("HtEYV4xB4wvsj5fgTkcfuChYpvGYzgzwvNhgDZQNh7wW").unwrap(); // ok 22
        let (dvn_derive_config, _) = Pubkey::find_program_address( // ok 23
            &[b"DvnConfig"],
            &dvn_program_id
        );
        let price_fee_program_id = Pubkey::from_str("8ahPGPjEbpgGaZx2NV1iG5Shj7TDwvsjkEDcGWjt94TP").unwrap(); // ok 24
        let (price_fee_program_pda, _) = Pubkey::find_program_address( // ok 25
            &[b"PriceFeed"],
            &price_fee_program_id
        );
        
        // remaining accounts
        accounts.extend_from_slice(&[
            // LzAccount { pubkey: endpoint_program_id, is_signer: false, is_writable: true },
            LzAccount { pubkey: tristero_oapp, is_signer: false, is_writable: true },
            // LzAccount { pubkey: send_library_program, is_signer: false, is_writable: true },
            LzAccount { pubkey: send_library_config, is_signer: false, is_writable: true },
            LzAccount { pubkey: default_send_library_config, is_signer: false, is_writable: true },
            LzAccount { pubkey: send_library_info, is_signer: false, is_writable: true },
            LzAccount { pubkey: endpoint_pda, is_signer: false, is_writable: true },
            LzAccount { pubkey: nonce_pda, is_signer: false, is_writable: true },
            LzAccount { pubkey: event_authority, is_signer: false, is_writable: true },
            LzAccount { pubkey: endpoint_program_id, is_signer: false, is_writable: true }, 
            LzAccount { pubkey: uln_program_pda, is_signer: false, is_writable: true },
            LzAccount { pubkey: send_config, is_signer: false, is_writable: true },
            LzAccount { pubkey: default_send_config, is_signer: false, is_writable: true },
            // LzAccount { pubkey: signer1, is_signer: false, is_writable: true },
            LzAccount { pubkey: sol_treasury, is_signer: false, is_writable: true },
            LzAccount { pubkey: system_program_id, is_signer: false, is_writable: true },
            LzAccount { pubkey: uln_authority, is_signer: false, is_writable: true },
            LzAccount { pubkey: send_library_program, is_signer: false, is_writable: true },
            LzAccount { pubkey: executor_program_id, is_signer: false, is_writable: true },
            LzAccount { pubkey: executor_pda_deriver, is_signer: false, is_writable: true },
            LzAccount { pubkey: price_fee_program_id, is_signer: false, is_writable: true },
            LzAccount { pubkey: price_fee_program_pda, is_signer: false, is_writable: true },
            LzAccount { pubkey: dvn_program_id, is_signer: false, is_writable: true },
            LzAccount { pubkey: dvn_derive_config, is_signer: false, is_writable: true },
            // LzAccount { pubkey: price_fee_program_id, is_signer: false, is_writable: true },
            // LzAccount { pubkey: price_fee_program_pda, is_signer: false, is_writable: true },
        ]);

        Ok(accounts)
    }
}

/// same to anchor_lang::prelude::AccountMeta
#[derive(Clone, AnchorSerialize, AnchorDeserialize, Debug)]
pub struct LzAccount {
    pub pubkey: Pubkey,
    pub is_signer: bool,
    pub is_writable: bool,
}
