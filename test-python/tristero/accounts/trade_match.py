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
    authority: str
    user_token_addr: str
    source_token_mint: str
    dest_token_mint: list[int]
    arb_user_token_account: str
    src_index: int
    dst_index: int
    source_sell_amount: int
    dest_buy_amount: int
    eid: int
    bump: int
    trade_match_id: int
    status: int


@dataclass
class TradeMatch:
    discriminator: typing.ClassVar = b"\x00\xa3a\t\x9a\xee\x01\xb1"
    layout: typing.ClassVar = borsh.CStruct(
        "authority" / BorshPubkey,
        "user_token_addr" / BorshPubkey,
        "source_token_mint" / BorshPubkey,
        "dest_token_mint" / borsh.U8[20],
        "arb_user_token_account" / BorshPubkey,
        "src_index" / borsh.U64,
        "dst_index" / borsh.U64,
        "source_sell_amount" / borsh.U64,
        "dest_buy_amount" / borsh.U64,
        "eid" / borsh.U32,
        "bump" / borsh.U8,
        "trade_match_id" / borsh.U64,
        "status" / borsh.U8,
    )
    authority: Pubkey
    user_token_addr: Pubkey
    source_token_mint: Pubkey
    dest_token_mint: list[int]
    arb_user_token_account: Pubkey
    src_index: int
    dst_index: int
    source_sell_amount: int
    dest_buy_amount: int
    eid: int
    bump: int
    trade_match_id: int
    status: int

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
            authority=dec.authority,
            user_token_addr=dec.user_token_addr,
            source_token_mint=dec.source_token_mint,
            dest_token_mint=dec.dest_token_mint,
            arb_user_token_account=dec.arb_user_token_account,
            src_index=dec.src_index,
            dst_index=dec.dst_index,
            source_sell_amount=dec.source_sell_amount,
            dest_buy_amount=dec.dest_buy_amount,
            eid=dec.eid,
            bump=dec.bump,
            trade_match_id=dec.trade_match_id,
            status=dec.status,
        )

    def to_json(self) -> TradeMatchJSON:
        return {
            "authority": str(self.authority),
            "user_token_addr": str(self.user_token_addr),
            "source_token_mint": str(self.source_token_mint),
            "dest_token_mint": self.dest_token_mint,
            "arb_user_token_account": str(self.arb_user_token_account),
            "src_index": self.src_index,
            "dst_index": self.dst_index,
            "source_sell_amount": self.source_sell_amount,
            "dest_buy_amount": self.dest_buy_amount,
            "eid": self.eid,
            "bump": self.bump,
            "trade_match_id": self.trade_match_id,
            "status": self.status,
        }

    @classmethod
    def from_json(cls, obj: TradeMatchJSON) -> "TradeMatch":
        return cls(
            authority=Pubkey.from_string(obj["authority"]),
            user_token_addr=Pubkey.from_string(obj["user_token_addr"]),
            source_token_mint=Pubkey.from_string(obj["source_token_mint"]),
            dest_token_mint=obj["dest_token_mint"],
            arb_user_token_account=Pubkey.from_string(obj["arb_user_token_account"]),
            src_index=obj["src_index"],
            dst_index=obj["dst_index"],
            source_sell_amount=obj["source_sell_amount"],
            dest_buy_amount=obj["dest_buy_amount"],
            eid=obj["eid"],
            bump=obj["bump"],
            trade_match_id=obj["trade_match_id"],
            status=obj["status"],
        )
