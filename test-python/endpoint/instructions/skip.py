from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SkipArgs(typing.TypedDict):
    params: types.skip_params.SkipParams


layout = borsh.CStruct("params" / types.skip_params.SkipParams.layout)


class SkipAccounts(typing.TypedDict):
    signer: Pubkey
    oapp_registry: Pubkey
    nonce: Pubkey
    pending_inbound_nonce: Pubkey
    payload_hash: Pubkey
    endpoint: Pubkey
    event_authority: Pubkey
    program: Pubkey


def skip(
    args: SkipArgs,
    accounts: SkipAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["pending_inbound_nonce"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["payload_hash"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9a?\xb55\x13\x1au-"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
