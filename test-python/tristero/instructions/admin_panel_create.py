from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class AdminPanelCreateArgs(typing.TypedDict):
    params: types.initialize_params.InitializeParams


layout = borsh.CStruct("params" / types.initialize_params.InitializeParams.layout)


class AdminPanelCreateAccounts(typing.TypedDict):
    admin_wallet: Pubkey
    admin_panel: Pubkey


def admin_panel_create(
    args: AdminPanelCreateArgs,
    accounts: AdminPanelCreateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin_wallet"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["admin_panel"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf6\t*l\xb3\x10\xed\x13"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
