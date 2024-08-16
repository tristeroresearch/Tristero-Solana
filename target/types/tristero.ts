export type Tristero = {
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
          "name": "authority",
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
          "name": "order",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "token account address"
          ]
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
      "name": "challenge",
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
            "defined": "ChallengeParams"
          }
        }
      ]
    },
    {
      "name": "lzReceive",
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
            "token account address"
          ]
        },
        {
          "name": "destOwner",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "stakingAccount",
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
            "defined": "LzReceiveParams"
          }
        }
      ]
    },
    {
      "name": "lzReceiveTypes",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "LzReceiveTypeParams"
          }
        }
      ],
      "returns": {
        "vec": {
          "defined": "LzAccount"
        }
      }
    },
    {
      "name": "registerConfig",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oappConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
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
      "name": "placeOrder",
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
          "name": "solTreasury",
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
            "token account address"
          ]
        },
        {
          "name": "stakingAccount",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "order",
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
            "defined": "PlaceOrderParams"
          }
        }
      ]
    },
    {
      "name": "sendStored",
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
            "arb user's token mint address"
          ]
        },
        {
          "name": "tokenAccount",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "arb user's token account address"
          ]
        },
        {
          "name": "destOwner",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "stakingAccount",
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
            "defined": "SendStoredParams"
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
            "name": "authority",
            "type": "publicKey"
          },
          {
            "name": "paymentWallet",
            "type": "publicKey"
          },
          {
            "name": "backendWallet",
            "type": "publicKey"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "tradeFee",
            "type": "u64"
          },
          {
            "name": "matchCount",
            "type": "u64"
          },
          {
            "name": "orderCount",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "lzReceiveTypesAccounts",
      "docs": [
        "LzReceiveTypesAccounts includes accounts that are used in the LzReceiveTypes",
        "instruction."
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oftConfig",
            "type": "publicKey"
          },
          {
            "name": "tokenMint",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "order",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "orderId",
            "type": "u64"
          },
          {
            "name": "userPubkey",
            "type": "publicKey"
          },
          {
            "name": "userTokenAddr",
            "type": "publicKey"
          },
          {
            "name": "sourceTokenMint",
            "type": "publicKey"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
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
            "name": "minSellAmount",
            "type": "u64"
          },
          {
            "name": "settled",
            "type": "u64"
          },
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "isValiable",
            "type": "bool"
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
            "name": "authority",
            "type": "publicKey"
          },
          {
            "name": "userTokenAddr",
            "type": "publicKey"
          },
          {
            "name": "sourceTokenMint",
            "type": "publicKey"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          },
          {
            "name": "srcIndex",
            "type": "u64"
          },
          {
            "name": "dstIndex",
            "type": "u64"
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
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "tradeMatchId",
            "type": "u64"
          },
          {
            "name": "isValiable",
            "type": "bool"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "CreateMatchParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "srcIndex",
            "type": "u64"
          },
          {
            "name": "dstIndex",
            "type": "u64"
          },
          {
            "name": "srcQuantity",
            "type": "u64"
          },
          {
            "name": "dstQuantity",
            "type": "u64"
          },
          {
            "name": "tradeMatchId",
            "type": "u64"
          },
          {
            "name": "arbSourceTokenAddr",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          }
        ]
      }
    },
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
      "name": "LzReceiveTypeParams",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "message",
            "type": "bytes"
          },
          {
            "name": "extraData",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "LzAccount",
      "docs": [
        "same to anchor_lang::prelude::AccountMeta"
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "pubkey",
            "type": "publicKey"
          },
          {
            "name": "isSigner",
            "type": "bool"
          },
          {
            "name": "isWritable",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "LzReceiveParams",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "message",
            "type": "bytes"
          },
          {
            "name": "extraData",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "ChallengeParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "tradeMatchId",
            "type": "u64"
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
                20
              ]
            }
          },
          {
            "name": "receiver",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          }
        ]
      }
    },
    {
      "name": "PlaceOrderParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sourceSellAmount",
            "type": "u64"
          },
          {
            "name": "minSellAmount",
            "type": "u64"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          },
          {
            "name": "destBuyAmount",
            "type": "u64"
          },
          {
            "name": "orderId",
            "type": "u64"
          },
          {
            "name": "eid",
            "type": "u32"
          }
        ]
      }
    },
    {
      "name": "SendStoredParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "tradeMatchId",
            "type": "u64"
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
                20
              ]
            }
          },
          {
            "name": "receiver",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          }
        ]
      }
    }
  ],
  "events": [
    {
      "name": "OFTReceived",
      "fields": [
        {
          "name": "guid",
          "type": {
            "array": [
              "u8",
              32
            ]
          },
          "index": false
        },
        {
          "name": "srcEid",
          "type": "u32",
          "index": false
        },
        {
          "name": "to",
          "type": "publicKey",
          "index": false
        },
        {
          "name": "amountReceivedLd",
          "type": "u64",
          "index": false
        }
      ]
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
      "name": "NotAgain",
      "msg": "Already canceled or traded"
    },
    {
      "code": 6007,
      "name": "WrongMsgTypeError",
      "msg": "Wrong msg type"
    },
    {
      "code": 6008,
      "name": "WrongMsgDstIndex",
      "msg": "Can not find with dst index"
    },
    {
      "code": 6009,
      "name": "WrongMsgSrcToken",
      "msg": "Can not find with src token address"
    },
    {
      "code": 6010,
      "name": "WrongMsgDstToken",
      "msg": "Can not find with dst token address"
    },
    {
      "code": 6011,
      "name": "WrongAuthorityToCancel",
      "msg": "Can not cancel with this authority"
    },
    {
      "code": 6012,
      "name": "MinSellAmountConflict",
      "msg": "Min Sell Amount Conflict"
    },
    {
      "code": 6013,
      "name": "InSufficientFundsOfOrder",
      "msg": "Insufficient Funds of Order"
    },
    {
      "code": 6014,
      "name": "InvalidSendLibrary"
    },
    {
      "code": 6015,
      "name": "InvalidReceiveLibrary"
    },
    {
      "code": 6016,
      "name": "SameValue"
    },
    {
      "code": 6017,
      "name": "AccountNotFound"
    },
    {
      "code": 6018,
      "name": "OnlySendLib"
    },
    {
      "code": 6019,
      "name": "OnlyReceiveLib"
    },
    {
      "code": 6020,
      "name": "InvalidExpiry"
    },
    {
      "code": 6021,
      "name": "OnlyNonDefaultLib"
    },
    {
      "code": 6022,
      "name": "InvalidAmount"
    },
    {
      "code": 6023,
      "name": "InvalidNonce"
    },
    {
      "code": 6024,
      "name": "Unauthorized"
    },
    {
      "code": 6025,
      "name": "ComposeNotFound"
    },
    {
      "code": 6026,
      "name": "InvalidPayloadHash"
    },
    {
      "code": 6027,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6028,
      "name": "ReadOnlyAccount"
    },
    {
      "code": 6029,
      "name": "InvalidMessageLib"
    },
    {
      "code": 6030,
      "name": "WritableAccountNotAllowed"
    }
  ]
};

export const IDL: Tristero = {
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
          "name": "authority",
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
          "name": "order",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "token account address"
          ]
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
      "name": "challenge",
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
            "defined": "ChallengeParams"
          }
        }
      ]
    },
    {
      "name": "lzReceive",
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
            "token account address"
          ]
        },
        {
          "name": "destOwner",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "stakingAccount",
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
            "defined": "LzReceiveParams"
          }
        }
      ]
    },
    {
      "name": "lzReceiveTypes",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "LzReceiveTypeParams"
          }
        }
      ],
      "returns": {
        "vec": {
          "defined": "LzAccount"
        }
      }
    },
    {
      "name": "registerConfig",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oappConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
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
      "name": "placeOrder",
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
          "name": "solTreasury",
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
            "token account address"
          ]
        },
        {
          "name": "stakingAccount",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "order",
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
            "defined": "PlaceOrderParams"
          }
        }
      ]
    },
    {
      "name": "sendStored",
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
            "arb user's token mint address"
          ]
        },
        {
          "name": "tokenAccount",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "arb user's token account address"
          ]
        },
        {
          "name": "destOwner",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "stakingAccount",
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
            "defined": "SendStoredParams"
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
            "name": "authority",
            "type": "publicKey"
          },
          {
            "name": "paymentWallet",
            "type": "publicKey"
          },
          {
            "name": "backendWallet",
            "type": "publicKey"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "tradeFee",
            "type": "u64"
          },
          {
            "name": "matchCount",
            "type": "u64"
          },
          {
            "name": "orderCount",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "lzReceiveTypesAccounts",
      "docs": [
        "LzReceiveTypesAccounts includes accounts that are used in the LzReceiveTypes",
        "instruction."
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oftConfig",
            "type": "publicKey"
          },
          {
            "name": "tokenMint",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "order",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "orderId",
            "type": "u64"
          },
          {
            "name": "userPubkey",
            "type": "publicKey"
          },
          {
            "name": "userTokenAddr",
            "type": "publicKey"
          },
          {
            "name": "sourceTokenMint",
            "type": "publicKey"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
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
            "name": "minSellAmount",
            "type": "u64"
          },
          {
            "name": "settled",
            "type": "u64"
          },
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "isValiable",
            "type": "bool"
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
            "name": "authority",
            "type": "publicKey"
          },
          {
            "name": "userTokenAddr",
            "type": "publicKey"
          },
          {
            "name": "sourceTokenMint",
            "type": "publicKey"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          },
          {
            "name": "srcIndex",
            "type": "u64"
          },
          {
            "name": "dstIndex",
            "type": "u64"
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
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "tradeMatchId",
            "type": "u64"
          },
          {
            "name": "isValiable",
            "type": "bool"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "CreateMatchParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "srcIndex",
            "type": "u64"
          },
          {
            "name": "dstIndex",
            "type": "u64"
          },
          {
            "name": "srcQuantity",
            "type": "u64"
          },
          {
            "name": "dstQuantity",
            "type": "u64"
          },
          {
            "name": "tradeMatchId",
            "type": "u64"
          },
          {
            "name": "arbSourceTokenAddr",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          }
        ]
      }
    },
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
      "name": "LzReceiveTypeParams",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "message",
            "type": "bytes"
          },
          {
            "name": "extraData",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "LzAccount",
      "docs": [
        "same to anchor_lang::prelude::AccountMeta"
      ],
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "pubkey",
            "type": "publicKey"
          },
          {
            "name": "isSigner",
            "type": "bool"
          },
          {
            "name": "isWritable",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "LzReceiveParams",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "message",
            "type": "bytes"
          },
          {
            "name": "extraData",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "ChallengeParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "tradeMatchId",
            "type": "u64"
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
                20
              ]
            }
          },
          {
            "name": "receiver",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          }
        ]
      }
    },
    {
      "name": "PlaceOrderParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sourceSellAmount",
            "type": "u64"
          },
          {
            "name": "minSellAmount",
            "type": "u64"
          },
          {
            "name": "destTokenMint",
            "type": {
              "array": [
                "u8",
                20
              ]
            }
          },
          {
            "name": "destBuyAmount",
            "type": "u64"
          },
          {
            "name": "orderId",
            "type": "u64"
          },
          {
            "name": "eid",
            "type": "u32"
          }
        ]
      }
    },
    {
      "name": "SendStoredParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "tradeMatchId",
            "type": "u64"
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
                20
              ]
            }
          },
          {
            "name": "receiver",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          }
        ]
      }
    }
  ],
  "events": [
    {
      "name": "OFTReceived",
      "fields": [
        {
          "name": "guid",
          "type": {
            "array": [
              "u8",
              32
            ]
          },
          "index": false
        },
        {
          "name": "srcEid",
          "type": "u32",
          "index": false
        },
        {
          "name": "to",
          "type": "publicKey",
          "index": false
        },
        {
          "name": "amountReceivedLd",
          "type": "u64",
          "index": false
        }
      ]
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
      "name": "NotAgain",
      "msg": "Already canceled or traded"
    },
    {
      "code": 6007,
      "name": "WrongMsgTypeError",
      "msg": "Wrong msg type"
    },
    {
      "code": 6008,
      "name": "WrongMsgDstIndex",
      "msg": "Can not find with dst index"
    },
    {
      "code": 6009,
      "name": "WrongMsgSrcToken",
      "msg": "Can not find with src token address"
    },
    {
      "code": 6010,
      "name": "WrongMsgDstToken",
      "msg": "Can not find with dst token address"
    },
    {
      "code": 6011,
      "name": "WrongAuthorityToCancel",
      "msg": "Can not cancel with this authority"
    },
    {
      "code": 6012,
      "name": "MinSellAmountConflict",
      "msg": "Min Sell Amount Conflict"
    },
    {
      "code": 6013,
      "name": "InSufficientFundsOfOrder",
      "msg": "Insufficient Funds of Order"
    },
    {
      "code": 6014,
      "name": "InvalidSendLibrary"
    },
    {
      "code": 6015,
      "name": "InvalidReceiveLibrary"
    },
    {
      "code": 6016,
      "name": "SameValue"
    },
    {
      "code": 6017,
      "name": "AccountNotFound"
    },
    {
      "code": 6018,
      "name": "OnlySendLib"
    },
    {
      "code": 6019,
      "name": "OnlyReceiveLib"
    },
    {
      "code": 6020,
      "name": "InvalidExpiry"
    },
    {
      "code": 6021,
      "name": "OnlyNonDefaultLib"
    },
    {
      "code": 6022,
      "name": "InvalidAmount"
    },
    {
      "code": 6023,
      "name": "InvalidNonce"
    },
    {
      "code": 6024,
      "name": "Unauthorized"
    },
    {
      "code": 6025,
      "name": "ComposeNotFound"
    },
    {
      "code": 6026,
      "name": "InvalidPayloadHash"
    },
    {
      "code": 6027,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6028,
      "name": "ReadOnlyAccount"
    },
    {
      "code": 6029,
      "name": "InvalidMessageLib"
    },
    {
      "code": 6030,
      "name": "WritableAccountNotAllowed"
    }
  ]
};
