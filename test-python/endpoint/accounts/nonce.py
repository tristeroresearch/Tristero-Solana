import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID


class NonceJSON(typing.TypedDict):
    bump: int
    outbound_nonce: int
    inbound_nonce: int


@dataclass
class Nonce:
    discriminator: typing.ClassVar = b"\x8f\xc5\x93_j\xa52+"
    layout: typing.ClassVar = borsh.CStruct(
        "bump" / borsh.U8, "outbound_nonce" / borsh.U64, "inbound_nonce" / borsh.U64
    )
    bump: int
    outbound_nonce: int
    inbound_nonce: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Nonce"]:
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
    ) -> typing.List[typing.Optional["Nonce"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Nonce"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Nonce":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Nonce.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            bump=dec.bump,
            outbound_nonce=dec.outbound_nonce,
            inbound_nonce=dec.inbound_nonce,
        )

    def to_json(self) -> NonceJSON:
        return {
            "bump": self.bump,
            "outbound_nonce": self.outbound_nonce,
            "inbound_nonce": self.inbound_nonce,
        }

    @classmethod
    def from_json(cls, obj: NonceJSON) -> "Nonce":
        return cls(
            bump=obj["bump"],
            outbound_nonce=obj["outbound_nonce"],
            inbound_nonce=obj["inbound_nonce"],
        )
