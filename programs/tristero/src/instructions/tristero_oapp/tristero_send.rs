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

/// MESSAGING STEP 1

#[event_cpi]
#[derive(CpiContext, Accounts)]
#[instruction(params: TristeroSendParams)]
pub struct TristeroSend<'info> {
    /// CHECK:
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub sender: UncheckedAccount<'info>,
    
    #[account(executable)]
    pub endpoint_program: UncheckedAccount<'info>,
}

pub fn tristero_send(ctx: &Context<TristeroSend>, params: &TristeroSendParams) -> Result<()> {
    let cpi_params = SendParams {
        dst_eid: params.dst_eid,
        receiver: params.receiver,
        message: (*params.message).clone(),
        options: (*params.options).clone(),
        native_fee: params.native_fee,
        lz_token_fee: params.lz_token_fee,
    };

    let cpi_ctx = Send::construct_context(ctx.accounts.endpoint_program.key(), ctx.remaining_accounts)?;

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.sender]]];
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    Ok(())

}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroSendParams {
    pub dst_eid: u32,
    pub receiver: [u8; 32],
    pub message: Box<Vec<u8>>,
    pub options: Box<Vec<u8>>,
    pub native_fee: u64,
    pub lz_token_fee: u64,
}