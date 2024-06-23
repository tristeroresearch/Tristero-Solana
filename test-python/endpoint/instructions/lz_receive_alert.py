from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class LzReceiveAlertArgs(typing.TypedDict):
    params: types.lz_receive_alert_params.LzReceiveAlertParams


layout = borsh.CStruct(
    "params" / types.lz_receive_alert_params.LzReceiveAlertParams.layout
)


class LzReceiveAlertAccounts(typing.TypedDict):
    executor: Pubkey
    event_authority: Pubkey
    program: Pubkey


def lz_receive_alert(
    args: LzReceiveAlertArgs,
    accounts: LzReceiveAlertAccounts,
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
    identifier = b"\x83\x8d0\xde\x0f\xeb\x8d\xa0"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
