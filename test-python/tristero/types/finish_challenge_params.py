from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class FinishChallengeParamsJSON(typing.TypedDict):
    arb_eid: int
    trade_match_id: int
    spl_token: str
    erc20token: list[int]
    receiver: list[int]


@dataclass
class FinishChallengeParams:
    layout: typing.ClassVar = borsh.CStruct(
        "arb_eid" / borsh.U32,
        "trade_match_id" / borsh.U64,
        "spl_token" / BorshPubkey,
        "erc20token" / borsh.U8[20],
        "receiver" / borsh.U8[32],
    )
    arb_eid: int
    trade_match_id: int
    spl_token: Pubkey
    erc20token: list[int]
    receiver: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "FinishChallengeParams":
        return cls(
            arb_eid=obj.arb_eid,
            trade_match_id=obj.trade_match_id,
            spl_token=obj.spl_token,
            erc20token=obj.erc20token,
            receiver=obj.receiver,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "arb_eid": self.arb_eid,
            "trade_match_id": self.trade_match_id,
            "spl_token": self.spl_token,
            "erc20token": self.erc20token,
            "receiver": self.receiver,
        }

    def to_json(self) -> FinishChallengeParamsJSON:
        return {
            "arb_eid": self.arb_eid,
            "trade_match_id": self.trade_match_id,
            "spl_token": str(self.spl_token),
            "erc20token": self.erc20token,
            "receiver": self.receiver,
        }

    @classmethod
    def from_json(cls, obj: FinishChallengeParamsJSON) -> "FinishChallengeParams":
        return cls(
            arb_eid=obj["arb_eid"],
            trade_match_id=obj["trade_match_id"],
            spl_token=Pubkey.from_string(obj["spl_token"]),
            erc20token=obj["erc20token"],
            receiver=obj["receiver"],
        )
