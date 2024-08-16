from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class AdminPanelUpdateArgs(typing.TypedDict):
    params: types.update_params.UpdateParams


layout = borsh.CStruct("params" / types.update_params.UpdateParams.layout)


class AdminPanelUpdateAccounts(typing.TypedDict):
    authority: Pubkey
    admin_panel: Pubkey


def admin_panel_update(
    args: AdminPanelUpdateArgs,
    accounts: AdminPanelUpdateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["admin_panel"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xbbn\xde\x0e\xfe`\xa5\x84"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
