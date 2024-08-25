from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class RegisterTristeroOappArgs(typing.TypedDict):
    params: types.register_tristero_o_app_params.RegisterTristeroOAppParams


layout = borsh.CStruct(
    "params" / types.register_tristero_o_app_params.RegisterTristeroOAppParams.layout
)


class RegisterTristeroOappAccounts(typing.TypedDict):
    payer: Pubkey
    oapp: Pubkey
    admin_panel: Pubkey
    oapp_registry: Pubkey
    event_authority: Pubkey
    endpoint_program: Pubkey


def register_tristero_oapp(
    args: RegisterTristeroOappArgs,
    accounts: RegisterTristeroOappAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin_panel"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["endpoint_program"], is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"E\r-\xa6\xa5\xb4\n>"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
