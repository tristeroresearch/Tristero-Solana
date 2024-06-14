use anchor_lang::prelude::*;

#[account]
#[derive(Default, Debug)]
pub struct TradeMatch {
    pub source_token_mint: Pubkey,
    pub dest_token_mint: Pubkey,
    pub source_sell_amount: u64,
    pub dest_buy_amount: u64,
    pub eid: u32, //which eco system
    pub match_bump: u8,
    pub trade_match_id: u8,
}

impl anchor_lang::Id for TradeMatch {
    fn id() -> Pubkey {
        crate::ID
    }
}

impl TradeMatch {
    pub const LEN: usize = 8 + std::mem::size_of::<TradeMatch>();
}