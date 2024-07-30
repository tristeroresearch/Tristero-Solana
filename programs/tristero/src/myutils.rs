pub fn vec_to_u128(v: [u8; 32]) -> u128{
    let mut arr = [0u8; 16];
    arr.copy_from_slice(&v[..16]);

    u128::from_be_bytes(arr)
}

pub fn vec_to_u64(v: [u8; 32]) -> u64{
    let mut arr = [0u8; 8];
    arr.copy_from_slice(&v[..8]);

    u64::from_be_bytes(arr)
}

pub fn vec_to_u32(v: [u8; 32]) -> u32{
    let mut arr = [0u8; 4];
    arr.copy_from_slice(&v[..4]);

    u32::from_be_bytes(arr)
}

pub fn vec_to_u16(v: [u8; 32]) -> u16{
    let mut arr = [0u8; 2];
    arr.copy_from_slice(&v[..2]);

    u16::from_be_bytes(arr)
}

pub fn vec_to_u8(v: [u8; 32]) -> u8{
    let mut arr = [0u8; 1];
    arr.copy_from_slice(&v[31..]);

    u8::from_be_bytes(arr)
}

pub fn split_into_chunks(v: Vec<u8>) -> Vec<[u8; 32]> {

    v.chunks(32)
        .map(|chunk| {
            let mut arr = [0u8; 32];
            arr.copy_from_slice(chunk);
            arr
        })
        .collect()
}