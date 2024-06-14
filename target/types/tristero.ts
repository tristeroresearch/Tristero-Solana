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
      "name": "tristeroInitSendLibrary",
      "accounts": [
        {
          "name": "delegate",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "only the delegate can initialize the send_library_config"
          ]
        },
        {
          "name": "oappRegistry",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendLibraryConfig",
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
            "defined": "TristeroInitSendLibraryParams"
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
    }
  ],
  "types": [
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
      "name": "TristeroInitSendLibraryParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sender",
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
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "InvalidSendLibrary"
    },
    {
      "code": 6001,
      "name": "InvalidReceiveLibrary"
    },
    {
      "code": 6002,
      "name": "SameValue"
    },
    {
      "code": 6003,
      "name": "AccountNotFound"
    },
    {
      "code": 6004,
      "name": "OnlySendLib"
    },
    {
      "code": 6005,
      "name": "OnlyReceiveLib"
    },
    {
      "code": 6006,
      "name": "InvalidExpiry"
    },
    {
      "code": 6007,
      "name": "OnlyNonDefaultLib"
    },
    {
      "code": 6008,
      "name": "InvalidAmount"
    },
    {
      "code": 6009,
      "name": "InvalidNonce"
    },
    {
      "code": 6010,
      "name": "Unauthorized"
    },
    {
      "code": 6011,
      "name": "PayloadHashNotFound"
    },
    {
      "code": 6012,
      "name": "ComposeNotFound"
    },
    {
      "code": 6013,
      "name": "InvalidPayloadHash"
    },
    {
      "code": 6014,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6015,
      "name": "ReadOnlyAccount"
    },
    {
      "code": 6016,
      "name": "InvalidMessageLib"
    },
    {
      "code": 6017,
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
      "name": "tristeroInitSendLibrary",
      "accounts": [
        {
          "name": "delegate",
          "isMut": true,
          "isSigner": true,
          "docs": [
            "only the delegate can initialize the send_library_config"
          ]
        },
        {
          "name": "oappRegistry",
          "isMut": false,
          "isSigner": false
        },
        {
          "name": "sendLibraryConfig",
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
            "defined": "TristeroInitSendLibraryParams"
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
    }
  ],
  "types": [
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
      "name": "TristeroInitSendLibraryParams",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "sender",
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
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "InvalidSendLibrary"
    },
    {
      "code": 6001,
      "name": "InvalidReceiveLibrary"
    },
    {
      "code": 6002,
      "name": "SameValue"
    },
    {
      "code": 6003,
      "name": "AccountNotFound"
    },
    {
      "code": 6004,
      "name": "OnlySendLib"
    },
    {
      "code": 6005,
      "name": "OnlyReceiveLib"
    },
    {
      "code": 6006,
      "name": "InvalidExpiry"
    },
    {
      "code": 6007,
      "name": "OnlyNonDefaultLib"
    },
    {
      "code": 6008,
      "name": "InvalidAmount"
    },
    {
      "code": 6009,
      "name": "InvalidNonce"
    },
    {
      "code": 6010,
      "name": "Unauthorized"
    },
    {
      "code": 6011,
      "name": "PayloadHashNotFound"
    },
    {
      "code": 6012,
      "name": "ComposeNotFound"
    },
    {
      "code": 6013,
      "name": "InvalidPayloadHash"
    },
    {
      "code": 6014,
      "name": "LzTokenUnavailable"
    },
    {
      "code": 6015,
      "name": "ReadOnlyAccount"
    },
    {
      "code": 6016,
      "name": "InvalidMessageLib"
    },
    {
      "code": 6017,
      "name": "WritableAccountNotAllowed"
    }
  ]
};
