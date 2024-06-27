"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const anchor = __importStar(require("@coral-xyz/anchor"));
const anchor_1 = require("@coral-xyz/anchor");
const lz_solana_sdk_v2_1 = require("@layerzerolabs/lz-solana-sdk-v2");
const web3_js_1 = require("@solana/web3.js");
const spl_token_1 = require("@solana/spl-token");
const node_test_1 = require("node:test");
const user_json_1 = __importDefault(require("./user.json"));
const other_json_1 = __importDefault(require("./other.json"));
const adminJson_json_1 = __importDefault(require("./adminJson.json"));
// arbitrum: 0x5C105836fAa55A42957D2cC1b86e880fdE998E81
const DEFAULT_MESSAGE_LIB = web3_js_1.PublicKey.default;
// Configure the client to use the local cluster.
// anchor.setProvider(anchor.AnchorProvider.env());
// const program = anchor.workspace.Tristero as Program<Tristero>;
const program = anchor.workspace.Tristero;
const endpointProgram = anchor.workspace.Endpoint;
const endpoint = (0, lz_solana_sdk_v2_1.getEndpointProgramId)('solana-mainnet');
// const uln = getULNProgramId('solana-sandbox-local');
const sendLibraryProgram = new web3_js_1.PublicKey("7a4WjyR8VZ7yZz5XJAKm39BUGn5iT9CKcv2pmG9tdXVH");
const executorProgramId = (0, lz_solana_sdk_v2_1.getExecutorProgramId)("solana-mainnet");
const priceFeeProgramId = (0, lz_solana_sdk_v2_1.getPricefeedProgramId)("solana-mainnet");
const dvnProgramId = (0, lz_solana_sdk_v2_1.getDVNProgramId)("solana-mainnet");
const ulnProgramId = (0, lz_solana_sdk_v2_1.getULNProgramId)("solana-mainnet");
const provider = program.provider;
const connection = program.provider.connection;
const programId = program.programId;
const user = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(user_json_1.default));
const otherUser = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(other_json_1.default));
const admin = anchor.web3.Keypair.fromSecretKey(Uint8Array.from(adminJson_json_1.default));
const receiverPubKey = Buffer.from(Array(32).fill(1)); // have to change to arbitrum side
const arbitrumEID = 40231;
(0, node_test_1.describe)("# test scenario - tristero ", () => {
    console.log("endpoint program id = ", endpoint);
    it("testing", () => __awaiter(void 0, void 0, void 0, function* () {
        console.log(">>> programId : ", programId);
        console.log("begin");
        try {
            const userAirDroptx = yield connection.requestAirdrop(user.publicKey, 5 * web3_js_1.LAMPORTS_PER_SOL);
            yield connection.confirmTransaction(userAirDroptx);
            console.log("User Airdrop successful: ", userAirDroptx);
            const adminAirDroptx = yield connection.requestAirdrop(admin.publicKey, 5 * web3_js_1.LAMPORTS_PER_SOL);
            yield connection.confirmTransaction(adminAirDroptx);
            console.log("User Airdrop successful: ", adminAirDroptx);
            console.log("balance(User): ", yield connection.getBalance(user.publicKey), "balance(Admin): ", yield connection.getBalance(admin.publicKey));
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
            // console.log("-------------------------Airdrop for tristero oapp-------------------------------------")
            const tristeroOappPubkey = getTristeroOapp();
            const endpointEventPdaDeriver = new lz_solana_sdk_v2_1.EventPDADeriver(endpoint);
            const uldEventPdaDeriver = new lz_solana_sdk_v2_1.EventPDADeriver(sendLibraryProgram);
            console.log("------------------------Register New Oapp(Sender)------------------------");
            console.log("user.publickey ===> ", user.publicKey.toString());
            const registerTristeroOAppParams = {
                delegate: user.publicKey
            };
            console.log("registerTristeroOapp => ", JSON.stringify({
                payer: user.publicKey,
                oapp: tristeroOappPubkey,
                oappRegistry: getOappPDA(tristeroOappPubkey),
                endpointProgram: endpoint,
                systemProgram: web3_js_1.SystemProgram.programId,
                eventAuthority: endpointEventPdaDeriver.eventAuthority()[0],
            }));
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
            console.log("-------------------Init Send Library-----------------------------");
            {
                const initSendLibraryInstructionAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
                    sendLibraryConfig: getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
                };
                const initSendLibraryParams = {
                    params: {
                        oapp: tristeroOappPubkey,
                        sender: tristeroOappPubkey,
                        eid: arbitrumEID
                    }
                };
                const sendLibraryInstruction = lz_solana_sdk_v2_1.EndpointProgram.instructions.createInitSendLibraryInstruction(initSendLibraryInstructionAccounts, initSendLibraryParams);
                console.log("InitSendLibrary well done");
                console.log("sendLibraryInstruction = " + sendLibraryInstruction);
                const transaction = new web3_js_1.Transaction().add(sendLibraryInstruction);
                const tx3 = yield (0, web3_js_1.sendAndConfirmTransaction)(connection, transaction, [user]);
                console.log("tx3 = ", tx3);
                console.log("-------------------------------------------------------------------------------");
            }
            console.log("----------------------------Init Receive Library-------------------------------");
            {
                const initReceiveLibraryInstructionAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey), // comes from other
                    receiveLibraryConfig: getReceiveLibraryConfigPDA(tristeroOappPubkey, arbitrumEID),
                };
                const initReceiveLibraryParams = {
                    params: {
                        receiver: tristeroOappPubkey,
                        eid: arbitrumEID
                    }
                };
                const receiveLibraryInstruction = lz_solana_sdk_v2_1.EndpointProgram.instructions.createInitReceiveLibraryInstruction(initReceiveLibraryInstructionAccounts, initReceiveLibraryParams);
                console.log("InitReceiveLibrary well done");
                const transaction4 = new web3_js_1.Transaction().add(receiveLibraryInstruction);
                const initReceiveLibTx = yield (0, web3_js_1.sendAndConfirmTransaction)(connection, transaction4, [user]);
                console.log("initReceiveLibTx = ", initReceiveLibTx);
                console.log("-------------------------------------------------------------------------------");
            }
            console.log("-------------------Init Nonce-----------------------------");
            {
                const initNonceAccounts = {
                    delegate: user.publicKey,
                    oappRegistry: getOappRegistryPDA(tristeroOappPubkey),
                    nonce: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                    pendingInboundNonce: getPendingInboundNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                    SystemProgram: web3_js_1.SystemProgram.programId
                };
                const initNonceParams = {
                    params: {
                        localOapp: tristeroOappPubkey,
                        remoteEid: arbitrumEID,
                        remoteOapp: Array.from(receiverPubKey)
                    }
                };
                const initNonceInstruction = lz_solana_sdk_v2_1.EndpointProgram.instructions.createInitNonceInstruction(initNonceAccounts, initNonceParams);
                console.log("InitNonce well done");
                console.log("initNonceInstruction = " + initNonceInstruction);
                const _transaction = new web3_js_1.Transaction().add(initNonceInstruction);
                const _tx3 = yield (0, web3_js_1.sendAndConfirmTransaction)(connection, _transaction, [user]);
                console.log("_tx3 = ", _tx3);
                console.log("-------------------------------------------------------------------------------");
            }
            console.log("------------------------------mint new spl token(only need in localnet)-------------------------------------------------");
            const mint = yield (0, spl_token_1.createMint)(connection, user, user.publicKey, null, 5 // Decimals
            );
            // const mint = new PublicKey("iwyvga9wLQAU9cNk9kycrLptQR8dgpMBvjDWZjc3npN")
            // console.log("Mint Address: ", mint.toBase58());
            // Create a token account for the mint
            const tokenAccount = yield (0, spl_token_1.getOrCreateAssociatedTokenAccount)(connection, user, mint, user.publicKey);
            // const tokenAccount = new PublicKey("FFKNLCf6tK6B7yoJivjgcW9uoaQXx38DdaAheMH857Jh")
            console.log("Token Account Address: ", tokenAccount.address.toBase58());
            // Mint some tokens to the token account
            yield (0, spl_token_1.mintTo)(connection, user, mint, tokenAccount.address, user.publicKey, 10000000000 // Amount to mint (int smallest units)
            );
            const usdCoinMintAddress = new web3_js_1.PublicKey("4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"); // dest Token Mint Address
            const selectedUser = yield program.account.user.fetch(getUserPDA(user.publicKey));
            console.log("selectedUser => ", selectedUser.matchCount);
            console.log("------------------------Create Match------------------------");
            {
                const sendLibraryConfig = getSendLibraryConfigPDA(tristeroOappPubkey, arbitrumEID);
                const defaultSendLibraryConfig = getDefaultSendLibraryConfig(arbitrumEID);
                const sendLibraryInfo = yield getSendLibraryInfoPDA(sendLibraryConfig, defaultSendLibraryConfig);
                const ulnPdaDeriver = new lz_solana_sdk_v2_1.UlnPDADeriver(sendLibraryProgram);
                let sendConfig = ulnPdaDeriver.sendConfig(arbitrumEID, tristeroOappPubkey)[0];
                let defaultSendConfig = ulnPdaDeriver.defaultSendConfig(arbitrumEID)[0]; //until here
                const sendInstructionRemainingAccounts = [
                    {
                        pubkey: endpoint,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: tristeroOappPubkey,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: sendLibraryProgram,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: sendLibraryConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: defaultSendLibraryConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: sendLibraryInfo,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: getEndpointPDA(arbitrumEID),
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: getNoncePDA(tristeroOappPubkey, arbitrumEID, receiverPubKey),
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: endpointEventPdaDeriver.eventAuthority()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: endpoint,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: getUlnPDA(),
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: sendConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: defaultSendConfig,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: user.publicKey,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: user.publicKey,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: web3_js_1.SystemProgram.programId,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: uldEventPdaDeriver.eventAuthority()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: sendLibraryProgram,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: executorProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: new lz_solana_sdk_v2_1.ExecutorPDADeriver(executorProgramId).config()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: priceFeeProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: new lz_solana_sdk_v2_1.PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: dvnProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: new lz_solana_sdk_v2_1.DVNDeriver(dvnProgramId).config()[0],
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: priceFeeProgramId,
                        isSigner: false,
                        isWritable: true
                    },
                    {
                        pubkey: new lz_solana_sdk_v2_1.PriceFeedPDADeriver(priceFeeProgramId).priceFeed()[0],
                        isSigner: false,
                        isWritable: true
                    },
                ];
                const sellAmount = new anchor_1.BN(100000);
                const buyAmount = new anchor_1.BN(10000);
                const sourceTokenAddressInArbitrumChain = Array(40).fill(0); //have to input arbitrum wallet address of user
                const messageToSend = selectedUser.matchCount.toString(16) //2
                    + mint.toString() // 32
                    + sellAmount.toString(16).padStart(32, '0') // 32
                    + usdCoinMintAddress.toString() //32
                    + buyAmount.toString(16).padStart(32, '0') //32
                    + Buffer.from(sourceTokenAddressInArbitrumChain); //40
                const additionalComputeBudgetInstruction = anchor.web3.ComputeBudgetProgram.requestUnits({
                    units: 800000,
                    additionalFee: 0,
                });
                let tx = new web3_js_1.Transaction();
                tx.add(web3_js_1.ComputeBudgetProgram.setComputeUnitLimit({ units: 2000000 }));
                let instruction = yield program.methods.createMatch({
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
                    tokenAccount: tokenAccount.address,
                    stakingAccount: getStakingPanel(mint),
                    user: getUserPDA(user.publicKey),
                    tradeMatch: getTradeMatchPDA(user.publicKey, selectedUser.matchCount),
                    tokenProgram: spl_token_1.TOKEN_PROGRAM_ID,
                    systemProgram: web3_js_1.SystemProgram.programId
                })
                    .remainingAccounts(sendInstructionRemainingAccounts)
                    .instruction();
                tx.add(instruction);
                const createMatchTx = yield (0, web3_js_1.sendAndConfirmTransaction)(connection, tx, [user]);
                console.log("createMatchTx = ", createMatchTx);
            }
        }
        catch (err) {
            console.log(err);
        }
    }));
});
const subscriptionId = endpointProgram.addEventListener("LzReceiveAlertEvent", (event) => __awaiter(void 0, void 0, void 0, function* () {
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
    };
    // message: matchId(2), 
    const messageStr = event.message.toString();
    const tradeMatchId = parseInt(messageStr.slice(0, 2), 16);
    const destTokenAccount = messageStr.slice(2);
    const tradeMatch = yield program.account.tradeMatch.fetch(getTradeMatchPDA(event.receiver, tradeMatchId));
    const swapTokenTx = yield program.methods.swapToken(swapParams)
        .accounts({
        adminPanel: getAdminPanel(),
        tokenMint: tradeMatch.sourceTokenMint,
        tokenAccount: new web3_js_1.PublicKey(destTokenAccount),
        endpoint: getEndpointPDA(event.srcEid),
        stakingAccount: getStakingPanel(tradeMatch.sourceTokenMint),
        tokenProgram: spl_token_1.TOKEN_PROGRAM_ID,
        systemProgram: web3_js_1.SystemProgram.programId,
        tradeMatch: getTradeMatchPDA(event.receiver, tradeMatchId),
        user: getUserPDA(event.receiver),
        payloadHash: getPayloadHashPDA(event.receiver, event.srcEid, event.sender, event.nonce)
    })
        .rpc();
    console.log("swapTokenTx = ", swapTokenTx);
}));
const getOappPDA = (authority) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.OAPP_SEED), authority.toBuffer()], endpoint)[0];
};
const getExecutorPDA = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.EXECUTOR_CONFIG_SEED)], executorProgramId)[0];
};
const getUlnPDA = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.ULN_SEED)], ulnProgramId)[0];
};
const getSendConfigPDA = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.ULN_SEED),], ulnProgramId)[0];
};
const getTristeroOapp = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("TristeroOapp")], programId)[0];
};
const getTristeroOappBump = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("TristeroOapp")], programId)[1];
};
const getMessageLibPDA = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.MESSAGE_LIB_SEED)], endpoint)[0];
};
const getMessageLibInfoPDA = (pubkey) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.MESSAGE_LIB_SEED), pubkey.toBuffer()], endpoint)[0];
};
const getOappRegistryPDA = (pubkey) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.OAPP_SEED), pubkey.toBuffer()], endpoint)[0];
};
const getSendLibraryConfigPDA = (senderPubkey, eid) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.SEND_LIBRARY_CONFIG_SEED), senderPubkey.toBuffer(), new anchor_1.BN(eid).toBuffer("be", 4)], endpoint)[0];
};
const getReceiveLibraryConfigPDA = (receiverPubkey, eid) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.RECEIVE_LIBRARY_CONFIG_SEED), receiverPubkey.toBuffer(), new anchor_1.BN(eid).toBuffer("be", 4)], endpoint)[0];
};
const getDefaultSendLibraryConfig = (eid) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.SEND_LIBRARY_CONFIG_SEED), new anchor_1.BN(eid).toBuffer("be", 4)], endpoint)[0];
};
const getSendLibraryInfoPDA = (sendLibraryConfig, defaultSendLibraryConfig) => __awaiter(void 0, void 0, void 0, function* () {
    const res = yield lz_solana_sdk_v2_1.EndpointProgram.accounts.SendLibraryConfig.fromAccountAddress(connection, defaultSendLibraryConfig);
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.MESSAGE_LIB_SEED), res.messageLib.toBuffer()], endpoint)[0];
});
const getEndpointPDA = (eid) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.ENDPOINT_SEED)], endpoint)[0];
};
const getPriceFeedPDA = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.PRICE_FEED_SEED)], priceFeeProgramId)[0];
};
const getNoncePDA = (senderKey, eid, receiver) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.NONCE_SEED), senderKey.toBytes(), new anchor_1.BN(eid).toBuffer("be", 4), receiver], endpoint)[0];
};
const getPendingInboundNoncePDA = (senderKey, eid, receiver) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.PENDING_NONCE_SEED), senderKey.toBytes(), new anchor_1.BN(eid).toBuffer("be", 4), receiver], endpoint)[0];
};
const getAdminPanel = () => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("admin_panel")], programId)[0];
};
const getStakingPanel = (mint) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("staking_account"), mint.toBuffer()], programId)[0];
};
const getUserPDA = (authority) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("user"), authority.toBytes()], programId)[0];
};
const getTradeMatchPDA = (authority, matchCount) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from("trade_match"), authority.toBuffer(), new anchor_1.BN(matchCount).toBuffer("be", 1)], programId)[0];
};
const getPayloadHashPDA = (receiver, srcEid, sender, nonce) => {
    return web3_js_1.PublicKey.findProgramAddressSync([Buffer.from(lz_solana_sdk_v2_1.PAYLOAD_HASH_SEED), receiver.toBuffer(), new anchor_1.BN(srcEid).toBuffer("be", 4), Buffer.from(sender), nonce.toBuffer("be", 8)], programId)[0];
};
