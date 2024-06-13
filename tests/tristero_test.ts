import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { getExecutorProgramId, ExecutorPDADeriver, getBlockedMessageLibProgramId, OAPP_SEED, getProgramKeypair, oappIDPDA, OftPDADeriver, OftTools, OPTIONS_SEED, SEND_LIBRARY_CONFIG_SEED, NONCE_SEED, ENDPOINT_SEED, EndpointProgram, MESSAGE_LIB_SEED, SupportedPrograms, getEndpointProgramId, EventPDADeriver, BaseOApp, getSimpleMessageLibProgramId, RECEIVE_LIBRARY_CONFIG_SEED, PENDING_NONCE_SEED, UlnProgram, getULNProgramId, UlnPDADeriver, getDVNProgramId, ULN_SEED, SEND_CONFIG_SEED, ULN_CONFIG_SEED, getPricefeedProgramId, PriceFeedPDADeriver, PRICE_FEED_SEED, EXECUTOR_CONFIG_SEED, DVNDeriver } from "@layerzerolabs/lz-solana-sdk-v2";
import { Options } from "@layerzerolabs/lz-v2-utilities";
import { ChainKey, EndpointVersion, networkToEndpointId } from '@layerzerolabs/lz-definitions';

import { PublicKey, SystemProgram, Keypair, LAMPORTS_PER_SOL, sendAndConfirmTransaction, Transaction, ComputeBudgetProgram } from "@solana/web3.js"
import { TOKEN_PROGRAM_ID, createMint, getOrCreateAssociatedTokenAccount, mintTo } from '@solana/spl-token'
import { Tristero } from "../target/types/tristero";
// import { Endpoint } from '../target/types/endpoint';
import fs from 'fs';
import { describe } from "node:test";
import { bs58 } from "@coral-xyz/anchor/dist/cjs/utils/bytes";
import { Endpoint } from "../target/types/endpoint";
import { userInfo } from "os";

import userJson from "./user.json"
import otherJson from "./other.json"
// arbitrum: 0x5C105836fAa55A42957D2cC1b86e880fdE998E81

const DEFAULT_MESSAGE_LIB: PublicKey = PublicKey.default;

// Configure the client to use the local cluster.
anchor.setProvider(anchor.AnchorProvider.env());

// const program = anchor.workspace.Tristero as Program<Tristero>;
const program = anchor.workspace.Tristero as Program<Tristero>;
const endpointProgram = anchor.workspace.Endpoint as Program<Endpoint>;
const endpoint = getEndpointProgramId('solana-mainnet');
// const uln = getULNProgramId('solana-sandbox-local');
const sendLibraryProgram = new PublicKey("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")
const executorProgramId = getExecutorProgramId("solana-mainnet")
const priceFeeProgramId = getPricefeedProgramId("solana-mainnet")
const dvnProgramId = getDVNProgramId("solana-mainnet")

const ulnProgramId = getULNProgramId("solana-mainnet");


const provider = program.provider;
const connection = program.provider.connection;

const programId = program.programId;

const user = anchor.web3.Keypair.generate();
const otherUser = anchor.web3.Keypair.generate();
const receiverPubKey = otherUser.publicKey;

// const endpointEvent = endpointProgram.addEventListener("LzReceiveAlertEvent", (event) => {
//     if (event.receiver === user.publicKey) {
//         //do something
//         console.log("Success!")
//     }
// })



describe("# test scenario - tristero ", () => {


    it("testing", async () => {
        // const user = anchor.web3.Keypair.generate();
        // const admin = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(adminJson));
        const user = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(userJson))
        const otherUser = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(otherJson))
        // const otherUser = anchor.web3.Keypair.generate();
        const receiverPubKey = otherUser.publicKey;

        console.log("ok1");
        const arbitrumEndpointsId = 0x1a44076050125825900e736c501f859c50fE728c;
        const arbitrumEID = 40231;
        const delegatePublicKey = getBlockedMessageLibProgramId("solana-sandbox-local");
        console.log("ok2");
        const messageLibProgramId = getSimpleMessageLibProgramId("solana-sandbox-local");
        // const receiver = [1, 2, 3, 4, 5, 6, 7, 8]; //Receiver public key(maybe)
        const oappId = new PublicKey("76y77prsiCMvXMjuoZ5VRrhG5qYBrUMYTE5WgHqgjEn6");

        console.log("ok3 messageLibProgramId : ", messageLibProgramId);
        console.log(">>> programId : ", programId);




        console.log("begin");
        try {

            // const secretKey = JSON.parse(fs.readFileSync('~/.config/solana/id.json', 'utf8'))
            // const user = Keypair.fromSecretKey(Uint8Array.from(secretKey))
            // console.log(">>> create user publickey : ", user.publicKey);

            // const signature = await connection.requestAirdrop(user.publicKey, 5 * LAMPORTS_PER_SOL)
            // await connection.confirmTransaction(signature)
            // console.log("Airdrop successful: ", signature)

            console.log("balance: ", connection.getBalance(user.publicKey));


            console.log("------------------------Register New Oapp(Sender)------------------------");

            // console.log("programAccounts ====> ", JSON.stringify(programAccounts));

            console.log("user.publickey ===> ", user.publicKey.toString())

            const registerTristeroOAppParams = {
                delegate: user.publicKey
            }

            let keypair = getProgramKeypair("solana-mainnet", "endpoint");
            console.log("keypair: ", JSON.stringify(keypair))


            const tristeroOappPubkey = getTristeroOapp();
            const endpointEventPdaDeriver = new EventPDADeriver(endpoint)
            const uldEventPdaDeriver = new EventPDADeriver(sendLibraryProgram)

            // const signature1 = await connection.requestAirdrop(tristeroOappPubkey, 5 * LAMPORTS_PER_SOL)
            // await connection.confirmTransaction(signature1)
            // console.log("Airdrop successful: ", signature1)

            const tx1 = await program.methods.registerTristeroOapp(registerTristeroOAppParams)
                .accounts({
                    payer: user.publicKey,
                    oapp: tristeroOappPubkey,
                    oappRegistry: getOappPDA(tristeroOappPubkey),
                    endpointProgram: endpoint,
                    systemProgram: SystemProgram.programId,
                    eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
                })
                .signers([user])
                .rpc();

            console.log("tx1 = " + tx1);

            console.log("------------------------------------------------------")


            {
                /*const messageLib = getMessageLibPDA();
                            const configInstructionAccounts = {
                                delegate: user.publicKey,
                                oappRegistry: getOappPDA(tristeroOappPubkey),
                                messageLib: messageLib,
                                messageLibInfo: getMessageLibInfoPDA(messageLib),
                                messageLibProgram: messageLibProgramId,
                            }
                
                            console.log("initConfigStructionAccounts well done")
                
                            const initConfigParams = {
                                params: {
                                    oapp: tristeroOappPubkey,
                                    eid: arbitrumEID,
                                }
                            }
                
                            const instruction2 = EndpointProgram.instructions.createInitConfigInstruction(configInstructionAccounts, initConfigParams)
                
                            const transaction = new Transaction().add(instruction2);
                
                            console.log("initconfig well done")
                            console.log("instruction2  = " + instruction2)
                            const tx2 = await sendAndConfirmTransaction(connection, transaction, [user])
                            console.log("tx2 = " + tx2)*/
            }


            {
                console.log("-------------------Init Send Library-----------------------------")
                const initSendLibraryInstructionAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
                    sendLibraryConfig: getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
                }

                const initSendLibraryParams = {
                    params: {
                        oapp: tristeroOappPubkey,
                        sender: tristeroOappPubkey,
                        eid: arbitrumEID
                    }
                }

                const sendLibraryInstruction = EndpointProgram.instructions.createInitSendLibraryInstruction(initSendLibraryInstructionAccounts, initSendLibraryParams)

                console.log("InitSendLibrary well done")
                console.log("sendLibraryInstruction = " + sendLibraryInstruction)
                const transaction = new Transaction().add(sendLibraryInstruction);
                const tx3 = await sendAndConfirmTransaction(connection, transaction, [user])
                console.log("tx3 = ", tx3)
                console.log("-------------------------------------------------------------------------------")
            }

            {
                console.log("----------------------------Init Receive Library-------------------------------")

                const initReceiveLibraryInstructionAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey), // comes from other
                    receiveLibraryConfig: getReceiveLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
                }

                const initReceiveLibraryParams = {
                    params: {
                        receiver: tristeroOappPubkey,
                        eid: arbitrumEID
                    }
                }

                const receiveLibraryInstruction = EndpointProgram.instructions.createInitReceiveLibraryInstruction(initReceiveLibraryInstructionAccounts, initReceiveLibraryParams)



                console.log("InitReceiveLibrary well done")
                const transaction4 = new Transaction().add(receiveLibraryInstruction);
                const initReceiveLibTx = await sendAndConfirmTransaction(connection, transaction4, [user])
                console.log("initReceiveLibTx = ", initReceiveLibTx)
                console.log("-------------------------------------------------------------------------------")
            }

            {
                console.log("-------------------Init Nonce-----------------------------")
                const initNonceAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
                    nonce: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                    pendingInboundNonce: getPendingInboundNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                    SystemProgram: SystemProgram.programId
                }

                const initNonceParams = {
                    params: {
                        localOapp: tristeroOappPubkey,
                        remoteEid: arbitrumEID,
                        remoteOapp: Array.from(receiverPubKey.toBytes())
                    }
                }

                const initNonceInstruction = EndpointProgram.instructions.createInitNonceInstruction(initNonceAccounts, initNonceParams)

                console.log("InitNonce well done")
                console.log("initNonceInstruction = " + initNonceInstruction)
                const _transaction = new Transaction().add(initNonceInstruction);
                const _tx3 = await sendAndConfirmTransaction(connection, _transaction, [user])
                console.log("_tx3 = ", _tx3)
                console.log("-------------------------------------------------------------------------------")
            }


            //send
            {
                const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
                const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
                const sendLibraryInfo = await getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);

                console.log("sendLibraryInfo => ", sendLibraryInfo)

                console.log("------------------------ulnPdaDeriver-------------------------")
                const ulnPdaDeriver = new UlnPDADeriver(sendLibraryProgram);
                console.log("ulnPdaDeriver.config => " + ulnPdaDeriver.config(arbitrumEID))
                console.log("ulnID => " + ulnPdaDeriver.program)
                console.log("uln => " + ulnPdaDeriver.setting())

                console.log("ulnPdaDeriver.messageLib => " + JSON.stringify(ulnPdaDeriver) + "______" + ulnPdaDeriver.program)
                let sendConfig = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];

                let defaultSendConfig = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0];


                const treasury = user.publicKey;



                console.log("sendConfig " + sendConfig + " defaultSendConfig " + defaultSendConfig)
                // console.log("executor config => ",)
                console.log("------------------------------------------------------------------------")



                // const sendLibraryProgram = getDVNProgramId("solana-sandbox-local");
                console.log("getSendLibraryProgram() => ", sendLibraryProgram);



                const uln1 = PublicKey.findProgramAddressSync(
                    [Buffer.from(ULN_CONFIG_SEED)],
                    ulnProgramId,
                )[0]

                console.log("uln1, ", uln1)

                // const sendInstructionAccounts = {
                //     sender: tristeroOappPubkey,
                //     eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
                //     sendLibraryInfo: sendLibraryInfo,
                //     sendLibraryConfig: sendLibraryConfig,
                //     defaultSendLibraryConfig: defaultSendLibraryConfig,
                //     sendLibraryProgram: sendLibraryProgram,
                //     endpoint: getEndpointPDA(arbitrumEID),
                //     nonce: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                //     endpointProgram: endpoint,
                //     uln: getUlnPDA(),
                //     sendConfig: sendConfig,
                //     defaultSendConfig: defaultSendConfig,
                //     payer: user.publicKey,
                //     uldEventAuthority: uldEventPdaDeriver.eventAuthority()[0],
                //     systemProgram: SystemProgram.programId,
                //     executorProgram: executorProgramId,
                //     executorConfig: new ExecutorPDADeriver(executorProgramId).config()[0],
                //     priceFeeProgram: priceFeeProgramId,
                //     priceFeed: new PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
                //     dvnProgram: dvnProgramId,
                //     dvnConfig: new DVNDeriver(dvnProgramId).config()[0]
                // }
                const sendInstructionAccounts = {
                    sender: tristeroOappPubkey,
                    endpointProgram: endpoint,
                }

                const sendInstructionRemainingAccounts = [
                    { //0
                        pubkey: endpoint,
                        isSigner: false,
                        isWritable: true
                    },
                    { //1
                        pubkey: tristeroOappPubkey,
                        isSigner: false,
                        isWritable: true
                    },
                    { //2
                        pubkey: sendLibraryProgram,
                        isSigner: false,
                        isWritable: true
                    },
                    { //3
                        pubkey: sendLibraryConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    { //4
                        pubkey: defaultSendLibraryConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    { //5
                        pubkey: sendLibraryInfo,
                        isSigner: false,
                        isWritable: true
                    },
                    { //6
                        pubkey: getEndpointPDA(arbitrumEID),
                        isSigner: false,
                        isWritable: true
                    },
                    { //7
                        pubkey: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                        isSigner: false,
                        isWritable: true
                    },
                    { //8
                        pubkey: endpointEventPdaDeriver.eventAuthority()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    { //9
                        pubkey: endpoint,
                        isSigner: false,
                        isWritable: true
                    },
                    { //10
                        pubkey: getUlnPDA(),
                        isSigner: false,
                        isWritable: true
                    },
                    { //11
                        pubkey: sendConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    { //12
                        pubkey: defaultSendConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    { //13
                        pubkey: user.publicKey,
                        isSigner: false,
                        isWritable: true
                    },
                    { //14
                        pubkey: user.publicKey,
                        isSigner: false,
                        isWritable: true
                    },
                    { //15
                        pubkey: SystemProgram.programId,
                        isSigner: false,
                        isWritable: true
                    },
                    { //16
                        pubkey: uldEventPdaDeriver.eventAuthority()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    { //17
                        pubkey: sendLibraryProgram,
                        isSigner: false,
                        isWritable: true
                    },
                    { //18
                        pubkey: executorProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    { //19
                        pubkey: new ExecutorPDADeriver(executorProgramId).config()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    { //20
                        pubkey: priceFeeProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    { //21
                        pubkey: new PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    { //22
                        pubkey: dvnProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    { //23
                        pubkey: new DVNDeriver(dvnProgramId).config()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    { //24
                        pubkey: priceFeeProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    { //25
                        pubkey: new PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
                        isSigner: false,
                        isWritable: true
                    },
                ]

                const sendParams1 = {
                    dstEid: arbitrumEID,
                    receiver: Array.from(receiverPubKey.toBytes()),
                    message: Buffer.from("Hello World"),
                    options: Buffer.from(Options.newOptions().addExecutorLzReceiveOption(100, 0).toBytes()),
                    nativeFee: new BN(LAMPORTS_PER_SOL * 3),
                    lzTokenFee: new BN(0),
                }

                // console.log("accounts => ", JSON.stringify(sendInstructionRemainingAccounts))
                // console.log("params => ", JSON.stringify(sendParams1))

                let tx = new Transaction()
                tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 90000000 }))

                const tristeroSendInstruction = await program.methods.tristeroSend(sendParams1)
                    .accounts(sendInstructionAccounts)
                    .remainingAccounts(sendInstructionRemainingAccounts)
                    .instruction();

                tx.add(tristeroSendInstruction)


                const tx5 = await sendAndConfirmTransaction(connection, tx, [user])

                // const tx5 = await program.methods.tristeroSend(sendParams1)
                //     .accounts(sendInstructionAccounts)
                //     .rpc();
                console.log("tx5 = ", tx5)
                console.log("-------------------------------------------------------------------------------")
            }


        } catch (err) {
            console.log(err)
        }
    })
});

const getOappPDA = (authority: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(OAPP_SEED), authority.toBuffer()],
        endpoint,
    )[0]
}

const getExecutorPDA = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(EXECUTOR_CONFIG_SEED)],
        executorProgramId,
    )[0]
}

const getUlnPDA = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(ULN_SEED)],
        ulnProgramId,
    )[0]
}

const getSendConfigPDA = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(ULN_SEED),],
        ulnProgramId,
    )[0]
}

const getTristeroOapp = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("TristeroOapp")],
        programId,
    )[0]
}

// const getSendLibraryProgram = () => {
//     return PublicKey.findProgramAddressSync(
//         [Buffer.from("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH")],
//         endpoint
//     )[0]
// }

const getMessageLibPDA = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(MESSAGE_LIB_SEED)],
        endpoint,
    )[0]
}

const getMessageLibInfoPDA = (pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(MESSAGE_LIB_SEED), pubkey.toBuffer()],
        endpoint,
    )[0]
}

const getOappRegistryPDA = (pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(OAPP_SEED), pubkey.toBuffer()],
        endpoint,
    )[0]
}

const getSendLibraryConfigPDA = (senderPubkey: PublicKey, eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_LIBRARY_CONFIG_SEED), senderPubkey.toBuffer(), new BN(eid).toBuffer("be", 4)],
        endpoint,
    )[0]
}

const getReceiveLibraryConfigPDA = (receiverPubkey: PublicKey, eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(RECEIVE_LIBRARY_CONFIG_SEED), receiverPubkey.toBuffer(), new BN(eid).toBuffer("be", 4)],
        endpoint,
    )[0]
}

const getDefaultSendLibraryConfig = (eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_LIBRARY_CONFIG_SEED), new BN(eid).toBuffer("be", 4)],
        endpoint,
    )[0]
}

const getSendLibraryInfoPDA = async (sendLibraryConfig: PublicKey, defaultSendLibraryConfig: PublicKey) => {
    const res = await EndpointProgram.accounts.SendLibraryConfig.fromAccountAddress(connection, defaultSendLibraryConfig);

    return PublicKey.findProgramAddressSync(
        [Buffer.from(MESSAGE_LIB_SEED), res.messageLib.toBuffer()],
        endpoint,
    )[0]
}

const getEndpointPDA = (eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(ENDPOINT_SEED)],
        endpoint,
    )[0]
}

const getPriceFeedPDA = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PRICE_FEED_SEED)],
        priceFeeProgramId,
    )[0]
}

const getNoncePDA = (senderKey: PublicKey, eid: number, receiver: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(NONCE_SEED), senderKey.toBytes(), new BN(eid).toBuffer("be", 4), receiver.toBytes()],
        endpoint,
    )[0]
}

const getPendingInboundNoncePDA = (senderKey: PublicKey, eid: number, receiver: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PENDING_NONCE_SEED), senderKey.toBytes(), new BN(eid).toBuffer("be", 4), receiver.toBytes()],
        endpoint,
    )[0]
}