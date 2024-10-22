const SEND_TO_OFFSET: usize = 0;
const SEND_AMOUNT_SD_OFFSET: usize = 32;
const COMPOSE_MSG_OFFSET: usize = 40;

pub fn encode(
    compose_msg: &Option<Vec<u8>>,
) -> Vec<u8> {
    let mut length = 0u64;
    if let Some(msg) = compose_msg {
        length = (msg.len() * 2) as u64;
        let mut encoded: Vec<u8> = Vec::new();
        for _ in 0..8 {
            encoded.push(0u8);
        }
        length.to_be_bytes().map(|value| encoded.push(value));
        encoded.extend_from_slice(&msg);
        encoded
    } else {
        let mut encoded:Vec<u8> = Vec::new(); // 32 + 8
        length.to_be_bytes().map(|value| encoded.push(value));
        encoded
    }
}

pub fn send_to(message: &[u8]) -> [u8; 32] {
    let mut send_to = [0; 32];
    send_to.copy_from_slice(&message[SEND_TO_OFFSET..SEND_AMOUNT_SD_OFFSET]);
    send_to
}

pub fn amount_sd(message: &[u8]) -> u64 {
    let mut amount_sd_bytes = [0; 8];
    amount_sd_bytes.copy_from_slice(&message[SEND_AMOUNT_SD_OFFSET..COMPOSE_MSG_OFFSET]);
    u64::from_be_bytes(amount_sd_bytes)
}

pub fn compose_msg(message: &[u8]) -> Option<Vec<u8>> {
    if message.len() > COMPOSE_MSG_OFFSET {
        Some(message[COMPOSE_MSG_OFFSET..].to_vec())
    } else {
        None
    }
}
