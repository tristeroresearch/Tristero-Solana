use crate::*;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate, InitSendLibrary, InitReceiveLibrary, InitNonce}, instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams, InitSendLibraryParams, InitReceiveLibraryParams, InitNonceParams,
    }, state::endpoint::*, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
pub struct TristeroInitSendLibrary<'info> {
    /// CHECK:
    pub endpoint_program: UncheckedAccount<'info>,
}

impl TristeroInitSendLibrary<'_> {
    pub fn apply(
        ctx: &mut Context<TristeroInitSendLibrary>,
        _params: &TristeroInitSendLibraryParams,
    ) -> Result<()> {
        let cpi_ctx = InitSendLibrary::construct_context(ctx.accounts.endpoint_program, ctx.remaining_accounts).unwrap();
        let signer_seeds: &[&[&[u8]]] = &[&[self.to_bytes()]];

        let cpi_param = InitSendLibraryParams {
            sender: params.sender,
            eid: params.eid
        };

        endpoint::cpi::init_send_library(cpi_ctx.with_signer(signer_seeds), cpi_param);
        Ok(())
    }
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroInitSendLibraryParams {
    pub sender: Pubkey,
    pub eid: u32,
}
