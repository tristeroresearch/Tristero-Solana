from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ExecuteMatchArgs(typing.TypedDict):
    params: types.execute_match_params.ExecuteMatchParams


layout = borsh.CStruct("params" / types.execute_match_params.ExecuteMatchParams.layout)


class ExecuteMatchAccounts(typing.TypedDict):
    authority: Pubkey
    token_account: Pubkey
    arb_user_token_account: Pubkey
    receipt: Pubkey


def execute_match(
    args: ExecuteMatchArgs,
    accounts: ExecuteMatchAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["arb_user_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["receipt"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"L/[\xdf\x14\n\x93\xe8"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
