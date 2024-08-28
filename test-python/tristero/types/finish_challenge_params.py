from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class FinishChallengeParamsJSON(typing.TypedDict):
    trade_match_id: int
    receiver: list[int]
    source_token_address_in_arbitrum_chain: list[int]


@dataclass
class FinishChallengeParams:
    layout: typing.ClassVar = borsh.CStruct(
        "trade_match_id" / borsh.U64,
        "receiver" / borsh.U8[32],
        "source_token_address_in_arbitrum_chain" / borsh.U8[20],
    )
    trade_match_id: int
    receiver: list[int]
    source_token_address_in_arbitrum_chain: list[int]

    @classmethod
    def from_decoded(cls, obj: Container) -> "FinishChallengeParams":
        return cls(
            trade_match_id=obj.trade_match_id,
            receiver=obj.receiver,
            source_token_address_in_arbitrum_chain=obj.source_token_address_in_arbitrum_chain,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "trade_match_id": self.trade_match_id,
            "receiver": self.receiver,
            "source_token_address_in_arbitrum_chain": self.source_token_address_in_arbitrum_chain,
        }

    def to_json(self) -> FinishChallengeParamsJSON:
        return {
            "trade_match_id": self.trade_match_id,
            "receiver": self.receiver,
            "source_token_address_in_arbitrum_chain": self.source_token_address_in_arbitrum_chain,
        }

    @classmethod
    def from_json(cls, obj: FinishChallengeParamsJSON) -> "FinishChallengeParams":
        return cls(
            trade_match_id=obj["trade_match_id"],
            receiver=obj["receiver"],
            source_token_address_in_arbitrum_chain=obj[
                "source_token_address_in_arbitrum_chain"
            ],
        )
