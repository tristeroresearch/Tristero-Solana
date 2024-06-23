from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetConfigArgs(typing.TypedDict):
    params: types.set_config_params.SetConfigParams


layout = borsh.CStruct("params" / types.set_config_params.SetConfigParams.layout)


class SetConfigAccounts(typing.TypedDict):
    signer: Pubkey
    oapp_registry: Pubkey
    message_lib_info: Pubkey
    message_lib: Pubkey
    message_lib_program: Pubkey


def set_config(
    args: SetConfigArgs,
    accounts: SetConfigAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["message_lib_info"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["message_lib"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["message_lib_program"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"l\x9e\x9a\xaf\xd4b4B"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
