use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct AdminPanel {
    pub admin_wallet: Pubkey,
    pub payment_wallet: Pubkey,
    pub admin_panel_bump: u8,
    pub freeze_fee: u64,
}

impl anchor_lang::Id for AdminPanel {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl AdminPanel {
    pub const LEN: usize = 8 + std::mem::size_of::<AdminPanel>();
}