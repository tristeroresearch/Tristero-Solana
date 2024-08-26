use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{token::{self, Transfer, Mint, TokenAccount}};
use endpoint::{
    self, cpi::accounts::Send, instructions::SendParams, ConstructCPIContext,
};
use std::str::FromStr;

use solana_program::{native_token::LAMPORTS_PER_SOL, program::invoke_signed};


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

        let trade_match = ctx.accounts.trade_match.as_mut();

        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let mix_id_msg_type = vec_to_u64(msg_vec[0]);
        let msg_type =  mix_id_msg_type % 16; // 1: start_challenge from arb, 2: finish_challenge from arb

        if msg_type == 1u64 {
            require!(trade_match.status == 0u8, CustomError::NotAgain);
            trade_match.status = 1u8;
        } else {
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
        }
        Ok(())
    }
}