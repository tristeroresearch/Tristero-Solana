use std::borrow::{Borrow, BorrowMut};

use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{token::{self, Transfer, Mint, TokenAccount}};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::Send, instructions::SendParams, ConstructCPIContext,
};
use oapp::{
    endpoint::{
        cpi::accounts::Clear,
        instructions::{ClearParams, SendComposeParams},
        ID as ENDPOINT_ID,
    }
};
use solana_program::native_token::LAMPORTS_PER_SOL;

#[derive(Accounts)]
#[instruction(params: LzReceiveParams)]
pub struct LzReceive<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,

    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump = oapp.bump
    )]
    pub oapp: Box<Account<'info, AdminPanel>>,

    /// token account address
    #[account(mut)]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"staking_account", token_account.mint.key().as_ref()],
        bump,
        
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        constraint = trade_match.is_valiable == true @ CustomError::NotAgain
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,
    
    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(
        constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard,
        constraint = token_account.mint.key() == trade_match.source_token_mint @ CustomError::InvalidTokenMintAddress
    )]
    pub token_program: AccountInfo<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzReceiveParams {
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
}

impl LzReceive<'_> {
    pub fn apply(ctx: &mut Context<LzReceive>, params: &LzReceiveParams) -> Result<()> {
        let admin_panel = ctx.accounts.oapp.as_mut().clone();
        
        let trade_match = ctx.accounts.trade_match.as_mut();
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        
        let msg_type =  vec_to_u64(msg_vec[0]);
        
        let stake_acc = ctx.accounts.staking_account.to_account_info();
        let token_acc = ctx.accounts.token_account.to_account_info();
        let authority = admin_panel.clone().to_account_info();

        let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[admin_panel.bump]]];

        // ---------------------Transfer the source token from the staking account----------------------------------
        let cpi_accounts = Transfer {
            from: stake_acc,
            to: token_acc,
            authority: authority
        };

        let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
        token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;

        let mut accounts = ctx.remaining_accounts.to_vec();

        // accounts.insert(1, admin_panel.clone().to_account_info());

        if msg_type == 1u64 { // B->A
            trade_match.is_valiable = false;

        } else { // B->A->B
            let arb_receive_addr = msg_vec[4];


            // --------------------------Send message through Oapp-----------------------------
            let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();

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

            for _ in 0..12 {
                message_to_send.push(0u8);
            }
            arb_receive_addr.map(|value| message_to_send.push(value)); // taker
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
                receiver: arb_receive_addr,
                message: message_to_send, 
                options: receive_options.to_vec(),
                native_fee: LAMPORTS_PER_SOL * 3,
                lz_token_fee: 0,
            };
            
            endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;
        }

        // the first 9 accounts are for clear()
        let accounts_for_clear = &ctx.remaining_accounts[0..2];
        let _ = oapp::endpoint_cpi::clear(
            ENDPOINT_ID,
            ctx.remaining_accounts[1].key(),
            accounts_for_clear,
            &[b"TristeroOapp", &[admin_panel.bump]],
            ClearParams {
                receiver: ctx.remaining_accounts[1].key(),
                src_eid: params.src_eid,
                sender: params.sender,
                nonce: params.nonce,
                guid: params.guid,
                message: params.message.clone(),
            },
        )?;
        Ok(())
    }
}