from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class RegisterConfigArgs(typing.TypedDict):
    param_pubkey: Pubkey


layout = borsh.CStruct("param_pubkey" / BorshPubkey)


class RegisterConfigAccounts(typing.TypedDict):
    payer: Pubkey
    oapp_config: Pubkey
    lz_receive_types_accounts: Pubkey


def register_config(
    args: RegisterConfigArgs,
    accounts: RegisterConfigAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp_config"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["lz_receive_types_accounts"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b" \xf7R\x83#\xb7\x079"
    encoded_args = layout.build(
        {
            "param_pubkey": args["param_pubkey"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
