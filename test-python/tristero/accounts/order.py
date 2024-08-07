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


class OrderJSON(typing.TypedDict):
    order_id: int
    user_pubkey: str
    user_token_addr: str
    source_token_mint: str
    dest_token_mint: list[int]
    source_sell_amount: int
    dest_buy_amount: int
    min_sell_amount: int
    settled: int
    eid: int
    bump: int
    is_valiable: bool


@dataclass
class Order:
    discriminator: typing.ClassVar = b"\x86\xad\xdf\xb9MV\x1c3"
    layout: typing.ClassVar = borsh.CStruct(
        "order_id" / borsh.U64,
        "user_pubkey" / BorshPubkey,
        "user_token_addr" / BorshPubkey,
        "source_token_mint" / BorshPubkey,
        "dest_token_mint" / borsh.U8[20],
        "source_sell_amount" / borsh.U64,
        "dest_buy_amount" / borsh.U64,
        "min_sell_amount" / borsh.U64,
        "settled" / borsh.U64,
        "eid" / borsh.U32,
        "bump" / borsh.U8,
        "is_valiable" / borsh.Bool,
    )
    order_id: int
    user_pubkey: Pubkey
    user_token_addr: Pubkey
    source_token_mint: Pubkey
    dest_token_mint: list[int]
    source_sell_amount: int
    dest_buy_amount: int
    min_sell_amount: int
    settled: int
    eid: int
    bump: int
    is_valiable: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Order"]:
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
    ) -> typing.List[typing.Optional["Order"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Order"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Order":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Order.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            order_id=dec.order_id,
            user_pubkey=dec.user_pubkey,
            user_token_addr=dec.user_token_addr,
            source_token_mint=dec.source_token_mint,
            dest_token_mint=dec.dest_token_mint,
            source_sell_amount=dec.source_sell_amount,
            dest_buy_amount=dec.dest_buy_amount,
            min_sell_amount=dec.min_sell_amount,
            settled=dec.settled,
            eid=dec.eid,
            bump=dec.bump,
            is_valiable=dec.is_valiable,
        )

    def to_json(self) -> OrderJSON:
        return {
            "order_id": self.order_id,
            "user_pubkey": str(self.user_pubkey),
            "user_token_addr": str(self.user_token_addr),
            "source_token_mint": str(self.source_token_mint),
            "dest_token_mint": self.dest_token_mint,
            "source_sell_amount": self.source_sell_amount,
            "dest_buy_amount": self.dest_buy_amount,
            "min_sell_amount": self.min_sell_amount,
            "settled": self.settled,
            "eid": self.eid,
            "bump": self.bump,
            "is_valiable": self.is_valiable,
        }

    @classmethod
    def from_json(cls, obj: OrderJSON) -> "Order":
        return cls(
            order_id=obj["order_id"],
            user_pubkey=Pubkey.from_string(obj["user_pubkey"]),
            user_token_addr=Pubkey.from_string(obj["user_token_addr"]),
            source_token_mint=Pubkey.from_string(obj["source_token_mint"]),
            dest_token_mint=obj["dest_token_mint"],
            source_sell_amount=obj["source_sell_amount"],
            dest_buy_amount=obj["dest_buy_amount"],
            min_sell_amount=obj["min_sell_amount"],
            settled=obj["settled"],
            eid=obj["eid"],
            bump=obj["bump"],
            is_valiable=obj["is_valiable"],
        )
