use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::*;

use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Send}, instructions::{SendParams}, 
    ConstructCPIContext
};

#[derive(Accounts)]
#[instruction(params: ChallengeParams)]
pub struct Challenge<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
        constraint = trade_match.authority == authority.key() @ CustomError::InvalidAuthority,
        constraint = trade_match.status == 0u8 @ CustomError::NotAgain
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct ChallengeParams {
    pub trade_match_id: u64,
    pub tristero_oapp_bump: u8,
    pub receiver: [u8; 32],
    pub taker: [u8; 20]
}

pub fn start_challenge(ctx: Context<Challenge>, params: &ChallengeParams) -> Result<()>  {

    let trade_match = ctx.accounts.trade_match.as_mut();

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[params.tristero_oapp_bump]]];

    let receive_options= [0, 3, 1, 0, 17, 1,  0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption

    let sol_eid: u32 = 40168u32; // testnet(if mainnet => 30168)

    //message: to send to arbitrum(trade_match_id, spltoken_mint_addr, erc20token_mint_addr, dest_owner, buy_quantity, msg_type)
    let mut message_to_send = Vec::<u8>::new();
    
    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    params.trade_match_id.to_be_bytes().map(|value| message_to_send.push(value));

    trade_match.source_token_mint.to_bytes().map(|value| message_to_send.push(value));

    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    trade_match.dest_token_mint.map(|value| message_to_send.push(value));

    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    params.taker.map(|value| message_to_send.push(value));

    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    trade_match.dest_buy_amount.to_be_bytes().map(|value| message_to_send.push(value));

    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(1u8); // _msgType 1: start_challenge 2: finish_challenge

    let cpi_params = SendParams {
        dst_eid: trade_match.eid,
        receiver: params.receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    trade_match.status = 1u8;
    Ok(())
}