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

    #[account(
        mut,
        seeds = [b"admin_panel"],
        bump,
    )]
    pub admin_panel: Box<Account<'info, AdminPanel>>,

    /// token mint address
    pub token_mint: Box<Account<'info, Mint>>,

    /// user's token account address
    #[account(
        mut,
        constraint = token_account.owner == authority.key() @ CustomError::InvalidTokenOwner,
        constraint = token_account.mint == token_mint.key() @ CustomError::InvalidTokenMintAddress,
        constraint = token_account.amount > params.source_sell_amount @ CustomError::InvalidTokenAmount,
    )]
    pub token_account: Box<Account<'info, TokenAccount>>,

    #[account(mut)]
    pub trade_match: Box<Account<'info, TradeMatch>>,

    pub system_program: Program<'info, System>,

    /// CHECK: This is not dangerous because we don't read or write from this account
    #[account(constraint = token_program.key() == TOKEN_PROGRAM_ID @ CustomError::InvalidTokenStandard)]
    pub token_program: AccountInfo<'info>,
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
        let admin_panel = ctx.accounts.admin_panel.as_mut();
        let trade_match = ctx.accounts.trade_match.as_mut();

        // ---------------------Analyzing payload from Arb(Have to check status later)---------------------------------
        let msg_vec:Vec<[u8; 32]> = split_into_chunks(message);
        require!(msg_vec.len() == 9, CustomError::WrongMsgTypeError);
        let sender = msg_vec[0];
        let src_token = msg_vec[2];
        let dst_token = msg_vec[3];
        let dst_index = vec_to_u128(msg_vec[5]);
        let taker = msg_vec[6];
        let min_amount = vec_to_u64(msg_vec[7]);
        let status = vec_to_u8(msg_vec[8]);

        require!(trade_match.trade_match_id == dst_index, CustomError::WrongMsgDstIndex);
        
        let sol_src_token = Vec::<u8>::new();
        trade_match.source_token_mint.map(|value| sol_src_token.push(value));
        require!(sol_src_token == dst_token[..sol_src_token.len()], CustomError::WrongMsgSrcToken);
        require!(trade_match.dest_token_mint == src_token[..trade_match.dest_token_mint.len()], CustomError::WrongMsgDstToken);

        // ---------------------Transfer the source token from the staking account----------------------------------
        let cpi_accounts = Transfer {
            from: ctx.accounts.staking_account.to_account_info(),
            to: ctx.accounts.token_account.to_account_info(),
            authority: ctx.accounts.admin_panel.to_account_info(),
        };

        let cpi_context = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);

        let signer_seeds: &[&[&[u8]]] = &[&[b"admin_panel", &[admin_panel.admin_panel_bump]]];
        
        msg!("Here is for transfer token");
        token::transfer(cpi_context.with_signer(signer_seeds), min_amount)?;
        
        trade_match.is_valiable = false;
        Ok(())
    }
}
