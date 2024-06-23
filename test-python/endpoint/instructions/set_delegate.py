from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class SetDelegateArgs(typing.TypedDict):
    params: types.set_delegate_params.SetDelegateParams


layout = borsh.CStruct("params" / types.set_delegate_params.SetDelegateParams.layout)


class SetDelegateAccounts(typing.TypedDict):
    oapp: Pubkey
    oapp_registry: Pubkey
    event_authority: Pubkey
    program: Pubkey


def set_delegate(
    args: SetDelegateArgs,
    accounts: SetDelegateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["oapp"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["oapp_registry"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["event_authority"], is_signer=False, is_writable=False
        ),
        AccountMeta(pubkey=accounts["program"], is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xf2\x1e.Ll\xeb\x80\xb5"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
