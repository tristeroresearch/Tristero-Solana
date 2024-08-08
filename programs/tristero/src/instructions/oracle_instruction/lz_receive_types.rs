use std::str::FromStr;

use crate::*;
use anchor_lang::solana_program;
use spl_token::ID as TOKEN_PROGRAM_ID;
use solana_program::system_program;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};

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

        let (admin_panel, _) = Pubkey::find_program_address(
            &[b"admin_panel"],
            &program_id,
        );

        let (sol_panel, _) = Pubkey::find_program_address(
            &[b"sol_panel"],
            &program_id,
        );

        let (oapp, _) = Pubkey::find_program_address(
            &[b"TristeroOapp"], 
            &program_id
        );

        // account 0..1
        let mut accounts = vec![
            LzAccount { pubkey: Pubkey::default(), is_signer: true, is_writable: true }, // 0
            LzAccount { pubkey: oapp, is_signer: false, is_writable: true }, //1
            LzAccount { pubkey: admin_panel, is_signer: false, is_writable: true },      // 2
            LzAccount { pubkey: sol_panel, is_signer: false, is_writable: true },      // 3
        ];

        // analyze msg from arb, msg consists of trade_match_id, dest_token_mint, to_address
        /*
        0: trade_match_id,
        1: token_mint,
        2: arb user's sol addr
        3: 
        4: sender_eid,
        5: 
        */
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let trade_match_id =  vec_to_u64(msg_vec[0]);
        let token_mint = Pubkey::new_from_array(msg_vec[1]);
        let to_address = Pubkey::new_from_array(msg_vec[2]);
        let sender_eid = vec_to_u32(msg_vec[4]);
        let sender_addr = msg_vec[5];

        msg!("trade_match_id => {:#?}, token_mint => {:#?}, to_address => {:#?}", trade_match_id, token_mint, to_address);

        accounts.extend_from_slice(&[
            LzAccount { pubkey: token_mint, is_signer: false, is_writable: true }, // 4
        ]);
        // account 3
        let (token_dest, _) = Pubkey::find_program_address(
            &[b"refund_account", &to_address.to_bytes()],
            &program_id,
        );
        accounts.extend_from_slice(&[
            LzAccount { pubkey: token_dest, is_signer: false, is_writable: true }, // 5
            LzAccount { pubkey: to_address, is_signer: false, is_writable: true }, // 6
        ]);

        // account 5
        let (staking_account, _) = Pubkey::find_program_address(
            &[b"staking_account", &token_mint.to_bytes()],
            &program_id
        );
        accounts.extend_from_slice(&[
            LzAccount { pubkey: staking_account, is_signer: false, is_writable: true }, // 7
        ]);

        // account 6
        let (trade_match, _) = Pubkey::find_program_address(
            &[b"trade_match", &trade_match_id.to_be_bytes()],
            &program_id
        );

        accounts.extend_from_slice(&[
            LzAccount { pubkey: trade_match, is_signer: false, is_writable: true }, // 8
        ]);

        // account 9, 10
        accounts.extend_from_slice(&[
            LzAccount { pubkey: system_program::ID, is_signer: false, is_writable: false }, // 9
            LzAccount { pubkey: TOKEN_PROGRAM_ID, is_signer: false, is_writable: false } // 10
        ]);

        // From here, handle remaining accounts
        let endpoint_program_id = Pubkey::from_str("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6").unwrap(); //ok 0
        let (tristero_oapp, _) = Pubkey::find_program_address( //ok 1
            &[b"TristeroOapp", &token_mint.to_bytes()],
            &program_id
        );
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
            &[b"MessageLib", &default_send_library_config.key().to_bytes()],
            &endpoint_program_id
        );
        let (endpoint_pda, _) = Pubkey::find_program_address( // ok 6
            &[b"Endpoint", &sender_eid.to_be_bytes()],
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
        //endpoint_program_id // ok 9
        let uln_program_id = send_library_program; // ok 10
        let (send_config, _) = Pubkey::find_program_address( // ok 11
            &[b"SendConfig", &sender_eid.to_be_bytes(), sender_addr.as_ref()], 
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
        

        Ok(accounts)
    }
}

/// same to anchor_lang::prelude::AccountMeta
#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzAccount {
    pub pubkey: Pubkey,
    pub is_signer: bool,
    pub is_writable: bool,
}
