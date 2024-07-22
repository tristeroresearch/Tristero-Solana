use crate::*;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams,
        SendParams, SetDelegateParams,
    }, state::endpoint::*, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
pub struct TristeroInitNonce<'info> {
    /// CHECK:
    pub endpoint_program: UncheckedAccount<'info>,
}

impl TristeroInitNonce<'_> {
    pub fn apply(
        ctx: &mut Context<TristeroInitNonce>,
        _params: &TristeroInitNonceParams,
    ) -> Result<()> {
        let cpi_ctx = InitNonceParams::construct_context(ctx.accounts.endpoint_program, ctx.remaining_accounts).unwrap();
        let signer_seeds: &[&[&[u8]]] = &[&[self.to_bytes()]];

        let cpi_param = InitNonceParams {
            local_oapp: params.local_oapp,
            remote_eid: params.remote_eid,
            remote_oapp: params.remote_oapp
        };

        endpoint::cpi::init_nonce(cpi_ctx.with_signer(signer_seeds), cpi_param);
        Ok(())
    }
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroInitNonceParams {
    local_oapp: Pubkey, // the PDA of the OApp
    remote_eid: u32,
    remote_oapp: [u8; 32],
}
