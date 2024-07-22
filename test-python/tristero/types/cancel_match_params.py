from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class CancelMatchParamsJSON(typing.TypedDict):
    match_id: int
    tristero_oapp_bump: int


@dataclass
class CancelMatchParams:
    layout: typing.ClassVar = borsh.CStruct(
        "match_id" / borsh.U32, "tristero_oapp_bump" / borsh.U8
    )
    match_id: int
    tristero_oapp_bump: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "CancelMatchParams":
        return cls(match_id=obj.match_id, tristero_oapp_bump=obj.tristero_oapp_bump)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "match_id": self.match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
        }

    def to_json(self) -> CancelMatchParamsJSON:
        return {
            "match_id": self.match_id,
            "tristero_oapp_bump": self.tristero_oapp_bump,
        }

    @classmethod
    def from_json(cls, obj: CancelMatchParamsJSON) -> "CancelMatchParams":
        return cls(
            match_id=obj["match_id"], tristero_oapp_bump=obj["tristero_oapp_bump"]
        )
