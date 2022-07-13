import rsa
from .config import *


class EncryptionType:
    @staticmethod
    def generate_keys() -> tuple[bytes, bytes]:
        pass

    @staticmethod
    def encrypt_message(message: str, receiver_public_key: bytes) -> bytes:
        pass

    @staticmethod
    def decrypt_message(ciphertext: bytes, receiver_private_key: bytes):
        pass

    @staticmethod
    def sign(message: str, sender_private_key: bytes):
        return rsa.sign(message.encode('ascii'), rsa.PrivateKey.load_pkcs1(sender_private_key), 'SHA-1')

    @staticmethod
    def verify(message: str, signature, public_key: bytes):
        pass


class RSA(EncryptionType):
    @staticmethod
    def generate_keys() -> tuple[bytes, bytes]:
        public, private = rsa.newkeys(RSA_KEY_LENGTH)
        return public.save_pkcs1(), private.save_pkcs1()

    @staticmethod
    def encrypt_message(message: str, receiver_public_key: bytes) -> bytes:
        return rsa.encrypt(message.encode('ascii'), rsa.PublicKey.load_pkcs1(receiver_public_key))

    @staticmethod
    def decrypt_message(ciphertext: bytes, receiver_private_key: bytes):
        try:
            return rsa.decrypt(ciphertext, rsa.PrivateKey.load_pkcs1(receiver_private_key)).decode('ascii')
        except:
            return False

    @staticmethod
    def sign(message: str, sender_private_key: bytes):
        return rsa.sign(message.encode('ascii'), rsa.PrivateKey.load_pkcs1(sender_private_key), 'SHA-1')

    @staticmethod
    def verify(message: str, signature, public_key: bytes):
        try:
            return rsa.verify(message.encode('ascii'), signature, rsa.PublicKey.load_pkcs1(public_key), ) == 'SHA-1'
        except:
            return False
