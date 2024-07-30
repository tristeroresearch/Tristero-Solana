use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;

#[derive(Accounts)]
#[instruction(params: LzReceiveParams)]
pub struct LzReceive<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// token account address
    #[account(
        init_if_needed,
        payer = payer,
        token::mint = token_mint,
        token::authority = dest_owner,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(mut)]
    pub dest_owner: AccountInfo<'info>,

    #[account(
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(mut)]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
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
        let admin_panel = ctx.accounts.admin_panel.as_mut();
        let trade_match = ctx.accounts.trade_match.as_mut();

        // ---------------------Transfer the source token from the staking account----------------------------------
        let cpi_accounts = Transfer {
            from: ctx.accounts.staking_account.to_account_info(),
            to: ctx.accounts.token_account.to_account_info(),
            authority: admin_panel.to_account_info(),
        };

        let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);

        let signer_seeds: &[&[&[u8]]] = &[&[b"admin_panel", &[admin_panel.admin_panel_bump]]];
        
        msg!("Here is for transfer token");
        token::transfer(cpi_context, trade_match.source_sell_amount)?;
        
        trade_match.is_valiable = false;
        Ok(())
    }
}
