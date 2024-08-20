use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct AdminPanel {
    pub authority: Pubkey,
    pub payment_wallet: Pubkey, // fee wallet
    pub backend_wallet: Pubkey, // authority
    pub bump: u8,
    pub trade_fee: u64, // trading fee
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
    pub message_lib: Pubkey,
}