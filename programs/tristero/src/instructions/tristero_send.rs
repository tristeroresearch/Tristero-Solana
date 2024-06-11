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
    pub sender: Signer<'info>,
    /// CHECK: assert this program in assert_send_library()
    pub send_library_program: UncheckedAccount<'info>,
    #[account(
        seeds = [SEND_LIBRARY_CONFIG_SEED, sender.key.as_ref(), &params.dst_eid.to_be_bytes()],
        bump = send_library_config.bump
    )]
    pub send_library_config: Account<'info, SendLibraryConfig>,
    #[account(
        seeds = [SEND_LIBRARY_CONFIG_SEED, &params.dst_eid.to_be_bytes()],
        bump = default_send_library_config.bump
    )]
    pub default_send_library_config: Account<'info, SendLibraryConfig>,
    /// The PDA signer to the send library when the endpoint calls the send library.
    #[account(
        seeds = [
            MESSAGE_LIB_SEED,
            &get_send_library(
                &send_library_config,
                &default_send_library_config
            ).key().to_bytes()
        ],
        bump = send_library_info.bump,
        constraint = !send_library_info.to_account_info().is_writable @LayerZeroError::ReadOnlyAccount
    )]
    pub send_library_info: Account<'info, MessageLibInfo>,
    #[account(seeds = [ENDPOINT_SEED], bump = endpoint.bump)]
    pub endpoint: Account<'info, EndpointSettings>,
    #[account(
        mut,
        seeds = [
            NONCE_SEED,
            &sender.key().to_bytes(),
            &params.dst_eid.to_be_bytes(),
            &params.receiver[..]
        ],
        bump = nonce.bump
    )]
    pub nonce: Account<'info, Nonce>,
}

pub fn tristero_send(ctx: Context<TristeroSend>, params: TristeroSendParams) -> Result<()> {
    // Solana endpoints: 76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6
    let cpi_param = SendParams {
        dst_eid: params.dst_eid,
        receiver: params.receiver,
        message: params.message.to_vec(),
        options: params.options.to_vec(),
        native_fee: params.native_fee,
        lz_token_fee: params.lz_token_fee,
    };
    let cpi_refs: Vec<&[u8]> = params.seeds.iter().map(|v| v.as_slice()).collect();
    let cpi_seeds: &[&[u8]] = &cpi_refs;
    let cpi_ctx = Send::construct_context(params.endpoint_program, &ctx.accounts.to_account_infos())?;
    endpoint::cpi::send(cpi_ctx.with_signer(&[cpi_seeds]), cpi_param);
    Ok(())
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct TristeroSendParams {
    pub endpoint_program: Pubkey,
    pub sender: Pubkey,
    pub seeds: Vec<Vec<u8>>,
    pub dst_eid: u32,
    pub receiver: [u8; 32],
    pub message: Vec<u8>,
    pub options: Vec<u8>,
    pub native_fee: u64,
    pub lz_token_fee: u64,
}

pub(crate) fn get_send_library(
    config: &SendLibraryConfig,
    default_config: &SendLibraryConfig,
) -> Pubkey {
    if config.message_lib == DEFAULT_MESSAGE_LIB {
        default_config.message_lib
    } else {
        config.message_lib
    }
}

// #[cfg(test)]
// mod tests {
//     use super::*;

//     #[test]
//     fn test_assert_send_library() {
//         let send_library_program1 = &Pubkey::new_unique();
//         let send_library_program2 = &Pubkey::new_unique();
//         let (send_library1, send_library_bump1) =
//             Pubkey::find_program_address(&[MESSAGE_LIB_SEED], send_library_program1);
//         let (send_library2, send_library_bump2) =
//             Pubkey::find_program_address(&[MESSAGE_LIB_SEED], send_library_program2);

//         // set library config
//         let mut send_library_config = SendLibraryConfig { message_lib: send_library1, bump: 0 };
//         let message_lib_info = MessageLibInfo {
//             message_lib_bump: send_library_bump1,
//             message_lib_type: MessageLibType::Send,
//             bump: 0,
//         };
//         // default send library config
//         let default_send_library_config = SendLibraryConfig { message_lib: send_library2, bump: 0 };
//         let message_lib_info_default = MessageLibInfo {
//             message_lib_bump: send_library_bump2,
//             message_lib_type: MessageLibType::Send,
//             bump: 0,
//         };

//         // test assert_send_library with oapp setting, which is send_library1
//         assert_eq!(
//             assert_send_library(
//                 &message_lib_info,
//                 send_library_program1,
//                 &send_library_config,
//                 &default_send_library_config
//             )
//             .unwrap(),
//             send_library1
//         );

//         // test assert_send_library with default setting
//         send_library_config.message_lib = DEFAULT_MESSAGE_LIB.clone(); // oapp set send library to default
//         assert_eq!(
//             assert_send_library(
//                 &message_lib_info_default,
//                 send_library_program2,
//                 &send_library_config,
//                 &default_send_library_config
//             )
//             .unwrap(),
//             send_library2
//         );

//         // expect err if wrong library
//         assert_eq!(
//             assert_send_library(
//                 &message_lib_info_default, // send-lib bump 2
//                 send_library_program1,     // wrong program
//                 &send_library_config,
//                 &default_send_library_config
//             )
//             .unwrap_err(),
//             LayerZeroError::InvalidSendLibrary.into()
//         );
//     }
// }
