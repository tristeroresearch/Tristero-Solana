use std::str::FromStr;

use crate::*;
use spl_token::ID as TOKEN_PROGRAM_ID;
use anchor_lang::solana_program::system_program::ID as SYSTEM_ID;

#[derive(Accounts)]
pub struct LzReceiveTypes<'info> {
    /// CHECK:
    pub oft_config: UncheckedAccount<'info>,
    /// CHECK:
    pub message_lib: UncheckedAccount<'info>,
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

        let (tristero_oapp, _) = Pubkey::find_program_address(
            &[b"TristeroOapp"], 
            &program_id
        );

        /* analyze msg from arb, msg consists of trade_match_id, to_token_address
        0: trade_match_id & msgTyp
        1: destTokenAddr,
        2: destTokenMint
        */
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        msg!("==> {:#?}", msg_vec.len());
        let mix_id_msg_type = vec_to_u64(msg_vec[0]);
        let trade_match_id =  mix_id_msg_type / 16u64;
        let msg_type = mix_id_msg_type % 16;
        let sender_eid: u32 = 40231;
        let mut accounts = Vec::new();
        let (trade_match, _) = Pubkey::find_program_address(
            &[b"trade_match", &trade_match_id.to_be_bytes()],
            &program_id
        );
        
        let to_token_addr = Pubkey::new_from_array(msg_vec[1]);
        let token_mint = Pubkey::new_from_array(msg_vec[2]);

        let (staking_account, _) = Pubkey::find_program_address(
            &[b"staking_account", &token_mint.to_bytes()],
            &program_id
        );

        accounts = vec![
            LzAccount { pubkey: tristero_oapp, is_signer: false, is_writable: true }, //0
            LzAccount { pubkey: trade_match, is_signer: false, is_writable: true }, // 1
            LzAccount { pubkey: tristero_oapp, is_signer: false, is_writable: true }, //2
            LzAccount { pubkey: staking_account, is_signer: false, is_writable: true }, // 3
            LzAccount { pubkey: to_token_addr, is_signer: false, is_writable: true }, // 4
            LzAccount { pubkey: TOKEN_PROGRAM_ID, is_signer: false, is_writable: false }, // 5
        ];
        
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
