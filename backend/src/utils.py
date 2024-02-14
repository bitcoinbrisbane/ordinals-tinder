# https://pypi.org/project/bitcoin/
from bitcoin import ecdsa_verify


def verify_message(address, signature, message):
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

    return ecdsa_verify(message, signature, address)
