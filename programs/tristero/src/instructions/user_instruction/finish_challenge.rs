use solana_program::native_token::LAMPORTS_PER_SOL;
use crate::*;
use crate::state::*;
use endpoint::{
    self, cpi::accounts::{Send}, instructions::{SendParams}, 
    ConstructCPIContext
};

#[derive(Accounts)]
#[instruction(params: FinishChallengeParams)]
pub struct FinishChallenge<'info> {
    #[account(mut)]
    pub authority: Signer<'info>,

    /// CHECK:
    #[account(
        mut,
        seeds = [b"TristeroOapp"],
        bump,
    )]
    pub oapp: AccountInfo<'info>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct FinishChallengeParams {
    pub arb_eid: u32,
    pub trade_match_id: u64,
    pub spl_token: Pubkey,
    pub erc20token: [u8; 20],
    pub receiver: [u8; 32]
}

pub fn finish_challenge(ctx: Context<FinishChallenge>, params: &FinishChallengeParams) -> Result<()>  {
    let receipt = &ctx.remaining_accounts[0];

    // --------------------------Send message through Oapp-----------------------------
    let cpi_ctx = Send::construct_context(ctx.remaining_accounts[9].key(), ctx.remaining_accounts).unwrap();

    let signer_seeds: &[&[&[u8]]] = &[&[b"TristeroOapp", &[ctx.bumps.oapp]]];

    let receive_options= [0, 3, 1, 0, 17, 1,  0,
            0, 0, 0, 0,  0, 0,   0,
            0, 0, 0, 0,  0, 7, 161,
            32]; // For lzReceiveOption

    //message: to send to arbitrum(trade_match_id, spltoken_mint_addr, erc20token_mint_addr, msg_type)
    let mut message_to_send = Vec::<u8>::new();
    
    let receipt_state = Receipt::try_from_slice(&receipt.data.borrow());
    let mut msg_type = 2u8;
    match receipt_state {
        Ok(receipt) => {
            if !receipt.is_valuable {
                msg_type = 3u8;
            }
        },
        Err(_) => {
            msg_type = 3u8;
        }
    }

    for _ in 0..24 {
        message_to_send.push(0u8);
    }
    params.trade_match_id.to_be_bytes().map(|value| message_to_send.push(value));

    params.spl_token.to_bytes().map(|value| message_to_send.push(value));

    for _ in 0..12 {
        message_to_send.push(0u8);
    }
    params.erc20token.map(|value| message_to_send.push(value));

    params.receiver.map(|value| message_to_send.push(value));
    for _ in 0..32 {
        message_to_send.push(0u8);
    }

    for _ in 0..31 {
        message_to_send.push(0u8);
    }
    message_to_send.push(msg_type); // _msgType

    let cpi_params = SendParams {
        dst_eid: params.arb_eid,
        receiver: params.receiver,
        message: message_to_send, 
        options: receive_options.to_vec(),
        native_fee: LAMPORTS_PER_SOL * 3,
        lz_token_fee: 0,
    };
    
    endpoint::cpi::send(cpi_ctx.with_signer(signer_seeds), cpi_params)?;
    Ok(())
}