use anchor_lang::prelude::*;
use {crate::error::*, crate::state::*};

#[derive(Accounts)]
pub struct CancelOrder<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    /// CHECK: PDA for OApp
    #[account(
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump = admin_panel.bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    #[account(
        mut,
        seeds = [b"order", &order.order_id.to_be_bytes()],
        bump = order.bump,
        constraint = order.user_pubkey == authority.key() @ CustomError::InvalidAuthority,
        constraint = order.match_pubkey.is_none() @ CustomError::OrderAlreadyMatched,
        constraint = order.is_valiable @ CustomError::OrderNotValid,
        close = authority
    )]
    pub order: Box<Account<'info, Order>>,

    pub system_program: Program<'info, System>,
}

pub fn cancel_order(ctx: Context<CancelOrder>) -> Result<()> {
    let order = &mut ctx.accounts.order;
    
    // Mark order as invalid
    order.is_valiable = false;

    // Note: No need to return tokens since they were never transferred in place_order
    
    msg!("Order {} cancelled", order.order_id);
    
    Ok(())
} 