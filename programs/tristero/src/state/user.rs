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


/// LzReceiveTypesAccounts includes accounts that are used in the LzReceiveTypes
/// instruction.
#[account]
#[derive(InitSpace)]
pub struct LzReceiveTypesAccounts {
    pub oft_config: Pubkey,
    pub token_mint: Pubkey,
}