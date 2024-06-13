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

#[derive(Accounts)]
#[instruction(params: TristeroSendParams)]
pub struct TristeroSend<'info> {
    /// CHECK:
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub sender: UncheckedAccount<'info>,
    // /// CHECK: assert this program in assert_send_library()
    // pub send_library_program: UncheckedAccount<'info>,
    // /// CHECK:
    // #[account(
    //     seeds = [SEND_LIBRARY_CONFIG_SEED, sender.key.as_ref(), &params.dst_eid.to_be_bytes()],
    //     bump,
    //     seeds::program = endpoint_program.key()
    // )]
    // pub send_library_config: UncheckedAccount<'info>,
    // /// CHECK:
    // #[account(
    //     seeds = [SEND_LIBRARY_CONFIG_SEED, &params.dst_eid.to_be_bytes()],
    //     bump,
    //     seeds::program = endpoint_program.key()
    // )]
    // pub default_send_library_config: UncheckedAccount<'info>,
    // /// The PDA signer to the send library when the endpoint calls the send library.
    // /// CHECK: will check in cpi
    // pub send_library_info: UncheckedAccount<'info>,
    // /// CHECK:
    // #[account(seeds = [ENDPOINT_SEED], bump, seeds::program = endpoint_program.key())]
    // pub endpoint: UncheckedAccount<'info>,
    // /// CHECK:
    // #[account(
    //     mut,
    //     seeds = [
    //         NONCE_SEED,
    //         &sender.key().to_bytes(),
    //         &params.dst_eid.to_be_bytes(),
    //         &params.receiver[..]
    //     ],
    //     bump,
    //     seeds::program = endpoint_program.key()
    // )]
    // pub nonce: UncheckedAccount<'info>,
    // /// CHECK: 
    // #[account(mut)]
    // pub event_authority: UncheckedAccount<'info>,
    /// CHECK: endpoint program's id
    #[account(executable)]
    pub endpoint_program: UncheckedAccount<'info>,
    // /// CHECK: uln
    // #[account(
    //     mut,
    //     seeds = [b"MessageLib"],
    //     bump,
    //     seeds::program = send_library_program.key()
    // )]
    // pub uln: UncheckedAccount<'info>,

    // /// CHECK:
    // #[account(mut)]
    // pub send_config: UncheckedAccount<'info>,

    // /// CHECK:
    // #[account(mut)]
    // pub default_send_config: UncheckedAccount<'info>,

    // /// CHECK:
    // #[account(mut)]
    // pub payer: UncheckedAccount<'info>,

    // /// CHECK: system program's id
    // pub system_program: UncheckedAccount<'info>,

    // /// CHECK: 
    // #[account(mut)]
    // pub uld_event_authority: UncheckedAccount<'info>,

    // /// CHECK: quoteExecutorProgramId's id
    // #[account(executable)]
    // pub executor_program: UncheckedAccount<'info>,

    // /// CHECK: 
    // #[account(mut)]
    // pub executor_config: UncheckedAccount<'info>,

    // /// CHECK: priceFeeProgram's id
    // #[account(executable)]
    // pub price_fee_program: UncheckedAccount<'info>,

    // /// CHECK: 
    // #[account(mut)]
    // pub price_feed: UncheckedAccount<'info>,

    // /// CHECK: dvnProgram's id
    // #[account(executable)]
    // pub dvn_program: UncheckedAccount<'info>,

    // /// CHECK:
    // #[account(mut)]
    // pub dvn_config: UncheckedAccount<'info>,
}

pub fn tristero_send(ctx: &Context<TristeroSend>, params: &TristeroSendParams) -> Result<()> {
    msg!("1 =====> tristero_send begin");
    let cpi_params = SendParams {
        dst_eid: params.dst_eid,
        receiver: params.receiver,
        message: (*params.message).clone(),
        options: (*params.options).clone(),
        native_fee: params.native_fee,
        lz_token_fee: params.lz_token_fee,
    };
    msg!("2 ====> making params good");

    // msg!("send_library_program ==> {}", ctx.accounts.send_library_program.to_account_info().key());
    // msg!("executor_program ==> {}", ctx.accounts.executor_program.to_account_info().key());
    // msg!("price_fee_program ==> {}", ctx.accounts.price_fee_program.to_account_info().key());
    // msg!("executor_config key ==> {}", ctx.accounts.executor_config.to_account_info().key());
    // msg!("executor_config owner ==> {}", ctx.accounts.executor_config.to_account_info().owner);

    // Solana endpoints: 76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6
    // let accounts = &[
    //     ctx.accounts.endpoint_program.to_account_info(),
    //     ctx.accounts.sender.to_account_info(), //#1
    //     ctx.accounts.send_library_program.to_account_info(), //#2
    //     ctx.accounts.send_library_config.to_account_info(), //#3
    //     ctx.accounts.default_send_library_config.to_account_info(), //#4
    //     ctx.accounts.send_library_info.to_account_info(), //#5
    //     ctx.accounts.endpoint.to_account_info(), //#6
    //     ctx.accounts.nonce.to_account_info(), //#7
    //     ctx.accounts.event_authority.to_account_info(), //#8
        
    //     ctx.accounts.endpoint_program.to_account_info(), //#9
    //     ctx.accounts.uln.to_account_info(), //#10
    //     ctx.accounts.send_config.to_account_info(), //#11
    //     ctx.accounts.default_send_config.to_account_info(), //#12
    //     ctx.accounts.payer.to_account_info(), //payer, signer #13
    //     // ctx.accounts.payer.to_account_info(), // treasury #14
    //     ctx.accounts.send_library_program.to_account_info(),
    //     ctx.accounts.system_program.to_account_info(), //#15
    //     ctx.accounts.uld_event_authority.to_account_info(), //#16
    //     ctx.accounts.send_library_program.to_account_info(), //#17
    //     ctx.accounts.executor_program.to_account_info(), //#18
    //     ctx.accounts.executor_config.to_account_info(), //#19
    //     ctx.accounts.price_fee_program.to_account_info(), //#20
    //     ctx.accounts.price_feed.to_account_info(), //#21
    //     ctx.accounts.dvn_program.to_account_info(), //#22
    //     ctx.accounts.dvn_config.to_account_info(), //#23
    //     ctx.accounts.price_fee_program.to_account_info(), //#24
    //     ctx.accounts.price_feed.to_account_info() //#25
    // ];

    msg!("3 ====> making accounts good");

    
    let cpi_ctx = Send::construct_context(ctx.accounts.endpoint_program.key(), ctx.remaining_accounts)?;
    msg!("4 ====> constructing context good");

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.sender]]];

    // msg!("5 ====> uln , {} {}", ctx.accounts.uln.key(), ctx.accounts.uln.owner);
    msg!("options => {:?}", cpi_params.options.clone());
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    msg!("6 ====> Excellent");

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