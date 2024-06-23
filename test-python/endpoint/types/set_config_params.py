from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class SetConfigParamsJSON(typing.TypedDict):
    oapp: str
    eid: int
    config_type: int
    config: list[int]


@dataclass
class SetConfigParams:
    layout: typing.ClassVar = borsh.CStruct(
        "oapp" / BorshPubkey,
        "eid" / borsh.U32,
        "config_type" / borsh.U32,
        "config" / borsh.Bytes,
    )
    oapp: Pubkey
    eid: int
    config_type: int
    config: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "SetConfigParams":
        return cls(
            oapp=obj.oapp, eid=obj.eid, config_type=obj.config_type, config=obj.config
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "oapp": self.oapp,
            "eid": self.eid,
            "config_type": self.config_type,
            "config": self.config,
        }

    def to_json(self) -> SetConfigParamsJSON:
        return {
            "oapp": str(self.oapp),
            "eid": self.eid,
            "config_type": self.config_type,
            "config": list(self.config),
        }

    @classmethod
    def from_json(cls, obj: SetConfigParamsJSON) -> "SetConfigParams":
        return cls(
            oapp=Pubkey.from_string(obj["oapp"]),
            eid=obj["eid"],
            config_type=obj["config_type"],
            config=bytes(obj["config"]),
        )
