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
from .. import types


class ReceiveLibraryConfigJSON(typing.TypedDict):
    message_lib: str
    timeout: typing.Optional[types.receive_library_timeout.ReceiveLibraryTimeoutJSON]
    bump: int


@dataclass
class ReceiveLibraryConfig:
    discriminator: typing.ClassVar = b"\x8e\xe2\xfb\x8a\x01\xce[\xc1"
    layout: typing.ClassVar = borsh.CStruct(
        "message_lib" / BorshPubkey,
        "timeout"
        / borsh.Option(types.receive_library_timeout.ReceiveLibraryTimeout.layout),
        "bump" / borsh.U8,
    )
    message_lib: Pubkey
    timeout: typing.Optional[types.receive_library_timeout.ReceiveLibraryTimeout]
    bump: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["ReceiveLibraryConfig"]:
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
    ) -> typing.List[typing.Optional["ReceiveLibraryConfig"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["ReceiveLibraryConfig"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "ReceiveLibraryConfig":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = ReceiveLibraryConfig.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            message_lib=dec.message_lib,
            timeout=(
                None
                if dec.timeout is None
                else types.receive_library_timeout.ReceiveLibraryTimeout.from_decoded(
                    dec.timeout
                )
            ),
            bump=dec.bump,
        )

    def to_json(self) -> ReceiveLibraryConfigJSON:
        return {
            "message_lib": str(self.message_lib),
            "timeout": (None if self.timeout is None else self.timeout.to_json()),
            "bump": self.bump,
        }

    @classmethod
    def from_json(cls, obj: ReceiveLibraryConfigJSON) -> "ReceiveLibraryConfig":
        return cls(
            message_lib=Pubkey.from_string(obj["message_lib"]),
            timeout=(
                None
                if obj["timeout"] is None
                else types.receive_library_timeout.ReceiveLibraryTimeout.from_json(
                    obj["timeout"]
                )
            ),
            bump=obj["bump"],
        )
