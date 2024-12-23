use anchor_lang::prelude::*;
use anchor_spl::{
    token::{self, Transfer, TokenAccount},
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

    #[account(
        mut,
        seeds = [b"order", &trade_match.order_idx.to_be_bytes()],
        bump = order.bump
    )]
    pub order: Box<Account<'info, Order>>,

    #[account(
        mut,
        seeds = [b"trade_match".as_ref(), &params.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    #[account(
        mut,
        seeds = [b"staking_account", trade_match.source_token_mint.as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"staking_bond_account", order.bond_asset_mint.as_ref()],
        bump,
    )]
    pub staking_bond_account: Box<Account<'info, TokenAccount>>,

    /// The maker's (bonder's) token account for receiving maker payout + bonder fee
    #[account(mut)]
    pub bonder_token_account: Box<Account<'info, TokenAccount>>,

    /// The bonder's bond token account (to return bond tokens)
    #[account(
        mut,
        constraint = bonder_bond_token_account.owner == trade_match.authority @ CustomError::InvalidAuthority,
        constraint = bonder_bond_token_account.mint == order.bond_asset_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub bonder_bond_token_account: Box<Account<'info, TokenAccount>>,

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

    let order_amount = trade_match.source_sell_amount;
    let fee = order.bond_fee;
    let basis_points = 10000u64;

    let bonder_fee_payout = (fee as u64)
        .checked_mul(order_amount)
        .unwrap()
        .checked_div(basis_points)
        .unwrap();

    let maker_payout = order_amount.checked_sub(bonder_fee_payout).unwrap();
        // Transfer maker_payout to bonder_token_account (assuming bonder is the maker)
        {
            let cpi_accounts = Transfer {
                from: ctx.accounts.staking_account.to_account_info(),
                to: ctx.accounts.bonder_token_account.to_account_info(),
                authority: ctx.accounts.oapp.to_account_info(),
            };
    
            let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];
            token::transfer(
                CpiContext::new_with_signer(ctx.accounts.token_program.to_account_info(), cpi_accounts, signer_seeds),
                maker_payout
            )?;
        }
    
        // Transfer bonder_fee_payout to bonder_token_account as well (in this scenario, bonder is also receiving the fee)
        {
            let cpi_accounts = Transfer {
                from: ctx.accounts.staking_account.to_account_info(),
                to: ctx.accounts.bonder_token_account.to_account_info(),
                authority: ctx.accounts.oapp.to_account_info(),
            };
            let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];
            token::transfer(
                CpiContext::new_with_signer(ctx.accounts.token_program.to_account_info(), cpi_accounts, signer_seeds),
                bonder_fee_payout
            )?;
        }
    
        // Return bond_amount to the bonder from staking_bond_account
        {
            let cpi_accounts = Transfer {
                from: ctx.accounts.staking_bond_account.to_account_info(),
                to: ctx.accounts.bonder_bond_token_account.to_account_info(),
                authority: ctx.accounts.oapp.to_account_info(),
            };
            let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];
            token::transfer(
                CpiContext::new_with_signer(ctx.accounts.token_program.to_account_info(), cpi_accounts, signer_seeds),
                order.bond_amount
            )?;
        }

    trade_match.status = 2u8;
    order.settled += trade_match.source_sell_amount;

    Ok(())
}