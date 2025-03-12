use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, TokenAccount, Transfer};
use spl_token::ID as TOKEN_PROGRAM_ID;
use {crate::error::*, crate::state::*};

#[derive(Accounts)]
#[instruction(params: FillSwapParams)]
pub struct FillSwap<'info> {
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
        seeds = [b"order", &params.order_idx.to_be_bytes()],
        bump = order.bump
    )]
    pub order: Box<Account<'info, Order>>,

    #[account(
        init,
        payer = authority,
        space = TradeMatch::LEN,
        seeds = [b"trade_match".as_ref(), &params.trade_match_id.to_be_bytes()],
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    #[account(
        init_if_needed,
        payer = authority,
        seeds = [b"staking_account", source_token_mint.key().as_ref()],
        bump,
        token::mint = source_token_mint,
        token::authority = oapp,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    pub bond_asset_mint: Box<Account<'info, Mint>>,
    pub source_token_mint: Box<Account<'info, Mint>>,

    #[account(
        init_if_needed,
        payer = authority,
        seeds = [b"staking_bond_account", order.bond_asset_mint.as_ref()],
        bump,
        token::mint = bond_asset_mint,
        token::authority = oapp,
    )]
    pub staking_bond_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = user_token_account.owner == order.user_pubkey @ CustomError::InvalidTokenOwner,
        constraint = user_token_account.mint == order.source_token_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub user_token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = bonder_bond_token_account.owner == authority.key() @ CustomError::InvalidAuthority,
        constraint = bonder_bond_token_account.mint == order.bond_asset_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub bonder_bond_token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct FillSwapParams {
    pub order_idx: u64,
    pub trade_match_id: u64,
}

pub fn fill_swap(ctx: Context<FillSwap>, params: &FillSwapParams) -> Result<()> {
    let order = ctx.accounts.order.as_mut();
    let trade_match = ctx.accounts.trade_match.as_mut();

    // Check conditions
    require!(order.settled == 0, CustomError::OrderAlreadyMatched);
    require!(
        order.match_pubkey == Some(ctx.accounts.authority.key()),
        CustomError::InvalidAuthority
    );

    // Update order and trade match
    order.settled += order.source_sell_amount;
    trade_match.status = 1; // Mark as filled

    // Transfer tokens
    let cpi_accounts = Transfer {
        from: ctx.accounts.user_token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };
    let seeds = &[b"TristeroOapp".as_ref(), &[ctx.bumps.oapp]];
    let signer_seeds = &[&seeds[..]];

    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            cpi_accounts,
            signer_seeds,
        ),
        order.source_sell_amount,
    )?;

    // Transfer bond tokens back to bonder
    let cpi_accounts_bond = Transfer {
        from: ctx.accounts.staking_bond_account.to_account_info(),
        to: ctx.accounts.bonder_bond_token_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };
    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            cpi_accounts_bond,
            signer_seeds,
        ),
        order.bond_amount,
    )?;

    Ok(())
}
