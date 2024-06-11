use crate::*;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use cpi_helper::CpiContext;
use endpoint::{
    self,
    cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate},
    instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    },
    ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED,
    NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED,
    state::endpoint::*,
};

#[derive(Accounts)]
pub struct RegisterTristeroOApp<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    /// The PDA of the OApp
    pub oapp: Signer<'info>,
    #[account(
        init,
        payer = payer,
        space = 8 + OAppRegistry::INIT_SPACE,
        seeds = [OAPP_SEED, oapp.key.as_ref()],
        bump
    )]
    pub oapp_registry: Account<'info, OAppRegistry>,
    pub system_program: Program<'info, System>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct RegisterTristeroOAppParams{
    pub endpoint_program: Pubkey,
    pub seeds: Vec<Vec<u8>>,
    pub delegate: Pubkey,
}

pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: &RegisterTristeroOAppParams) -> Result<()> {
    // Solana endpoints id: 76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6
    let cpi_param = RegisterOAppParams {
        delegate: params.delegate
    };
    let cpi_refs: Vec<&[u8]> = params.seeds.iter().map(|v| v.as_slice()).collect();
    let cpi_seeds: &[&[u8]] = &cpi_refs;
    let cpi_ctx = RegisterOApp::construct_context(params.endpoint_program, &ctx.accounts.to_account_infos())?;
    
    msg!("cpi_ctx complete success");

    endpoint::cpi::register_oapp(cpi_ctx.with_signer(&[cpi_seeds]), cpi_param);
    Ok(())
}