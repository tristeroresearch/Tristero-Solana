from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetReceiveLibraryArgs(typing.TypedDict):
    params: types.set_receive_library_params.SetReceiveLibraryParams


layout = borsh.CStruct(
    "params" / types.set_receive_library_params.SetReceiveLibraryParams.layout
)


class SetReceiveLibraryAccounts(typing.TypedDict):
    signer: Pubkey
    oapp_registry: Pubkey
    receive_library_config: Pubkey
    message_lib_info: typing.Optional[Pubkey]
    event_authority: Pubkey
    program: Pubkey


def set_receive_library(
    args: SetReceiveLibraryArgs,
    accounts: SetReceiveLibraryAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["receive_library_config"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["message_lib_info"], is_signer=False, is_writable=False
        )
        if accounts["message_lib_info"]
        else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdf\xac\xb4i\xa5\xa1\x93\xe4"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
