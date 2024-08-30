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

    #[account(
        init,
        payer = authority,
        space = Receipt::LEN,
        seeds = [b"receipt".as_ref(), params.sender.as_ref(), &params.trade_match_id.to_be_bytes()],
        bump
    )]
    pub receipt: Box<Account<'info, Receipt>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct ExecuteMatchParams {
    pub dst_eid: u32,
    pub trade_match_id: u64,
    pub source_sell_amount: u64,
    pub sender: [u8; 20]
}

pub fn execute_match(ctx: Context<ExecuteMatch>, params: &ExecuteMatchParams) -> Result<()>  {
    let receipt = ctx.accounts.receipt.as_mut();

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.token_account.to_account_info(),
        to: ctx.accounts.arb_user_token_account.to_account_info(),
        authority: ctx.accounts.authority.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    token::transfer(cpi_context, params.source_sell_amount)?;

    receipt.maker = ctx.accounts.authority.key();
    receipt.payout_quantity = params.source_sell_amount;
    receipt.token_mint = ctx.accounts.token_account.mint;
    receipt.receiver = ctx.accounts.arb_user_token_account.owner.key();
    receipt.is_valuable = false;
    Ok(())
}