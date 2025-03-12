use std::str::FromStr;
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};
use spl_token::ID as TOKEN_PROGRAM_ID;
use crate::error::CustomError;

#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub upgrade_authority: Signer<'info>,

    #[account(
        mut,
        constraint = oapp_token_account.owner == oapp.key() @ CustomError::InvalidTokenOwner
    )]
    pub oapp_token_account: Box<Account<'info, TokenAccount>>,

    #[account(mut)]
    pub destination_account: Box<Account<'info, TokenAccount>>,
    
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID)]
    pub token_program: Program<'info, Token>,

    /// CHECK: This is the OApp account

    /// CHECK: OApp PDA
    #[account(
        seeds = [b"TristeroOapp".as_ref()],
        bump, // <–– Important!
        constraint = upgrade_authority.key() == Pubkey::from_str("BxxRsRviq7227G8gLf6b2dqRGZXCen7tnmCcMzop9wFj").unwrap()
    )]
    pub oapp: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct TransferTokensParams {
    pub amount: u64,
}

pub fn transfer_tokens(ctx: Context<TransferTokens>, params: &TransferTokensParams) -> Result<()> {
    let bump = ctx.bumps.oapp; // single u8
    
    // Our cpi accounts: note that `authority` should be `oapp` (the PDA),
    // not `oapp_token_account`.
    let cpi_accounts = Transfer {
        from: ctx.accounts.oapp_token_account.to_account_info(),
        to:   ctx.accounts.destination_account.to_account_info(),
        authority: ctx.accounts.oapp.to_account_info(),
    };

    // Prepare the seeds for the signer
    let signer_seeds = &[
        b"TristeroOapp".as_ref(), // the same bytes you used in `#[account(seeds = [...])]`
        &[bump],
    ];

    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            cpi_accounts,
            &[signer_seeds], // slice of slices
        ),
        params.amount,
    )?;

    Ok(())
}