use std::borrow::{Borrow, BorrowMut};

use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{token::{self, Transfer, Mint, TokenAccount}};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::Send, instructions::SendParams, ConstructCPIContext,
};
use oapp::{
    endpoint::{
        cpi::accounts::Clear,
        instructions::{ClearParams, SendComposeParams},
        ID as ENDPOINT_ID,
    }
};

use solana_program::native_token::LAMPORTS_PER_SOL;

#[event_cpi]
#[derive(Accounts, Clone)]
#[instruction(params: LzReceiveParams)]
pub struct LzReceive<'info> {
    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump = oapp.bump
    )]
    pub oapp: Box<Account<'info, AdminPanel>>,

    /// token account address
    #[account(mut)]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"staking_account", token_account.mint.key().as_ref()],
        bump,
        
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = trade_match.is_valiable == true @ CustomError::NotAgain
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,
    
    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(
        constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard,
        constraint = token_account.mint.key() == trade_match.source_token_mint @ CustomError::InvalidTokenMintAddress
    )]
    pub token_program: AccountInfo<'info>,
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
        let mut accounts = ctx.accounts.clone().to_account_infos();
        let admin_panel = ctx.accounts.oapp.as_mut().clone();
        
        let trade_match = ctx.accounts.trade_match.as_mut();
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        
        let msg_type =  vec_to_u64(msg_vec[0]) % 16;

        msg!("msg_type: => {} {}", msg_type, vec_to_u64(msg_vec[0]));
        
        let stake_acc = ctx.accounts.staking_account.to_account_info();
        let token_acc = ctx.accounts.token_account.to_account_info();
        let authority = admin_panel.clone().to_account_info();

        let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[admin_panel.bump]]];

        // ---------------------Transfer the source token from the staking account----------------------------------
        let cpi_accounts = Transfer {
            from: stake_acc,
            to: token_acc,
            authority: authority
        };

        let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
        token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;

        

        if msg_type == 1u64 { // B->A
            trade_match.is_valiable = false;

        } else { // B->A->B
            emit_cpi!(MsgReceived{
                src_eid: params.src_eid,
                sender: params.sender,
                nonce: params.nonce,
                guid: params.guid,
                message: params.message.clone(),
                extra_data: params.extra_data.clone(),
            });
        }
        Ok(())
    }
}