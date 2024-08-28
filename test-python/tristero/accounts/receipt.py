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


class ReceiptJSON(typing.TypedDict):
    maker: str
    payout_quantity: int
    token_mint: str
    receiver: str
    is_valuable: bool


@dataclass
class Receipt:
    discriminator: typing.ClassVar = b"'\x9aIjPf\x91\x99"
    layout: typing.ClassVar = borsh.CStruct(
        "maker" / BorshPubkey,
        "payout_quantity" / borsh.U64,
        "token_mint" / BorshPubkey,
        "receiver" / BorshPubkey,
        "is_valuable" / borsh.Bool,
    )
    maker: Pubkey
    payout_quantity: int
    token_mint: Pubkey
    receiver: Pubkey
    is_valuable: bool

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Receipt"]:
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
    ) -> typing.List[typing.Optional["Receipt"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Receipt"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Receipt":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Receipt.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            maker=dec.maker,
            payout_quantity=dec.payout_quantity,
            token_mint=dec.token_mint,
            receiver=dec.receiver,
            is_valuable=dec.is_valuable,
        )

    def to_json(self) -> ReceiptJSON:
        return {
            "maker": str(self.maker),
            "payout_quantity": self.payout_quantity,
            "token_mint": str(self.token_mint),
            "receiver": str(self.receiver),
            "is_valuable": self.is_valuable,
        }

    @classmethod
    def from_json(cls, obj: ReceiptJSON) -> "Receipt":
        return cls(
            maker=Pubkey.from_string(obj["maker"]),
            payout_quantity=obj["payout_quantity"],
            token_mint=Pubkey.from_string(obj["token_mint"]),
            receiver=Pubkey.from_string(obj["receiver"]),
            is_valuable=obj["is_valuable"],
        )
