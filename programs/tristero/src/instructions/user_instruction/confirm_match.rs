use anchor_lang::{
    prelude::*
};

use {crate::error::*, crate::state::*};
use spl_token::ID as TOKEN_PROGRAM_ID;
use endpoint::{
    self, cpi::accounts::{Send}, instructions::{SendParams}, 
    ConstructCPIContext
};

#[derive(Accounts)]
#[instruction(params: ConfirmMatchParams)]
pub struct ConfirmMatch<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [b"trade_match".as_ref(), &params.trade_match_id.to_be_bytes()],
        bump = trade_match.bump,
        constraint = trade_match.status == 2u8 @ CustomError::InvalidTradeMatch
    )]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    #[account(
        mut,
        seeds = [b"staking_account", trade_match.source_token_mint.as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    /// sol user's token account address
    #[account(
        mut,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == trade_match.source_token_mint @ CustomError::InvalidTokenMintAddress,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, Copy)]
pub struct ConfirmMatchParams {
    pub trade_match_id: u64,
    pub tristero_oapp_bump: u8
}

pub fn create_match(ctx: Context<ConfirmMatch>, params: &ConfirmMatchParams) -> Result<()>  {
    let trade_match = ctx.accounts.trade_match.as_mut();

    // ---------------------Transfer the source token to the staking account----------------------------------
    let cpi_accounts = Transfer {
        from: ctx.accounts.staking_account.to_account_info(),
        to: ctx.accounts.token_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };

    let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    
    token::transfer(cpi_context, trade_match.source_sell_amount)?;

    trade_match.status = 2u8;

    Ok(())
}