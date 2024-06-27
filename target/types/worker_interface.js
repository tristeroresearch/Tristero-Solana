"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IDL = void 0;
exports.IDL = {
    "version": "0.1.0",
    "name": "worker_interface",
    "instructions": [
        {
            "name": "quoteExecutor",
            "accounts": [
                {
                    "name": "workerConfig",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "priceFeedProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "priceFeedConfig",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "QuoteExecutorParams"
                    }
                }
            ],
            "returns": "u64"
        },
        {
            "name": "quoteDvn",
            "accounts": [
                {
                    "name": "workerConfig",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "priceFeedProgram",
                    "isMut": false,
                    "isSigner": false
                },
                {
                    "name": "priceFeedConfig",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "QuoteDvnParams"
                    }
                }
            ],
            "returns": "u64"
        }
    ],
    "types": [
        {
            "name": "LzOption",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "optionType",
                        "type": "u8"
                    },
                    {
                        "name": "params",
                        "type": "bytes"
                    }
                ]
            }
        },
        {
            "name": "QuoteDvnParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "msglib",
                        "type": "publicKey"
                    },
                    {
                        "name": "dstEid",
                        "type": "u32"
                    },
                    {
                        "name": "sender",
                        "type": "publicKey"
                    },
                    {
                        "name": "packetHeader",
                        "type": "bytes"
                    },
                    {
                        "name": "payloadHash",
                        "type": {
                            "array": [
                                "u8",
                                32
                            ]
                        }
                    },
                    {
                        "name": "confirmations",
                        "type": "u64"
                    },
                    {
                        "name": "options",
                        "type": {
                            "vec": {
                                "defined": "LzOption"
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "QuoteExecutorParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "msglib",
                        "type": "publicKey"
                    },
                    {
                        "name": "dstEid",
                        "type": "u32"
                    },
                    {
                        "name": "sender",
                        "type": "publicKey"
                    },
                    {
                        "name": "calldataSize",
                        "type": "u64"
                    },
                    {
                        "name": "options",
                        "type": {
                            "vec": {
                                "defined": "LzOption"
                            }
                        }
                    }
                ]
            }
        }
    ],
    "errors": [
        {
            "code": 6000,
            "name": "PermissionDenied"
        },
        {
            "code": 6001,
            "name": "InvalidSize"
        }
    ]
};
