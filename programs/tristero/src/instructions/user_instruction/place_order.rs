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
// use crate::instructions::tristero_send;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        oapp::send::*, ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams, SendParams, SetDelegateParams
    }, state::{endpoint::*, message_lib::*, messaging_channel::*}, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
#[instruction(params: PlaceOrderParams)]
pub struct PlaceOrder<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// CHECK:
    #[account(
        mut,
        seeds = [b"sol_panel"],
        bump,
    )]
    pub sol_panel: AccountInfo<'info>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// token account address
    #[account(
        mut,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
        constraint = token_account.amount > params.source_sell_amount @ CustomError::InvalidTokenAmount,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        init_if_needed,
        payer = authority,
        token::mint = token_mint,
        token::authority = admin_panel,
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        init,
        payer = authority,
        space = Order::LEN,
        seeds = [b"order".as_ref(), &params.order_id.to_be_bytes()],
        bump,
    )]
    pub order: Box<Account<'info, Order>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct PlaceOrderParams {
    pub source_sell_amount: u64,
    pub min_sell_amount: u64,
    pub dest_token_mint: [u8; 20],
    pub dest_buy_amount: u64,
    pub order_id: u64,
    pub eid: u32,
}

pub fn place_order(ctx: Context<PlaceOrder>, params: &PlaceOrderParams) -> Result<()>  {
    let admin_panel = ctx.accounts.admin_panel.as_mut();

    let order = ctx.accounts.order.as_mut();
    order.user_pubkey = ctx.accounts.authority.key();
    order.user_token_addr = ctx.accounts.token_account.key();
    order.source_token_mint = ctx.accounts.token_mint.key();
    order.source_sell_amount = params.source_sell_amount;
    order.min_sell_amount = params.min_sell_amount;
    order.dest_token_mint = params.dest_token_mint;
    order.dest_buy_amount = params.dest_buy_amount;
    order.eid = params.eid;
    order.bump = ctx.bumps.order;
    order.order_id = admin_panel.order_count;
    order.settled = 0u64;
    order.is_valiable = true;
    admin_panel.order_count += 1;

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    msg!("Here is for transfer token");
    token::transfer(cpi_context, params.source_sell_amount)?;

    // ---------------------Transfer the sol for fee to the sol staking account----------------------------------
    let ix = anchor_lang::solana_program::system_instruction::transfer(
        &ctx.accounts.authority.key(), 
        &ctx.accounts.sol_panel.key(), 
        5000000
    );
    msg!("Here is for transfer sol");
    let _ = anchor_lang::solana_program::program::invoke(
        &ix, 
        &[ctx.accounts.authority.to_account_info(), ctx.accounts.sol_panel.to_account_info()],
    );

    Ok(())
}