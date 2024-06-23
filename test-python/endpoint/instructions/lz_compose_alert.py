from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class LzComposeAlertArgs(typing.TypedDict):
    params: types.lz_compose_alert_params.LzComposeAlertParams


layout = borsh.CStruct(
    "params" / types.lz_compose_alert_params.LzComposeAlertParams.layout
)


class LzComposeAlertAccounts(typing.TypedDict):
    executor: Pubkey
    event_authority: Pubkey
    program: Pubkey


def lz_compose_alert(
    args: LzComposeAlertArgs,
    accounts: LzComposeAlertAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["executor"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x1b[\xc6MB\\z\xa7"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
