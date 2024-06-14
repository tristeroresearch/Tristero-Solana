export type MessagelibInterface = {
  "version": "0.1.0",
  "name": "messagelib_interface",
  "instructions": [
    {
      "name": "send",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
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
          "isSigner": true
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
          "isSigner": true
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
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
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
    }
  ]
};

export const IDL: MessagelibInterface = {
  "version": "0.1.0",
  "name": "messagelib_interface",
  "instructions": [
    {
      "name": "send",
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
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
          "isSigner": true
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
          "isSigner": true
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
      "accounts": [
        {
          "name": "endpoint",
          "isMut": false,
          "isSigner": true
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
    }
  ]
};
