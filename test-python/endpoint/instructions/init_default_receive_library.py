from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitDefaultReceiveLibraryArgs(typing.TypedDict):
    params: types.init_default_receive_library_params.InitDefaultReceiveLibraryParams


layout = borsh.CStruct(
    "params"
    / types.init_default_receive_library_params.InitDefaultReceiveLibraryParams.layout
)


class InitDefaultReceiveLibraryAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    default_receive_library_config: Pubkey
    message_lib_info: Pubkey
    event_authority: Pubkey
    program: Pubkey


def init_default_receive_library(
    args: InitDefaultReceiveLibraryArgs,
    accounts: InitDefaultReceiveLibraryAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["default_receive_library_config"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["message_lib_info"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b" \xcaL\x16*\xf9\xe3m"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
