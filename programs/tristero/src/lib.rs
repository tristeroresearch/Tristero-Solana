use anchor_lang::prelude::*;
pub mod error;
pub mod instructions;
pub mod state;

pub use messagelib_interface::{
    self, InitConfigParams, MessageLibType, MessagingFee, MessagingReceipt, Packet, SetConfigParams,
};
use instructions::*;
use error::*;

declare_id!("58nEPFCuebJsxjcyg6p6q2fXNLY2ApMiSQ619wZHe88h");

pub const ENDPOINT_SEED: &[u8] = b"Endpoint";
pub const MESSAGE_LIB_SEED: &[u8] = b"MessageLib";
pub const SEND_LIBRARY_CONFIG_SEED: &[u8] = b"SendLibraryConfig";
pub const RECEIVE_LIBRARY_CONFIG_SEED: &[u8] = b"ReceiveLibraryConfig";
pub const NONCE_SEED: &[u8] = b"Nonce";
pub const PENDING_NONCE_SEED: &[u8] = b"PendingNonce";
pub const PAYLOAD_HASH_SEED: &[u8] = b"PayloadHash";
pub const COMPOSED_MESSAGE_HASH_SEED: &[u8] = b"ComposedMessageHash";
pub const OAPP_SEED: &[u8] = b"OApp";

pub const DEFAULT_MESSAGE_LIB: Pubkey = Pubkey::new_from_array([0u8; 32]);
#[program]
pub mod tristero {
    use endpoint::instructions::SendParams;

    use super::*;

    pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: RegisterTristeroOAppParams) -> Result<()> {
        instructions::register_tristero_oapp(ctx, &params)
    }

    // pub fn tristero_send(ctx: Context<TristeroSend>, params: TristeroSendParams) -> Result<()> {
    //     instructions::tristero_send(ctx, params)
    // }
    pub fn tristero_send(ctx: Context<TristeroSend>, params: TristeroSendParams) -> Result<()> {
        instructions::tristero_send(&ctx, &params)
    }

    // pub fn tristero_init_send_library(ctx: Context<TristeroInitSendLibrary>, params: TristeroInitSendLibraryParams) -> Result<()> {
    //     instructions::tristero_init_send_library(ctx, &params)
    // }
} 

#[cfg(feature = "cpi")]
pub trait ConstructCPIContext<'a, 'b, 'c, 'info, T>
where
    T: ToAccountMetas + ToAccountInfos<'info>,
{
    const MIN_ACCOUNTS_LEN: usize;

    fn construct_context(
        program_id: Pubkey,
        accounts: &[AccountInfo<'info>],
    ) -> Result<CpiContext<'a, 'b, 'c, 'info, T>>;
}