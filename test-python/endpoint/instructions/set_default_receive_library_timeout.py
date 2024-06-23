from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetDefaultReceiveLibraryTimeoutArgs(typing.TypedDict):
    params: types.set_default_receive_library_timeout_params.SetDefaultReceiveLibraryTimeoutParams


layout = borsh.CStruct(
    "params"
    / types.set_default_receive_library_timeout_params.SetDefaultReceiveLibraryTimeoutParams.layout
)


class SetDefaultReceiveLibraryTimeoutAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    default_receive_library_config: Pubkey
    message_lib_info: Pubkey
    event_authority: Pubkey
    program: Pubkey


def set_default_receive_library_timeout(
    args: SetDefaultReceiveLibraryTimeoutArgs,
    accounts: SetDefaultReceiveLibraryTimeoutAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["default_receive_library_config"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(
            pubkey=accounts["message_lib_info"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"v ^3\x19\xf7\x10\xe8"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
