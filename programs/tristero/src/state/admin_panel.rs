use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct AdminPanel {
    pub admin_wallet: Pubkey,
    pub payment_wallet: Pubkey,
    pub admin_panel_bump: u8,
    pub freeze_fee: u64,
    pub match_count: u64,
    pub order_count: u64,
}

impl anchor_lang::Id for AdminPanel {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl AdminPanel {
    pub const LEN: usize = 8 + std::mem::size_of::<AdminPanel>();
}

/// LzReceiveTypesAccounts includes accounts that are used in the LzReceiveTypes
/// instruction.
#[account]
#[derive(InitSpace)]
pub struct LzReceiveTypesAccounts {
    pub oft_config: Pubkey,
    pub token_mint: Pubkey,
}