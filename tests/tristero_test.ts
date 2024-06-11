import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { getBlockedMessageLibProgramId, OAPP_SEED, oappIDPDA, OftPDADeriver, OftTools, OPTIONS_SEED, SEND_LIBRARY_CONFIG_SEED, NONCE_SEED, ENDPOINT_SEED, EndpointProgram} from "@layerzerolabs/lz-solana-sdk-v2";
import { addressToBytes32 } from "@layerzerolabs/lz-v2-utilities";
import { PublicKey, SystemProgram, Keypair, LAMPORTS_PER_SOL } from "@solana/web3.js"
import { TOKEN_PROGRAM_ID, createMint, getOrCreateAssociatedTokenAccount, mintTo } from '@solana/spl-token'
import { Tristero } from "../target/types/tristero";
import fs from 'fs';
import { describe } from "node:test";

// Configure the client to use the local cluster.
anchor.setProvider(anchor.AnchorProvider.env());

const program = anchor.workspace.Tristero as Program<Tristero>;
const provider = program.provider;
const connection = program.provider.connection;

const programId = program.programId;





describe("# test scenario - tristero ", () => {
    it("testing", async () => {
        const endpoint = new PublicKey("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6");
        console.log("ok1");
        const arbitrumEndpointsId = 0x1a44076050125825900e736c501f859c50fE728c;
        const arbitrumEID = 421614;
        const delegatePublicKey = getBlockedMessageLibProgramId("solana-sandbox-local");
        console.log("ok2");
        const messageLibProgramId = getBlockedMessageLibProgramId("solana-sandbox-local");
        const receiver = [1, 2, 3, 4, 5, 6, 7, 8]; //Receiver public key(maybe)
        const oappId = new PublicKey("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6");

        console.log("ok3 messageLibProgramId : ", messageLibProgramId);
        console.log(">>> programId : ", programId);

        console.log("begin");
        try {
            const user = anchor.web3.Keypair.generate();
            // const secretKey = JSON.parse(fs.readFileSync('~/.config/solana/id.json', 'utf8'))
            // const user = Keypair.fromSecretKey(Uint8Array.from(secretKey))
            console.log(">>> create user publickey : ", user.publicKey);

            const signature = await connection.requestAirdrop(user.publicKey, 5 * LAMPORTS_PER_SOL)
            await connection.confirmTransaction(signature)
            console.log("Airdrop successful: ", signature)

            // const seed: number[][] = Array.from(Array.from(user.publicKey.toBytes()))

            // const serializedSeed = seed.map(innerArray => Buffer.from(innerArray));

            const programAccounts = await connection.getProgramAccounts(endpoint);
            console.log("------------------------------------------------");
            // console.log("programAccounts ====> ", JSON.stringify(programAccounts));

            console.log("user.publickey ===> ", user.publicKey.toString())
            
            // const registerTristeroOAppParams = {
            //     endpointProgram: endpoint,
            //     seeds: [user.publicKey.toBuffer()],
            //     delegate: user.publicKey
            // }

            // const tx1 = await program.methods.registerTristeroOapp(registerTristeroOAppParams)
            //     .accounts({
            //         payer: user.publicKey,
            //         oapp: user.publicKey,
            //         oappRegistry: getOappPDA(oappId),
            //         systemProgram: SystemProgram.programId
            //     })
            //     .signers([user])
            //     .rpc();
            // console.log("Good tx1 = ", tx1)

            // Convert each field to little-endian Uint8Array
            const nativeFeeBytes = new Uint8Array(new ArrayBuffer(8));
            nativeFeeBytes.set((new BN(100)).toArray());

            const lzTokenFeeBytes = new Uint8Array(new ArrayBuffer(8));
            lzTokenFeeBytes.set((new BN(0)).toArray());

            // Concatenate the byte arrays
            const bytes = new Uint8Array(16);
            bytes.set(nativeFeeBytes, 0);
            bytes.set(lzTokenFeeBytes, 8);

            const tristeroSendParams = {
                endpointProgram: endpoint,
                sender: user.publicKey,
                dstEid: arbitrumEID,
                receiver: receiver, // have to change in the future
                message: Buffer.from("Hello world"),
                options: Buffer.concat([new BN(100).toBuffer(), new BN(0).toBuffer()]), // have to consist of native_fee and lz_token_fee
                nativeFee: new BN(100),
                lzTokenFee: new BN(0),
            }



            const tx2 = await program.methods.tristeroSend(tristeroSendParams)
                .accounts({
                    sender: user.publicKey,
                    sendLibraryProgram: messageLibProgramId,
                    sendLibraryConfig: getSendLibraryConfigPDA(user.publicKey, messageLibProgramId),
                    defaultSendLibraryConfig: getDefaultSendLibraryConfigPDA(messageLibProgramId),
                    sendLibraryInfo: getSendLibraryInfo(),
                    endpoint: getEndpoint(),
                    nonce: getNoncePDA(user.publicKey, arbitrumEID, receiver),
                })
                .signers([user])
                .rpc();
            console.log("Good tx2 = ", tx2)
        } catch (err) {
            console.log(err)
        }
    })
});

const getOappPDA = (authority: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(OAPP_SEED), authority.toBuffer()],
        programId,
    )[0]
}

const getOapp = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(OAPP_SEED)],
        programId,
    )[0]
}

const getSendLibraryConfigPDA = (senderKey: PublicKey, dstEid: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_LIBRARY_CONFIG_SEED), senderKey.toBuffer(), dstEid.toBuffer()],
        programId,
    )[0]
}

const getDefaultSendLibraryConfigPDA = (dstEid: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_LIBRARY_CONFIG_SEED), dstEid.toBuffer()],
        programId,
    )[0]
}

const getSendLibraryInfo = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_LIBRARY_CONFIG_SEED)],
        programId,
    )[0]
}

const getEndpoint = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(ENDPOINT_SEED)],
        programId,
    )[0]
}

const getNoncePDA = (senderKey: PublicKey, dstEid: number, receiver: number[]) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(NONCE_SEED), senderKey.toBuffer(), Buffer.from(dstEid.toString()), Buffer.from(receiver)],
        programId
    )[0]
}

const getOftConfigPDA = (authority: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(OftTools.OFT_SEED), authority.toBuffer()],
        programId,
    )[0]
}