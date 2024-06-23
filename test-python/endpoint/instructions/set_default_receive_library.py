from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetDefaultReceiveLibraryArgs(typing.TypedDict):
    params: types.set_default_receive_library_params.SetDefaultReceiveLibraryParams


layout = borsh.CStruct(
    "params"
    / types.set_default_receive_library_params.SetDefaultReceiveLibraryParams.layout
)


class SetDefaultReceiveLibraryAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    default_receive_library_config: Pubkey
    message_lib_info: Pubkey
    event_authority: Pubkey
    program: Pubkey


def set_default_receive_library(
    args: SetDefaultReceiveLibraryArgs,
    accounts: SetDefaultReceiveLibraryAccounts,
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
    identifier = b"\x0e\xa2\xa7\xd4\r\x14\x97\x81"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
