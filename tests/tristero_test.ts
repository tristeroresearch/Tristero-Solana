import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { getExecutorProgramId, ExecutorPDADeriver, getBlockedMessageLibProgramId, OAPP_SEED, getProgramKeypair, oappIDPDA, OftPDADeriver, OftTools, OPTIONS_SEED, SEND_LIBRARY_CONFIG_SEED, NONCE_SEED, ENDPOINT_SEED, EndpointProgram, MESSAGE_LIB_SEED, SupportedPrograms, getEndpointProgramId, EventPDADeriver, BaseOApp, getSimpleMessageLibProgramId, RECEIVE_LIBRARY_CONFIG_SEED, PENDING_NONCE_SEED, UlnProgram, getULNProgramId, UlnPDADeriver, getDVNProgramId, ULN_SEED, SEND_CONFIG_SEED, ULN_CONFIG_SEED, getPricefeedProgramId, PriceFeedPDADeriver, PRICE_FEED_SEED, EXECUTOR_CONFIG_SEED, DVNDeriver, PAYLOAD_HASH_SEED } from "@layerzerolabs/lz-solana-sdk-v2";
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
import adminJson from "./adminJson.json"
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
const user = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(userJson))
const otherUser = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(otherJson))
const admin = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(adminJson))
const receiverPubKey = Buffer.from(Array(32).fill(1)) // have to change to arbitrum side
const arbitrumEID = 40231;

describe("# test scenario - tristero ", () => {

    console.log("endpoint program id = ", endpoint);


    it("testing", async () => {
        console.log(">>> programId : ", programId);
        console.log("begin");
        try {

            // const userAirDroptx = await connection.requestAirdrop(user.publicKey, 5 * LAMPORTS_PER_SOL)
            // await connection.confirmTransaction(userAirDroptx)
            // console.log("User Airdrop successful: ", userAirDroptx)

            // const adminAirDroptx = await connection.requestAirdrop(admin.publicKey, 5 * LAMPORTS_PER_SOL)
            // await connection.confirmTransaction(adminAirDroptx)
            // console.log("User Airdrop successful: ", adminAirDroptx)

            // console.log("balance(User): ", await connection.getBalance(user.publicKey), "balance(Admin): ", await connection.getBalance(admin.publicKey));

            console.log("------------------------Create admin panel------------------------");

            // const adminPanelCreateTx = await program.methods.adminPanelCreate({ adminWallet: admin.publicKey, paymentWallet: admin.publicKey })
            //     .accounts({
            //         adminWallet: admin.publicKey,
            //         adminPanel: getAdminPanel(),
            //     })
            //     .signers([admin])
            //     .rpc();
            // console.log("adminPanelCreateTx = ", adminPanelCreateTx)

            console.log("------------------------Update admin panel------------------------");

            // const adminPanelUpdateTx = await program.methods.adminPanelUpdate({ adminWallet: admin.publicKey, paymentWallet: admin.publicKey })
            //     .accounts({
            //         adminWallet: admin.publicKey,
            //         adminPanel: getAdminPanel(),
            //     })
            //     .signers([admin])
            //     .rpc();
            // console.log("adminPanelUpdateTx = ", adminPanelUpdateTx)

            console.log("------------------------Create User------------------------");

            // const createUserTx = await program.methods.createUser()
            //     .accounts({
            //         authority: user.publicKey,
            //         user: getUserPDA(user.publicKey),
            //     })
            //     .signers([user])
            //     .rpc();
            // console.log("createUserTx = ", createUserTx)

            const tristeroOappPubkey = getTristeroOapp();
            const endpointEventPdaDeriver = new EventPDADeriver(endpoint)
            const uldEventPdaDeriver = new EventPDADeriver(sendLibraryProgram)

            console.log("------------------------Register New Oapp(Sender)------------------------");

            console.log("user.publickey ===> ", user.publicKey.toString())

            // const registerTristeroOAppParams = {
            //     delegate: user.publicKey
            // }

            // console.log("registerTristeroOapp => ", JSON.stringify({
            //     payer: user.publicKey,
            //     oapp: tristeroOappPubkey,
            //     oappRegistry: getOappPDA(tristeroOappPubkey),
            //     endpointProgram: endpoint,
            //     systemProgram: SystemProgram.programId,
            //     eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            // }))

            // const tx1 = await program.methods.registerTristeroOapp(registerTristeroOAppParams)
            //     .accounts({
            //         payer: user.publicKey,
            //         oapp: tristeroOappPubkey,
            //         oappRegistry: getOappPDA(tristeroOappPubkey),
            //         endpointProgram: endpoint,
            //         // systemProgram: SystemProgram.programId,
            //         eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            //     })
            //     .signers([user])
            //     .rpc();

            // console.log("tx1 = " + tx1);

            // console.log("------------------------------------------------------")


            console.log("-------------------Init Send Library-----------------------------")
            // {
            //     const initSendLibraryInstructionAccounts = {
            //         delegate: user.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
            //         sendLibraryConfig: getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
            //     }

            //     const initSendLibraryParams = {
            //         params: {
            //             oapp: tristeroOappPubkey,
            //             sender: tristeroOappPubkey,
            //             eid: arbitrumEID
            //         }
            //     }

            //     const sendLibraryInstruction = EndpointProgram.instructions.createInitSendLibraryInstruction(initSendLibraryInstructionAccounts, initSendLibraryParams)

            //     console.log("InitSendLibrary well done")
            //     console.log("sendLibraryInstruction = " + sendLibraryInstruction)
            //     const transaction = new Transaction().add(sendLibraryInstruction);
            //     const tx3 = await sendAndConfirmTransaction(connection, transaction, [user])
            //     console.log("tx3 = ", tx3)
            //     console.log("-------------------------------------------------------------------------------")
            // }


            console.log("----------------------------Init Receive Library-------------------------------")
            // {

            //     const initReceiveLibraryInstructionAccounts = {
            //         delegate: user.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey), // comes from other
            //         receiveLibraryConfig: getReceiveLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
            //     }

            //     const initReceiveLibraryParams = {
            //         params: {
            //             receiver: tristeroOappPubkey,
            //             eid: arbitrumEID
            //         }
            //     }

            //     const receiveLibraryInstruction = EndpointProgram.instructions.createInitReceiveLibraryInstruction(initReceiveLibraryInstructionAccounts, initReceiveLibraryParams)



            //     console.log("InitReceiveLibrary well done")
            //     const transaction4 = new Transaction().add(receiveLibraryInstruction);
            //     const initReceiveLibTx = await sendAndConfirmTransaction(connection, transaction4, [user])
            //     console.log("initReceiveLibTx = ", initReceiveLibTx)
            //     console.log("-------------------------------------------------------------------------------")
            // }

            console.log("-------------------Init Nonce-----------------------------")
            // {
            //     const initNonceAccounts = {
            //         delegate: user.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
            //         nonce: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
            //         pendingInboundNonce: getPendingInboundNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
            //         SystemProgram: SystemProgram.programId
            //     }

            //     const initNonceParams = {
            //         params: {
            //             localOapp: tristeroOappPubkey,
            //             remoteEid: arbitrumEID,
            //             remoteOapp: Array.from(receiverPubKey)
            //         }
            //     }

            //     const initNonceInstruction = EndpointProgram.instructions.createInitNonceInstruction(initNonceAccounts, initNonceParams)

            //     console.log("InitNonce well done")
            //     console.log("initNonceInstruction = " + initNonceInstruction)
            //     const _transaction = new Transaction().add(initNonceInstruction);
            //     const _tx3 = await sendAndConfirmTransaction(connection, _transaction, [user])
            //     console.log("_tx3 = ", _tx3)
            //     console.log("-------------------------------------------------------------------------------")
            // }

            // console.log("------------------------------mint new spl token(only need in localnet)-------------------------------------------------");
            // const mint = await createMint(
            //     connection,
            //     user,
            //     user.publicKey,
            //     null,
            //     5 // Decimals
            // )
            const mint = new PublicKey("iwyvga9wLQAU9cNk9kycrLptQR8dgpMBvjDWZjc3npN")

            // console.log("Mint Address: ", mint.toBase58());

            // Create a token account for the mint
            // const tokenAccount = await getOrCreateAssociatedTokenAccount(
            //     connection,
            //     user,
            //     mint,
            //     user.publicKey
            // )

            const tokenAccount = new PublicKey("FFKNLCf6tK6B7yoJivjgcW9uoaQXx38DdaAheMH857Jh")

            console.log("Token Account Address: ", tokenAccount.toBase58())

            // Mint some tokens to the token account
            // await mintTo(
            //     connection,
            //     user,
            //     mint,
            //     tokenAccount,
            //     user.publicKey,
            //     10000000000 // Amount to mint (int smallest units)
            // )

            const usdCoinMintAddress = new PublicKey("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU") // dest Token Mint Address

            const selectedUser = await program.account.user.fetch(getUserPDA(user.publicKey));
            console.log("selectedUser => ", selectedUser.matchCount)

            console.log("------------------------Create Match------------------------");

            {
                const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
                const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
                const sendLibraryInfo = await getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);
                const ulnPdaDeriver = new UlnPDADeriver(sendLibraryProgram);
                let sendConfig = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];
                let defaultSendConfig = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0]; //until here
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
                const sellAmount = new BN(100000)
                const buyAmount = new BN(10000)
                const sourceTokenAddressInArbitrumChain = Array(40).fill(0); //have to input arbitrum wallet address of user
                const messageToSend = selectedUser.matchCount.toString(16) //2
                    + mint.toString() // 32
                    + sellAmount.toString(16).padStart(32, '0') // 32
                    + usdCoinMintAddress.toString() //32
                    + buyAmount.toString(16).padStart(32, '0') //32
                    + Buffer.from(sourceTokenAddressInArbitrumChain) //40

                const additionalComputeBudgetInstruction =
                    anchor.web3.ComputeBudgetProgram.requestUnits({
                        units: 800000,
                        additionalFee: 0,
                    });

                let tx = new Transaction();
                tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 2000000 }))

                let instruction = await program.methods.createMatch({
                    sourceSellAmount: sellAmount,
                    destTokenMint: usdCoinMintAddress,
                    destBuyAmount: buyAmount,
                    eid: arbitrumEID,
                    tristeroOappBump: getTristeroOappBump(),
                    sourceTokenAddressInArbitrumChain: sourceTokenAddressInArbitrumChain
                })
                    .accounts({
                        authority: user.publicKey,
                        adminPanel: getAdminPanel(),
                        tokenMint: mint,
                        tokenAccount: tokenAccount,
                        stakingAccount: getStakingPanel(mint),
                        user: getUserPDA(user.publicKey),
                        tradeMatch: getTradeMatchPDA(user.publicKey, selectedUser.matchCount),
                        tokenProgram: TOKEN_PROGRAM_ID,
                        systemProgram: SystemProgram.programId
                    })
                    .remainingAccounts(sendInstructionRemainingAccounts)
                    .instruction();
                tx.add(instruction)
                const createMatchTx = await sendAndConfirmTransaction(connection, tx, [user])

                console.log("createMatchTx = ", createMatchTx)
            }

            console.log("------------------------Cancel Match------------------------");

            {
                const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
                const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
                const sendLibraryInfo = await getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);
                const ulnPdaDeriver = new UlnPDADeriver(sendLibraryProgram);
                let sendConfig = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];
                let defaultSendConfig = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0]; //until here
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
                const sellAmount = new BN(100000)
                const buyAmount = new BN(10000)
                const sourceTokenAddressInArbitrumChain = Array(40).fill(0); //have to input arbitrum wallet address of user
                const messageToSend = selectedUser.matchCount.toString(16) //2
                    + mint.toString() // 32
                    + sellAmount.toString(16).padStart(32, '0') // 32
                    + usdCoinMintAddress.toString() //32
                    + buyAmount.toString(16).padStart(32, '0') //32
                    + Buffer.from(sourceTokenAddressInArbitrumChain) //40

                const additionalComputeBudgetInstruction =
                    anchor.web3.ComputeBudgetProgram.requestUnits({
                        units: 800000,
                        additionalFee: 0,
                    });

                let tx = new Transaction();
                tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 2000000 }))

                let instruction = await program.methods.cancelMatch({
                    matchId: selectedUser.matchCount,
                    tristeroOappBump: getTristeroOappBump(),
                })
                    .accounts({
                        authority: user.publicKey,
                        adminPanel: getAdminPanel(),
                        tokenMint: mint,
                        tokenAccount: tokenAccount,
                        stakingAccount: getStakingPanel(mint),
                        user: getUserPDA(user.publicKey),
                        tradeMatch: getTradeMatchPDA(user.publicKey, selectedUser.matchCount),
                        tokenProgram: TOKEN_PROGRAM_ID,
                        systemProgram: SystemProgram.programId
                    })
                    .remainingAccounts(sendInstructionRemainingAccounts)
                    .instruction();
                tx.add(instruction)
                const createMatchTx = await sendAndConfirmTransaction(connection, tx, [user])

                console.log("cancelMatchTx = ", createMatchTx)
            }

        } catch (err) {
            console.log(err)
        }
    })
});

const subscriptionId = endpointProgram.addEventListener("LzReceiveAlertEvent", async (event) => {
    const swapParams = {
        receiver: event.receiver,
        executor: event.executor,
        srcEid: event.srcEid,
        sender: event.sender,
        nonce: event.nonce,
        guid: event.guid,
        computeUnits: event.computeUnits,
        value: event.value,
        message: event.message,
        extraData: event.extraData,
        reason: event.reason,
    }
    // message: matchId(2), 
    const messageStr = event.message.toString();
    const tradeMatchId = parseInt(messageStr.slice(0, 2), 16)
    const destTokenAccount = messageStr.slice(2)
    const tradeMatch = await program.account.tradeMatch.fetch(getTradeMatchPDA(event.receiver, tradeMatchId))
    const swapTokenTx = await program.methods.swapToken(swapParams)
        .accounts({
            adminPanel: getAdminPanel(),
            tokenMint: tradeMatch.sourceTokenMint,
            tokenAccount: new PublicKey(destTokenAccount),
            endpoint: getEndpointPDA(event.srcEid),
            stakingAccount: getStakingPanel(tradeMatch.sourceTokenMint),
            tokenProgram: TOKEN_PROGRAM_ID,
            systemProgram: SystemProgram.programId,
            tradeMatch: getTradeMatchPDA(event.receiver, tradeMatchId),
            user: getUserPDA(event.receiver),
            payloadHash: getPayloadHashPDA(event.receiver, event.srcEid, event.sender, event.nonce)
        })
        .rpc();

    console.log("swapTokenTx = ", swapTokenTx);
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

const getTristeroOappBump = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("TristeroOapp")],
        programId,
    )[1]
}

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

const getNoncePDA = (senderKey: PublicKey, eid: number, receiver: Buffer) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(NONCE_SEED), senderKey.toBytes(), new BN(eid).toBuffer("be", 4), receiver],
        endpoint,
    )[0]
}

const getPendingInboundNoncePDA = (senderKey: PublicKey, eid: number, receiver: Buffer) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PENDING_NONCE_SEED), senderKey.toBytes(), new BN(eid).toBuffer("be", 4), receiver],
        endpoint,
    )[0]
}

const getAdminPanel = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("admin_panel")],
        programId,
    )[0]
}

const getStakingPanel = (mint: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("staking_account"), mint.toBuffer()],
        programId,
    )[0]
}

const getUserPDA = (authority: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("user"), authority.toBytes()],
        programId,
    )[0]
}

const getTradeMatchPDA = (authority: PublicKey, matchCount: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("trade_match"), authority.toBuffer(), new BN(matchCount).toBuffer("be", 1)],
        programId,
    )[0]
}

const getPayloadHashPDA = (receiver: PublicKey, srcEid: number, sender: number[], nonce: BN) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PAYLOAD_HASH_SEED), receiver.toBuffer(), new BN(srcEid).toBuffer("be", 4), Buffer.from(sender), nonce.toBuffer("be", 8)],
        programId,
    )[0]
}