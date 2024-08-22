from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SendStoredArgs(typing.TypedDict):
    params: types.send_stored_params.SendStoredParams


layout = borsh.CStruct("params" / types.send_stored_params.SendStoredParams.layout)


class SendStoredAccounts(typing.TypedDict):
    authority: Pubkey
    oapp: Pubkey
    trade_match: Pubkey


def send_stored(
    args: SendStoredArgs,
    accounts: SendStoredAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["trade_match"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xad\x0f\xdd\xae^\xd7\x95\x11"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
