from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class BurnArgs(typing.TypedDict):
    params: types.burn_params.BurnParams


layout = borsh.CStruct("params" / types.burn_params.BurnParams.layout)


class BurnAccounts(typing.TypedDict):
    signer: Pubkey
    oapp_registry: Pubkey
    nonce: Pubkey
    payload_hash: Pubkey
    endpoint: Pubkey
    event_authority: Pubkey
    program: Pubkey


def burn(
    args: BurnArgs,
    accounts: BurnAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payload_hash"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"tn\x1d8k\xdb*]"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
