export type Myoft = {
  "version": "0.1.0",
  "name": "myoft",
  "instructions": [
    {
      "name": "version",
      "accounts": [],
      "args": [],
      "returns": {
        "defined": "Version"
      }
    },
    {
      "name": "initOft",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
          "isMut": false,
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
            "defined": "InitOftParams"
          }
        }
      ]
    },
    {
      "name": "initAdapterOft",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "tokenProgram",
          "isMut": false,
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
            "defined": "InitAdapterOftParams"
          }
        }
      ]
    },
    {
      "name": "transferAdmin",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "TransferAdminParams"
          }
        }
      ]
    },
    {
      "name": "setPeer",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
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
            "defined": "SetPeerParams"
          }
        }
      ]
    },
    {
      "name": "setEnforcedOptions",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "enforcedOptions",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
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
            "defined": "SetEnforcedOptionsParams"
          }
        }
      ]
    },
    {
      "name": "setMintAuthority",
      "accounts": [
        {
          "name": "signer",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The admin or the mint authority"
          ]
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetMintAuthorityParams"
          }
        }
      ]
    },
    {
      "name": "mintTo",
      "accounts": [
        {
          "name": "minter",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false,
          "docs": [
            "only the non-adapter oft can mint token to the destination account"
          ]
        },
        {
          "name": "tokenDest",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": true,
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
            "defined": "MintToParams"
          }
        }
      ]
    },
    {
      "name": "quoteOft",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "peer",
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
            "defined": "QuoteOftParams"
          }
        }
      ],
      "returns": {
        "defined": "QuoteOftResult"
      }
    },
    {
      "name": "quote",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "peer",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "enforcedOptions",
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
            "defined": "QuoteParams"
          }
        }
      ],
      "returns": {
        "defined": "MessagingFee"
      }
    },
    {
      "name": "send",
      "accounts": [
        {
          "name": "signer",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "enforcedOptions",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenSource",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": false,
          "isOptional": true
        },
        {
          "name": "tokenMint",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
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
            "defined": "SendParams"
          }
        }
      ],
      "returns": {
        "defined": "MessagingReceipt"
      }
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
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": false,
          "isOptional": true
        },
        {
          "name": "toAddress",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenDest",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "associatedTokenProgram",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "systemProgram",
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
            "defined": "LzReceiveParams"
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
      "name": "setRateLimit",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetRateLimitParams"
          }
        }
      ]
    },
    {
      "name": "setDelegate",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetDelegateParams"
          }
        }
      ]
    }
  ],
  "accounts": [
    {
      "name": "enforcedOptions",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "send",
            "type": "bytes"
          },
          {
            "name": "sendAndCall",
            "type": "bytes"
          },
          {
            "name": "bump",
            "type": "u8"
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
      "name": "oftConfig",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "ld2sdRate",
            "type": "u64"
          },
          {
            "name": "tokenMint",
            "type": "publicKey"
          },
          {
            "name": "tokenProgram",
            "type": "publicKey"
          },
          {
            "name": "endpointProgram",
            "type": "publicKey"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "ext",
            "type": {
              "defined": "OftConfigExt"
            }
          }
        ]
      }
    },
    {
      "name": "peer",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "address",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "rateLimiter",
            "type": {
              "option": {
                "defined": "RateLimiter"
              }
            }
          },
          {
            "name": "bump",
            "type": "u8"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "MessagingFee",
      "type": {
        "kind": "struct",
        "fields": [
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
      "name": "MessagingReceipt",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "nonce",
            "type": "u64"
          },
          {
            "name": "fee",
            "type": {
              "defined": "MessagingFee"
            }
          }
        ]
      }
    },
    {
      "name": "Version",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sdkVersion",
            "type": "u64"
          },
          {
            "name": "oftVersion",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "InitAdapterOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "sharedDecimals",
            "type": "u8"
          },
          {
            "name": "endpointProgram",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "InitOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "sharedDecimals",
            "type": "u8"
          },
          {
            "name": "endpointProgram",
            "type": {
              "option": "publicKey"
            }
          },
          {
            "name": "mintAuthority",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "MintToParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "amount",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "QuoteParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "payInLzToken",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "OFTFeeDetail",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "feeAmountLd",
            "type": "u64"
          },
          {
            "name": "description",
            "type": "string"
          }
        ]
      }
    },
    {
      "name": "OFTLimits",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "maxAmountLd",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "OFTReceipt",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "amountSentLd",
            "type": "u64"
          },
          {
            "name": "amountReceivedLd",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "QuoteOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "payInLzToken",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "QuoteOftResult",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oftLimits",
            "type": {
              "defined": "OFTLimits"
            }
          },
          {
            "name": "oftFeeDetails",
            "type": {
              "vec": {
                "defined": "OFTFeeDetail"
              }
            }
          },
          {
            "name": "oftReceipt",
            "type": {
              "defined": "OFTReceipt"
            }
          }
        ]
      }
    },
    {
      "name": "SendParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
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
      "name": "SetDelegateParams",
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
      "name": "SetEnforcedOptionsParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "send",
            "type": "bytes"
          },
          {
            "name": "sendAndCall",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "SetMintAuthorityParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "mintAuthority",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "SetPeerParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "peer",
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
      "name": "SetRateLimitParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "refillPerSecond",
            "type": {
              "option": "u64"
            }
          },
          {
            "name": "capacity",
            "type": {
              "option": "u64"
            }
          },
          {
            "name": "enabled",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "TransferAdminParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "OftConfigExt",
      "type": {
        "kind": "enum",
        "variants": [
          {
            "name": "Native",
            "fields": [
              {
                "option": "publicKey"
              }
            ]
          },
          {
            "name": "Adapter",
            "fields": [
              "publicKey"
            ]
          }
        ]
      }
    },
    {
      "name": "RateLimiter",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "capacity",
            "type": "u64"
          },
          {
            "name": "tokens",
            "type": "u64"
          },
          {
            "name": "refillPerSecond",
            "type": "u64"
          },
          {
            "name": "lastRefillTime",
            "type": "u64"
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
    },
    {
      "name": "OFTSent",
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
          "name": "dstEid",
          "type": "u32",
          "index": false
        },
        {
          "name": "from",
          "type": "publicKey",
          "index": false
        },
        {
          "name": "amountSentLd",
          "type": "u64",
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
      "name": "Unauthorized"
    },
    {
      "code": 6001,
      "name": "InvalidSender"
    },
    {
      "code": 6002,
      "name": "InvalidDecimals"
    },
    {
      "code": 6003,
      "name": "SlippageExceeded"
    },
    {
      "code": 6004,
      "name": "InvalidTokenMint"
    },
    {
      "code": 6005,
      "name": "InvalidTokenEscrow"
    },
    {
      "code": 6006,
      "name": "InvalidTokenDest"
    },
    {
      "code": 6007,
      "name": "InvalidOptions"
    },
    {
      "code": 6008,
      "name": "InvalidEndpointProgram"
    },
    {
      "code": 6009,
      "name": "RateLimitExceeded"
    }
  ]
};

export const IDL: Myoft = {
  "version": "0.1.0",
  "name": "myoft",
  "instructions": [
    {
      "name": "version",
      "accounts": [],
      "args": [],
      "returns": {
        "defined": "Version"
      }
    },
    {
      "name": "initOft",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
          "isMut": false,
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
            "defined": "InitOftParams"
          }
        }
      ]
    },
    {
      "name": "initAdapterOft",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "lzReceiveTypesAccounts",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "tokenProgram",
          "isMut": false,
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
            "defined": "InitAdapterOftParams"
          }
        }
      ]
    },
    {
      "name": "transferAdmin",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "TransferAdminParams"
          }
        }
      ]
    },
    {
      "name": "setPeer",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
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
            "defined": "SetPeerParams"
          }
        }
      ]
    },
    {
      "name": "setEnforcedOptions",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "enforcedOptions",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
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
            "defined": "SetEnforcedOptionsParams"
          }
        }
      ]
    },
    {
      "name": "setMintAuthority",
      "accounts": [
        {
          "name": "signer",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The admin or the mint authority"
          ]
        },
        {
          "name": "oftConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetMintAuthorityParams"
          }
        }
      ]
    },
    {
      "name": "mintTo",
      "accounts": [
        {
          "name": "minter",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false,
          "docs": [
            "only the non-adapter oft can mint token to the destination account"
          ]
        },
        {
          "name": "tokenDest",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": true,
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
            "defined": "MintToParams"
          }
        }
      ]
    },
    {
      "name": "quoteOft",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "peer",
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
            "defined": "QuoteOftParams"
          }
        }
      ],
      "returns": {
        "defined": "QuoteOftResult"
      }
    },
    {
      "name": "quote",
      "accounts": [
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "peer",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "enforcedOptions",
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
            "defined": "QuoteParams"
          }
        }
      ],
      "returns": {
        "defined": "MessagingFee"
      }
    },
    {
      "name": "send",
      "accounts": [
        {
          "name": "signer",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "enforcedOptions",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenSource",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": false,
          "isOptional": true
        },
        {
          "name": "tokenMint",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
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
            "defined": "SendParams"
          }
        }
      ],
      "returns": {
        "defined": "MessagingReceipt"
      }
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
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenEscrow",
          "isMut": true,
          "isSigner": false,
          "isOptional": true
        },
        {
          "name": "toAddress",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "tokenDest",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenMint",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "tokenProgram",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "associatedTokenProgram",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "systemProgram",
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
            "defined": "LzReceiveParams"
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
      "name": "setRateLimit",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "peer",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetRateLimitParams"
          }
        }
      ]
    },
    {
      "name": "setDelegate",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "oftConfig",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetDelegateParams"
          }
        }
      ]
    }
  ],
  "accounts": [
    {
      "name": "enforcedOptions",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "send",
            "type": "bytes"
          },
          {
            "name": "sendAndCall",
            "type": "bytes"
          },
          {
            "name": "bump",
            "type": "u8"
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
      "name": "oftConfig",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "ld2sdRate",
            "type": "u64"
          },
          {
            "name": "tokenMint",
            "type": "publicKey"
          },
          {
            "name": "tokenProgram",
            "type": "publicKey"
          },
          {
            "name": "endpointProgram",
            "type": "publicKey"
          },
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "ext",
            "type": {
              "defined": "OftConfigExt"
            }
          }
        ]
      }
    },
    {
      "name": "peer",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "address",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "rateLimiter",
            "type": {
              "option": {
                "defined": "RateLimiter"
              }
            }
          },
          {
            "name": "bump",
            "type": "u8"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "MessagingFee",
      "type": {
        "kind": "struct",
        "fields": [
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
      "name": "MessagingReceipt",
      "type": {
        "kind": "struct",
        "fields": [
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
            "name": "nonce",
            "type": "u64"
          },
          {
            "name": "fee",
            "type": {
              "defined": "MessagingFee"
            }
          }
        ]
      }
    },
    {
      "name": "Version",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sdkVersion",
            "type": "u64"
          },
          {
            "name": "oftVersion",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "InitAdapterOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "sharedDecimals",
            "type": "u8"
          },
          {
            "name": "endpointProgram",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "InitOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "sharedDecimals",
            "type": "u8"
          },
          {
            "name": "endpointProgram",
            "type": {
              "option": "publicKey"
            }
          },
          {
            "name": "mintAuthority",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "MintToParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "amount",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "QuoteParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "payInLzToken",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "OFTFeeDetail",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "feeAmountLd",
            "type": "u64"
          },
          {
            "name": "description",
            "type": "string"
          }
        ]
      }
    },
    {
      "name": "OFTLimits",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "maxAmountLd",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "OFTReceipt",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "amountSentLd",
            "type": "u64"
          },
          {
            "name": "amountReceivedLd",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "QuoteOftParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "payInLzToken",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "QuoteOftResult",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oftLimits",
            "type": {
              "defined": "OFTLimits"
            }
          },
          {
            "name": "oftFeeDetails",
            "type": {
              "vec": {
                "defined": "OFTFeeDetail"
              }
            }
          },
          {
            "name": "oftReceipt",
            "type": {
              "defined": "OFTReceipt"
            }
          }
        ]
      }
    },
    {
      "name": "SendParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "to",
            "type": {
              "array": [
                "u8",
                32
              ]
            }
          },
          {
            "name": "amountLd",
            "type": "u64"
          },
          {
            "name": "minAmountLd",
            "type": "u64"
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "composeMsg",
            "type": {
              "option": "bytes"
            }
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
      "name": "SetDelegateParams",
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
      "name": "SetEnforcedOptionsParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "send",
            "type": "bytes"
          },
          {
            "name": "sendAndCall",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "SetMintAuthorityParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "mintAuthority",
            "type": {
              "option": "publicKey"
            }
          }
        ]
      }
    },
    {
      "name": "SetPeerParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "peer",
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
      "name": "SetRateLimitParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "dstEid",
            "type": "u32"
          },
          {
            "name": "refillPerSecond",
            "type": {
              "option": "u64"
            }
          },
          {
            "name": "capacity",
            "type": {
              "option": "u64"
            }
          },
          {
            "name": "enabled",
            "type": "bool"
          }
        ]
      }
    },
    {
      "name": "TransferAdminParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "admin",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "OftConfigExt",
      "type": {
        "kind": "enum",
        "variants": [
          {
            "name": "Native",
            "fields": [
              {
                "option": "publicKey"
              }
            ]
          },
          {
            "name": "Adapter",
            "fields": [
              "publicKey"
            ]
          }
        ]
      }
    },
    {
      "name": "RateLimiter",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "capacity",
            "type": "u64"
          },
          {
            "name": "tokens",
            "type": "u64"
          },
          {
            "name": "refillPerSecond",
            "type": "u64"
          },
          {
            "name": "lastRefillTime",
            "type": "u64"
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
    },
    {
      "name": "OFTSent",
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
          "name": "dstEid",
          "type": "u32",
          "index": false
        },
        {
          "name": "from",
          "type": "publicKey",
          "index": false
        },
        {
          "name": "amountSentLd",
          "type": "u64",
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
      "name": "Unauthorized"
    },
    {
      "code": 6001,
      "name": "InvalidSender"
    },
    {
      "code": 6002,
      "name": "InvalidDecimals"
    },
    {
      "code": 6003,
      "name": "SlippageExceeded"
    },
    {
      "code": 6004,
      "name": "InvalidTokenMint"
    },
    {
      "code": 6005,
      "name": "InvalidTokenEscrow"
    },
    {
      "code": 6006,
      "name": "InvalidTokenDest"
    },
    {
      "code": 6007,
      "name": "InvalidOptions"
    },
    {
      "code": 6008,
      "name": "InvalidEndpointProgram"
    },
    {
      "code": 6009,
      "name": "RateLimitExceeded"
    }
  ]
};
