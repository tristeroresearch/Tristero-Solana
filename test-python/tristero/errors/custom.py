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


class InvalidTokenStandard(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "InvalidTokenStandard")

    code = 6004
    name = "InvalidTokenStandard"
    msg = "InvalidTokenStandard"


class PayloadHashNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "PayloadHashNotFound")

    code = 6005
    name = "PayloadHashNotFound"
    msg = "PayloadHashNotFound"


class NotAgain(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Already canceled or traded")

    code = 6006
    name = "NotAgain"
    msg = "Already canceled or traded"


class WrongMsgTypeError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Wrong msg type")

    code = 6007
    name = "WrongMsgTypeError"
    msg = "Wrong msg type"


class WrongMsgDstIndex(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Can not find with dst index")

    code = 6008
    name = "WrongMsgDstIndex"
    msg = "Can not find with dst index"


class WrongMsgSrcToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Can not find with src token address")

    code = 6009
    name = "WrongMsgSrcToken"
    msg = "Can not find with src token address"


class WrongMsgDstToken(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "Can not find with dst token address")

    code = 6010
    name = "WrongMsgDstToken"
    msg = "Can not find with dst token address"


class WrongAuthorityToCancel(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Can not cancel with this authority")

    code = 6011
    name = "WrongAuthorityToCancel"
    msg = "Can not cancel with this authority"


class MinSellAmountConflict(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Min Sell Amount Conflict")

    code = 6012
    name = "MinSellAmountConflict"
    msg = "Min Sell Amount Conflict"


class InSufficientFundsOfOrder(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Insufficient Funds of Order")

    code = 6013
    name = "InSufficientFundsOfOrder"
    msg = "Insufficient Funds of Order"


class InvalidSendLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, None)

    code = 6014
    name = "InvalidSendLibrary"
    msg = None


class InvalidReceiveLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, None)

    code = 6015
    name = "InvalidReceiveLibrary"
    msg = None


class SameValue(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, None)

    code = 6016
    name = "SameValue"
    msg = None


class AccountNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, None)

    code = 6017
    name = "AccountNotFound"
    msg = None


class OnlySendLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, None)

    code = 6018
    name = "OnlySendLib"
    msg = None


class OnlyReceiveLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, None)

    code = 6019
    name = "OnlyReceiveLib"
    msg = None


class InvalidExpiry(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, None)

    code = 6020
    name = "InvalidExpiry"
    msg = None


class OnlyNonDefaultLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, None)

    code = 6021
    name = "OnlyNonDefaultLib"
    msg = None


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, None)

    code = 6022
    name = "InvalidAmount"
    msg = None


class InvalidNonce(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, None)

    code = 6023
    name = "InvalidNonce"
    msg = None


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6024, None)

    code = 6024
    name = "Unauthorized"
    msg = None


class ComposeNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6025, None)

    code = 6025
    name = "ComposeNotFound"
    msg = None


class InvalidPayloadHash(ProgramError):
    def __init__(self) -> None:
        super().__init__(6026, None)

    code = 6026
    name = "InvalidPayloadHash"
    msg = None


class LzTokenUnavailable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6027, None)

    code = 6027
    name = "LzTokenUnavailable"
    msg = None


class ReadOnlyAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6028, None)

    code = 6028
    name = "ReadOnlyAccount"
    msg = None


class InvalidMessageLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6029, None)

    code = 6029
    name = "InvalidMessageLib"
    msg = None


class WritableAccountNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6030, None)

    code = 6030
    name = "WritableAccountNotAllowed"
    msg = None


CustomError = typing.Union[
    InvalidAuthority,
    InvalidTokenOwner,
    InvalidTokenMintAddress,
    InvalidTokenAmount,
    InvalidTokenStandard,
    PayloadHashNotFound,
    NotAgain,
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
    6004: InvalidTokenStandard(),
    6005: PayloadHashNotFound(),
    6006: NotAgain(),
    6007: WrongMsgTypeError(),
    6008: WrongMsgDstIndex(),
    6009: WrongMsgSrcToken(),
    6010: WrongMsgDstToken(),
    6011: WrongAuthorityToCancel(),
    6012: MinSellAmountConflict(),
    6013: InSufficientFundsOfOrder(),
    6014: InvalidSendLibrary(),
    6015: InvalidReceiveLibrary(),
    6016: SameValue(),
    6017: AccountNotFound(),
    6018: OnlySendLib(),
    6019: OnlyReceiveLib(),
    6020: InvalidExpiry(),
    6021: OnlyNonDefaultLib(),
    6022: InvalidAmount(),
    6023: InvalidNonce(),
    6024: Unauthorized(),
    6025: ComposeNotFound(),
    6026: InvalidPayloadHash(),
    6027: LzTokenUnavailable(),
    6028: ReadOnlyAccount(),
    6029: InvalidMessageLib(),
    6030: WritableAccountNotAllowed(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
