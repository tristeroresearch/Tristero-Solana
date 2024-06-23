from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetLzTokenArgs(typing.TypedDict):
    params: types.set_lz_token_params.SetLzTokenParams


layout = borsh.CStruct("params" / types.set_lz_token_params.SetLzTokenParams.layout)


class SetLzTokenAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    event_authority: Pubkey
    program: Pubkey


def set_lz_token(
    args: SetLzTokenArgs,
    accounts: SetLzTokenAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x16\x97p\xae\xd5\xe1\xdfH"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
