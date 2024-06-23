from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitNonceArgs(typing.TypedDict):
    params: types.init_nonce_params.InitNonceParams


layout = borsh.CStruct("params" / types.init_nonce_params.InitNonceParams.layout)


class InitNonceAccounts(typing.TypedDict):
    delegate: Pubkey
    oapp_registry: Pubkey
    nonce: Pubkey
    pending_inbound_nonce: Pubkey


def init_nonce(
    args: InitNonceArgs,
    accounts: InitNonceAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["delegate"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["pending_inbound_nonce"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcc\xab\x10\xd6\xb6\xbf\x1b\xc4"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
