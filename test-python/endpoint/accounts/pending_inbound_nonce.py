import typing
from dataclasses import dataclass
from construct import Construct
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID


class PendingInboundNonceJSON(typing.TypedDict):
    nonces: list[int]
    bump: int


@dataclass
class PendingInboundNonce:
    discriminator: typing.ClassVar = b"\xaa\xb0_\xf0x\xe7\xf1\xda"
    layout: typing.ClassVar = borsh.CStruct(
        "nonces" / borsh.Vec(typing.cast(Construct, borsh.U64)), "bump" / borsh.U8
    )
    nonces: list[int]
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["PendingInboundNonce"]:
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
    ) -> typing.List[typing.Optional["PendingInboundNonce"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["PendingInboundNonce"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "PendingInboundNonce":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = PendingInboundNonce.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            nonces=dec.nonces,
            bump=dec.bump,
        )

    def to_json(self) -> PendingInboundNonceJSON:
        return {
            "nonces": self.nonces,
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: PendingInboundNonceJSON) -> "PendingInboundNonce":
        return cls(
            nonces=obj["nonces"],
            bump=obj["bump"],
        )
