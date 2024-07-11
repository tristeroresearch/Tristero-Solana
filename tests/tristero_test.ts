import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { getExecutorProgramId, ExecutorPDADeriver, getBlockedMessageLibProgramId, OAPP_SEED, getProgramKeypair, oappIDPDA, OftPDADeriver, OftTools, OPTIONS_SEED, SEND_LIBRARY_CONFIG_SEED, NONCE_SEED, ENDPOINT_SEED, EndpointProgram, MESSAGE_LIB_SEED, SupportedPrograms, getEndpointProgramId, EventPDADeriver, BaseOApp, getSimpleMessageLibProgramId, RECEIVE_LIBRARY_CONFIG_SEED, PENDING_NONCE_SEED, UlnProgram, getULNProgramId, UlnPDADeriver, getDVNProgramId, ULN_SEED, SEND_CONFIG_SEED, ULN_CONFIG_SEED, getPricefeedProgramId, PriceFeedPDADeriver, PRICE_FEED_SEED, EXECUTOR_CONFIG_SEED, DVNDeriver, PAYLOAD_HASH_SEED, messageLibs, SimpleMessageLibProgram, RECEIVE_CONFIG_SEED } from "@layerzerolabs/lz-solana-sdk-v2";
import { Options } from "@layerzerolabs/lz-v2-utilities";
import { ChainKey, EndpointVersion, networkToEndpointId } from '@layerzerolabs/lz-definitions';

import { PublicKey, SystemProgram, Keypair, LAMPORTS_PER_SOL, sendAndConfirmTransaction, Transaction, ComputeBudgetProgram } from "@solana/web3.js"
import { TOKEN_PROGRAM_ID, createMint, getOrCreateAssociatedTokenAccount, mintTo } from '@solana/spl-token'
import { Tristero } from "../target/types/tristero";
import { Endpoint, IDL } from '../target/types/endpoint';
import fs from 'fs';
import { describe } from "node:test";
import { bs58 } from "@coral-xyz/anchor/dist/cjs/utils/bytes";
import { userInfo } from "os";

import userJson from "./user.json"
import otherJson from "./other.json"
import adminJson from "./adminJson.json"
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
const otherUser = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(otherJson))
const admin = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(adminJson))
const receiverPubKey = Buffer.alloc(32, 0);
// const paddedBuffer = Buffer.from('20eda7b413e525ccff9ffba610f5c4b8e189eb53', 'hex') // have to change to arbitrum side
const paddedBuffer = Buffer.from('c07d42d6f46f4C4228f9901788456a05EBDfd9DB', 'hex')
paddedBuffer.copy(receiverPubKey, 12);
console.log("receiverPubKey => ", receiverPubKey)
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
            const ulnEventPdaDeriver = new EventPDADeriver(sendLibraryProgram)

            console.log("------------------------Register New Oapp------------------------");

            // console.log("user.publickey ===> ", user.publicKey.toString())

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
            //         // systemProgram: SystemProgram.programId,
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
            //     const txInitNonce = await sendAndConfirmTransaction(connection, _transaction, [user])
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
            //             endpoint: getEndpointPDA(arbitrumEID),
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
            {
                const setConfigRemainingAccounts = [
                    { //2
                        pubkey: getUlnPDA(),
                        isSigner: false,
                        isWritable: false
                    },
                    { //3
                        pubkey: sendConfigPDA(arbitrumEID, tristeroOappPubkey),
                        isSigner: false,
                        isWritable: true
                    },
                    { //4
                        pubkey: receiveConfigPDA(arbitrumEID, tristeroOappPubkey),
                        isSigner: false,
                        isWritable: true
                    },
                    { //5
                        pubkey: getDefaultSendConfig(arbitrumEID),
                        isSigner: false,
                        isWritable: false
                    },
                    { //6
                        pubkey: getDefaultReceiveConfig(arbitrumEID),
                        isSigner: false,
                        isWritable: false
                    },
                    { //7
                        pubkey: ulnEventPdaDeriver.eventAuthority()[0],
                        isSigner: false,
                        isWritable: false,
                    },
                    { //8
                        pubkey: ulnProgramId,
                        isSigner: false,
                        isWritable: false,
                    }
                ]
                console.log("setConfigRemainingAccounts: ", JSON.stringify(setConfigRemainingAccounts))
                const setConfigAccounts = {
                    signer: user.publicKey,
                    oappRegistry: getOappPDA(tristeroOappPubkey),
                    messageLibInfo: getMessageLibInfoPDA(messageLib),
                    messageLib: messageLib,
                    messageLibProgram: ulnProgramId,
                    anchorRemainingAccounts: setConfigRemainingAccounts
                }

            //     const executorConfig = UlnProgram.executorConfigBeet.serialize({
            //         executor: PublicKey.findProgramAddressSync(
            //             [Buffer.from(EXECUTOR_CONFIG_SEED, 'utf8')],
            //             executorProgramId,
            //         )[0],
            //         maxMessageSize: 10000,
            //     })[0];

            //     const setConfigExecutorParams = {
            //         params: {
            //             oapp: tristeroOappPubkey,
            //             eid: arbitrumEID,
            //             configType: OftTools.ConfigType.Executor,
            //             config: executorConfig,
            //         }
            //     }

                const ulnReceiveConfig = UlnProgram.types.ulnConfigBeet.serialize({
                    confirmations: 10,
                    requiredDvnCount: 1,
                    optionalDvnCount: 0,
                    optionalDvnThreshold: 0,
                    requiredDvns: [new PublicKey("4VDjp6XQaxoZf5RGwiPU9NR1EXSZn2TP4ATMmiSzLfhb")].sort(),
                    optionalDvns: [].sort(),
                  })[0];

                const setConfigReceiveParams = {
                    params: {
                        oapp: tristeroOappPubkey,
                        eid: arbitrumEID,
                        configType: OftTools.ConfigType.ReceiveUln,
                        config: ulnReceiveConfig,
                    }
                }

            //     const setConfigExecutorInstruction = EndpointProgram.instructions.createSetConfigInstruction(setConfigAccounts, setConfigExecutorParams)
                const setConfigReceiveInstruction = EndpointProgram.instructions.createSetConfigInstruction(setConfigAccounts, setConfigReceiveParams)

            //     console.log("setConfig well done")
            //     const transSetConfigExecutor = new Transaction().add(setConfigExecutorInstruction);
                const transSetConfigReceive = new Transaction().add(setConfigReceiveInstruction);
            //     const setConfigExecutorTx = await sendAndConfirmTransaction(connection, transSetConfigExecutor, [user])
            //     console.log("setConfigExecutorTx = ", setConfigExecutorTx)
                const setConfigReceiveTx = await sendAndConfirmTransaction(connection, transSetConfigReceive, [user])
                console.log("setConfigReceiveTx = ", setConfigReceiveTx)
                console.log("-------------------------------------------------------------------------------")
            }

            console.log("------------------------------mint new spl token(only need in localnet)-------------------------------------------------");
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

            const usdCoinMintAddress = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU" // dest Token Mint Address
            const numberArray: number[] = [];
            for (let i = 0; i < usdCoinMintAddress.length; i++) {
                const hexChar = usdCoinMintAddress[i];
                const num = parseInt(hexChar, 16);
                numberArray.push(num);
            }

            console.log("getUserPDA(user.publicKey) => ", getUserPDA(user.publicKey));
            const selectedUser = await program.account.user.fetch(getUserPDA(user.publicKey));
            console.log("selectedUser => ", selectedUser)

            console.log("------------------------Create Match------------------------");

            {
                const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
                const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
                console.log(sendLibraryConfig, " ", defaultSendLibraryConfig);
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
                        pubkey: ulnEventPdaDeriver.eventAuthority()[0],
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
                const sourceTokenAddressInArbitrumChain = Array(20).fill(0); //have to input arbitrum wallet address of user
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

                // console.log("Remaining Accounts ==> ", JSON.stringify(sendInstructionRemainingAccounts, null, '\t'));
                // console.log("Params => ", JSON.stringify({
                //     sourceSellAmount: sellAmount,
                //     destTokenMint: numberArray,
                //     destBuyAmount: buyAmount,
                //     eid: arbitrumEID,
                //     tristeroOappBump: getTristeroOappBump(),
                //     sourceTokenAddressInArbitrumChain: sourceTokenAddressInArbitrumChain,
                //     receiver: Array.from(receiverPubKey),
                // }, null, '\t'))
                // console.log("Accounts => ", JSON.stringify({
                //     authority: user.publicKey,
                //     adminPanel: getAdminPanel(),
                //     tokenMint: mint,
                //     tokenAccount: tokenAccount,
                //     stakingAccount: getStakingPanel(mint),
                //     user: getUserPDA(user.publicKey),
                //     tradeMatch: getTradeMatchPDA(user.publicKey, selectedUser.matchCount),
                //     tokenProgram: TOKEN_PROGRAM_ID,
                //     systemProgram: SystemProgram.programId
                // }, null, '\t'))

                let instruction = await program.methods.createMatch({
                    sourceSellAmount: sellAmount,
                    destTokenMint: numberArray,
                    destBuyAmount: buyAmount,
                    eid: arbitrumEID,
                    tristeroOappBump: getTristeroOappBump(),
                    sourceTokenAddressInArbitrumChain: sourceTokenAddressInArbitrumChain,
                    receiver: Array.from(receiverPubKey),
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
                    .signers([user])
                    .instruction();
                // console.log(" params => ", JSON.stringify({
                //     sourceSellAmount: sellAmount,
                //     destTokenMint: usdCoinMintAddress,
                //     destBuyAmount: buyAmount,
                //     eid: arbitrumEID,
                //     tristeroOappBump: getTristeroOappBump(),
                //     sourceTokenAddressInArbitrumChain: sourceTokenAddressInArbitrumChain
                // }, null, '\t'))
                tx.add(instruction)
                const createMatchTx = await sendAndConfirmTransaction(connection, tx, [user])

                console.log("createMatchTx = ", createMatchTx)
            }

            console.log("------------------------Cancel Match------------------------");

            // {
            //     const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
            //     const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
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
            //             pubkey: getEndpointPDA(arbitrumEID),
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
            //             pubkey: uldEventPdaDeriver.eventAuthority()[0],
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
            //     const sellAmount = new BN(100000)
            //     const buyAmount = new BN(10000)
            //     const sourceTokenAddressInArbitrumChain = Array(40).fill(0); //have to input arbitrum wallet address of user
            //     const messageToSend = selectedUser.matchCount.toString(16) //2
            //         + mint.toString() // 32
            //         + sellAmount.toString(16).padStart(32, '0') // 32
            //         + usdCoinMintAddress.toString() //32
            //         + buyAmount.toString(16).padStart(32, '0') //32
            //         + Buffer.from(sourceTokenAddressInArbitrumChain) //40

            //     const additionalComputeBudgetInstruction =
            //         anchor.web3.ComputeBudgetProgram.requestUnits({
            //             units: 800000,
            //             additionalFee: 0,
            //         });

            //     let tx = new Transaction();
            //     tx.add(ComputeBudgetProgram.setComputeUnitLimit({ units: 2000000 }))

            //     let instruction = await program.methods.cancelMatch({
            //         matchId: selectedUser.matchCount,
            //         tristeroOappBump: getTristeroOappBump(),
            //     })
            //         .accounts({
            //             authority: user.publicKey,
            //             adminPanel: getAdminPanel(),
            //             tokenMint: mint,
            //             tokenAccount: tokenAccount,
            //             stakingAccount: getStakingPanel(mint),
            //             user: getUserPDA(user.publicKey),
            //             tradeMatch: getTradeMatchPDA(user.publicKey, selectedUser.matchCount),
            //             tokenProgram: TOKEN_PROGRAM_ID,
            //             systemProgram: SystemProgram.programId
            //         })
            //         .remainingAccounts(sendInstructionRemainingAccounts)
            //         .instruction();
            //     tx.add(instruction)
            //     const createMatchTx = await sendAndConfirmTransaction(connection, tx, [user])

            //     console.log("cancelMatchTx = ", createMatchTx)
            // }

        } catch (err) {
            console.log(err)
        }
    })
});

console.log("EndpointProgram ----> ", EndpointProgram.PROGRAM_ID)
console.log("UlnProgram ----> ", UlnProgram.PROGRAM_ID)

const endpointProgram = new Program<Endpoint>(IDL, endpoint, anchor.getProvider())

const subscriptionId =  endpointProgram.addEventListener("LzReceiveAlertEvent", async (event) => {
    console.log("LzReceiveAlertEvent is called....")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
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

const sendConfigPDA = (eid: number, pubkey: PublicKey) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(SEND_CONFIG_SEED), new BN(eid).toBuffer("be", 4), pubkey.toBuffer()],
        ulnProgramId,
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
        [Buffer.from("trade_match"), authority.toBuffer(), new BN(matchCount).toBuffer("be", 4)],
        programId,
    )[0]
}

const getPayloadHashPDA = (receiver: PublicKey, srcEid: number, sender: number[], nonce: BN) => {
    return PublicKey.findProgramAddressSync(
        [Buffer.from(PAYLOAD_HASH_SEED), receiver.toBuffer(), new BN(srcEid).toBuffer("be", 4), Buffer.from(sender), nonce.toBuffer("be", 8)],
        programId,
    )[0]
}