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


class InvalidSendLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, None)

    code = 6007
    name = "InvalidSendLibrary"
    msg = None


class InvalidReceiveLibrary(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, None)

    code = 6008
    name = "InvalidReceiveLibrary"
    msg = None


class SameValue(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, None)

    code = 6009
    name = "SameValue"
    msg = None


class AccountNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, None)

    code = 6010
    name = "AccountNotFound"
    msg = None


class OnlySendLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, None)

    code = 6011
    name = "OnlySendLib"
    msg = None


class OnlyReceiveLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, None)

    code = 6012
    name = "OnlyReceiveLib"
    msg = None


class InvalidExpiry(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, None)

    code = 6013
    name = "InvalidExpiry"
    msg = None


class OnlyNonDefaultLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, None)

    code = 6014
    name = "OnlyNonDefaultLib"
    msg = None


class InvalidAmount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, None)

    code = 6015
    name = "InvalidAmount"
    msg = None


class InvalidNonce(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, None)

    code = 6016
    name = "InvalidNonce"
    msg = None


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, None)

    code = 6017
    name = "Unauthorized"
    msg = None


class ComposeNotFound(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, None)

    code = 6018
    name = "ComposeNotFound"
    msg = None


class InvalidPayloadHash(ProgramError):
    def __init__(self) -> None:
        super().__init__(6019, None)

    code = 6019
    name = "InvalidPayloadHash"
    msg = None


class LzTokenUnavailable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6020, None)

    code = 6020
    name = "LzTokenUnavailable"
    msg = None


class ReadOnlyAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6021, None)

    code = 6021
    name = "ReadOnlyAccount"
    msg = None


class InvalidMessageLib(ProgramError):
    def __init__(self) -> None:
        super().__init__(6022, None)

    code = 6022
    name = "InvalidMessageLib"
    msg = None


class WritableAccountNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6023, None)

    code = 6023
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
    6007: InvalidSendLibrary(),
    6008: InvalidReceiveLibrary(),
    6009: SameValue(),
    6010: AccountNotFound(),
    6011: OnlySendLib(),
    6012: OnlyReceiveLib(),
    6013: InvalidExpiry(),
    6014: OnlyNonDefaultLib(),
    6015: InvalidAmount(),
    6016: InvalidNonce(),
    6017: Unauthorized(),
    6018: ComposeNotFound(),
    6019: InvalidPayloadHash(),
    6020: LzTokenUnavailable(),
    6021: ReadOnlyAccount(),
    6022: InvalidMessageLib(),
    6023: WritableAccountNotAllowed(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
