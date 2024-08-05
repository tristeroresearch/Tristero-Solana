use crate::*;
use {crate::error::*, crate::state::*};
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Transfer, Mint, Token, TokenAccount},
};
use mpl_token_metadata::instructions::*;
use spl_token::ID as TOKEN_PROGRAM_ID;
use std::str::FromStr;

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

    /// CHECK:
    #[account(
        mut,
        seeds = [b"sol_panel"],
        bump,
    )]
    pub sol_panel: AccountInfo<'info>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// token account address
    #[account(
        init_if_needed,
        payer = payer,
        token::mint = token_mint,
        token::authority = dest_owner,
        seeds = [b"refund_account", dest_owner.key().as_ref()],
        bump,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    /// CHECK:
    #[account(mut)]
    pub dest_owner: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [b"staking_account", token_mint.key().as_ref()],
        bump,
    )]
    pub staking_account: Box<Account<'info, TokenAccount>>,

    #[account(mut)]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    // /// CHECK:
    // #[account(mut)]
    // pub program_id_account: AccountInfo<'info>,

    // /// CHECK:
    // #[account(mut)]
    // pub executor_id_account: AccountInfo<'info>,

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
        token::transfer(cpi_context.with_signer(signer_seeds), trade_match.source_sell_amount)?;
        
        trade_match.is_valiable = false;

        // ------------------------Transfer fee to executor-----------------------------------
        let ix = anchor_lang::solana_program::system_instruction::transfer(
            &ctx.accounts.sol_panel.key(), 
            &ctx.accounts.payer.key(), 
            5000000
        );
        msg!("Here is for transfer sol");
        let sol_seeds: &[&[&[u8]]] = &[&[b"sol_panel", &[ctx.bumps.sol_panel]]];
        let _ = anchor_lang::solana_program::program::invoke_signed(
            &ix, 
            &[ctx.accounts.sol_panel.to_account_info(), ctx.accounts.payer.to_account_info()],
            sol_seeds
        );

        // emit_cpi!(OFTReceived {
        //     guid: params.guid,
        //     src_eid: params.src_eid,
        //     to: *ctx.accounts.dest_owner.key(),
        //     amount_received_ld: 5000u64,
        // });

        Ok(())
    }
}
