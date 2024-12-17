use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct TradeMatch {
    pub authority: Pubkey,
    pub user_token_addr: Pubkey,
    pub source_token_mint: Pubkey,
    pub dst_token_mint: [u8; 32],
    pub arb_user_token_account: Pubkey,
    pub order_idx: u64,
    pub source_sell_amount: u64,
    pub dst_buy_amount: u64,
    pub eid: u32, //which eco system
    pub bump: u8,
    pub trade_match_id: u64,
    pub status: u8,
}

impl anchor_lang::Id for TradeMatch {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl TradeMatch {
    pub const LEN: usize = 8 + std::mem::size_of::<TradeMatch>();
}