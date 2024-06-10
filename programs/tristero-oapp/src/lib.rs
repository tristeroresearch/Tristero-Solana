use anchor_lang::prelude::*;

declare_id!("7vw59auCSq6kZjYkACh3buYaBCUavjeNmLMf9V6HQx7o");

#[program]
pub mod tristero_oapp {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
