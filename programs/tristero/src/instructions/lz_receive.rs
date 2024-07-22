use crate::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token_interface::{self, Mint, MintTo, TokenAccount, TokenInterface, TransferChecked},
};

#[derive(Accounts)]
#[instruction(params: LzReceiveParams)]
pub struct LzReceive<'info> {
    // #[account(mut)]
    // pub payer: Signer<'info>,
    // pub system_program: Program<'info, System>,
    #[account(mut)]
    pub payer: Signer<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzReceiveParams {
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
}

impl LzReceive<'_> {
    pub fn apply(ctx: &mut Context<LzReceive>, params: &LzReceiveParams) -> Result<()> {
        msg!("Message Received!!!!");
        Ok(())
    }
}
