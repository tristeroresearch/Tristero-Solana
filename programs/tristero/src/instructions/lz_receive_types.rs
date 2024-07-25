use crate::*;
use anchor_lang::solana_program;
use anchor_spl::{
    associated_token::{get_associated_token_address_with_program_id, ID as ASSOCIATED_TOKEN_ID},
    token_interface::Mint,
};
use solana_sdk::{pubkey::Pubkey};

#[derive(Accounts)]
pub struct LzReceiveTypes<'info> {
    /// CHECK:
    pub oft_config: UncheckedAccount<'info>,
    /// CHECK:
    pub token_mint: UncheckedAccount<'info>,
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

fn find_pda(program_id: &Pubkey, seeds: &[&[u8]]) -> (Pubkey, u8) {
    Pubkey::find_program_address(seeds, program_id)
}

// account structure
impl LzReceiveTypes<'_> {
    pub fn apply(
        ctx: &Context<LzReceiveTypes>,
        params: &LzReceiveTypeParams,
    ) -> Result<Vec<LzAccount>> {

        let program_id = Pubkey::from(b"5wrxGvTGkUCAusBSpkgGjW7N4G1xvWA2Aw1Pk1fAmuMf");
        let seeds = &[b"admin_panel"];

        //Find PDA
        let (pda, bump_seed) = find_pda(&program_id, seeds);

        // account 0..1
        let mut accounts = vec![
            LzAccount { pubkey: Pubkey::default(), is_signer: true, is_writable: true }, // 0
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //admin_panel
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //token_mint
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //token_account
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //trade_match
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //system_program
            LzAccount { pubkey: pda, is_signer: false, is_writable: true}, //token_program
        ];

        Ok(accounts)
    }
}

/// same to anchor_lang::prelude::AccountMeta
#[derive(Clone, AnchorSerialize, AnchorDeserialize)]
pub struct LzAccount {
    pub pubkey: Pubkey,
    pub is_signer: bool,
    pub is_writable: bool,
}
