from __future__ import annotations
import typing
from solders.pubkey import Pubkey
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
    oapp: Pubkey


def finish_challenge(
    args: FinishChallengeArgs,
    accounts: FinishChallengeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True),
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
