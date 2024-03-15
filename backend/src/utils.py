# https://pypi.org/project/bitcoin/
from bitcoin import ecdsa_verify
import ecdsa
import hashlib
import os
from dotenv import load_dotenv
from Crypto.Hash import SHA256, RIPEMD160
import base58
import re
from bech32 import bech32_encode, convertbits


load_dotenv()

# https://github.com/BRO200BS/Bitcoin-Address-Generator/blob/main/Gen.py
# https://pypi.org/project/bitcoinaddress/


def verify_message(address, signature, message):

    check_signature = os.getenv('CHECK_SIGNATURE')
    if check_signature == 'False':
        return True

    if not address or not signature or not message:
        return False

    """
    Verify a message signed by a Bitcoin private key.

    :param address: The Bitcoin address as a string.
    :param signature: The signature as a string.
    :param message: The message as a string.
    :return: True if the signature is valid, False otherwise.
    """
    # # Convert the address to a public key
    # public_key = P2PKHBitcoinAddress(address).to_redeemScript()
    # # Create a BitcoinMessage object
    # bitcoin_message = BitcoinMessage(message)
    # # Verify the message
    # return VerifyMessage(public_key, signature, bitcoin_message)

    message_hash = hashlib.sha256(message.encode()).digest()
    public_key = ecdsa.VerifyingKey.from_string(
        bytes.fromhex(address), curve=ecdsa.SECP256k1)
    signature = bytes.fromhex(signature)
    verify_message = public_key.verify(signature, message_hash)

    return ecdsa_verify(message, signature, address)


def generate_bitcoin_address():
    # Generate private key
    private_key = os.urandom(32)
    fullkey = '80' + private_key.hex()
    sha256a = SHA256.new(bytes.fromhex(fullkey)).hexdigest()
    sha256b = SHA256.new(bytes.fromhex(sha256a)).hexdigest()
    WIF = base58.b58encode(bytes.fromhex(fullkey + sha256b[:8]))

    # Get public key
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    public_key = '04' + x.to_bytes(32, 'big').hex() + \
        y.to_bytes(32, 'big').hex()

    # Get compressed public key
    compressed_public_key = '02' if y % 2 == 0 else '03'
    compressed_public_key += x.to_bytes(32, 'big').hex()

    # Get P2PKH address
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(public_key)).digest())
    public_key_hash = '00' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(
        public_key_hash)).digest()).hexdigest()[:8]
    p2pkh_address = base58.b58encode(bytes.fromhex(public_key_hash + checksum))

    # Get compressed P2PKH address
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(compressed_public_key)).digest())
    public_key_hash = '00' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(
        public_key_hash)).digest()).hexdigest()[:8]
    compressed_p2pkh_address = base58.b58encode(
        bytes.fromhex(public_key_hash + checksum))

    # Get P2SH address
    redeem_script = '21' + compressed_public_key + 'ac'
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(redeem_script)).digest())
    script_hash = '05' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(
        bytes.fromhex(script_hash)).digest()).hexdigest()[:8]
    p2sh_address = base58.b58encode(bytes.fromhex(script_hash + checksum))

    # Get Bech32 address
    witness_program = bytes([0x00, 0x14]) + hash160.digest()
    bech32_address = bech32_encode('bc', convertbits(witness_program, 8, 5))

    return {
        'private_key': private_key.hex(),
        'WIF': WIF.decode(),
        'public_key': public_key,
        'compressed_public_key': compressed_public_key,
        'p2pkh_address': p2pkh_address.decode(),
        'compressed_p2pkh_address': compressed_p2pkh_address.decode(),
        'p2sh_address': p2sh_address.decode(),
        'bech32_address': bech32_address
    }

def is_hex(s):
    hex_pattern = r'^0x[0-9a-fA-F]+$|^0X[0-9a-fA-F]+$|^[0-9a-fA-F]+$'
    if re.match(hex_pattern, s):
        return True
    else:
        return False