"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.IDL = void 0;
exports.IDL = {
    "version": "0.1.0",
    "name": "pricefeed",
    "instructions": [
        {
            "name": "initPriceFeed",
            "docs": [
                "--------------------------- Admin Instructions ---------------------------"
            ],
            "accounts": [
                {
                    "name": "payer",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "priceFeed",
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
                        "defined": "InitPriceFeedParams"
                    }
                }
            ]
        },
        {
            "name": "setPriceFeed",
            "accounts": [
                {
                    "name": "admin",
                    "isMut": true,
                    "isSigner": true
                },
                {
                    "name": "priceFeed",
                    "isMut": true,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "SetPriceFeedParams"
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
                    "name": "priceFeed",
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
            "name": "setPrice",
            "docs": [
                "--------------------------- Updater Instructions --------------------------"
            ],
            "accounts": [
                {
                    "name": "updater",
                    "isMut": false,
                    "isSigner": true
                },
                {
                    "name": "priceFeed",
                    "isMut": true,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "SetPriceParams"
                    }
                }
            ]
        },
        {
            "name": "setSolPrice",
            "accounts": [
                {
                    "name": "updater",
                    "isMut": false,
                    "isSigner": true
                },
                {
                    "name": "priceFeed",
                    "isMut": true,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "SetSolPriceParams"
                    }
                }
            ]
        },
        {
            "name": "getFee",
            "docs": [
                "--------------------------- Getter Instructions ---------------------------"
            ],
            "accounts": [
                {
                    "name": "priceFeed",
                    "isMut": false,
                    "isSigner": false
                }
            ],
            "args": [
                {
                    "name": "params",
                    "type": {
                        "defined": "GetFeeParams"
                    }
                }
            ]
        }
    ],
    "accounts": [
        {
            "name": "priceFeed",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "admin",
                        "type": "publicKey"
                    },
                    {
                        "name": "updaters",
                        "type": {
                            "vec": "publicKey"
                        }
                    },
                    {
                        "name": "priceRatioDenominator",
                        "type": "u128"
                    },
                    {
                        "name": "arbitrumCompressionPercent",
                        "type": "u128"
                    },
                    {
                        "name": "nativeTokenPriceUsd",
                        "type": {
                            "option": "u128"
                        }
                    },
                    {
                        "name": "prices",
                        "type": {
                            "vec": {
                                "defined": "Price"
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
            "name": "InitPriceFeedParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "admin",
                        "type": "publicKey"
                    },
                    {
                        "name": "updaters",
                        "type": {
                            "vec": "publicKey"
                        }
                    }
                ]
            }
        },
        {
            "name": "SetPriceFeedParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "updaters",
                        "type": {
                            "vec": "publicKey"
                        }
                    },
                    {
                        "name": "priceRatioDenominator",
                        "type": "u128"
                    },
                    {
                        "name": "arbitrumCompressionPercent",
                        "type": "u128"
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
            "name": "GetFeeParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "dstEid",
                        "type": "u32"
                    },
                    {
                        "name": "calldataSize",
                        "type": "u64"
                    },
                    {
                        "name": "totalGas",
                        "type": "u128"
                    }
                ]
            }
        },
        {
            "name": "PriceParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "priceRatio",
                        "type": "u128"
                    },
                    {
                        "name": "gasPriceInUnit",
                        "type": "u64"
                    },
                    {
                        "name": "gasPerByte",
                        "type": "u32"
                    },
                    {
                        "name": "modelType",
                        "type": {
                            "option": {
                                "defined": "ModelType"
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "SetPriceParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "dstEid",
                        "type": "u32"
                    },
                    {
                        "name": "params",
                        "type": {
                            "option": {
                                "defined": "PriceParams"
                            }
                        }
                    }
                ]
            }
        },
        {
            "name": "SetSolPriceParams",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "nativeTokenPriceUsd",
                        "type": {
                            "option": "u128"
                        }
                    }
                ]
            }
        },
        {
            "name": "ModelType",
            "type": {
                "kind": "enum",
                "variants": [
                    {
                        "name": "Arbitrum",
                        "fields": [
                            {
                                "name": "gasPerL2Tx",
                                "type": "u64"
                            },
                            {
                                "name": "gasPerL1CalldataByte",
                                "type": "u32"
                            }
                        ]
                    },
                    {
                        "name": "Optimism",
                        "fields": [
                            {
                                "name": "l1Eid",
                                "type": "u32"
                            }
                        ]
                    }
                ]
            }
        },
        {
            "name": "Price",
            "type": {
                "kind": "struct",
                "fields": [
                    {
                        "name": "eid",
                        "type": "u32"
                    },
                    {
                        "name": "priceRatio",
                        "type": "u128"
                    },
                    {
                        "name": "gasPriceInUnit",
                        "type": "u64"
                    },
                    {
                        "name": "gasPerByte",
                        "type": "u32"
                    },
                    {
                        "name": "modelType",
                        "type": {
                            "option": {
                                "defined": "ModelType"
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
            "name": "TooManyUpdaters"
        },
        {
            "code": 6001,
            "name": "InvalidUpdater"
        },
        {
            "code": 6002,
            "name": "NotFound"
        },
        {
            "code": 6003,
            "name": "InvalidSize"
        }
    ]
};
