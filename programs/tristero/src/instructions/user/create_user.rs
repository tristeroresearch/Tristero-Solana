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

    // /// CHECK: The PDA of the OApp
    // #[account(
    //     mut,
    //     seeds = [b"TristeroOapp"],
    //     bump
    // )]
    // pub oapp: AccountInfo<'info>,

    pub system_program: Program<'info, System>,
}


pub fn create_user(ctx: Context<CreateUser>) -> Result<()> {
    //   Remain Accounts
    //         payer: user.publicKey, //0
    //         oapp: tristeroOappPubkey, //1
    //         oappRegistry: getOappPDA(tristeroOappPubkey), //2
    //         endpointProgram: endpoint, //3
    //         systemProgram: SystemProgram.programId, //4
    //         eventAuthority: endpointEventPdaDeriver.eventAuthority()[0], //5

    // -------------------register tristero oapp-----------------------
    // let cpi_param = RegisterOAppParams {
    //     delegate: ctx.accounts.authority.key()
    // };

    // let cpi_ctx = RegisterOApp::construct_context(ctx.remaining_accounts[3].key(), ctx.remaining_accounts)?;
    // msg!("cpi_ctx complete success");
    // let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];
    // endpoint::cpi::register_oapp(cpi_ctx.with_signer(signer_seeds), cpi_param)?;


    // --------------------create new user------------------------------
    let user = ctx.accounts.user.as_mut();
    user.authority = ctx.accounts.authority.key();
    user.user_bump = ctx.bumps.user;
    user.match_count = 0u8;

    Ok(())
}