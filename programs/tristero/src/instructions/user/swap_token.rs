use {anchor_lang::prelude::*, crate::state::*};
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};

use {crate::error::*, crate::state::*};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        oapp::send::*, ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams, SendParams, SetDelegateParams
    }, state::{endpoint::*, message_lib::*, messaging_channel::*}, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

use endpoint::events::LzReceiveAlertEvent;

#[derive(Accounts)]
#[instruction(params: SwapTokenParams)]
pub struct SwapToken<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// user's token account address
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"staking_account", authority.key().as_ref(), token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"user", authority.key().as_ref()],
        bump,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
        constraint = token_account.amount > params.source_sell_amount @ CustomError::InvalidTokenAmount,
    )]
    pub user: Box<Account<'info, User>>,

    #[account(
        mut,
        seeds = [b"trade_match", authority.key().as_ref(), token_mint.key().as_ref(), &trade_match.trade_match_id.to_be_bytes()],
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct SwapTokenParams {
    pub source_token_mint: Pubkey,
    pub source_sell_amount: u64,
    pub dest_token_mint: Pubkey,
    pub dest_buy_amount: u64,
    pub eid: u32,
    pub receiver: [u8; 32],
    pub options: Box<Vec<u8>>,
    pub native_fee: u64,
    pub lz_token_fee: u64,
}

pub fn swap_token(ctx: Context<SwapToken>, params: &SwapTokenParams) -> Result<()>  {
    LzReceiveAlertEvent

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    token::transfer(cpi_context, params.source_sell_amount)?;
    // -------------------------------------------------------
    
    Ok(())
}