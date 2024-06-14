use {anchor_lang::prelude::*, crate::state::*};
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use anchor_lang::solana_program::keccak::hashv;

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

    /// close the account and return the lamports to endpoint settings account
    #[account(
        mut,
        seeds = [
            PAYLOAD_HASH_SEED,
            params.receiver.as_ref(),
            &params.src_eid.to_be_bytes(),
            &params.sender[..],
            &params.nonce.to_be_bytes()
        ],
        bump = payload_hash.bump,
        //close = endpoint
    )]
    pub payload_hash: Box<Account<'info, PayloadHash>>,

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
    pub receiver: Pubkey,
    pub executor: Pubkey,
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub compute_units: u64,
    pub value: u64,
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
    pub reason: Vec<u8>,
}

pub fn swap_token(ctx: Context<SwapToken>, params: &SwapTokenParams) -> Result<()>  {
    let payload_hash = hash_payload(&params.guid, &params.message);
    require!(
        payload_hash == ctx.accounts.payload_hash.hash,
        CustomError::PayloadHashNotFound
    );

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    token::transfer(cpi_context, ctx.accounts.trade_match.source_sell_amount)?;
    // -------------------------------------------------------
    
    Ok(())
}

pub fn hash_payload(guid: &[u8; 32], message: &[u8]) -> [u8; 32] {
    hashv(&[&guid[..], &message[..]]).to_bytes()
}