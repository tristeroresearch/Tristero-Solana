use std::str::FromStr;

use crate::*;
use oapp::endpoint_cpi::LzAccount;

#[derive(Accounts)]
pub struct LzReceiveTypes<'info> {
    /// CHECK:
    pub oft_config: UncheckedAccount<'info>,
    /// CHECK:
    pub message_lib: UncheckedAccount<'info>,
}

#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzReceiveTypeParams {
    pub src_eid: u32,
    pub sender: [u8; 32],
    pub nonce: u64,
    pub guid: [u8; 32],
    pub message: Vec<u8>,
    pub extra_data: Vec<u8>,
}

impl LzReceiveTypes<'_> {
    pub fn apply(
        ctx: &Context<LzReceiveTypes>,
        params: &LzReceiveTypeParams,
    ) -> Result<Vec<LzAccount>> {
        let program_id = ctx.program_id;

        let (tristero_oapp, _) = Pubkey::find_program_address(
            &[b"TristeroOapp"], 
            &program_id
        );

        let msg_vec:Vec<[u8; 32]> = split_into_chunks(params.message.clone());
        msg!("==> {:#?}", msg_vec.len());
        let mix_id_msg_type = vec_to_u64(msg_vec[0]);
        let trade_match_id =  mix_id_msg_type / 16u64;
        let msg_type = mix_id_msg_type % 16;
        let mut accounts = vec![
            LzAccount { pubkey: tristero_oapp, is_signer: false, is_writable: true }, //0
        ];

        let endpoint_program_id = Pubkey::from_str("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6").unwrap();
        // remaining accounts 0..9
        let accounts_for_clear = oapp::endpoint_cpi::get_accounts_for_clear(
            endpoint_program_id,
            &tristero_oapp.key(),
            params.src_eid,
            &params.sender,
            params.nonce,
        );
        accounts.extend(accounts_for_clear);

        if msg_type == 1 {
            let (receipt, _) = Pubkey::find_program_address(
                &[b"receipt", params.sender.as_ref(), &trade_match_id.to_be_bytes()],
                &program_id
            );
            accounts.extend([
                LzAccount { pubkey: receipt, is_signer: false, is_writable: true }
            ]);
        } else if msg_type == 2 {
            let (trade_match, _) = Pubkey::find_program_address(
                &[b"trade_match", &trade_match_id.to_be_bytes()],
                &program_id
            );
            accounts.extend([
                LzAccount { pubkey: trade_match, is_signer: false, is_writable: true }
            ]);
        }
        
        Ok(accounts)
    }
}

// /// same to anchor_lang::prelude::AccountMeta
// #[derive(Clone, AnchorSerialize, AnchorDeserialize, Debug)]
// pub struct LzAccount {
//     pub pubkey: Pubkey,
//     pub is_signer: bool,
//     pub is_writable: bool,
// }
