use anchor_lang::{
    prelude::*
};
use solana_program::native_token::LAMPORTS_PER_SOL;
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
#[instruction(params: ExecuteMatchParams)]
pub struct ExecuteMatch<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    /// sol user's token account address
    #[account(
        mut,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    /// arb user's token account address
    #[account(mut)]
    pub arb_user_token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct ExecuteMatchParams {
    pub dst_eid: u32,
    pub trade_match_id: u64,
    pub tristero_oapp_bump: u8,
    pub source_sell_amount: u64,
    pub receiver: [u8; 32],
}

pub fn execute_match(ctx: Context<ExecuteMatch>, params: &ExecuteMatchParams) -> Result<()>  {

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.arb_user_token_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    token::transfer(cpi_context, params.source_sell_amount)?;

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[params.tristero_oapp_bump]]];

    let receive_options= [0, 3, 1, 0, 17, 1,  0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption

    let sol_eid: u32 = 40168u32; // testnet(if mainnet => 30168)

    //message: to send to arbitrum
    let mut message_to_send = Vec::<u8>::new();
    
    // payload(sol_eid, trade_match_id, arb_user_token_account, source_sell_amount, msg_type)
    for _ in 0..28 {
        message_to_send.push(0u8);
    }
    sol_eid.to_be_bytes().map(|value: u8| message_to_send.push(value)); //srcLzc
    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    params.trade_match_id.to_be_bytes().map(|value: u8| message_to_send.push(value));
    ctx.accounts.arb_user_token_account.key().to_bytes().map(|value: u8| message_to_send.push(value));
    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    params.source_sell_amount.to_be_bytes().map(|value: u8| message_to_send.push(value));
    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(0u8); //msg_type: (0: execute_match)

    let cpi_params = SendParams {
        dst_eid: params.dst_eid,
        receiver: params.receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;

    Ok(())
}