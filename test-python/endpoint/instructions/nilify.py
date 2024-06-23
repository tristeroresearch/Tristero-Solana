from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class NilifyArgs(typing.TypedDict):
    params: types.nilify_params.NilifyParams


layout = borsh.CStruct("params" / types.nilify_params.NilifyParams.layout)


class NilifyAccounts(typing.TypedDict):
    signer: Pubkey
    oapp_registry: Pubkey
    nonce: Pubkey
    pending_inbound_nonce: Pubkey
    payload_hash: Pubkey
    event_authority: Pubkey
    program: Pubkey


def nilify(
    args: NilifyArgs,
    accounts: NilifyAccounts,
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
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x8f\x88\x81\xc7$#\xa0U"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
