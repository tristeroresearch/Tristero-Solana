import typing
from anchorpy.error import ProgramError


class InvalidSendLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, None)

    code = 6000
    name = "InvalidSendLibrary"
    msg = None


class InvalidReceiveLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, None)

    code = 6001
    name = "InvalidReceiveLibrary"
    msg = None


class SameValue(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, None)

    code = 6002
    name = "SameValue"
    msg = None


class AccountNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, None)

    code = 6003
    name = "AccountNotFound"
    msg = None


class OnlySendLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, None)

    code = 6004
    name = "OnlySendLib"
    msg = None


class OnlyReceiveLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, None)

    code = 6005
    name = "OnlyReceiveLib"
    msg = None


class InvalidExpiry(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, None)

    code = 6006
    name = "InvalidExpiry"
    msg = None


class OnlyNonDefaultLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, None)

    code = 6007
    name = "OnlyNonDefaultLib"
    msg = None


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, None)

    code = 6008
    name = "InvalidAmount"
    msg = None


class InvalidNonce(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, None)

    code = 6009
    name = "InvalidNonce"
    msg = None


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, None)

    code = 6010
    name = "Unauthorized"
    msg = None


class PayloadHashNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, None)

    code = 6011
    name = "PayloadHashNotFound"
    msg = None


class ComposeNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, None)

    code = 6012
    name = "ComposeNotFound"
    msg = None


class InvalidPayloadHash(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, None)

    code = 6013
    name = "InvalidPayloadHash"
    msg = None


class LzTokenUnavailable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, None)

    code = 6014
    name = "LzTokenUnavailable"
    msg = None


class ReadOnlyAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, None)

    code = 6015
    name = "ReadOnlyAccount"
    msg = None


class InvalidMessageLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, None)

    code = 6016
    name = "InvalidMessageLib"
    msg = None


class WritableAccountNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, None)

    code = 6017
    name = "WritableAccountNotAllowed"
    msg = None


CustomError = typing.Union[
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
    PayloadHashNotFound,
    ComposeNotFound,
    InvalidPayloadHash,
    LzTokenUnavailable,
    ReadOnlyAccount,
    InvalidMessageLib,
    WritableAccountNotAllowed,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InvalidSendLibrary(),
    6001: InvalidReceiveLibrary(),
    6002: SameValue(),
    6003: AccountNotFound(),
    6004: OnlySendLib(),
    6005: OnlyReceiveLib(),
    6006: InvalidExpiry(),
    6007: OnlyNonDefaultLib(),
    6008: InvalidAmount(),
    6009: InvalidNonce(),
    6010: Unauthorized(),
    6011: PayloadHashNotFound(),
    6012: ComposeNotFound(),
    6013: InvalidPayloadHash(),
    6014: LzTokenUnavailable(),
    6015: ReadOnlyAccount(),
    6016: InvalidMessageLib(),
    6017: WritableAccountNotAllowed(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
