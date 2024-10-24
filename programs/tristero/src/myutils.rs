pub fn vec_to_u128(v: [u8; 32]) -> u128{
    let array = v.clone();
    let mut arr = [0u8; 16];
    arr.copy_from_slice(&array[16..]);

    u128::from_be_bytes(arr)
}

pub fn vec_to_u64(v: [u8; 32]) -> u64{
    let array = v.clone();
    let mut arr = [0u8; 8];
    arr.copy_from_slice(&array[24..]);

    u64::from_be_bytes(arr)
}

pub fn vec_to_u32(v: [u8; 32]) -> u32{
    let array = v.clone();
    let mut arr = [0u8; 4];
    arr.copy_from_slice(&array[28..]);

    u32::from_be_bytes(arr)
}

pub fn vec_to_u16(v: [u8; 32]) -> u16{
    let array = v.clone();
    let mut arr = [0u8; 2];
    arr.copy_from_slice(&array[30..]);

    u16::from_be_bytes(arr)
}

pub fn vec_to_u8(v: [u8; 32]) -> u8{
    let array = v.clone();
    let mut arr = [0u8; 1];
    arr.copy_from_slice(&array[31..]);

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