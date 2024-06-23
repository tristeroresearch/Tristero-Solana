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


class ComposeMessageStateJSON(typing.TypedDict):
    received: bool
    bump: int


@dataclass
class ComposeMessageState:
    discriminator: typing.ClassVar = b"7kO\xfe\xf3\x16\xac\xf0"
    layout: typing.ClassVar = borsh.CStruct("received" / borsh.Bool, "bump" / borsh.U8)
    received: bool
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ComposeMessageState"]:
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
    ) -> typing.List[typing.Optional["ComposeMessageState"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ComposeMessageState"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ComposeMessageState":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ComposeMessageState.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            received=dec.received,
            bump=dec.bump,
        )

    def to_json(self) -> ComposeMessageStateJSON:
        return {
            "received": self.received,
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: ComposeMessageStateJSON) -> "ComposeMessageState":
        return cls(
            received=obj["received"],
            bump=obj["bump"],
        )
