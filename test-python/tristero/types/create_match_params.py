from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class CreateMatchParamsJSON(typing.TypedDict):
    source_sell_amount: int
    dest_token_mint: str
    dest_buy_amount: int
    eid: int
    tristero_oapp_bump: int
    source_token_address_in_arbitrum_chain: list[int]


@dataclass
class CreateMatchParams:
    layout: typing.ClassVar = borsh.CStruct(
        "source_sell_amount" / borsh.U64,
        "dest_token_mint" / BorshPubkey,
        "dest_buy_amount" / borsh.U64,
        "eid" / borsh.U32,
        "tristero_oapp_bump" / borsh.U8,
        "source_token_address_in_arbitrum_chain" / borsh.U8[40],
    )
    source_sell_amount: int
    dest_token_mint: Pubkey
    dest_buy_amount: int
    eid: int
    tristero_oapp_bump: int
    source_token_address_in_arbitrum_chain: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "CreateMatchParams":
        return cls(
            source_sell_amount=obj.source_sell_amount,
            dest_token_mint=obj.dest_token_mint,
            dest_buy_amount=obj.dest_buy_amount,
            eid=obj.eid,
            tristero_oapp_bump=obj.tristero_oapp_bump,
            source_token_address_in_arbitrum_chain=obj.source_token_address_in_arbitrum_chain,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "source_sell_amount": self.source_sell_amount,
            "dest_token_mint": self.dest_token_mint,
            "dest_buy_amount": self.dest_buy_amount,
            "eid": self.eid,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "source_token_address_in_arbitrum_chain": self.source_token_address_in_arbitrum_chain,
        }

    def to_json(self) -> CreateMatchParamsJSON:
        return {
            "source_sell_amount": self.source_sell_amount,
            "dest_token_mint": str(self.dest_token_mint),
            "dest_buy_amount": self.dest_buy_amount,
            "eid": self.eid,
            "tristero_oapp_bump": self.tristero_oapp_bump,
            "source_token_address_in_arbitrum_chain": self.source_token_address_in_arbitrum_chain,
        }

    @classmethod
    def from_json(cls, obj: CreateMatchParamsJSON) -> "CreateMatchParams":
        return cls(
            source_sell_amount=obj["source_sell_amount"],
            dest_token_mint=Pubkey.from_string(obj["dest_token_mint"]),
            dest_buy_amount=obj["dest_buy_amount"],
            eid=obj["eid"],
            tristero_oapp_bump=obj["tristero_oapp_bump"],
            source_token_address_in_arbitrum_chain=obj[
                "source_token_address_in_arbitrum_chain"
            ],
        )
