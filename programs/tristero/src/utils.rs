mod error;
use error::*;
pub fn vec_to_u128(v: Vec<u8>) -> u128{
    let mut arr = [0u8; 16];
    arr.copy_from_slice(&v);

    u128::from_be_bytes(arr)
}

pub fn vec_to_u64(v: Vec<u8>) -> u64{
    let mut arr = [0u8; 8];
    arr.copy_from_slice(&v);

    u64::from_be_bytes(arr)
}

pub fn vec_to_u32(v: Vec<u8>) -> u32{
    let mut arr = [0u8; 4];
    arr.copy_from_slice(&v);

    u32::from_be_bytes(arr)
}

pub fn vec_to_u16(v: Vec<u8>) -> u16{
    let mut arr = [0u8; 2];
    arr.copy_from_slice(&v);

    u16::from_be_bytes(arr)
}

pub fn vec_to_u8(v: Vec<u8>) -> u8{
    let mut arr = [0u8; 1];
    arr.copy_from_slice(&v);

    u8::from_be_bytes(arr)
}

pub fn split_into_chunks(v: Vec<u8>) -> Vec<[u8; 32]> {
    require!(v.len() % 32 == 0, CustomError::WrongMsgTypeError);

    v.chunks(32)
        .map(|chunk| {
            let mut arr = [0u8; 32];
            arr.copy_from_slice(chunk);
            arr
        })
        .collect()
}