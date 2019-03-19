from Crypto.Cipher import AES
import pickle


class MyAES(AES.AESCipher):
    padding = 'acbdefghijklmnop'

    def __init__(self, key):
        super().__init__(key, AES.MODE_ECB)

    def pack(self, plaintext):
        byte_count = len(plaintext)
        missing_chars = 0
        # AES module works with number of bytes not letters and
        # danish vowels use up two bytes instead of the usual one byte
        for char in plaintext:
            if char in 'æøåÆØÅ':
                byte_count += 1
        # AES only works with string lengths that are multiples of 16
        if byte_count % 16 != 0:
            missing_chars = 16 - byte_count % 16
            plaintext += self.padding[:missing_chars]

        ciphertext = self.encrypt(plaintext)

        return pickle.dumps((missing_chars, ciphertext))

    def unpack(self, pickled_tuple):
        tuple = pickle.loads(pickled_tuple)
        plaintext = self.decrypt(tuple[1]).decode()
        plaintext = plaintext[:len(plaintext) - tuple[0]] # Removes padding
        return plaintext

""" Testing """
# crypto = MyAES(b'Sixteen byte key!ixteen byte key')
#
# plaintext = 'Hejsa med dig unge dansker æøå'
# print(plaintext)
#
# enc_msg = crypto.pack(plaintext)
# print(enc_msg)
#
#
# print(crypto.unpack(enc_msg))
