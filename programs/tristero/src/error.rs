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

    #[msg("InvalidOwnerWithTradeMatch")]
    InvalidOwnerWithTradeMatch,
    
    #[msg("InvalidTradeMatch")]
    InvalidTradeMatch,

    #[msg("InvalidTokenStandard")]
    InvalidTokenStandard,

    #[msg("PayloadHashNotFound")]
    PayloadHashNotFound,

    #[msg("Already canceled or traded")]
    NotAgain,

    #[msg("Not even started")]
    NotEvenStarted,

    #[msg("Wrong msg type")]
    WrongMsgTypeError,

    #[msg("Can not find with dst index")]
    WrongMsgDstIndex,

    #[msg("Can not find with src token address")]
    WrongMsgSrcToken,

    #[msg("Can not find with dst token address")]
    WrongMsgDstToken,

    #[msg("Can not cancel with this authority")]
    WrongAuthorityToCancel,

    #[msg("Min Sell Amount Conflict")]
    MinSellAmountConflict,

    #[msg("Insufficient Funds of Order")]
    InSufficientFundsOfOrder,

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
