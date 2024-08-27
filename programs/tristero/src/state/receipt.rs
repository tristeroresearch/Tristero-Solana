use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct Receipt {
    pub maker: Pubkey,
    pub payout_quantity: u64,
    pub token_mint: Pubkey,
    pub receiver: Pubkey,
    pub is_valuable: bool
}

impl anchor_lang::Id for Receipt {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl Receipt {
    pub const LEN: usize = 8 + std::mem::size_of::<Receipt>();
}