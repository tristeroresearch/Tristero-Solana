use {anchor_lang::prelude::*, crate::state::*};
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use cpi_helper::CpiContext;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    }, state::endpoint::*, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
pub struct CreateUser<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        init,
        payer = authority,
        space = User::LEN,
        seeds = [b"user", authority.key().as_ref()],
        bump
    )]
    pub user: Box<Account<'info, User>>,

    pub system_program: Program<'info, System>,
}


pub fn create_user(ctx: Context<CreateUser>) -> Result<()> {
    // --------------------create new user------------------------------
    let user = ctx.accounts.user.as_mut();
    user.authority = ctx.accounts.authority.key();
    user.user_bump = ctx.bumps.user;
    user.match_count = 0u8;

    Ok(())
}