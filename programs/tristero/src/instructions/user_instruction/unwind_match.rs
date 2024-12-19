use anchor_lang::prelude::*;
use anchor_spl::{
    token::{self, Transfer, TokenAccount},
};
use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;

#[derive(Accounts)]
pub struct UnwindMatch<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    /// CHECK: PDA for OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [b"order", &trade_match.order_idx.to_be_bytes()],
        bump = order.bump,
    )]
    pub order: Box<Account<'info, Order>>,

    #[account(
        mut,
        seeds = [b"trade_match", &trade_match.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
        constraint = trade_match.authority == authority.key() @ CustomError::InvalidAuthority,
        constraint = trade_match.status == 0 @ CustomError::MatchAlreadyFinalized,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    #[account(
        mut,
        seeds = [b"staking_account", order.source_token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = user_token_account.owner == order.user_pubkey @ CustomError::InvalidTokenOwner,
        constraint = user_token_account.mint == order.source_token_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub user_token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

pub fn unwind_match(ctx: Context<UnwindMatch>) -> Result<()> {
    let trade_match = &mut ctx.accounts.trade_match;
    let order = &mut ctx.accounts.order;

    // Mark match as finalized
    trade_match.status = 1; // 1 = finalized

    // Return tokens from staking account to user
    let cpi_accounts = Transfer {
        from: ctx.accounts.staking_account.to_account_info(),
        to: ctx.accounts.user_token_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };

    let seeds = &[b"TristeroOapp".as_ref(), &[ctx.bumps.oapp]];
    let signer_seeds = &[&seeds[..]];

    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            cpi_accounts,
            signer_seeds
        ),
        trade_match.source_sell_amount
    )?;

    // Update order settled amount
    order.settled = order.settled.checked_sub(trade_match.source_sell_amount)
        .ok_or(CustomError::ArithmeticError)?;

    msg!("Match {} unwound", trade_match.trade_match_id);

    Ok(())
} 