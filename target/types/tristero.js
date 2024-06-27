"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IDL = void 0;
exports.IDL = {
    "version": "0.1.0",
    "name": "tristero",
    "instructions": [
        {
            "name": "registerTristeroOapp",
            "accounts": [
                {
                    "name": "payer",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "oapp",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "oappRegistry",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "eventAuthority",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "endpointProgram",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "RegisterTristeroOAppParams"
                    }
                }
            ]
        },
        {
            "name": "tristeroSend",
            "accounts": [
                {
                    "name": "sender",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "endpointProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "eventAuthority",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "program",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "TristeroSendParams"
                    }
                }
            ]
        },
        {
            "name": "adminPanelCreate",
            "accounts": [
                {
                    "name": "adminWallet",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "adminPanel",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "InitializeParams"
                    }
                }
            ]
        },
        {
            "name": "adminPanelUpdate",
            "accounts": [
                {
                    "name": "adminWallet",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "adminPanel",
                    "isMut": true,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "UpdateParams"
                    }
                }
            ]
        },
        {
            "name": "createUser",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "user",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": []
        },
        {
            "name": "updateUser",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "user",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "UpdateUserParams"
                    }
                }
            ]
        },
        {
            "name": "createMatch",
            "accounts": [
                {
                    "name": "authority",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "adminPanel",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "tokenMint",
                    "isMut": false,
                    "isSigner": false,
                    "docs": [
                        "token mint address"
                    ]
                },
                {
                    "name": "tokenAccount",
                    "isMut": true,
                    "isSigner": false,
                    "docs": [
                        "user's token account address"
                    ]
                },
                {
                    "name": "stakingAccount",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "user",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "tradeMatch",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "tokenProgram",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "CreateMatchParams"
                    }
                }
            ]
        },
        {
            "name": "swapToken",
            "accounts": [
                {
                    "name": "adminPanel",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "tokenMint",
                    "isMut": false,
                    "isSigner": false,
                    "docs": [
                        "token mint address"
                    ]
                },
                {
                    "name": "tokenAccount",
                    "isMut": true,
                    "isSigner": false,
                    "docs": [
                        "user's token account address"
                    ]
                },
                {
                    "name": "payloadHash",
                    "isMut": true,
                    "isSigner": false,
                    "docs": [
                        "close the account and return the lamports to endpoint settings account"
                    ]
                },
                {
                    "name": "stakingAccount",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "user",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "tradeMatch",
                    "isMut": true,
                    "isSigner": false
                },
                {
                    "name": "systemProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "tokenProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "endpoint",
                    "isMut": true,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "SwapTokenParams"
                    }
                }
            ]
        }
    ],
    "accounts": [
        {
            "name": "adminPanel",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "adminWallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "paymentWallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "adminPanelBump",
                        "type": "u8"
                    },
                    {
                        "name": "freezeFee",
                        "type": "u64"
                    }
                ]
            }
        },
        {
            "name": "tradeMatch",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "sourceTokenMint",
                        "type": "publicKey"
                    },
                    {
                        "name": "destTokenMint",
                        "type": "publicKey"
                    },
                    {
                        "name": "sourceSellAmount",
                        "type": "u64"
                    },
                    {
                        "name": "destBuyAmount",
                        "type": "u64"
                    },
                    {
                        "name": "sourceTokenAccount",
                        "type": "publicKey"
                    },
                    {
                        "name": "eid",
                        "type": "u32"
                    },
                    {
                        "name": "matchBump",
                        "type": "u8"
                    },
                    {
                        "name": "tradeMatchId",
                        "type": "u8"
                    }
                ]
            }
        },
        {
            "name": "user",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "authority",
                        "type": "publicKey"
                    },
                    {
                        "name": "userBump",
                        "type": "u8"
                    },
                    {
                        "name": "matchCount",
                        "type": "u8"
                    }
                ]
            }
        }
    ],
    "types": [
        {
            "name": "InitializeParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "adminWallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "paymentWallet",
                        "type": "publicKey"
                    }
                ]
            }
        },
        {
            "name": "UpdateParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "adminWallet",
                        "type": "publicKey"
                    },
                    {
                        "name": "paymentWallet",
                        "type": "publicKey"
                    }
                ]
            }
        },
        {
            "name": "RegisterTristeroOAppParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "delegate",
                        "type": "publicKey"
                    }
                ]
            }
        },
        {
            "name": "TristeroSendParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "dstEid",
                        "type": "u32"
                    },
                    {
                        "name": "receiver",
                        "type": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    },
                    {
                        "name": "message",
                        "type": "bytes"
                    },
                    {
                        "name": "options",
                        "type": "bytes"
                    },
                    {
                        "name": "nativeFee",
                        "type": "u64"
                    },
                    {
                        "name": "lzTokenFee",
                        "type": "u64"
                    }
                ]
            }
        },
        {
            "name": "CreateMatchParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "sourceSellAmount",
                        "type": "u64"
                    },
                    {
                        "name": "destTokenMint",
                        "type": "publicKey"
                    },
                    {
                        "name": "destBuyAmount",
                        "type": "u64"
                    },
                    {
                        "name": "eid",
                        "type": "u32"
                    },
                    {
                        "name": "tristeroOappBump",
                        "type": "u8"
                    },
                    {
                        "name": "sourceTokenAddressInArbitrumChain",
                        "type": {
                            "array": [
                                "u8",
                                40
                            ]
                        }
                    }
                ]
            }
        },
        {
            "name": "SwapTokenParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "receiver",
                        "type": "publicKey"
                    },
                    {
                        "name": "executor",
                        "type": "publicKey"
                    },
                    {
                        "name": "srcEid",
                        "type": "u32"
                    },
                    {
                        "name": "sender",
                        "type": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    },
                    {
                        "name": "nonce",
                        "type": "u64"
                    },
                    {
                        "name": "guid",
                        "type": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    },
                    {
                        "name": "computeUnits",
                        "type": "u64"
                    },
                    {
                        "name": "value",
                        "type": "u64"
                    },
                    {
                        "name": "message",
                        "type": "bytes"
                    },
                    {
                        "name": "extraData",
                        "type": "bytes"
                    },
                    {
                        "name": "reason",
                        "type": "bytes"
                    }
                ]
            }
        },
        {
            "name": "UpdateUserParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "newUser",
                        "type": "publicKey"
                    }
                ]
            }
        }
    ],
    "errors": [
        {
            "code": 6000,
            "name": "InvalidAuthority",
            "msg": "Invalid Authority"
        },
        {
            "code": 6001,
            "name": "InvalidTokenOwner",
            "msg": "InvalidTokenOwner"
        },
        {
            "code": 6002,
            "name": "InvalidTokenMintAddress",
            "msg": "InvalidTokenMintAddress"
        },
        {
            "code": 6003,
            "name": "InvalidTokenAmount",
            "msg": "InvalidTokenAmount"
        },
        {
            "code": 6004,
            "name": "InvalidTokenStandard",
            "msg": "InvalidTokenStandard"
        },
        {
            "code": 6005,
            "name": "PayloadHashNotFound",
            "msg": "PayloadHashNotFound"
        },
        {
            "code": 6006,
            "name": "InvalidSendLibrary"
        },
        {
            "code": 6007,
            "name": "InvalidReceiveLibrary"
        },
        {
            "code": 6008,
            "name": "SameValue"
        },
        {
            "code": 6009,
            "name": "AccountNotFound"
        },
        {
            "code": 6010,
            "name": "OnlySendLib"
        },
        {
            "code": 6011,
            "name": "OnlyReceiveLib"
        },
        {
            "code": 6012,
            "name": "InvalidExpiry"
        },
        {
            "code": 6013,
            "name": "OnlyNonDefaultLib"
        },
        {
            "code": 6014,
            "name": "InvalidAmount"
        },
        {
            "code": 6015,
            "name": "InvalidNonce"
        },
        {
            "code": 6016,
            "name": "Unauthorized"
        },
        {
            "code": 6017,
            "name": "ComposeNotFound"
        },
        {
            "code": 6018,
            "name": "InvalidPayloadHash"
        },
        {
            "code": 6019,
            "name": "LzTokenUnavailable"
        },
        {
            "code": 6020,
            "name": "ReadOnlyAccount"
        },
        {
            "code": 6021,
            "name": "InvalidMessageLib"
        },
        {
            "code": 6022,
            "name": "WritableAccountNotAllowed"
        }
    ]
};
