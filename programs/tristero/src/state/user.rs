use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct User {
    pub authority: Pubkey,
    pub user_bump: u8,
    pub match_count: u32,
}

impl anchor_lang::Id for User {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl User {
    pub const LEN: usize = 8 + std::mem::size_of::<User>();
}