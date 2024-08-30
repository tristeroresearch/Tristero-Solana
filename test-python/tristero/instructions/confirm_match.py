from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class ConfirmMatchArgs(typing.TypedDict):
    params: types.confirm_match_params.ConfirmMatchParams


layout = borsh.CStruct("params" / types.confirm_match_params.ConfirmMatchParams.layout)


class ConfirmMatchAccounts(typing.TypedDict):
    signer: Pubkey
    oapp: Pubkey
    order: Pubkey
    trade_match: Pubkey
    staking_account: Pubkey
    token_account: Pubkey


def confirm_match(
    args: ConfirmMatchArgs,
    accounts: ConfirmMatchAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["trade_match"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xc8X;\x04\x07\x1d\xd4\x14"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
