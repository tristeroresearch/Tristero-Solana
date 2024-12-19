use anchor_lang::prelude::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{
    token::{self, Token, Transfer, TokenAccount, Mint},
};
use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;


#[derive(Accounts)]
#[instruction(params: CreateMatchParams)]
pub struct CreateMatch<'info> {
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
        seeds = [b"admin_panel"],
        bump = admin_panel.bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    #[account(
        mut,
        seeds = [b"order", &params.order_idx.to_be_bytes()],
        bump = order.bump
    )]
    pub order: Box<Account<'info, Order>>,

    pub source_token_mint: Box<Account<'info, Mint>>,

    #[account(
        mut,
        constraint = token_account.owner == order.user_pubkey @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == source_token_mint.key() @ CustomError::InvalidTokenMintAddress,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        init_if_needed,
        payer = authority,
        seeds = [b"staking_account", source_token_mint.key().as_ref()],
        bump,
        token::mint = source_token_mint,
        token::authority = oapp,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        init,
        payer = authority,
        space = TradeMatch::LEN,
        seeds = [b"trade_match".as_ref(), &admin_panel.match_count.to_be_bytes()],
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID)]
    pub token_program: Program<'info, Token>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct CreateMatchParams {
    pub order_idx: u64,
    pub src_quantity: u64,
    pub dst_quantity: u64,
}

pub fn create_match(ctx: Context<CreateMatch>, params: &CreateMatchParams) -> Result<()> {
    let admin_panel = ctx.accounts.admin_panel.as_mut();
    let order = ctx.accounts.order.as_mut();
    let trade_match = ctx.accounts.trade_match.as_mut();

    require!(params.src_quantity >= order.min_sell_amount, CustomError::MinSellAmountConflict);
    require!(order.source_sell_amount - order.settled >= params.src_quantity, CustomError::InSufficientFundsOfOrder);
    require!(order.match_pubkey!=None && order.match_pubkey == Some(ctx.accounts.authority.key()), CustomError::InvalidAuthority);

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let seeds = &[b"TristeroOapp".as_ref(), &[ctx.bumps.oapp]];
    let signer_seeds = &[&seeds[..]];

    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            cpi_accounts,
            signer_seeds
        ),
        params.src_quantity
    )?;

    // Set trade match details
    trade_match.authority = ctx.accounts.authority.key();
    trade_match.user_token_addr = order.user_token_addr;
    trade_match.source_token_mint = order.source_token_mint;
    trade_match.dst_token_mint = order.dst_token_mint;
    trade_match.eid = order.eid;
    trade_match.bump = ctx.bumps.trade_match;
    trade_match.trade_match_id = admin_panel.match_count;
    trade_match.order_idx = params.order_idx;
    trade_match.source_sell_amount = params.src_quantity;
    trade_match.dst_buy_amount = params.dst_quantity;
    trade_match.status = 0u8;

    admin_panel.match_count += 1;

    Ok(())
}