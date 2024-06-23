from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class TristeroSendArgs(typing.TypedDict):
    params: types.tristero_send_params.TristeroSendParams


layout = borsh.CStruct("params" / types.tristero_send_params.TristeroSendParams.layout)


class TristeroSendAccounts(typing.TypedDict):
    sender: Pubkey
    endpoint_program: Pubkey
    event_authority: Pubkey
    program: Pubkey


def tristero_send(
    args: TristeroSendArgs,
    accounts: TristeroSendAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["sender"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["endpoint_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"y0\xda40X\xc1\xd1"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
