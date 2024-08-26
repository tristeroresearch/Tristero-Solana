from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class FinishChallengeArgs(typing.TypedDict):
    params: types.finish_challenge_params.FinishChallengeParams


layout = borsh.CStruct(
    "params" / types.finish_challenge_params.FinishChallengeParams.layout
)


class FinishChallengeAccounts(typing.TypedDict):
    authority: Pubkey
    trade_match: Pubkey
    oapp: Pubkey
    arb_user_token_account: Pubkey
    staking_account: Pubkey


def finish_challenge(
    args: FinishChallengeArgs,
    accounts: FinishChallengeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["trade_match"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["arb_user_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xbap\xaa\xc4\xb4{Ip"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
