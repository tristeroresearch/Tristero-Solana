use anchor_lang::prelude::error_code;

#[error_code]
pub enum CustomError {
    #[msg("Invalid Authority")]
    InvalidAuthority,

    #[msg("InvalidTokenOwner")]
    InvalidTokenOwner,

    #[msg("InvalidTokenMintAddress")]
    InvalidTokenMintAddress,

    #[msg("InvalidTokenAmount")]
    InvalidTokenAmount,

    #[msg("InvalidTokenStandard")]
    InvalidTokenStandard,

    #[msg("PayloadHashNotFound")]
    PayloadHashNotFound,

    InvalidSendLibrary,
    InvalidReceiveLibrary,
    SameValue,
    AccountNotFound,
    OnlySendLib,
    OnlyReceiveLib,
    InvalidExpiry,
    OnlyNonDefaultLib,
    InvalidAmount,
    InvalidNonce,
    Unauthorized,
    ComposeNotFound,
    InvalidPayloadHash,
    LzTokenUnavailable,
    ReadOnlyAccount,
    InvalidMessageLib,
    WritableAccountNotAllowed,
}
