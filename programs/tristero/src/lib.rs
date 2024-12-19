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
use oapp::endpoint_cpi::LzAccount;

// declare_id!("E2okPYndsWqtniTNnoK2YHdZUwMEWpN1PtPW3woaY5Lm"); // for devnet
declare_id!("B32JUhPbfuQ4ai59DVLzpvSFqodr99YEpkovEx2XnKDK"); // for mainnet

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

    use super::*;

    pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: RegisterTristeroOAppParams) -> Result<()> {
        instructions::register_tristero_oapp(ctx, &params)
    }

    pub fn admin_panel_update(ctx: Context<Update>, params: UpdateParams) -> Result<()> {
        instructions::update(ctx, &params)
    }

    pub fn create_match(ctx: Context<CreateMatch>, params: CreateMatchParams) -> Result<()> {
        instructions::create_match(ctx, &params)
    }

    pub fn execute_match(ctx: Context<ExecuteMatch>, params: ExecuteMatchParams) -> Result<()> {
        instructions::execute_match(ctx, &params)
    }

    pub fn confirm_match(ctx: Context<ConfirmMatch>) -> Result<()> {
        instructions::confirm_match(ctx)
    }

    pub fn start_challenge(ctx: Context<Challenge>, params: ChallengeParams) -> Result<()> {
        instructions::start_challenge(ctx, &params)
    }

    pub fn finish_challenge(ctx: Context<FinishChallenge>, params: FinishChallengeParams) -> Result<()> {
        instructions::finish_challenge(ctx, &params)
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

    pub fn register_config(mut ctx: Context<InitOft>, param_pubkey: Pubkey) -> Result<()> {
        InitOft::apply(&mut ctx, param_pubkey)
    }

    pub fn place_order(ctx: Context<PlaceOrder>, params: PlaceOrderParams) -> Result<()> {
        instructions::place_order(ctx, &params)
    }

    pub fn cancel_order(ctx: Context<CancelOrder>) -> Result<()> {
        instructions::cancel_order(ctx)
    }

    pub fn unwind_match(ctx: Context<UnwindMatch>) -> Result<()> {
        instructions::unwind_match(ctx)
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