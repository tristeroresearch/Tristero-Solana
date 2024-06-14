export type SimpleMessagelib = {
  "version": "0.1.0",
  "name": "simple_messagelib",
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
      "name": "initMessageLib",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
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
            "defined": "InitMessageLibParams"
          }
        }
      ]
    },
    {
      "name": "transferAdmin",
      "docs": [
        "--------------------------- Admin Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
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
      "name": "setWlCaller",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetWlCallerParams"
          }
        }
      ]
    },
    {
      "name": "setFee",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetFeeParams"
          }
        }
      ]
    },
    {
      "name": "withdrawFees",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiver",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "WithdrawFeesParams"
          }
        }
      ]
    },
    {
      "name": "initDefaultConfig",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "InitDefaultConfigParams"
          }
        }
      ]
    },
    {
      "name": "setDefaultConfig",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "SetDefaultConfigParams"
          }
        }
      ]
    },
    {
      "name": "validatePacket",
      "docs": [
        "--------------------------- WhitelistedCaller Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "payer",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "receiveLibrary",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "ValidatePacketParams"
          }
        }
      ]
    },
    {
      "name": "send",
      "docs": [
        "--------------------------- Endpoint Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "receive the native fee"
          ]
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "pay for the native fee"
          ]
        },
        {
          "name": "systemProgram",
          "isMut": false,
          "isSigner": false,
          "docs": [
            "for native fee transfer"
          ]
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SendParams"
          }
        }
      ]
    },
    {
      "name": "sendWithLzToken",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "receive the native fee"
          ]
        },
        {
          "name": "messageLibLzToken",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "pay for the native fee"
          ]
        },
        {
          "name": "lzTokenSource",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "The token account to pay the lz token fee"
          ]
        },
        {
          "name": "lzTokenMint",
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
          "isSigner": false,
          "docs": [
            "for native fee transfer"
          ]
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SendWithLzTokenParams"
          }
        }
      ]
    },
    {
      "name": "quote",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
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
      "name": "initConfig",
      "docs": [
        "--------------------------- Endpoint Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "InitConfigParams"
          }
        }
      ]
    },
    {
      "name": "setConfig",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetConfigParams"
          }
        }
      ]
    },
    {
      "name": "revertCall",
      "docs": [
        "--------------------------- For Test ---------------------------"
      ],
      "accounts": [],
      "args": []
    }
  ],
  "accounts": [
    {
      "name": "messageLib",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "endpoint",
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
            "name": "fee",
            "type": "u64"
          },
          {
            "name": "lzTokenFee",
            "type": "u64"
          },
          {
            "name": "wlCaller",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "receiveConfigStore",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "data",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "sendConfigStore",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "data",
            "type": "bytes"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "InitConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oapp",
            "type": "publicKey"
          },
          {
            "name": "eid",
            "type": "u32"
          }
        ]
      }
    },
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
      "name": "Packet",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "nonce",
            "type": "u64"
          },
          {
            "name": "srcEid",
            "type": "u32"
          },
          {
            "name": "sender",
            "type": "publicKey"
          },
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
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "payInLzToken",
            "type": "bool"
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
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "nativeFee",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "SendWithLzTokenParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
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
          },
          {
            "name": "lzTokenMint",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "SetConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oapp",
            "type": "publicKey"
          },
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "configType",
            "type": "u32"
          },
          {
            "name": "config",
            "type": "bytes"
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
            "name": "major",
            "type": "u64"
          },
          {
            "name": "minor",
            "type": "u8"
          },
          {
            "name": "endpointVersion",
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "InitDefaultConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "sendConfig",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "receiveConfig",
            "type": {
              "option": "bytes"
            }
          }
        ]
      }
    },
    {
      "name": "InitMessageLibParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "endpoint",
            "type": "publicKey"
          },
          {
            "name": "endpointProgram",
            "type": "publicKey"
          },
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "fee",
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
      "name": "SetDefaultConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "sendConfig",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "receiveConfig",
            "type": {
              "option": "bytes"
            }
          }
        ]
      }
    },
    {
      "name": "SetFeeParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "fee",
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
      "name": "SetWlCallerParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "newCaller",
            "type": "publicKey"
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
      "name": "WithdrawFeesParams",
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
      "name": "ValidatePacketParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "packet",
            "type": "bytes"
          }
        ]
      }
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "OnlyWhitelistedCaller"
    },
    {
      "code": 6001,
      "name": "InsufficientFee"
    },
    {
      "code": 6002,
      "name": "InvalidAmount"
    },
    {
      "code": 6003,
      "name": "InvalidConfigType"
    },
    {
      "code": 6004,
      "name": "InvalidLzTokenMint"
    },
    {
      "code": 6005,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6006,
      "name": "SendReentrancy"
    },
    {
      "code": 6007,
      "name": "OnlyRevert"
    }
  ]
};

export const IDL: SimpleMessagelib = {
  "version": "0.1.0",
  "name": "simple_messagelib",
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
      "name": "initMessageLib",
      "accounts": [
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
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
            "defined": "InitMessageLibParams"
          }
        }
      ]
    },
    {
      "name": "transferAdmin",
      "docs": [
        "--------------------------- Admin Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
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
      "name": "setWlCaller",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetWlCallerParams"
          }
        }
      ]
    },
    {
      "name": "setFee",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetFeeParams"
          }
        }
      ]
    },
    {
      "name": "withdrawFees",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiver",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "WithdrawFeesParams"
          }
        }
      ]
    },
    {
      "name": "initDefaultConfig",
      "accounts": [
        {
          "name": "admin",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "InitDefaultConfigParams"
          }
        }
      ]
    },
    {
      "name": "setDefaultConfig",
      "accounts": [
        {
          "name": "admin",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "SetDefaultConfigParams"
          }
        }
      ]
    },
    {
      "name": "validatePacket",
      "docs": [
        "--------------------------- WhitelistedCaller Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "payer",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "receiveLibrary",
          "isMut": false,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "ValidatePacketParams"
          }
        }
      ]
    },
    {
      "name": "send",
      "docs": [
        "--------------------------- Endpoint Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "receive the native fee"
          ]
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "pay for the native fee"
          ]
        },
        {
          "name": "systemProgram",
          "isMut": false,
          "isSigner": false,
          "docs": [
            "for native fee transfer"
          ]
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SendParams"
          }
        }
      ]
    },
    {
      "name": "sendWithLzToken",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "receive the native fee"
          ]
        },
        {
          "name": "messageLibLzToken",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "pay for the native fee"
          ]
        },
        {
          "name": "lzTokenSource",
          "isMut": true,
          "isSigner": false,
          "docs": [
            "The token account to pay the lz token fee"
          ]
        },
        {
          "name": "lzTokenMint",
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
          "isSigner": false,
          "docs": [
            "for native fee transfer"
          ]
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SendWithLzTokenParams"
          }
        }
      ]
    },
    {
      "name": "quote",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true,
          "docs": [
            "The message lib authority of the endpoint"
          ]
        },
        {
          "name": "messageLib",
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
      "name": "initConfig",
      "docs": [
        "--------------------------- Endpoint Instructions ---------------------------"
      ],
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "payer",
          "isMut": true,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
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
            "defined": "InitConfigParams"
          }
        }
      ]
    },
    {
      "name": "setConfig",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
        },
        {
          "name": "messageLib",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendConfig",
          "isMut": true,
          "isSigner": false
        },
        {
          "name": "receiveConfig",
          "isMut": true,
          "isSigner": false
        }
      ],
      "args": [
        {
          "name": "params",
          "type": {
            "defined": "SetConfigParams"
          }
        }
      ]
    },
    {
      "name": "revertCall",
      "docs": [
        "--------------------------- For Test ---------------------------"
      ],
      "accounts": [],
      "args": []
    }
  ],
  "accounts": [
    {
      "name": "messageLib",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "endpoint",
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
            "name": "fee",
            "type": "u64"
          },
          {
            "name": "lzTokenFee",
            "type": "u64"
          },
          {
            "name": "wlCaller",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "receiveConfigStore",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "data",
            "type": "bytes"
          }
        ]
      }
    },
    {
      "name": "sendConfigStore",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "bump",
            "type": "u8"
          },
          {
            "name": "data",
            "type": "bytes"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "InitConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oapp",
            "type": "publicKey"
          },
          {
            "name": "eid",
            "type": "u32"
          }
        ]
      }
    },
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
      "name": "Packet",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "nonce",
            "type": "u64"
          },
          {
            "name": "srcEid",
            "type": "u32"
          },
          {
            "name": "sender",
            "type": "publicKey"
          },
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
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "payInLzToken",
            "type": "bool"
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
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
          },
          {
            "name": "options",
            "type": "bytes"
          },
          {
            "name": "nativeFee",
            "type": "u64"
          }
        ]
      }
    },
    {
      "name": "SendWithLzTokenParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "packet",
            "type": {
              "defined": "Packet"
            }
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
          },
          {
            "name": "lzTokenMint",
            "type": "publicKey"
          }
        ]
      }
    },
    {
      "name": "SetConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "oapp",
            "type": "publicKey"
          },
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "configType",
            "type": "u32"
          },
          {
            "name": "config",
            "type": "bytes"
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
            "name": "major",
            "type": "u64"
          },
          {
            "name": "minor",
            "type": "u8"
          },
          {
            "name": "endpointVersion",
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "InitDefaultConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "sendConfig",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "receiveConfig",
            "type": {
              "option": "bytes"
            }
          }
        ]
      }
    },
    {
      "name": "InitMessageLibParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "endpoint",
            "type": "publicKey"
          },
          {
            "name": "endpointProgram",
            "type": "publicKey"
          },
          {
            "name": "admin",
            "type": "publicKey"
          },
          {
            "name": "fee",
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
      "name": "SetDefaultConfigParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "eid",
            "type": "u32"
          },
          {
            "name": "sendConfig",
            "type": {
              "option": "bytes"
            }
          },
          {
            "name": "receiveConfig",
            "type": {
              "option": "bytes"
            }
          }
        ]
      }
    },
    {
      "name": "SetFeeParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "fee",
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
      "name": "SetWlCallerParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "newCaller",
            "type": "publicKey"
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
      "name": "WithdrawFeesParams",
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
      "name": "ValidatePacketParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "packet",
            "type": "bytes"
          }
        ]
      }
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "OnlyWhitelistedCaller"
    },
    {
      "code": 6001,
      "name": "InsufficientFee"
    },
    {
      "code": 6002,
      "name": "InvalidAmount"
    },
    {
      "code": 6003,
      "name": "InvalidConfigType"
    },
    {
      "code": 6004,
      "name": "InvalidLzTokenMint"
    },
    {
      "code": 6005,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6006,
      "name": "SendReentrancy"
    },
    {
      "code": 6007,
      "name": "OnlyRevert"
    }
  ]
};
