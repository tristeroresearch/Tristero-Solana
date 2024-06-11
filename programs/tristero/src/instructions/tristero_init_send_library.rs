use crate::*;
use cpi_helper::CpiContext;
use anchor_lang::{
    prelude::*,
    solana_program::{keccak::hash, system_program::ID as SYSTEM_ID},
};
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        oapp::send::*, ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams, SendParams, SetDelegateParams
    }, state::{endpoint::*, message_lib::*, messaging_channel::*}, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
#[instruction(params: TristeroInitSendLibraryParams)]
pub struct TristeroInitSendLibrary<'info> {
    /// only the delegate can initialize the send_library_config
    #[account(mut)]
    pub delegate: Signer<'info>,
    #[account(
        seeds = [OAPP_SEED, params.sender.as_ref()],
        bump = oapp_registry.bump,
        has_one = delegate
    )]
    pub oapp_registry: Account<'info, OAppRegistry>,
    #[account(
        init,
        payer = delegate,
        space = 8 + SendLibraryConfig::INIT_SPACE,
        seeds = [SEND_LIBRARY_CONFIG_SEED, &params.sender.to_bytes(), &params.eid.to_be_bytes()],
        bump
    )]
    pub send_library_config: Account<'info, SendLibraryConfig>,
    pub system_program: Program<'info, System>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroInitSendLibraryParams {
    pub sender: Pubkey,
    pub eid: u32,
}

pub fn tristero_init_send_library(
    ctx: Context<TristeroInitSendLibrary>,
    _params: &TristeroInitSendLibraryParams,
) -> Result<()> {
    ctx.accounts.send_library_config.message_lib = DEFAULT_MESSAGE_LIB;
    ctx.accounts.send_library_config.bump = ctx.bumps.send_library_config;
    Ok(())
}