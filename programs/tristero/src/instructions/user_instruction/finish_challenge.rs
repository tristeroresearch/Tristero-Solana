use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::*;
use anchor_spl::{
    token::{self, Transfer, Mint, TokenAccount},
};
use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Send}, instructions::{SendParams}, 
    ConstructCPIContext
};

#[derive(Accounts)]
#[instruction(params: FinishChallengeParams)]
pub struct FinishChallenge<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
        constraint = trade_match.authority == authority.key() @ CustomError::InvalidAuthority,
        constraint = trade_match.status == 1u8 @ CustomError::NotEvenStarted
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    /// CHECK:
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump,
    )]
    pub oapp: AccountInfo<'info>,

    #[account(
        mut,
        constraint = arb_user_token_account.mint == trade_match.source_token_mint @ CustomError::InvalidTokenMintAddress,
        constraint = arb_user_token_account.key() == trade_match.arb_user_token_account @ CustomError::InvalidTokenOwner
    )]
    pub arb_user_token_account: Box<Account<'info, TokenAccount>>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct FinishChallengeParams {
    pub trade_match_id: u64,
    pub receiver:[u8; 32]
}

pub fn finish_challenge(ctx: Context<FinishChallenge>, params: &FinishChallengeParams) -> Result<()>  {

    let trade_match = ctx.accounts.trade_match.as_mut();
    let receipt = &ctx.remaining_accounts[0];

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];

    let receive_options= [0, 3, 1, 0, 17, 1,  0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption

    let sol_eid: u32 = 40168u32; // testnet(if mainnet => 30168)

    //message: to send to arbitrum(trade_match_id, msg_type)
    let mut message_to_send = Vec::<u8>::new();
    
    let receipt_state = Receipt::try_from_slice(&receipt.data.borrow());
    let mut msg_type = 2u8;
    match receipt_state {
        Ok(receipt) => {
            if !receipt.is_valuable {
                msg_type = 3u8;
            }
        },
        Err(_) => {
            msg_type = 3u8;
        }
    }

    for _ in 0..28 {
        message_to_send.push(0u8);
    }
    params.trade_match_id.to_be_bytes().map(|value| message_to_send.push(value));

    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(msg_type); // _msgType

    let cpi_params = SendParams {
        dst_eid: trade_match.eid,
        receiver: params.receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;
    Ok(())
}