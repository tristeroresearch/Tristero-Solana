## Prerequisites

- [rust](https://www.rust-lang.org/tools/install) (nightly)
- [solana](https://docs.solana.com/cli/install-solana-cli-tools) (v1.17.31)
- [anchor](https://book.anchor-lang.com/getting_started/installation.html) (v0.29.0)
- [jq](https://stedolan.github.io/jq/download/)

-python version: 3.10

## Install

`anchor build` will install the dependencies automatically. If you want to install the dependencies manually, run the following command:

```shell
rustup default nightly
```

## Build

```shell
anchor build
```

## Test

```shell
yarn test
```

or

```shell
TEST_SCOPES=uln yarn test
```

or

```shell
anchor test --skip-build
```

## deploy

```shell
anchor deploy -p tristero
```


## test with python
python3.10 ./test-python/test.py