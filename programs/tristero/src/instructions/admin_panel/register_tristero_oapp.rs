use crate::*;
use anchor_lang::{
    prelude::*
};
use endpoint::{
    self, cpi::accounts::{RegisterOApp}, instructions::{RegisterOAppParams}, ConstructCPIContext, OAPP_SEED
};

#[derive(Accounts)]
pub struct RegisterTristeroOApp<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    /// CHECK: The PDA of the OApp
    #[account(
        init,
        space = AdminPanel::LEN,
        payer = payer,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: Box<Account<'info, AdminPanel>>,
    /// CHECK: oapp registry
    #[account(
        mut,
        seeds = [OAPP_SEED, oapp.key().as_ref()],
        bump,
        seeds::program = endpoint_program.key()
    )]
    pub oapp_registry: AccountInfo<'info>,
    /// CHECK: 
    pub event_authority: AccountInfo<'info>,
    pub system_program: Program<'info, System>,
    /// CHECK: endpoint program's id
    #[account(executable)]
    pub endpoint_program: AccountInfo<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct RegisterTristeroOAppParams{
    pub delegate: Pubkey,
    pub admin_wallet: Pubkey,
    pub payment_wallet: Pubkey,
}

pub fn register_tristero_oapp(ctx: Context<RegisterTristeroOApp>, params: &RegisterTristeroOAppParams) -> Result<()> {
    let admin_panel = ctx.accounts.oapp.as_mut();

    admin_panel.authority = params.admin_wallet;
    admin_panel.bump = ctx.bumps.oapp;
    admin_panel.payment_wallet = params.payment_wallet;


    let cpi_param = RegisterOAppParams {
        delegate: params.delegate
    };

    let accounts = &[
        ctx.accounts.endpoint_program.to_account_info(),
        ctx.accounts.payer.to_account_info(),
        ctx.accounts.oapp.to_account_info(),
        ctx.accounts.oapp_registry.to_account_info(),
        ctx.accounts.system_program.to_account_info(),
        ctx.accounts.event_authority.to_account_info(),
        ctx.accounts.endpoint_program.to_account_info(),
    ];
    
    let cpi_ctx = RegisterOApp::construct_context(ctx.accounts.endpoint_program.key(), accounts)?;

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];

    endpoint::cpi::register_oapp(cpi_ctx.with_signer(signer_seeds), cpi_param)
}