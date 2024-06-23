from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class RegisterLibraryArgs(typing.TypedDict):
    params: types.register_library_params.RegisterLibraryParams


layout = borsh.CStruct(
    "params" / types.register_library_params.RegisterLibraryParams.layout
)


class RegisterLibraryAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    message_lib_info: Pubkey
    event_authority: Pubkey
    program: Pubkey


def register_library(
    args: RegisterLibraryArgs,
    accounts: RegisterLibraryAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["message_lib_info"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x17\xab\x1cto\xc1\xee\x8e"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
