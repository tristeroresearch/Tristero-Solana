use {anchor_lang::prelude::*, crate::error::*, crate::state::*};


#[derive(Accounts)]
pub struct Update<'info> {
    #[account(mut,
    constraint = admin_wallet.key() == admin_panel.admin_wallet @ CustomError::InvalidAuthority
    )]
    pub admin_wallet: Signer<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone)]
pub struct UpdateParams {
    pub admin_wallet: Pubkey,
    pub payment_wallet: Pubkey
}

pub fn update(ctx: Context<Update>, params: &UpdateParams) -> Result<()> {
    let admin_panel = ctx.accounts.admin_panel.as_mut();
    admin_panel.admin_wallet = params.admin_wallet;
    admin_panel.admin_panel_bump = ctx.bumps.admin_panel;
    admin_panel.payment_wallet = params.payment_wallet;
    Ok(())
}