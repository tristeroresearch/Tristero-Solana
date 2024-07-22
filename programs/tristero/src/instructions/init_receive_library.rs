use crate::*;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    }, state::endpoint::*, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
pub struct TristeroInitReceiveLibrary<'info> {
    /// CHECK:
    pub endpoint_program: UncheckedAccount<'info>,
}

impl TristeroInitReceiveLibrary<'_> {
    pub fn apply(
        ctx: &mut Context<TristeroInitReceiveLibrary>,
        _params: &TristeroInitReceiveLibraryParams,
    ) -> Result<()> {
        let cpi_ctx = InitReceiveLibrary::construct_context(ctx.accounts.endpoint_program, ctx.remaining_accounts).unwrap();
        let signer_seeds: &[&[&[u8]]] = &[&[self.to_bytes()]];

        let cpi_param = InitReceiveLibraryParams {
            receiver: params.receiver,
            eid: params.eid
        };

        endpoint::cpi::init_receive_library(cpi_ctx.with_signer(signer_seeds), cpi_param);
        Ok(())
    }
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroInitReceiveLibraryParams {
    pub receiver: Pubkey,
    pub eid: u32,
}
