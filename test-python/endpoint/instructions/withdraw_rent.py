from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class WithdrawRentArgs(typing.TypedDict):
    params: types.withdraw_rent_params.WithdrawRentParams


layout = borsh.CStruct("params" / types.withdraw_rent_params.WithdrawRentParams.layout)


class WithdrawRentAccounts(typing.TypedDict):
    admin: Pubkey
    endpoint: Pubkey
    receiver: Pubkey
    event_authority: Pubkey
    program: Pubkey


def withdraw_rent(
    args: WithdrawRentArgs,
    accounts: WithdrawRentAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["receiver"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe2\x07)\x9e\xado\xc0k"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
