use crate::*;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use anchor_spl::token::TokenAccount;
use cpi_helper::CpiContext;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    }, state::endpoint::*, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
pub struct RegisterTristeroOApp<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    /// CHECK: The PDA of the OApp
    #[account(
        init,
        space = 8 + 165,
        payer = payer,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,
    /// CHECK: oapp registry
    #[account(
        mut,
        seeds = [OAPP_SEED, oapp.key.as_ref()],
        bump,
        seeds::program = endpoint_program.key()
    )]
    pub oapp_registry: AccountInfo<'info>,
    /// CHECK: 
    pub event_authority: AccountInfo<'info>,
    pub system_program: Program<'info, System>,
    /// CHECK: endpoint program's id
    #[account(executable)]
    pub endpoint_program: AccountInfo<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct RegisterTristeroOAppParams{
    pub delegate: Pubkey,
}

pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: &RegisterTristeroOAppParams) -> Result<()> {
    msg!("oapp start!");
    // Solana endpoints id: 76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6
    let cpi_param = RegisterOAppParams {
        delegate: params.delegate
    };

    let accounts = &[
        ctx.accounts.endpoint_program.to_account_info(),
        ctx.accounts.payer.to_account_info(),
        ctx.accounts.oapp.to_account_info(),
        ctx.accounts.oapp_registry.to_account_info(),
        ctx.accounts.system_program.to_account_info(),
        ctx.accounts.event_authority.to_account_info(),
        ctx.accounts.endpoint_program.to_account_info(),
    ];
    msg!("constructing cpi context");

    
    msg!("oapp {}", ctx.accounts.oapp.key());
    msg!("oapp_registry {}", ctx.accounts.oapp_registry.key());
    msg!("endpoint_program {}", ctx.accounts.endpoint_program.key());
    
    let cpi_ctx = RegisterOApp::construct_context(ctx.accounts.endpoint_program.key(), accounts)?;
    
    msg!("cpi_ctx complete success");

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];


    endpoint::cpi::register_oapp(cpi_ctx.with_signer(signer_seeds), cpi_param)
}