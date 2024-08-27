use std::str::FromStr;

use crate::*;
use oapp::endpoint::instructions::ClearParams;

#[derive(Accounts, Clone)]
pub struct LzReceive<'info> {
    /// CHECK: The PDA of the OApp
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump
    )]
    pub oapp: AccountInfo<'info>,
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
        let remaining_accounts = ctx.remaining_accounts;
        let tristero_oapp_bump = ctx.bumps.oapp;
        let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[tristero_oapp_bump]]];
        let seed = signer_seeds[0];

        let accounts_for_clear = &ctx.remaining_accounts[0..8];
        let endpoint_program_id = Pubkey::from_str("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6").unwrap();
        let _ = oapp::endpoint_cpi::clear(
            endpoint_program_id,
            ctx.accounts.oapp.key(),
            accounts_for_clear,
            seed,
            ClearParams {
                receiver: ctx.accounts.oapp.key(),
                src_eid: params.src_eid,
                sender: params.sender,
                nonce: params.nonce,
                guid: params.guid,
                message: params.message.clone(),
            },
        )?;

        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        let mix_id_msg_type = vec_to_u64(msg_vec[0]);
        let msg_type =  mix_id_msg_type % 16; // 1: start_challenge from arb, 2: finish_challenge from arb with ok, 3: with no
        if msg_type == 1u64 {
            let dest_token_mint = Pubkey::new_from_array(msg_vec[1]);
            let dest_owner = Pubkey::new_from_array(msg_vec[2]);
            let buy_quantity = vec_to_u64(msg_vec[3]);
            let market_maker = Pubkey::new_from_array(msg_vec[4]);

            let receipt = &remaining_accounts[9];
            let mut receipt_state = Receipt::try_from_slice(&receipt.data.borrow())?;
            if receipt_state.maker == market_maker && receipt_state.payout_quantity >= buy_quantity && receipt_state.receiver == dest_owner && receipt_state.token_mint == dest_token_mint && !receipt_state.is_valuable {
                receipt_state.is_valuable = true;
            }
        } else if msg_type == 2u64{
            let trade_match_acc = &remaining_accounts[9];
            let mut trade_match = TradeMatch::try_from_slice(&trade_match_acc.data.borrow())?;
            trade_match.status = 2u8;
        }
        Ok(())
    }
}