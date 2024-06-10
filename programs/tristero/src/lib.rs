use anchor_lang::prelude::*;

declare_id!("GtSiJ1BsQTykvWjLrTSpTq6mZHgonDk4TWX3zrG7oWSS");

#[program]
pub mod tristero {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}
