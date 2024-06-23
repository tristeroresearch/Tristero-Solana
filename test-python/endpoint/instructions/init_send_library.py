from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitSendLibraryArgs(typing.TypedDict):
    params: types.init_send_library_params.InitSendLibraryParams


layout = borsh.CStruct(
    "params" / types.init_send_library_params.InitSendLibraryParams.layout
)


class InitSendLibraryAccounts(typing.TypedDict):
    delegate: Pubkey
    oapp_registry: Pubkey
    send_library_config: Pubkey


def init_send_library(
    args: InitSendLibraryArgs,
    accounts: InitSendLibraryAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["delegate"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["send_library_config"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9c\x18\xebxI\xc1\x90\x13"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
