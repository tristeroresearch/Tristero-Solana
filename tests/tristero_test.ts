import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { getExecutorProgramId, simulateTransaction, ExecutorPDADeriver, getBlockedMessageLibProgramId, OAPP_SEED, getProgramKeypair, oappIDPDA, OftPDADeriver, OftTools, OPTIONS_SEED, SEND_LIBRARY_CONFIG_SEED, NONCE_SEED, ENDPOINT_SEED, EndpointProgram, MESSAGE_LIB_SEED, SupportedPrograms, getEndpointProgramId, EventPDADeriver, BaseOApp, getSimpleMessageLibProgramId, RECEIVE_LIBRARY_CONFIG_SEED, PENDING_NONCE_SEED, UlnProgram, getULNProgramId, UlnPDADeriver, getDVNProgramId, ULN_SEED, SEND_CONFIG_SEED, ULN_CONFIG_SEED, getPricefeedProgramId, PriceFeedPDADeriver, PRICE_FEED_SEED, EXECUTOR_CONFIG_SEED, DVNDeriver, PAYLOAD_HASH_SEED, messageLibs, SimpleMessageLibProgram, RECEIVE_CONFIG_SEED } from "@layerzerolabs/lz-solana-sdk-v2";
import { Options } from "@layerzerolabs/lz-v2-utilities";
import { ChainKey, EndpointVersion, networkToEndpointId } from '@layerzerolabs/lz-definitions';

import { PublicKey, SystemProgram, Keypair, LAMPORTS_PER_SOL, sendAndConfirmTransaction, Transaction, ComputeBudgetProgram } from "@solana/web3.js"
import { TOKEN_PROGRAM_ID, createAssociatedTokenAccount, createMint, getOrCreateAssociatedTokenAccount, mintTo } from '@solana/spl-token'
import { Tristero } from "../target/types/tristero";
import { Endpoint, IDL } from '../target/types/endpoint';
import fs from 'fs';
import { describe } from "node:test";
import { bs58 } from "@coral-xyz/anchor/dist/cjs/utils/bytes";
import { userInfo } from "os";

import userJson from "./user.json"
import otherJson from "./other.json"
import adminJson from "./adminJson.json"
import otherUserJson from "./another_user.json"
import { min } from "bn.js";
// arbitrum: 0x5C105836fAa55A42957D2cC1b86e880fdE998E81
anchor.AnchorProvider

const DEFAULT_MESSAGE_LIB: PublicKey = PublicKey.default;

// Configure the client to use the local cluster.
anchor.setProvider(anchor.AnchorProvider.env());

// const program = anchor.workspace.Tristero as Program<Tristero>;
const program = anchor.workspace.Tristero as Program<Tristero>;

// const simpleMessageLibProgram = anchor.workspace.SimpleMessagelib as Program<SimpleMessagelib>
// const endpointProgram = anchor.workspace.Endpoint as Program<Endpoint>

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
const anotherUser = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(otherJson))
const admin = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(adminJson))
// const receiverPubKey = Buffer.alloc(32, 0);
// const paddedBuffer = Buffer.from('20eda7b413e525ccff9ffba610f5c4b8e189eb53', 'hex') // have to change to arbitrum side
// const paddedBuffer = Buffer.from('5F2D12ab071Bd20b25a031FED5dCe1ABDBB9f8A8', 'hex')
// paddedBuffer.copy(Uint8Array.from(receiverPubKey), 12);
// console.log("receiverPubKey => ", receiverPubKey.toString())
const receiverPubKey = Buffer.from('0000000000000000000000005f2d12ab071bd20b25a031fed5dce1abdbb9f8a8', 'hex')

const tempStr = Buffer.from('000000000000000000000000000000000000000000000000000000000000005183247218e466e48b0ea8b8a7b99e7a53cc8153766c6ac5c88076290adee38d513b442cb3912157f13a933d0134282d032b5ffecd01a2dbf1b7790608df002ea70000000000000000000000005f2d12ab071bd20b25a031fed5dce1abdbb9f8a8', "hex")

const arbitrumEID = 40231; // Here is for Arbitrum Sepolia Testnet
//const arbitrumEID = 30110;

const options = Options.newOptions().addExecutorLzReceiveOption(500000, 0);
console.log("options => ", options.toHex(), " => ", options.toBytes());

describe("# test scenario - tristero ", () => {

    console.log("endpoint program id = ", endpoint);


    it("testing", async () => {
        console.log(">>> programId : ", programId);
        console.log("begin");

        try {
            anchor.setProvider(anchor.AnchorProvider.env());

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

            const tristeroOappPubkey = getTristeroOapp();
            const endpointEventPdaDeriver = new EventPDADeriver(endpoint)
            const ulnEventPdaDeriver = new EventPDADeriver(sendLibraryProgram)

            console.log("------------------------Register New Oapp------------------------");

            // console.log("user.publickey ===> ", user.publicKey.toString())
            // console.log("tristeroOAppPubkey => ", tristeroOappPubkey.toString())

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

            // const txRegisterOapp = await program.methods.registerTristeroOapp(registerTristeroOAppParams)
            //     .accounts({
            //         payer: user.publicKey,
            //         oapp: tristeroOappPubkey,
            //         oappRegistry: getOappPDA(tristeroOappPubkey),
            //         endpointProgram: endpoint,
            //         eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            //     })
            //     .signers([user])
            //     .rpc();

            // console.log("txRegisterOapp = " + txRegisterOapp);

            console.log("------------------------------------------------------")


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
            //     const txInitSendLibrary = await sendAndConfirmTransaction(connection, transaction, [user])
            //     console.log("txInitSendLibrary = ", txInitSendLibrary)
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

            // console.log("-------------------Init Nonce-----------------------------")
            // {
            //     const non = getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey);
            //     console.log("non => ", non);
            //     const initNonceAccounts = {
            //         delegate: admin.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
            //         nonce: non,
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
            //     const txInitNonce = await sendAndConfirmTransaction(connection, _transaction, [admin])
            //     console.log("txInitNonce = ", txInitNonce)
            //     console.log("-------------------------------------------------------------------------------")
            // }

            const messageLib = getMessageLibPDA();
            console.log("-------------------Init Message Lib-----------------------------")
            // {
            //     const initMessageLibAccounts = {
            //         payer: user.publicKey,
            //         messageLib: messageLib,
            //         systemProgram: SystemProgram.programId
            //     }

            //     const initMessageLibParams = {
            //             eid: arbitrumEID,
            //             endpoint: getEndpointPDA(),
            //             endpointProgram: EndpointProgram.PROGRAM_ID,
            //             admin: user.publicKey,
            //             fee: new BN(25000),
            //             lzTokenFee: new BN(0)
            //     }

            //     console.log("simpleMessageLibProgramId: ", simpleMessageLibProgram.programId.toString())

            //     const initMessagelibTx = await simpleMessageLibProgram.methods.initMessageLib(initMessageLibParams)
            //                                                             .accounts(initMessageLibAccounts)
            //                                                             .signers([user])
            //                                                             .rpc();

            //     console.log("initMessagelibTx = ", initMessagelibTx)
            //     console.log("-----------------------------------------------------------------------------")

            // }

            console.log("-------------------Init Config-----------------------------")
            // {
            //     const anchorRemainingAccounts = [
            //         { //1
            //             pubkey: user.publicKey,
            //             isSigner: true,
            //             isWritable: true
            //         },
            //         { //2
            //             pubkey: messageLib,
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //3
            //             pubkey: sendConfigPDA(arbitrumEID, tristeroOappPubkey),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //4
            //             pubkey: receiveConfigPDA(arbitrumEID, tristeroOappPubkey),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //5
            //             pubkey: SystemProgram.programId,
            //             isSigner: false,
            //             isWritable: false
            //         },
            //     ]
            //     const initConfigAccounts = {
            //         delegate: user.publicKey,
            //         oappRegistry: getOappPDA(tristeroOappPubkey),
            //         messageLibInfo: getMessageLibInfoPDA(messageLib),
            //         messageLib: messageLib,
            //         messageLibProgram: ulnProgramId,
            //         anchorRemainingAccounts: anchorRemainingAccounts
            //     }

            //     const initConfigRemainAccounts = [
            //         { //1
            //             pubkey: user.publicKey,
            //             isSigner: true,
            //             isWritable: true
            //         },
            //         { //2
            //             pubkey: getOappPDA(tristeroOappPubkey),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //3
            //             pubkey: getMessageLibInfoPDA(messageLib),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //4
            //             pubkey: messageLib,
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //5
            //             pubkey: ulnProgramId,
            //             isSigner: false,
            //             isWritable: false,
            //         },
            //         { //6
            //             pubkey: getMessageLibInfoPDA(messageLib),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //     ]

            //     const initConfigParams = {
            //         params: {
            //             oapp: tristeroOappPubkey,
            //             eid: arbitrumEID
            //         }
            //     }

            //     const initConfigInstruction = EndpointProgram.instructions.createInitConfigInstruction(initConfigAccounts, initConfigParams)

            //     console.log("initConfig well done")
            //     const transInitConfig = new Transaction().add(initConfigInstruction);
            //     const initConfigTx = await sendAndConfirmTransaction(connection, transInitConfig, [user])
            //     console.log("initConfigTx = ", initConfigTx)
            //     console.log("-------------------------------------------------------------------------------")
            // }

            console.log("-------------------Set Receive Library-----------------------------")
            // {
            //     const setReceiveLibraryAccounts = {
            //         signer: user.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
            //         receiveLibraryConfig: getReceiveLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
            //         messageLibInfo: getMessageLibInfoPDA(messageLib),
            //         eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            //         program: EndpointProgram.PROGRAM_ID
            //     }

            //     const setReceiveLibraryParams = {
            //         params: {
            //             receiver: tristeroOappPubkey,
            //             eid: arbitrumEID,
            //             newLib: messageLib,
            //             gracePeriod: 0,
            //         }
            //     }

            //     const setReceiveLibraryInstruction = EndpointProgram.instructions.createSetReceiveLibraryInstruction(setReceiveLibraryAccounts, setReceiveLibraryParams)
            //     const setReceiveTrans = new Transaction().add(setReceiveLibraryInstruction);
            //     const setReceiveTx = await sendAndConfirmTransaction(connection, setReceiveTrans, [user])
            //     console.log("SetReceiveLibraryTx = ", setReceiveTx)
            // }

            console.log("-------------------Set Send Library-----------------------------")
            // {
            //     const setSendLibraryAccounts = {
            //         signer: user.publicKey,
            //         oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
            //         sendLibraryConfig: getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
            //         messageLibInfo: getMessageLibInfoPDA(messageLib),
            //         eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            //         program: EndpointProgram.PROGRAM_ID
            //     }

            //     const setSendLibraryParams = {
            //         params: {
            //             sender: tristeroOappPubkey,
            //             eid: arbitrumEID,
            //             newLib: messageLib,
            //             gracePeriod: 0,
            //         }
            //     }

            //     const setSendLibraryInstruction = EndpointProgram.instructions.createSetSendLibraryInstruction(setSendLibraryAccounts, setSendLibraryParams)
            //     const setSendTrans = new Transaction().add(setSendLibraryInstruction);
            //     const setSendTx = await sendAndConfirmTransaction(connection, setSendTrans, [user])
            //     console.log("SetSendLibraryTx = ", setSendTx)
            // }

            console.log("-------------------------Set Config-----------------------------")
            // {
            //     const setConfigRemainingAccounts = [
            //         { //2
            //             pubkey: getUlnPDA(),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //3
            //             pubkey: sendConfigPDA(arbitrumEID, tristeroOappPubkey),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //4
            //             pubkey: receiveConfigPDA(arbitrumEID, tristeroOappPubkey),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //5
            //             pubkey: getDefaultSendConfig(arbitrumEID),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //6
            //             pubkey: getDefaultReceiveConfig(arbitrumEID),
            //             isSigner: false,
            //             isWritable: false
            //         },
            //         { //7
            //             pubkey: ulnEventPdaDeriver.eventAuthority()[0],
            //             isSigner: false,
            //             isWritable: false,
            //         },
            //         { //8
            //             pubkey: ulnProgramId,
            //             isSigner: false,
            //             isWritable: false,
            //         }
            //     ]
            //     console.log("setConfigRemainingAccounts: ", JSON.stringify(setConfigRemainingAccounts))
            //     const setConfigAccounts = {
            //         signer: user.publicKey,
            //         oappRegistry: getOappPDA(tristeroOappPubkey),
            //         messageLibInfo: getMessageLibInfoPDA(messageLib),
            //         messageLib: messageLib,
            //         messageLibProgram: ulnProgramId,
            //         anchorRemainingAccounts: setConfigRemainingAccounts
            //     }

            // //     const executorConfig = UlnProgram.executorConfigBeet.serialize({
            // //         executor: PublicKey.findProgramAddressSync(
            // //             [Buffer.from(EXECUTOR_CONFIG_SEED, 'utf8')],
            // //             executorProgramId,
            // //         )[0],
            // //         maxMessageSize: 10000,
            // //     })[0];

            // //     const setConfigExecutorParams = {
            // //         params: {
            // //             oapp: tristeroOappPubkey,
            // //             eid: arbitrumEID,
            // //             configType: OftTools.ConfigType.Executor,
            // //             config: executorConfig,
            // //         }
            // //     }

            //     const ulnReceiveConfig = UlnProgram.types.ulnConfigBeet.serialize({
            //         confirmations: 10,
            //         requiredDvnCount: 1,
            //         optionalDvnCount: 0,
            //         optionalDvnThreshold: 0,
            //         requiredDvns: [new PublicKey("4VDjp6XQaxoZf5RGwiPU9NR1EXSZn2TP4ATMmiSzLfhb")].sort(),
            //         optionalDvns: [].sort(),
            //       })[0];

            //     const setConfigReceiveParams = {
            //         params: {
            //             oapp: tristeroOappPubkey,
            //             eid: arbitrumEID,
            //             configType: OftTools.ConfigType.ReceiveUln,
            //             config: ulnReceiveConfig,
            //         }
            //     }

            // //     const setConfigExecutorInstruction = EndpointProgram.instructions.createSetConfigInstruction(setConfigAccounts, setConfigExecutorParams)
            //     const setConfigReceiveInstruction = EndpointProgram.instructions.createSetConfigInstruction(setConfigAccounts, setConfigReceiveParams)

            // //     console.log("setConfig well done")
            // //     const transSetConfigExecutor = new Transaction().add(setConfigExecutorInstruction);
            //     const transSetConfigReceive = new Transaction().add(setConfigReceiveInstruction);
            // //     const setConfigExecutorTx = await sendAndConfirmTransaction(connection, transSetConfigExecutor, [user])
            // //     console.log("setConfigExecutorTx = ", setConfigExecutorTx)
            //     const setConfigReceiveTx = await sendAndConfirmTransaction(connection, transSetConfigReceive, [user])
            //     console.log("setConfigReceiveTx = ", setConfigReceiveTx)
            //     console.log("-------------------------------------------------------------------------------")
            // }

            
            console.log("------------------------------mint new spl token(only need in localnet)-------------------------------------------------");
            // const mint = await createMint(
            //     connection,
            //     user,
            //     user.publicKey,
            //     null,
            //     5 // Decimals
            // )
            const mint = new PublicKey("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU")

            console.log("Mint Address: ", mint.toBase58());

            // Create a token account for the mint
            // const tokenAccount = (await getOrCreateAssociatedTokenAccount(
            //     connection,
            //     user,
            //     mint,
            //     user.publicKey
            // )).address;

            const tokenAccount = new PublicKey("6RzJ96TziaKHitum3KW5524D6GbvqqYJAeaNfQyicmEx")

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

            const usdCoinMintAddress = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU" // dest Token Mint Address
            const numberArray: number[] = [];
            for (let i = 0; i < usdCoinMintAddress.length; i++) {
                const hexChar = usdCoinMintAddress[i];
                const num = parseInt(hexChar, 16);
                numberArray.push(num);
            }


            console.log("-----------------------Init Oft-Config------------------------------");
            // {
            //     const initOftTx = await program.methods.registerConfig().accounts({
            //         payer: user.publicKey,
            //         oappConfig: tristeroOappPubkey,
            //         lzReceiveTypesAccounts: getLzReceiveTypesPDA(tristeroOappPubkey),
            //         systemProgram: SystemProgram.programId
            //     })
            //     .signers([user])
            //     .rpc();
            //     console.log("initOftTx: ", initOftTx);
            // }

            // const adminPanel = await program.account.adminPanel.fetch(getAdminPanel());
            // console.log("orderId => ", adminPanel.orderCount)
            // console.log("orderPDA => ", getOrderPDA(adminPanel.orderCount))
            // const erc20Addr = Buffer.from('75faf114eafb1bdbe2f0316df893fd58ce46aa4d', 'hex')
            // const arbWalletAddr = Buffer.from('De7014167c36c39aAfb56aA0Bd87776d8911369A', 'hex')
            console.log("------------------------Place Order----------------------------");
            // {
            //     const placeOrderTx = await program.methods.placeOrder({
            //             sourceSellAmount: new BN(100),
            //             minSellAmount: new BN(10),
            //             destTokenMint: Array.from(erc20Addr),
            //             destBuyAmount: new BN(100),
            //             eid: arbitrumEID,
            //             orderId: adminPanel.orderCount
            //         })
            //         .accounts({
            //             authority: user.publicKey,
            //             adminPanel: getAdminPanel(),
            //             solPanel: getSolPanel(),
            //             tokenMint: mint,
            //             tokenAccount: tokenAccount,
            //             stakingAccount: getStakingPanel(mint),
            //             order: getOrderPDA(adminPanel.orderCount),
            //             systemProgram: SystemProgram.programId,
            //             tokenProgram: TOKEN_PROGRAM_ID
            //         })
            //         .signers([user])
            //         .rpc();
            //     console.log("placeOrderTx: ", placeOrderTx)
            //     console.log("orderId: ", adminPanel.orderCount)
            // }

            console.log("------------------------Create Match1------------------------------");
            // {
            //     const createMatchTx = await program.methods.createMatch({
            //             srcIndex: new BN(12),
            //             dstIndex: new BN(1),
            //             srcQuantity: new BN(90),
            //             dstQuantity: new BN(90),
            //             tradeMatchId: adminPanel.matchCount,
            //             arbSourceTokenAddr: Array.from(arbWalletAddr)
            //         })
            //         .accounts({
            //             authority: admin.publicKey,
            //             adminPanel: getAdminPanel(),
            //             order: getOrderPDA(new BN(12)),
            //             tradeMatch: getTradeMatchPDA(adminPanel.matchCount),
            //             systemProgram: SystemProgram.programId,
            //             tokenProgram: TOKEN_PROGRAM_ID
            //         })
            //         .signers([admin])
            //         .rpc();
            //     console.log("createMatchTx: ", createMatchTx)
            // }

            // const challengeId = adminPanel.matchCount;
            // adminPanel.matchCount = new BN(adminPanel.matchCount.toNumber() + 1);

            // console.log("------------------------Create Match2------------------------------");
            // // {
            // //     const createMatchTx = await program.methods.createMatch({
            // //             srcIndex: new BN(74),
            // //             dstIndex: new BN(1),
            // //             srcQuantity: new BN(90),
            // //             dstQuantity: new BN(90),
            // //             tradeMatchId: adminPanel.matchCount,
            // //             arbSourceTokenAddr: Array.from(arbWalletAddr)
            // //         })
            // //         .accounts({
            // //             authority: user.publicKey,
            // //             adminPanel: getAdminPanel(),
            // //             order: getOrderPDA(new BN(74)),
            // //             tradeMatch: getTradeMatchPDA(adminPanel.matchCount),
            // //             systemProgram: SystemProgram.programId,
            // //             tokenProgram: TOKEN_PROGRAM_ID
            // //         })
            // //         .signers([user])
            // //         .rpc();
            // //     console.log("createMatchTx: ", createMatchTx)
            // // }

            // const sendStoredId = adminPanel.matchCount;

            // const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
            // const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
            // console.log(sendLibraryConfig, " ", defaultSendLibraryConfig);
            // const sendLibraryInfo = await getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);
            // console.log("sendLibraryInfo: ", sendLibraryInfo)

            console.log("------------------------Challenge------------------------");
            // {
            //     const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
            //     const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
            //     console.log(sendLibraryConfig, " ", defaultSendLibraryConfig);
            //     const sendLibraryInfo = await getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);
            //     const ulnPdaDeriver = new UlnPDADeriver(sendLibraryProgram);
            //     let sendConfig = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];
            //     let defaultSendConfig = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0]; //until here
            //     const sendInstructionRemainingAccounts = [
            //         { //0
            //             pubkey: endpoint,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //1
            //             pubkey: tristeroOappPubkey,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //2
            //             pubkey: sendLibraryProgram,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //3
            //             pubkey: sendLibraryConfig,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //4
            //             pubkey: defaultSendLibraryConfig,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //5
            //             pubkey: sendLibraryInfo,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //6
            //             pubkey: getEndpointPDA(),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //7
            //             pubkey: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //8
            //             pubkey: endpointEventPdaDeriver.eventAuthority()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //9
            //             pubkey: endpoint,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //10
            //             pubkey: getUlnPDA(),
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //11
            //             pubkey: sendConfig,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //12
            //             pubkey: defaultSendConfig,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //13
            //             pubkey: user.publicKey,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //14
            //             pubkey: user.publicKey,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //15
            //             pubkey: SystemProgram.programId,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //16
            //             pubkey: ulnEventPdaDeriver.eventAuthority()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //17
            //             pubkey: sendLibraryProgram,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //18
            //             pubkey: executorProgramId,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //19
            //             pubkey: new ExecutorPDADeriver(executorProgramId).config()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //20
            //             pubkey: priceFeeProgramId,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //21
            //             pubkey: new PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //22
            //             pubkey: dvnProgramId,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //23
            //             pubkey: new DVNDeriver(dvnProgramId).config()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //24
            //             pubkey: priceFeeProgramId,
            //             isSigner: false,
            //             isWritable: true
            //         },
            //         { //25
            //             pubkey: new PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
            //             isSigner: false,
            //             isWritable: true
            //         },
            //     ]

            //     console.log("sendInstructionRemainingAcc => ", JSON.stringify(sendInstructionRemainingAccounts))

            //     const sellAmount = new BN(100000)
            //     const buyAmount = new BN(10000)
            //     const sourceTokenAddressInArbitrumChain = Array(20).fill(0); //have to input arbitrum wallet address of user

            //     const additionalComputeBudgetInstruction =
            //         anchor.web3.ComputeBudgetProgram.requestUnits({
            //             units: 800000,
            //             additionalFee: 0,
            //         });

            //     let tx = new Transaction();
            //     tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 2000000 }))

            //     let instruction = await program.methods.challenge({
            //         tradeMatchId: challengeId,
            //         tristeroOappBump: getTristeroOappBump(),
            //         sourceTokenAddressInArbitrumChain: Array.from(arbWalletAddr),
            //         receiver: Array.from(receiverPubKey)
            //     })
            //         .accounts({
            //             authority: user.publicKey,
            //             adminPanel: getAdminPanel(),
            //             tradeMatch: getTradeMatchPDA(challengeId),
            //             tokenProgram: TOKEN_PROGRAM_ID,
            //             systemProgram: SystemProgram.programId
            //         })
            //         .remainingAccounts(sendInstructionRemainingAccounts)
            //         .signers([user])
            //         .instruction();

            //     tx.add(instruction)
            //     const challengeTx = await sendAndConfirmTransaction(connection, tx, [user])

            //     console.log("trade_match_id = ", challengeId)
            //     console.log("challengeTx = ", challengeTx)
            // }

            const res = await EndpointProgram.accounts.SendLibraryConfig.fromAccountAddress(connection, (await getDefaultSendLibraryConfig(arbitrumEID)))
            

            console.log("--------testing lz_receive_types ---------");
            {
                let lzReceiveTypesIx = await program.methods.lzReceiveTypes({
                    srcEid: arbitrumEID,
                    sender: Array.from(receiverPubKey),
                    nonce: new BN(4),
                    guid: Array.from(receiverPubKey),
                    message: tempStr,
                    extraData: Buffer.from("")
                })
                .accounts({
                    messageLib: res.messageLib,
                    oftConfig: PublicKey.default
                })
                .view();
                
                // let tx = new Transaction();
                // tx.add(ComputeBudgetProgram.setComputeUnitLimit({units: 500000}));
                // tx.add(lzReceiveTypesIx)

                // const lzReceiveTypesTx = await sendAndConfirmTransaction(connection, tx, [user])
                console.log("lzReceiveTypesIx: ", lzReceiveTypesIx)
                console.log("length => ", lzReceiveTypesIx.length)

                console.log("=> ", JSON.stringify({
                    oapp: lzReceiveTypesIx[0].pubkey,
                    tokenAccount: lzReceiveTypesIx[1].pubkey,
                    stakingAccount: lzReceiveTypesIx[2].pubkey,
                    tradeMatch: lzReceiveTypesIx[3].pubkey,
                    tokenProgram: lzReceiveTypesIx[4].pubkey
                }))

                let lzReceiveTypesTx = await program.methods.lzReceive({
                    srcEid: arbitrumEID,
                    sender: Array.from(receiverPubKey),
                    nonce: new BN(4),
                    guid: Array.from(receiverPubKey),
                    message: tempStr,
                    extraData: Buffer.from("")
                })
                .accounts({
                    oapp: lzReceiveTypesIx[0].pubkey,
                    tokenAccount: lzReceiveTypesIx[1].pubkey,
                    stakingAccount: lzReceiveTypesIx[2].pubkey,
                    tradeMatch: lzReceiveTypesIx[3].pubkey,
                    tokenProgram: lzReceiveTypesIx[4].pubkey
                })
                .remainingAccounts(lzReceiveTypesIx.slice(5))
                .rpc();
                console.log("lzReceiveTypesTx: ", lzReceiveTypesTx)
            }
            
        } catch (err) {
            console.log(err)
        }
    })
});

console.log("EndpointProgram ----> ", EndpointProgram.PROGRAM_ID)
console.log("UlnProgram ----> ", UlnProgram.PROGRAM_ID)

const getOrderPDA = (orderId: BN) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("order"), orderId.toBuffer("be", 8)],
        program.programId
    )[0]
}

const getRefundTokenAccountPDA = (pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("refund_account"), pubkey.toBuffer()],
        programId,
    )[0]
}

const sendConfigPDA = (eid: number, pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_CONFIG_SEED), new BN(eid).toBuffer("be", 4), pubkey.toBuffer()],
        ulnProgramId,
    )[0]
}

const getLzReceiveTypesPDA = (oappConfig: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("LzReceiveTypes"), oappConfig.toBuffer()],
        program.programId
    )[0]
}

const getSolPanel = () => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("sol_treasury")],
        program.programId
    )[0]
}

const receiveConfigPDA = (eid: number, pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(RECEIVE_CONFIG_SEED), new BN(eid).toBuffer("be", 4), pubkey.toBuffer()],
        ulnProgramId,
    )[0]
}

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
        ulnProgramId,
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

const getDefaultSendConfig = (eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_CONFIG_SEED), new BN(eid).toBuffer("be", 4)],
        ulnProgramId,
    )[0]
}

const getDefaultReceiveConfig = (eid: number) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(RECEIVE_CONFIG_SEED), new BN(eid).toBuffer("be", 4)],
        ulnProgramId,
    )[0]
}

const getSendLibraryInfoPDA = async (sendLibraryConfig: PublicKey, defaultSendLibraryConfig: PublicKey) => {
    const res = await EndpointProgram.accounts.SendLibraryConfig.fromAccountAddress(connection, defaultSendLibraryConfig);

    return PublicKey.findProgramAddressSync(
        [Buffer.from(MESSAGE_LIB_SEED), res.messageLib.toBuffer()],
        endpoint,
    )[0]
}

const getEndpointPDA = () => {
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

const getTradeMatchPDA = (matchCount: BN) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from("trade_match"), matchCount.toBuffer("be", 8)],
        programId,
    )[0]
}

const getPayloadHashPDA = (receiver: PublicKey, srcEid: number, sender: number[], nonce: BN) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PAYLOAD_HASH_SEED), receiver.toBuffer(), new BN(srcEid).toBuffer("be", 4), Buffer.from(sender), nonce.toBuffer("be", 8)],
        programId,
    )[0]
}

function hexToUint8Array(hex: string): Uint8Array {
    if (hex.length % 2 !== 0) {
        throw new Error("Hex string must have an even length");
    }
    const uint8Array = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        uint8Array[i / 2] = parseInt(hex.substr(i, 2), 16);
    }
    return uint8Array;
}