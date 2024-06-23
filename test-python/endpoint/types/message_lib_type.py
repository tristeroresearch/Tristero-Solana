from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class SendJSON(typing.TypedDict):
    kind: typing.Literal["Send"]


class ReceiveJSON(typing.TypedDict):
    kind: typing.Literal["Receive"]


class SendAndReceiveJSON(typing.TypedDict):
    kind: typing.Literal["SendAndReceive"]


@dataclass
class Send:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Send"

    @classmethod
    def to_json(cls) -> SendJSON:
        return SendJSON(
            kind="Send",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Send": {},
        }


@dataclass
class Receive:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Receive"

    @classmethod
    def to_json(cls) -> ReceiveJSON:
        return ReceiveJSON(
            kind="Receive",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Receive": {},
        }


@dataclass
class SendAndReceive:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "SendAndReceive"

    @classmethod
    def to_json(cls) -> SendAndReceiveJSON:
        return SendAndReceiveJSON(
            kind="SendAndReceive",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "SendAndReceive": {},
        }


MessageLibTypeKind = typing.Union[Send, Receive, SendAndReceive]
MessageLibTypeJSON = typing.Union[SendJSON, ReceiveJSON, SendAndReceiveJSON]


def from_decoded(obj: dict) -> MessageLibTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Send" in obj:
        return Send()
    if "Receive" in obj:
        return Receive()
    if "SendAndReceive" in obj:
        return SendAndReceive()
    raise ValueError("Invalid enum object")


def from_json(obj: MessageLibTypeJSON) -> MessageLibTypeKind:
    if obj["kind"] == "Send":
        return Send()
    if obj["kind"] == "Receive":
        return Receive()
    if obj["kind"] == "SendAndReceive":
        return SendAndReceive()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Send" / borsh.CStruct(),
    "Receive" / borsh.CStruct(),
    "SendAndReceive" / borsh.CStruct(),
)
