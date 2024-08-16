use {anchor_lang::prelude::*, crate::state::*};

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub admin_wallet: Signer<'info>,

    #[account(
        init,
        payer = admin_wallet,
        space = AdminPanel::LEN,
        seeds = [b"admin_panel"],
        bump
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone)]
pub struct InitializeParams {
    pub admin_wallet: Pubkey,
    pub payment_wallet: Pubkey,
}

pub fn initialize(ctx: Context<Initialize>, params: &InitializeParams) -> Result<()> {
    let admin_panel = ctx.accounts.admin_panel.as_mut();
    admin_panel.authority = params.admin_wallet;
    admin_panel.bump = ctx.bumps.admin_panel;
    admin_panel.payment_wallet = params.payment_wallet;
    Ok(())
}