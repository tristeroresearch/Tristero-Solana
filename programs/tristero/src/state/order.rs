use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct Order {
    pub order_id: u64,
    pub user_pubkey: Pubkey,
    pub user_token_addr: Pubkey,
    pub source_token_mint: Pubkey,
    pub match_pubkey: Option<Pubkey>,
    pub dst_token_mint: [u8; 32],
    pub source_sell_amount: u64,
    pub dst_buy_amount: u64,
    pub min_sell_amount: u64,
    pub settled: u64,
    pub eid: u32,
    pub bump: u8,
    pub is_valiable: bool,
    pub target_address: [u8; 32],
}

impl anchor_lang::Id for Order {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl Order {
    pub const LEN: usize = 8 + std::mem::size_of::<Order>();
}