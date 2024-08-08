use anchor_lang::prelude::*;
pub mod error;
pub mod instructions;
pub mod state;
pub mod msg_codec;
pub mod myutils;
pub mod events;

pub use messagelib_interface::{
    self, InitConfigParams, MessageLibType, MessagingFee, MessagingReceipt, Packet, SetConfigParams,
};
use instructions::*;
use state::*;
use myutils::*;
use events::*;

declare_id!("APob25xoaC1Zz2FKePPCRfRBgJ5nhrjg7dUfV68ZNobP"); // for testnet
// declare_id!("Eq22HfHg6KjtAoqeEU1UhmbA2iSxUdJQC1syuv36xK1U"); // for mainnet

pub const ENDPOINT_SEED: &[u8] = b"Endpoint";
pub const MESSAGE_LIB_SEED: &[u8] = b"MessageLib";
pub const SEND_LIBRARY_CONFIG_SEED: &[u8] = b"SendLibraryConfig";
pub const RECEIVE_LIBRARY_CONFIG_SEED: &[u8] = b"ReceiveLibraryConfig";
pub const NONCE_SEED: &[u8] = b"Nonce";
pub const PENDING_NONCE_SEED: &[u8] = b"PendingNonce";
pub const PAYLOAD_HASH_SEED: &[u8] = b"PayloadHash";
pub const COMPOSED_MESSAGE_HASH_SEED: &[u8] = b"ComposedMessageHash";
pub const OAPP_SEED: &[u8] = b"OApp";
pub const LZ_RECEIVE_TYPES_SEED: &[u8] = b"LzReceiveTypes";

pub const DEFAULT_MESSAGE_LIB: Pubkey = Pubkey::new_from_array([0u8; 32]);
#[program]
pub mod tristero {
    use endpoint::instructions::SendParams;

    use super::*;

    pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: RegisterTristeroOAppParams) -> Result<()> {
        instructions::register_tristero_oapp(ctx, &params)
    }

    pub fn admin_panel_create(ctx: Context<Initialize>, params: InitializeParams) -> Result<()> {
        instructions::initialize(ctx, &params)
    }

    pub fn admin_panel_update(ctx: Context<Update>, params: UpdateParams) -> Result<()> {
        instructions::update(ctx, &params)
    }

    pub fn create_match(ctx: Context<CreateMatch>, params: CreateMatchParams) -> Result<()> {
        instructions::create_match(ctx, &params)
    }

    // pub fn cancel_match(ctx: Context<CancelMatch>, params: CancelMatchParams) -> Result<()> {
    //     instructions::cancel_match(ctx, &params)
    // }

    pub fn challenge(ctx: Context<Challenge>, params: ChallengeParams) -> Result<()> {
        instructions::challenge(ctx, &params)
    }

    pub fn lz_receive(mut ctx: Context<LzReceive>, params: LzReceiveParams) -> Result<()> {
        LzReceive::apply(&mut ctx, &params)
    }

    pub fn lz_receive_types(
        ctx: Context<LzReceiveTypes>,
        params: LzReceiveTypeParams,
    ) -> Result<Vec<LzAccount>> {
        LzReceiveTypes::apply(&ctx, &params)
    }

    pub fn register_config(mut ctx: Context<InitOft>) -> Result<()> {
        InitOft::apply(&mut ctx)
    }

    pub fn place_order(mut ctx: Context<PlaceOrder>, params: PlaceOrderParams) -> Result<()> {
        instructions::place_order(ctx, &params)
    }

    pub fn send_stored(mut ctx: Context<SendStored>, params: SendStoredParams) -> Result<()> {
        instructions::send_stored(ctx, &params)
    }
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