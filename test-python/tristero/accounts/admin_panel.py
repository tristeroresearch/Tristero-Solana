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


class AdminPanelJSON(typing.TypedDict):
    admin_wallet: str
    payment_wallet: str
    admin_panel_bump: int
    freeze_fee: int
    match_count: int
    order_count: int


@dataclass
class AdminPanel:
    discriminator: typing.ClassVar = b"\x90\xad\x0b\xfd\x16O\x06$"
    layout: typing.ClassVar = borsh.CStruct(
        "admin_wallet" / BorshPubkey,
        "payment_wallet" / BorshPubkey,
        "admin_panel_bump" / borsh.U8,
        "freeze_fee" / borsh.U64,
        "match_count" / borsh.U64,
        "order_count" / borsh.U64,
    )
    admin_wallet: Pubkey
    payment_wallet: Pubkey
    admin_panel_bump: int
    freeze_fee: int
    match_count: int
    order_count: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["AdminPanel"]:
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
    ) -> typing.List[typing.Optional["AdminPanel"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["AdminPanel"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "AdminPanel":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = AdminPanel.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            admin_wallet=dec.admin_wallet,
            payment_wallet=dec.payment_wallet,
            admin_panel_bump=dec.admin_panel_bump,
            freeze_fee=dec.freeze_fee,
            match_count=dec.match_count,
            order_count=dec.order_count,
        )

    def to_json(self) -> AdminPanelJSON:
        return {
            "admin_wallet": str(self.admin_wallet),
            "payment_wallet": str(self.payment_wallet),
            "admin_panel_bump": self.admin_panel_bump,
            "freeze_fee": self.freeze_fee,
            "match_count": self.match_count,
            "order_count": self.order_count,
        }

    @classmethod
    def from_json(cls, obj: AdminPanelJSON) -> "AdminPanel":
        return cls(
            admin_wallet=Pubkey.from_string(obj["admin_wallet"]),
            payment_wallet=Pubkey.from_string(obj["payment_wallet"]),
            admin_panel_bump=obj["admin_panel_bump"],
            freeze_fee=obj["freeze_fee"],
            match_count=obj["match_count"],
            order_count=obj["order_count"],
        )
