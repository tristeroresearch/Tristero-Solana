use anchor_lang::{
    prelude::*,
    solana_program::{
        program::{invoke, invoke_signed},
        system_instruction,
    }, system_program,
};
use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::program::Tristero;

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
pub struct CreateMatch<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// user's token account address
    #[account(mut)]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(
        init_if_needed,
        payer = authority,
        token::mint = token_mint,
        token::authority = admin_panel,
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"user", authority.key().as_ref()],
        bump = user.user_bump,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
        constraint = token_account.amount > params.source_sell_amount @ CustomError::InvalidTokenAmount,
    )]
    pub user: Box<Account<'info, User>>,

    #[account(
        init,
        payer = authority,
        space = TradeMatch::LEN,
        seeds = [b"trade_match", authority.key().as_ref(), &user.match_count.to_be_bytes()],
        bump,
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct CreateMatchParams {
    pub source_sell_amount: u64,
    pub dest_token_mint: [u8; 20],
    pub dest_buy_amount: u64,
    pub eid: u32,
    pub tristero_oapp_bump: u8, 
    pub source_token_address_in_arbitrum_chain:[u8; 20]
}

pub fn create_match(ctx: Context<CreateMatch>, params: &CreateMatchParams) -> Result<()>  {
    let user = ctx.accounts.user.as_mut();
    

    let trade_match = ctx.accounts.trade_match.as_mut();
    trade_match.source_token_mint = ctx.accounts.token_mint.key();
    trade_match.source_sell_amount = params.source_sell_amount;
    trade_match.dest_token_mint = params.dest_token_mint;
    trade_match.dest_buy_amount = params.dest_buy_amount;
    trade_match.eid = params.eid;
    trade_match.match_bump = ctx.bumps.trade_match;
    trade_match.trade_match_id = user.match_count;
    trade_match.source_token_account = ctx.accounts.token_account.key();
    trade_match.is_valiable = true;
    user.match_count += 1;

    trade_match.source_token_mint.to_bytes();

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();
    msg!("4 ====> constructing context good");

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[params.tristero_oapp_bump]]];

    let receive_options= [0, 3, 1, 0, 17, 1,   0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption
    //let receiver:[u8; 32] = [1u8; 32]; // have to change. This should be receiver
    // let receiver:[u8; 32] = [
    //     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
    //     21, 159, 172, 75, 179, 64, 128, 61, 
    //     41, 24, 136, 120, 112, 163, 222, 202, 
    //     139, 120, 199, 116
    //   ];
    let receiver:[u8; 32] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 178, 9, 14, 222, 128, 3, 178, 164, 104, 120, 62, 73, 200, 137, 50, 113, 191, 173, 240, 68];

    let sol_eid: u32 = 30168u32;

    //message: to send to arbitrum
    let mut message_to_send = Vec::<u8>::new();
    
    for _ in 0..20 { // Here is for sender
        message_to_send.push(0u8);
    }
    sol_eid.to_be_bytes().map(|value: u8| message_to_send.push(value)); // Here is for srcLzc
    trade_match.source_token_mint.to_bytes().map(|value| message_to_send.push(value)); // srcToken
    trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // dstToken
    trade_match.trade_match_id.to_be_bytes().map(|value| message_to_send.push(value)); // srcIndex
    for _ in 0..4 {
        message_to_send.push(0u8); // dstIndex
    }
    params.source_token_address_in_arbitrum_chain.map(|value| message_to_send.push(value)); // dstIndex
    for _ in 0..24 {
        message_to_send.push(0u8); 
    }
    trade_match.source_sell_amount.to_be_bytes().map(|value| message_to_send.push(value)); // minAmount
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(0u8);

    let cpi_params = SendParams {
        dst_eid: params.eid,
        receiver: receiver,
        message: message_to_send, // have to change, have to contain message.
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    msg!("Here is for send message through oapp");
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.staking_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);

    let signer_seeds: &[&[&[u8]]] = &[&[b"user", &[user.user_bump]]];
    
    msg!("Here is for transfer token");
    //token::transfer(cpi_context.with_signer(signer_seeds), params.source_sell_amount)?;
    token::transfer(cpi_context, params.source_sell_amount)?;

    Ok(())
}