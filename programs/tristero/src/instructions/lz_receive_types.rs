use crate::*;
use anchor_lang::solana_program;
use anchor_spl::{
    associated_token::{get_associated_token_address_with_program_id, ID as ASSOCIATED_TOKEN_ID},
    token_interface::Mint,
};
use spl_token::ID as TOKEN_PROGRAM_ID;
use solana_program::system_program;

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

fn find_pda(program_id: &Pubkey, seeds: &[&[u8]]) -> (Pubkey, u8) {
    Pubkey::find_program_address(seeds, program_id)
}

// account structure
// account 0 - payer (executor)
// account 1 - admin_panel
// account 2 - token mint
// account 3 - associated token account
// account 4 - dest wallet address
// account 4 - staking account
// account 5 - trade match
// account 6 - system program
// account 7 - associated token program
impl LzReceiveTypes<'_> {
    pub fn apply(
        ctx: &Context<LzReceiveTypes>,
        params: &LzReceiveTypeParams,
    ) -> Result<Vec<LzAccount>> {
        let oft = &ctx.accounts.oft_config;

        let (admin_panel, _) = Pubkey::find_program_address(
            &[b"admin_panel"],
            ctx.program_id,
        );

        // account 0..1
        let mut accounts = vec![
            LzAccount { pubkey: Pubkey::default(), is_signer: true, is_writable: true }, // 0
            LzAccount { pubkey: admin_panel, is_signer: false, is_writable: true },      // 1
        ];

        // analyze msg from arb, msg consists of trade_match_id, dest_token_mint, to_address
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let trade_match_id =  vec_to_u64(msg_vec[0]);
        let token_mint = Pubkey::new_from_array(msg_vec[1]);
        let to_address = Pubkey::new_from_array(msg_vec[2]);

        msg!("trade_match_id => {:#?}, token_mint => {:#?}, to_address => {:#?}", trade_match_id, token_mint, to_address);

        accounts.extend_from_slice(&[
            LzAccount { pubkey: token_mint, is_signer: false, is_writable: false }, // 2
        ]);
        // account 3
        let (token_dest, _) = Pubkey::find_program_address(
            &[b"refund_account", &to_address.to_bytes()],
            ctx.program_id,
        );
        accounts.extend_from_slice(&[
            LzAccount { pubkey: token_dest, is_signer: false, is_writable: false }, // 3
            LzAccount { pubkey: to_address, is_signer: true, is_writable: false }, // 4
        ]);

        // account 5
        let (staking_account, _) = Pubkey::find_program_address(
            &[b"staking_account", &token_dest.to_bytes()],
            ctx.program_id
        );
        accounts.extend_from_slice(&[
            LzAccount { pubkey: staking_account, is_signer: false, is_writable: false }, // 5
        ]);

        // account 6
        let (trade_match, _) = Pubkey::find_program_address(
            &[b"trade_match", &trade_match_id.to_be_bytes()],
            ctx.program_id
        );

        accounts.extend_from_slice(&[
            LzAccount { pubkey: trade_match, is_signer: false, is_writable: false }, // 6
        ]);

        // account 7, 8
        accounts.extend_from_slice(&[
            LzAccount { pubkey: system_program::ID, is_signer: false, is_writable: false }, // 7
            LzAccount { pubkey: TOKEN_PROGRAM_ID, is_signer: false, is_writable: false } // 8
        ]);

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
