from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class LzReceiveTypesArgs(typing.TypedDict):
    params: types.lz_receive_type_params.LzReceiveTypeParams


layout = borsh.CStruct(
    "params" / types.lz_receive_type_params.LzReceiveTypeParams.layout
)


class LzReceiveTypesAccounts(typing.TypedDict):
    oft_config: Pubkey
    message_lib: Pubkey


def lz_receive_types(
    args: LzReceiveTypesArgs,
    accounts: LzReceiveTypesAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["oft_config"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["message_lib"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdd\x11\xf6\x9f\xf8\x80\x1f`"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
