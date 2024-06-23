from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class InitEndpointArgs(typing.TypedDict):
    params: types.init_endpoint_params.InitEndpointParams


layout = borsh.CStruct("params" / types.init_endpoint_params.InitEndpointParams.layout)


class InitEndpointAccounts(typing.TypedDict):
    payer: Pubkey
    endpoint: Pubkey


def init_endpoint(
    args: InitEndpointArgs,
    accounts: InitEndpointAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["endpoint"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb2\x1e\x1d\xcfx\xe1\xf6\x86"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
