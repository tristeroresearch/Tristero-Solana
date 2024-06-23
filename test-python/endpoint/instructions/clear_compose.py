from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ClearComposeArgs(typing.TypedDict):
    params: types.clear_compose_params.ClearComposeParams


layout = borsh.CStruct("params" / types.clear_compose_params.ClearComposeParams.layout)


class ClearComposeAccounts(typing.TypedDict):
    to: Pubkey
    compose_message: Pubkey
    event_authority: Pubkey
    program: Pubkey


def clear_compose(
    args: ClearComposeArgs,
    accounts: ClearComposeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["to"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["compose_message"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"v\x01\x12\x8e_\xaf\x15}"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
