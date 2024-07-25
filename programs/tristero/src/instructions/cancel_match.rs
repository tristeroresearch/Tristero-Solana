use anchor_lang::{
    prelude::*,
    solana_program::{
        program::{invoke, invoke_signed},
        system_instruction,
    }, system_program,
};
use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::*;

use {crate::error::*, crate::state::*};
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;

#[derive(Accounts)]
#[instruction(params: CancelMatchParams)]
pub struct CancelMatch<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// token account address
    #[account(
        mut,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.src_index.to_be_bytes()],
        constraint = trade_match.user_pubkey == authority.key() @ CustomError::WrongAuthorityToCancel,
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct CancelMatchParams {
    pub src_index: u64
}

pub fn cancel_match(ctx: Context<CancelMatch>, params: &CancelMatchParams) -> Result<()>  {
    let trade_match = ctx.accounts.trade_match.as_mut();
    
    // ---------------------Transfer from staking account to source token account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.staking_account.to_account_info(),
        to: ctx.accounts.token_account.to_account_info(),
        authority: ctx.accounts.admin_panel.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    msg!("Here is for transfer token");

    let signer_seeds: &[&[&[u8]]] = &[&[b"admin_panel", &[ctx.bumps.admin_panel]]];
    token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;

    trade_match.is_valiable = false;

    Ok(())
}