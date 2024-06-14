use {anchor_lang::prelude::*, crate::state::*};

#[derive(Accounts)]
pub struct CreateUser<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    #[account(
        init,
        payer = authority,
        space = User::LEN,
        seeds = [b"user", authority.key().as_ref()],
        bump
    )]
    pub user: Box<Account<'info, User>>,

    pub system_program: Program<'info, System>,
}


pub fn create_user(ctx: Context<CreateUser>) -> Result<()> {
    let user = ctx.accounts.user.as_mut();
    user.authority = ctx.accounts.authority.key();
    user.user_bump = ctx.bumps.user;
    user.match_count = 0u8;
    Ok(())
}