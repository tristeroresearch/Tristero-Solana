use crate::*;
use anchor_spl::token_interface::{Mint, TokenInterface};

/// This instruction should always be in the same transaction as InitializeMint.
/// Otherwise, it is possible for your settings to be front-run by another transaction.
/// If such a case did happen, you should initialize another mint for this oft.
#[derive(Accounts)]
pub struct InitOft<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    /// CHECK:
    pub oapp_config: UncheckedAccount<'info>,
    #[account(
        init,
        payer = payer,
        space = 8 + LzReceiveTypesAccounts::INIT_SPACE,
        seeds = [LZ_RECEIVE_TYPES_SEED, &oapp_config.key().as_ref()],
        bump
    )]
    pub lz_receive_types_accounts: Account<'info, LzReceiveTypesAccounts>,

    pub system_program: Program<'info, System>,
}

impl InitOft<'_> {
    pub fn apply(ctx: &mut Context<InitOft>) -> Result<()> {
        ctx.accounts.lz_receive_types_accounts.oft_config = ctx.accounts.oapp_config.key();
        ctx.accounts.lz_receive_types_accounts.token_mint = ctx.accounts.oapp_config.key();
        Ok(())
    }
}