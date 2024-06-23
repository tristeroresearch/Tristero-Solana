from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class VerifyArgs(typing.TypedDict):
    params: types.verify_params.VerifyParams


layout = borsh.CStruct("params" / types.verify_params.VerifyParams.layout)


class VerifyAccounts(typing.TypedDict):
    receive_library: Pubkey
    receive_library_config: Pubkey
    default_receive_library_config: Pubkey
    nonce: Pubkey
    pending_inbound_nonce: Pubkey
    payload_hash: Pubkey
    event_authority: Pubkey
    program: Pubkey


def verify(
    args: VerifyArgs,
    accounts: VerifyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["receive_library"], is_signer=True, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["receive_library_config"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["default_receive_library_config"],
            is_signer=False,
            is_writable=False,
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
    identifier = b"\x85\xa1\x8d0x\xc6X\x96"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
