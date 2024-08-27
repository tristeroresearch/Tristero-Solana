use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{token::{self, Transfer, Mint, TokenAccount}};
use endpoint::{
    self, cpi::accounts::Send, instructions::SendParams, ConstructCPIContext,
};
use std::str::FromStr;

use solana_program::{native_token::LAMPORTS_PER_SOL, program::invoke_signed};
use oapp::endpoint::{
    cpi::accounts::Clear,
    instructions::{ClearParams, SendComposeParams},
};

#[derive(Accounts, Clone)]
pub struct LzReceive<'info> {
    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,

    #[account(
        mut
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzReceiveParams {
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
}

impl LzReceive<'_> {
    pub fn apply(ctx: &mut Context<LzReceive>, params: &LzReceiveParams) -> Result<()> {
        let remaining_accounts = ctx.remaining_accounts;
        let tristero_oapp_bump = ctx.bumps.oapp;
        let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[tristero_oapp_bump]]];
        let seed = signer_seeds[0];

        let accounts_for_clear = &ctx.remaining_accounts[4..12];
        let endpoint_program_id = Pubkey::from_str("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6").unwrap();
        let _ = oapp::endpoint_cpi::clear(
            endpoint_program_id,
            ctx.accounts.oapp.key(),
            accounts_for_clear,
            seed,
            ClearParams {
                receiver: ctx.accounts.oapp.key(),
                src_eid: params.src_eid,
                sender: params.sender,
                nonce: params.nonce,
                guid: params.guid,
                message: params.message.clone(),
            },
        )?;

        let trade_match = ctx.accounts.trade_match.as_mut();

        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let mix_id_msg_type = vec_to_u64(msg_vec[0]);
        let to_token_addr = Pubkey::new_from_array(msg_vec[1]);
        let msg_type =  mix_id_msg_type % 16; // 1: start_challenge from arb, 2: finish_challenge from arb

        /* analyze msg from arb, msg consists of trade_match_id, to_token_address
        0: trade_match_id & msgType(1: start_challenge, 2: finish_challenge, 3: create_match, 4: execute_match)
        1: destTokenAddr,
        2: destTokenMint
        */
        if msg_type == 1u64 {
            require!(trade_match.status == 0u8, CustomError::NotAgain);
            trade_match.arb_user_token_account = to_token_addr;
            trade_match.status = 1u8;
        } else if msg_type == 2u64{
            require!(trade_match.status == 1u8, CustomError::NotEvenStarted);
            let authority = remaining_accounts[0].to_account_info();
            let stake_acc = remaining_accounts[1].to_account_info();
            let token_acc = remaining_accounts[2].to_account_info();

            // ---------------------Transfer the source token from the staking account----------------------------------
            let cpi_accounts = Transfer {
                from: stake_acc,
                to: token_acc,
                authority: authority
            };

            let cpi_context = CpiContext::new(remaining_accounts[3].to_account_info(), cpi_accounts);
            token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;

            trade_match.status = 2u8;
        } else if msg_type == 3u64 {
            trade_match.status = 1u8;
        } else if msg_type == 4u64 {

        }
        Ok(())
    }
}