import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID


class LzReceiveTypesAccountsJSON(typing.TypedDict):
    oft_config: str
    token_mint: str


@dataclass
class LzReceiveTypesAccounts:
    discriminator: typing.ClassVar = b"\xf8W\xa7u\x05\xfb\x15~"
    layout: typing.ClassVar = borsh.CStruct(
        "oft_config" / BorshPubkey, "token_mint" / BorshPubkey
    )
    oft_config: Pubkey
    token_mint: Pubkey

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["LzReceiveTypesAccounts"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["LzReceiveTypesAccounts"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["LzReceiveTypesAccounts"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "LzReceiveTypesAccounts":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = LzReceiveTypesAccounts.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            oft_config=dec.oft_config,
            token_mint=dec.token_mint,
        )

    def to_json(self) -> LzReceiveTypesAccountsJSON:
        return {
            "oft_config": str(self.oft_config),
            "token_mint": str(self.token_mint),
        }

    @classmethod
    def from_json(cls, obj: LzReceiveTypesAccountsJSON) -> "LzReceiveTypesAccounts":
        return cls(
            oft_config=Pubkey.from_string(obj["oft_config"]),
            token_mint=Pubkey.from_string(obj["token_mint"]),
        )
