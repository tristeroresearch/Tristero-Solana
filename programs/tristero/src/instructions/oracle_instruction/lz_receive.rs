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


#[derive(Accounts, Clone)]
#[instruction(params: LzReceiveParams)]
pub struct LzReceive<'info> {
    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump = oapp.bump
    )]
    pub oapp: Box<Account<'info, AdminPanel>>,

    #[account(
        mut,
        constraint = trade_match.status == 0u8 @ CustomError::NotAgain
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

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
        let mut accounts = ctx.accounts.clone().to_account_infos();
        let mut remaining_accounts = ctx.remaining_accounts;
        let admin_panel = ctx.accounts.oapp.as_mut().clone();
        let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[admin_panel.bump]]];
        let trade_match = ctx.accounts.trade_match.as_mut();
        
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let msg_type =  vec_to_u64(msg_vec[0]) % 16;

        msg!("msg_type: => {} {}", msg_type, vec_to_u64(msg_vec[0]));
        if msg_type == 1u64 && trade_match.status == 1u8 { // B->A
            let authority = remaining_accounts[0].to_account_info();
            let stake_acc = remaining_accounts[1].to_account_info();
            let token_acc = remaining_accounts[2].to_account_info();

            

            // ---------------------Transfer the source token from the staking account----------------------------------
            let cpi_accounts = Transfer {
                from: stake_acc,
                to: token_acc,
                authority: authority
            };

            let cpi_context = CpiContext::new(remaining_accounts[3].to_account_info(), cpi_accounts);
            token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;


            trade_match.status = 2u8;
        } 
        else { // B->A->B
            let mut remaining_accounts = ctx.remaining_accounts.to_vec();
            // let tristero_oapp = accounts[0].clone();
            let endpoint_program_id = remaining_accounts[7].clone();
            let signer1 = remaining_accounts[10].clone();
            let send_library_program_id = remaining_accounts[14].clone();
            let price_fee_program_id = remaining_accounts[17].clone();
            let price_fee_program_pda = remaining_accounts[18].clone();
            remaining_accounts.insert(0, endpoint_program_id);
            // remaining_accounts.insert(1, tristero_oapp);

            remaining_accounts.insert(2, send_library_program_id);
            remaining_accounts.insert(13, signer1);
            remaining_accounts.extend_from_slice(&[
                price_fee_program_id,
                price_fee_program_pda
            ]);

            // --------------------------Send message through Oapp-----------------------------
            let cpi_ctx = Send::construct_context(remaining_accounts[9].key(), remaining_accounts.as_ref()).unwrap();

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

            trade_match.status = 1u8;
        }
        Ok(())
    }
}