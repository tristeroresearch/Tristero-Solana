import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID
from .. import types


class MessageLibInfoJSON(typing.TypedDict):
    message_lib_type: types.message_lib_type.MessageLibTypeJSON
    bump: int
    message_lib_bump: int


@dataclass
class MessageLibInfo:
    discriminator: typing.ClassVar = b"gf\xda\x1c\xcc\x87G\x0e"
    layout: typing.ClassVar = borsh.CStruct(
        "message_lib_type" / types.message_lib_type.layout,
        "bump" / borsh.U8,
        "message_lib_bump" / borsh.U8,
    )
    message_lib_type: types.message_lib_type.MessageLibTypeKind
    bump: int
    message_lib_bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MessageLibInfo"]:
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
    ) -> typing.List[typing.Optional["MessageLibInfo"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MessageLibInfo"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MessageLibInfo":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = MessageLibInfo.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            message_lib_type=types.message_lib_type.from_decoded(dec.message_lib_type),
            bump=dec.bump,
            message_lib_bump=dec.message_lib_bump,
        )

    def to_json(self) -> MessageLibInfoJSON:
        return {
            "message_lib_type": self.message_lib_type.to_json(),
            "bump": self.bump,
            "message_lib_bump": self.message_lib_bump,
        }

    @classmethod
    def from_json(cls, obj: MessageLibInfoJSON) -> "MessageLibInfo":
        return cls(
            message_lib_type=types.message_lib_type.from_json(obj["message_lib_type"]),
            bump=obj["bump"],
            message_lib_bump=obj["message_lib_bump"],
        )
