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


class TradeMatchJSON(typing.TypedDict):
    source_token_mint: str
    dest_token_mint: list[int]
    source_sell_amount: int
    dest_buy_amount: int
    source_token_account: str
    eid: int
    match_bump: int
    trade_match_id: int
    is_valiable: bool


@dataclass
class TradeMatch:
    discriminator: typing.ClassVar = b"\x00\xa3a\t\x9a\xee\x01\xb1"
    layout: typing.ClassVar = borsh.CStruct(
        "source_token_mint" / BorshPubkey,
        "dest_token_mint" / borsh.U8[20],
        "source_sell_amount" / borsh.U64,
        "dest_buy_amount" / borsh.U64,
        "source_token_account" / BorshPubkey,
        "eid" / borsh.U32,
        "match_bump" / borsh.U8,
        "trade_match_id" / borsh.U32,
        "is_valiable" / borsh.Bool,
    )
    source_token_mint: Pubkey
    dest_token_mint: list[int]
    source_sell_amount: int
    dest_buy_amount: int
    source_token_account: Pubkey
    eid: int
    match_bump: int
    trade_match_id: int
    is_valiable: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["TradeMatch"]:
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
    ) -> typing.List[typing.Optional["TradeMatch"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["TradeMatch"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "TradeMatch":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = TradeMatch.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            source_token_mint=dec.source_token_mint,
            dest_token_mint=dec.dest_token_mint,
            source_sell_amount=dec.source_sell_amount,
            dest_buy_amount=dec.dest_buy_amount,
            source_token_account=dec.source_token_account,
            eid=dec.eid,
            match_bump=dec.match_bump,
            trade_match_id=dec.trade_match_id,
            is_valiable=dec.is_valiable,
        )

    def to_json(self) -> TradeMatchJSON:
        return {
            "source_token_mint": str(self.source_token_mint),
            "dest_token_mint": self.dest_token_mint,
            "source_sell_amount": self.source_sell_amount,
            "dest_buy_amount": self.dest_buy_amount,
            "source_token_account": str(self.source_token_account),
            "eid": self.eid,
            "match_bump": self.match_bump,
            "trade_match_id": self.trade_match_id,
            "is_valiable": self.is_valiable,
        }

    @classmethod
    def from_json(cls, obj: TradeMatchJSON) -> "TradeMatch":
        return cls(
            source_token_mint=Pubkey.from_string(obj["source_token_mint"]),
            dest_token_mint=obj["dest_token_mint"],
            source_sell_amount=obj["source_sell_amount"],
            dest_buy_amount=obj["dest_buy_amount"],
            source_token_account=Pubkey.from_string(obj["source_token_account"]),
            eid=obj["eid"],
            match_bump=obj["match_bump"],
            trade_match_id=obj["trade_match_id"],
            is_valiable=obj["is_valiable"],
        )
