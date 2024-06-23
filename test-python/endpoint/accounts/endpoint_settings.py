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


class EndpointSettingsJSON(typing.TypedDict):
    eid: int
    bump: int
    admin: str
    lz_token_mint: typing.Optional[str]


@dataclass
class EndpointSettings:
    discriminator: typing.ClassVar = b"\xdd\xe8I8\nBH\x0e"
    layout: typing.ClassVar = borsh.CStruct(
        "eid" / borsh.U32,
        "bump" / borsh.U8,
        "admin" / BorshPubkey,
        "lz_token_mint" / borsh.Option(BorshPubkey),
    )
    eid: int
    bump: int
    admin: Pubkey
    lz_token_mint: typing.Optional[Pubkey]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["EndpointSettings"]:
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
    ) -> typing.List[typing.Optional["EndpointSettings"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["EndpointSettings"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "EndpointSettings":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = EndpointSettings.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            eid=dec.eid,
            bump=dec.bump,
            admin=dec.admin,
            lz_token_mint=dec.lz_token_mint,
        )

    def to_json(self) -> EndpointSettingsJSON:
        return {
            "eid": self.eid,
            "bump": self.bump,
            "admin": str(self.admin),
            "lz_token_mint": (
                None if self.lz_token_mint is None else str(self.lz_token_mint)
            ),
        }

    @classmethod
    def from_json(cls, obj: EndpointSettingsJSON) -> "EndpointSettings":
        return cls(
            eid=obj["eid"],
            bump=obj["bump"],
            admin=Pubkey.from_string(obj["admin"]),
            lz_token_mint=(
                None
                if obj["lz_token_mint"] is None
                else Pubkey.from_string(obj["lz_token_mint"])
            ),
        )
