from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SendArgs(typing.TypedDict):
    params: types.send_params.SendParams


layout = borsh.CStruct("params" / types.send_params.SendParams.layout)


class SendAccounts(typing.TypedDict):
    sender: Pubkey
    send_library_program: Pubkey
    send_library_config: Pubkey
    default_send_library_config: Pubkey
    send_library_info: Pubkey
    endpoint: Pubkey
    nonce: Pubkey
    event_authority: Pubkey
    program: Pubkey


def send(
    args: SendArgs,
    accounts: SendAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["sender"], is_signer=True, is_writable=False),
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
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"f\xfb\x14\xbbAK\x0cE"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
