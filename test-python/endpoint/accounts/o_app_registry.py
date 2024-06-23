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


class OAppRegistryJSON(typing.TypedDict):
    delegate: str
    bump: int


@dataclass
class OAppRegistry:
    discriminator: typing.ClassVar = b"\x06\x98\xc7\x1e\xd92E\x95"
    layout: typing.ClassVar = borsh.CStruct("delegate" / BorshPubkey, "bump" / borsh.U8)
    delegate: Pubkey
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["OAppRegistry"]:
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
    ) -> typing.List[typing.Optional["OAppRegistry"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["OAppRegistry"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "OAppRegistry":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = OAppRegistry.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            delegate=dec.delegate,
            bump=dec.bump,
        )

    def to_json(self) -> OAppRegistryJSON:
        return {
            "delegate": str(self.delegate),
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: OAppRegistryJSON) -> "OAppRegistry":
        return cls(
            delegate=Pubkey.from_string(obj["delegate"]),
            bump=obj["bump"],
        )
