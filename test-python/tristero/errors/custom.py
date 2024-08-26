import typing
from anchorpy.error import ProgramError


class InvalidAuthority(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Invalid Authority")

    code = 6000
    name = "InvalidAuthority"
    msg = "Invalid Authority"


class InvalidTokenOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "InvalidTokenOwner")

    code = 6001
    name = "InvalidTokenOwner"
    msg = "InvalidTokenOwner"


class InvalidTokenMintAddress(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "InvalidTokenMintAddress")

    code = 6002
    name = "InvalidTokenMintAddress"
    msg = "InvalidTokenMintAddress"


class InvalidTokenAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "InvalidTokenAmount")

    code = 6003
    name = "InvalidTokenAmount"
    msg = "InvalidTokenAmount"


class InvalidTradeMatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "InvalidTradeMatch")

    code = 6004
    name = "InvalidTradeMatch"
    msg = "InvalidTradeMatch"


class InvalidTokenStandard(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "InvalidTokenStandard")

    code = 6005
    name = "InvalidTokenStandard"
    msg = "InvalidTokenStandard"


class PayloadHashNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "PayloadHashNotFound")

    code = 6006
    name = "PayloadHashNotFound"
    msg = "PayloadHashNotFound"


class NotAgain(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Already canceled or traded")

    code = 6007
    name = "NotAgain"
    msg = "Already canceled or traded"


class NotEvenStarted(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Not even started")

    code = 6008
    name = "NotEvenStarted"
    msg = "Not even started"


class WrongMsgTypeError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Wrong msg type")

    code = 6009
    name = "WrongMsgTypeError"
    msg = "Wrong msg type"


class WrongMsgDstIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "Can not find with dst index")

    code = 6010
    name = "WrongMsgDstIndex"
    msg = "Can not find with dst index"


class WrongMsgSrcToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Can not find with src token address")

    code = 6011
    name = "WrongMsgSrcToken"
    msg = "Can not find with src token address"


class WrongMsgDstToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Can not find with dst token address")

    code = 6012
    name = "WrongMsgDstToken"
    msg = "Can not find with dst token address"


class WrongAuthorityToCancel(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Can not cancel with this authority")

    code = 6013
    name = "WrongAuthorityToCancel"
    msg = "Can not cancel with this authority"


class MinSellAmountConflict(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Min Sell Amount Conflict")

    code = 6014
    name = "MinSellAmountConflict"
    msg = "Min Sell Amount Conflict"


class InSufficientFundsOfOrder(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "Insufficient Funds of Order")

    code = 6015
    name = "InSufficientFundsOfOrder"
    msg = "Insufficient Funds of Order"


class InvalidSendLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, None)

    code = 6016
    name = "InvalidSendLibrary"
    msg = None


class InvalidReceiveLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, None)

    code = 6017
    name = "InvalidReceiveLibrary"
    msg = None


class SameValue(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, None)

    code = 6018
    name = "SameValue"
    msg = None


class AccountNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, None)

    code = 6019
    name = "AccountNotFound"
    msg = None


class OnlySendLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, None)

    code = 6020
    name = "OnlySendLib"
    msg = None


class OnlyReceiveLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, None)

    code = 6021
    name = "OnlyReceiveLib"
    msg = None


class InvalidExpiry(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, None)

    code = 6022
    name = "InvalidExpiry"
    msg = None


class OnlyNonDefaultLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, None)

    code = 6023
    name = "OnlyNonDefaultLib"
    msg = None


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6024, None)

    code = 6024
    name = "InvalidAmount"
    msg = None


class InvalidNonce(ProgramError):
    def __init__(self) -> None:
        super().__init__(6025, None)

    code = 6025
    name = "InvalidNonce"
    msg = None


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6026, None)

    code = 6026
    name = "Unauthorized"
    msg = None


class ComposeNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6027, None)

    code = 6027
    name = "ComposeNotFound"
    msg = None


class InvalidPayloadHash(ProgramError):
    def __init__(self) -> None:
        super().__init__(6028, None)

    code = 6028
    name = "InvalidPayloadHash"
    msg = None


class LzTokenUnavailable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6029, None)

    code = 6029
    name = "LzTokenUnavailable"
    msg = None


class ReadOnlyAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6030, None)

    code = 6030
    name = "ReadOnlyAccount"
    msg = None


class InvalidMessageLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6031, None)

    code = 6031
    name = "InvalidMessageLib"
    msg = None


class WritableAccountNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6032, None)

    code = 6032
    name = "WritableAccountNotAllowed"
    msg = None


CustomError = typing.Union[
    InvalidAuthority,
    InvalidTokenOwner,
    InvalidTokenMintAddress,
    InvalidTokenAmount,
    InvalidTradeMatch,
    InvalidTokenStandard,
    PayloadHashNotFound,
    NotAgain,
    NotEvenStarted,
    WrongMsgTypeError,
    WrongMsgDstIndex,
    WrongMsgSrcToken,
    WrongMsgDstToken,
    WrongAuthorityToCancel,
    MinSellAmountConflict,
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
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InvalidAuthority(),
    6001: InvalidTokenOwner(),
    6002: InvalidTokenMintAddress(),
    6003: InvalidTokenAmount(),
    6004: InvalidTradeMatch(),
    6005: InvalidTokenStandard(),
    6006: PayloadHashNotFound(),
    6007: NotAgain(),
    6008: NotEvenStarted(),
    6009: WrongMsgTypeError(),
    6010: WrongMsgDstIndex(),
    6011: WrongMsgSrcToken(),
    6012: WrongMsgDstToken(),
    6013: WrongAuthorityToCancel(),
    6014: MinSellAmountConflict(),
    6015: InSufficientFundsOfOrder(),
    6016: InvalidSendLibrary(),
    6017: InvalidReceiveLibrary(),
    6018: SameValue(),
    6019: AccountNotFound(),
    6020: OnlySendLib(),
    6021: OnlyReceiveLib(),
    6022: InvalidExpiry(),
    6023: OnlyNonDefaultLib(),
    6024: InvalidAmount(),
    6025: InvalidNonce(),
    6026: Unauthorized(),
    6027: ComposeNotFound(),
    6028: InvalidPayloadHash(),
    6029: LzTokenUnavailable(),
    6030: ReadOnlyAccount(),
    6031: InvalidMessageLib(),
    6032: WritableAccountNotAllowed(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
