from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class QuoteArgs(typing.TypedDict):
    params: types.quote_params.QuoteParams


layout = borsh.CStruct("params" / types.quote_params.QuoteParams.layout)


class QuoteAccounts(typing.TypedDict):
    send_library_program: Pubkey
    send_library_config: Pubkey
    default_send_library_config: Pubkey
    send_library_info: Pubkey
    endpoint: Pubkey
    nonce: Pubkey


def quote(
    args: QuoteArgs,
    accounts: QuoteAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["send_library_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["send_library_config"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["default_send_library_config"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["send_library_info"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x95*m\xf7\x86\x92\xd5{"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
