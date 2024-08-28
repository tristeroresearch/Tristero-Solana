from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class LzReceiveArgs(typing.TypedDict):
    params: types.lz_receive_params.LzReceiveParams


layout = borsh.CStruct("params" / types.lz_receive_params.LzReceiveParams.layout)


class LzReceiveAccounts(typing.TypedDict):
    oapp: Pubkey


def lz_receive(
    args: LzReceiveArgs,
    accounts: LzReceiveAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True)
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x08\xb3xm!v\xbdP"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
