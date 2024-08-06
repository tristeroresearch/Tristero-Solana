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
#[instruction(params: SendStoredParams)]
pub struct SendStored<'info> {

    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// arb user's token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// arb user's token account address
    #[account(
        init_if_needed,
        payer = authority,
        token::mint = token_mint,
        token::authority = dest_owner,
        seeds = [b"refund_account", dest_owner.key().as_ref()],
        bump,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: arb user's wallet address
    #[account(mut)]
    pub dest_owner: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(
        mut,
        seeds = [b"trade_match", &params.trade_match_id.to_be_bytes()],
        bump,
        constraint = trade_match.source_token_mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
        constraint = token_account.amount > trade_match.source_sell_amount @ CustomError::InvalidAmount, 
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct SendStoredParams {
    pub trade_match_id: u64,
    pub tristero_oapp_bump: u8, 
    pub source_token_address_in_arbitrum_chain: [u8; 20],
    pub receiver:[u8; 32]
}

pub fn send_stored(ctx: Context<SendStored>, params: &SendStoredParams) -> Result<()>  {
    let trade_match = ctx.accounts.trade_match.as_mut();
    let admin_panel = ctx.accounts.admin_panel.as_mut();

    // ---------------------Transfer from staking account to Arb user's token account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.staking_account.to_account_info(),
        to: ctx.accounts.token_account.to_account_info(),
        authority: admin_panel.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);

    let admin_signer_seeds: &[&[&[u8]]] = &[&[b"admin_panel", &[admin_panel.admin_panel_bump]]];
    
    msg!("Here is for transfer token");
    token::transfer(cpi_context.with_signer(admin_signer_seeds), trade_match.source_sell_amount)?;

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
    //     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 237, 167, 180, 19, 229, 37, 204, 255, 159, 251, 166, 16, 245, 196, 184, 225, 137, 235, 83
    //   ];

    //let sol_eid: u32 = 30168u32; // mainnet
    let sol_eid: u32 = 40168u32; // testnet

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
    
    // for _ in 0..12 {
    //     message_to_send.push(0u8);
    // }
    // trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // have to be srcToken but now use dstToken for instance
    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    trade_match.dest_token_mint.map(|value| message_to_send.push(value)); // erc20Token


    trade_match.source_token_mint.to_bytes().map(|value| message_to_send.push(value)); // splToken

    msg!("SourceTokenMint ToBytes() => ");
    msg!("{:?}", trade_match.source_token_mint.to_bytes());
    msg!("dest_token_mint ToBytes() => ");
    msg!("{:?}", trade_match.dest_token_mint);

    
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
    params.source_token_address_in_arbitrum_chain.map(|value| message_to_send.push(value)); // taker
    for _ in 0..24 {
        message_to_send.push(0u8); 
    }
    trade_match.source_sell_amount.to_be_bytes().map(|value| message_to_send.push(value)); // minAmount
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(1u8); //status

    // Here is for message_types
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(1u8); // Here is for _msgType

    // for _ in 0..32 { // Here is for _extraOptionsLength
    //     message_to_send.push(0u8);
    // }

    let cpi_params = SendParams {
        dst_eid: trade_match.eid,
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