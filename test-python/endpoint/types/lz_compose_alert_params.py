from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class LzComposeAlertParamsJSON(typing.TypedDict):
    from_: str
    to: str
    guid: list[int]
    index: int
    compute_units: int
    value: int
    message: list[int]
    extra_data: list[int]
    reason: list[int]


@dataclass
class LzComposeAlertParams:
    layout: typing.ClassVar = borsh.CStruct(
        "from_" / BorshPubkey,
        "to" / BorshPubkey,
        "guid" / borsh.U8[32],
        "index" / borsh.U16,
        "compute_units" / borsh.U64,
        "value" / borsh.U64,
        "message" / borsh.Bytes,
        "extra_data" / borsh.Bytes,
        "reason" / borsh.Bytes,
    )
    from_: Pubkey
    to: Pubkey
    guid: list[int]
    index: int
    compute_units: int
    value: int
    message: bytes
    extra_data: bytes
    reason: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "LzComposeAlertParams":
        return cls(
            from_=obj.from_,
            to=obj.to,
            guid=obj.guid,
            index=obj.index,
            compute_units=obj.compute_units,
            value=obj.value,
            message=obj.message,
            extra_data=obj.extra_data,
            reason=obj.reason,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "from_": self.from_,
            "to": self.to,
            "guid": self.guid,
            "index": self.index,
            "compute_units": self.compute_units,
            "value": self.value,
            "message": self.message,
            "extra_data": self.extra_data,
            "reason": self.reason,
        }

    def to_json(self) -> LzComposeAlertParamsJSON:
        return {
            "from_": str(self.from_),
            "to": str(self.to),
            "guid": self.guid,
            "index": self.index,
            "compute_units": self.compute_units,
            "value": self.value,
            "message": list(self.message),
            "extra_data": list(self.extra_data),
            "reason": list(self.reason),
        }

    @classmethod
    def from_json(cls, obj: LzComposeAlertParamsJSON) -> "LzComposeAlertParams":
        return cls(
            from_=Pubkey.from_string(obj["from"]),
            to=Pubkey.from_string(obj["to"]),
            guid=obj["guid"],
            index=obj["index"],
            compute_units=obj["compute_units"],
            value=obj["value"],
            message=bytes(obj["message"]),
            extra_data=bytes(obj["extra_data"]),
            reason=bytes(obj["reason"]),
        )
