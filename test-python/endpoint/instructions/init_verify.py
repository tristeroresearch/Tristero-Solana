from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitVerifyArgs(typing.TypedDict):
    params: types.init_verify_params.InitVerifyParams


layout = borsh.CStruct("params" / types.init_verify_params.InitVerifyParams.layout)


class InitVerifyAccounts(typing.TypedDict):
    payer: Pubkey
    nonce: Pubkey
    payload_hash: Pubkey


def init_verify(
    args: InitVerifyArgs,
    accounts: InitVerifyAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["nonce"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payload_hash"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"L\xf6\xf4|s\x11\xeb["
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
