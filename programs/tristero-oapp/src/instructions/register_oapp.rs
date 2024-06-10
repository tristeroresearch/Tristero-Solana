use crate::*;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use endpoint::{
    self,
    cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate},
    instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    },
    ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED,
    NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED,
};

#[derive(Accounts)]
pub struct RegisterOApp<'info> {
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

impl RegisterOApp<'_> {
    pub fn apply(ctx: &mut Context<RegisterOApp>, params: &TRegisterOAppParams) -> Result<()> {
        // Solana endpoints: 76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6
        oapp::cpi::register_oapp(params.endpoint_program, ctx.accounts.oapp.key(), ctx.accounts, params.seeds, params.delegate)
        Ok(())
    }
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TRegisterOAppParams {
    pub endpoint_program: Pubkey,
    pub seeds: &['static &['static u8]],
    pub delegate: Pubkey,
}
