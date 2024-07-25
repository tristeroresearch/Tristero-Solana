use anchor_lang::{
    prelude::*,
    solana_program::{
        program::{invoke, invoke_signed},
        system_instruction,
    }, system_program,
};
use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::*;

use {crate::error::*, crate::state::*};
// use crate::instructions::tristero_send;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Clear, ClearCompose, Quote, RegisterOApp, Send, SendCompose, SetDelegate}, instructions::{
        oapp::send::*, ClearComposeParams, ClearParams, QuoteParams, RegisterOAppParams, SendComposeParams, SendParams, SetDelegateParams
    }, state::{endpoint::*, message_lib::*, messaging_channel::*}, ConstructCPIContext, MessagingFee, MessagingReceipt, COMPOSED_MESSAGE_HASH_SEED, ENDPOINT_SEED, NONCE_SEED, OAPP_SEED, PAYLOAD_HASH_SEED
};

#[derive(Accounts)]
#[instruction(params: CreateMatchParams)]
pub struct Challenge<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.src_index.to_be_bytes()],
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct ChallengeParams {
    pub src_index: u128
    pub tristero_oapp_bump: u8, 
    pub source_token_address_in_arbitrum_chain:[u8; 20],
    pub receiver:[u8; 32]
}

pub fn challenge(ctx: Context<Challenge>, params: &ChallengeParams) -> Result<()>  {
    let user = ctx.accounts.user.as_mut();
    

    let trade_match = ctx.accounts.trade_match.as_mut();

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();
    msg!("4 ====> constructing context good");

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[params.tristero_oapp_bump]]];

    let receive_options= [0, 3, 1, 0, 17, 1,  0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption
    //let receiver:[u8; 32] = [1u8; 32]; // have to change. This should be receiver
    // let receiver:[u8; 32] = [
    //     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 237, 167, 180, 19, 229, 37, 204, 255, 159, 251, 166, 16, 245, 196, 184, 225, 137, 235, 83
    //   ];

    let sol_eid: u32 = 30168u32;

    //message: to send to arbitrum
    let mut message_to_send = Vec::<u8>::new();
    
    // Here is for payload

    for _ in 0..32 { // Here is for sender
        message_to_send.push(0u8);
    }
    for _ in 0..28 {
        message_to_send.push(0u8);
    }
    sol_eid.to_be_bytes().map(|value: u8| message_to_send.push(value)); // Here is for srcLzc
    // trade_match.source_token_mint.to_bytes().map(|value| message_to_send.push(value)); // srcToken
    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // have to be srcToken but now use dstToken for instance
    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // dstToken
    for _ in 0..16 {
        message_to_send.push(0u8);
    }
    trade_match.trade_match_id.to_be_bytes().map(|value| message_to_send.push(value)); // srcIndex
    for _ in 0..32 {
        message_to_send.push(0u8); // dstIndex
    }
    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    params.source_token_address_in_arbitrum_chain.map(|value| message_to_send.push(value)); // taker
    for _ in 0..24 {
        message_to_send.push(0u8); 
    }
    trade_match.source_sell_amount.to_be_bytes().map(|value| message_to_send.push(value)); // minAmount
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(0u8); //status

    // Here is for message_types
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(2u8); // Here is for _msgType

    // for _ in 0..32 { // Here is for _extraOptionsLength
    //     message_to_send.push(0u8);
    // }

    let cpi_params = SendParams {
        dst_eid: params.eid,
        receiver: params.receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    msg!("Here is for send message through oapp");
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    Ok(())
}