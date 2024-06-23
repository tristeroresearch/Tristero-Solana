from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class LzReceiveAlertParamsJSON(typing.TypedDict):
    receiver: str
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    compute_units: int
    value: int
    message: list[int]
    extra_data: list[int]
    reason: list[int]


@dataclass
class LzReceiveAlertParams:
    layout: typing.ClassVar = borsh.CStruct(
        "receiver" / BorshPubkey,
        "src_eid" / borsh.U32,
        "sender" / borsh.U8[32],
        "nonce" / borsh.U64,
        "guid" / borsh.U8[32],
        "compute_units" / borsh.U64,
        "value" / borsh.U64,
        "message" / borsh.Bytes,
        "extra_data" / borsh.Bytes,
        "reason" / borsh.Bytes,
    )
    receiver: Pubkey
    src_eid: int
    sender: list[int]
    nonce: int
    guid: list[int]
    compute_units: int
    value: int
    message: bytes
    extra_data: bytes
    reason: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "LzReceiveAlertParams":
        return cls(
            receiver=obj.receiver,
            src_eid=obj.src_eid,
            sender=obj.sender,
            nonce=obj.nonce,
            guid=obj.guid,
            compute_units=obj.compute_units,
            value=obj.value,
            message=obj.message,
            extra_data=obj.extra_data,
            reason=obj.reason,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "receiver": self.receiver,
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "compute_units": self.compute_units,
            "value": self.value,
            "message": self.message,
            "extra_data": self.extra_data,
            "reason": self.reason,
        }

    def to_json(self) -> LzReceiveAlertParamsJSON:
        return {
            "receiver": str(self.receiver),
            "src_eid": self.src_eid,
            "sender": self.sender,
            "nonce": self.nonce,
            "guid": self.guid,
            "compute_units": self.compute_units,
            "value": self.value,
            "message": list(self.message),
            "extra_data": list(self.extra_data),
            "reason": list(self.reason),
        }

    @classmethod
    def from_json(cls, obj: LzReceiveAlertParamsJSON) -> "LzReceiveAlertParams":
        return cls(
            receiver=Pubkey.from_string(obj["receiver"]),
            src_eid=obj["src_eid"],
            sender=obj["sender"],
            nonce=obj["nonce"],
            guid=obj["guid"],
            compute_units=obj["compute_units"],
            value=obj["value"],
            message=bytes(obj["message"]),
            extra_data=bytes(obj["extra_data"]),
            reason=bytes(obj["reason"]),
        )
