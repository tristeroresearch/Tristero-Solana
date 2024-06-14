use {anchor_lang::prelude::*, crate::state::*};
use {crate::error::*, crate::state::*};

#[derive(Accounts)]
#[instruction(params: UpdateUserParams)]
pub struct UpdateUser<'info> {
    #[account(mut,
        constraint = user.authority == authority.key() @ CustomError::InvalidAuthority
    )]
    pub authority: Signer<'info>,

    #[account(
        mut,
        seeds = [b"user", authority.key().as_ref()],
        bump
    )]
    pub user: Box<Account<'info, User>>,

    pub system_program: Program<'info, System>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone)]
pub struct UpdateUserParams {
    pub new_user: Pubkey
}

pub fn update_user(ctx: Context<UpdateUser>, params: &UpdateUserParams) -> Result<()> {
    let user = ctx.accounts.user.as_mut();
    user.authority = params.new_user;
    Ok(())
}