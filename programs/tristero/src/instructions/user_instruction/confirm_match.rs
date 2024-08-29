use anchor_lang::prelude::*;
use anchor_spl::{
    token::{self, Transfer, Mint, TokenAccount},
};
use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;

#[derive(Accounts)]
#[instruction(params: ConfirmMatchParams)]
pub struct ConfirmMatch<'info> {
    #[account(mut)]
    pub signer: Signer<'info>,

    /// CHECK: The PDA of the OApp
    #[account(
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,

    /// token account address
    #[account(
        mut,
        seeds = [b"order", &trade_match.src_index.to_be_bytes()],
        bump = order.bump
    )]
    pub order: Box<Account<'info, Order>>,

    #[account(
        mut,
        seeds = [b"trade_match".as_ref(), &params.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
        // constraint = trade_match.status == 1u8 @ CustomError::InvalidTradeMatch
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    #[account(
        mut,
        seeds = [b"staking_account", trade_match.source_token_mint.as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    /// sol user's token account address
    #[account(
        mut,
        constraint = token_account.mint == trade_match.source_token_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct ConfirmMatchParams {
    pub trade_match_id: u64
}

pub fn confirm_match(ctx: Context<ConfirmMatch>, params: &ConfirmMatchParams) -> Result<()>  {
    let trade_match = ctx.accounts.trade_match.as_mut();
    let order = ctx.accounts.order.as_mut();

    // ---------------------Transfer the source token to the user from staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.staking_account.to_account_info(),
        to: ctx.accounts.token_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];
    
    token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;

    trade_match.status = 2u8;
    order.settled += trade_match.source_sell_amount;

    Ok(())
}