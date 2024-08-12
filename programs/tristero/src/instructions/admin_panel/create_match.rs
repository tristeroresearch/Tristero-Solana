use anchor_lang::{
    prelude::*
};

use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;

#[derive(Accounts)]
#[instruction(params: CreateMatchParams)]
pub struct CreateMatch<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump = admin_panel.admin_panel_bump,
        has_one = authority
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// token account address
    #[account(
        mut,
        seeds = [b"order", &params.src_index.to_be_bytes()],
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

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct CreateMatchParams {
    pub src_index: u64,
    pub dst_index: u64,
    pub src_quantity: u64,
    pub dst_quantity: u64,
    pub trade_match_id: u64,
    pub arb_source_token_addr: [u8; 20],
}

pub fn create_match(ctx: Context<CreateMatch>, params: &CreateMatchParams) -> Result<()>  {
    let admin_panel = ctx.accounts.admin_panel.as_mut();
    let order = ctx.accounts.order.as_mut();
    let trade_match = ctx.accounts.trade_match.as_mut();

    require!(params.src_quantity >= order.min_sell_amount, CustomError::MinSellAmountConflict);
    require!(order.source_sell_amount - order.settled >= params.src_quantity, CustomError::InSufficientFundsOfOrder);

    trade_match.authority = order.user_pubkey;
    trade_match.user_token_addr = order.user_token_addr;
    trade_match.source_token_mint = order.source_token_mint;
    trade_match.dest_token_mint = order.dest_token_mint;
    trade_match.eid = order.eid;
    trade_match.bump = ctx.bumps.trade_match;
    trade_match.trade_match_id = admin_panel.match_count;
    trade_match.src_index = params.src_index;
    trade_match.dst_index = params.dst_index;
    trade_match.source_sell_amount = params.src_quantity;
    trade_match.dest_buy_amount = params.dst_quantity;
    trade_match.is_valiable = true;
    
    admin_panel.match_count += 1;

    Ok(())
}