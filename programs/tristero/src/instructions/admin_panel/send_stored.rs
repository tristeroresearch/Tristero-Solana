use anchor_lang::{
    prelude::*
};
use solana_program::native_token::LAMPORTS_PER_SOL;

use {crate::error::*, crate::state::*};
use anchor_spl::{
    token::{self, Transfer, Mint, TokenAccount},
};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Send}, instructions::{SendParams}, ConstructCPIContext
};

#[derive(Accounts)]
#[instruction(params: SendStoredParams)]
pub struct SendStored<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

   /// CHECK: The PDA of the OApp
   #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump = oapp.bump,
        constraint = oapp.authority == authority.key() @ CustomError::InvalidAuthority
    )]
    pub oapp: Box<Account<'info, AdminPanel>>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.trade_match_id.to_be_bytes()],
        bump,
        constraint = trade_match.trade_match_id == params.trade_match_id @ CustomError::InvalidTradeMatch
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct SendStoredParams {
    pub trade_match_id: u64
}

pub fn send_stored(ctx: Context<SendStored>, params: &SendStoredParams) -> Result<()>  {
    let trade_match = ctx.accounts.trade_match.as_mut();
    let remaining_accounts = ctx.remaining_accounts;
    let admin_panel = ctx.accounts.oapp.as_mut();

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(remaining_accounts[9].key(), remaining_accounts.as_ref()).unwrap();
    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[admin_panel.bump]]];

    let receive_options= [0, 3, 1, 0, 17, 1, 0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption
    let sol_eid: u32 = 40168u32; // testnet(mainnet: 30168)

    //message: to send to arbitrum
    let mut message_to_send = Vec::<u8>::new();

    //payload
    for _ in 0..32 { // sender
        message_to_send.push(0u8);
    }
    for _ in 0..28 {
        message_to_send.push(0u8);
    }
    sol_eid.to_be_bytes().map(|value: u8| message_to_send.push(value)); // srcLzc
    
    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // erc20Token
    trade_match.source_token_mint.to_bytes().map(|value| message_to_send.push(value)); // splToken
    
    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    trade_match.dst_index.to_be_bytes().map(|value| message_to_send.push(value)); // srcIndex(arb index)

    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    trade_match.src_index.to_be_bytes().map(|value| message_to_send.push(value)); // dstIndex(sol index)

    let receiver = [0u8; 32];
    receiver.map(|value| message_to_send.push(value)); // taker
    for _ in 0..24 {
        message_to_send.push(0u8); 
    }
    trade_match.source_sell_amount.to_be_bytes().map(|value| message_to_send.push(value)); // minAmount
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(1u8); //status

    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(1u8); // _msgType

    let cpi_params = SendParams {
        dst_eid: trade_match.eid,
        receiver: receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    Ok(())
}