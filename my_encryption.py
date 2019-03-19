from Crypto.Cipher import AES
import pickle


class MyAES(AES):
    padding = 'acbdefghijklmnop'

    def __init__(self, key):
        self.cipher = super().new(key, AES.MODE_ECB)

    def pack(self, plaintext):
        byte_count = len(plaintext)
        # AES module works with number of bytes not letters and
        # danish vowels use up two bytes instead of the usual one byte
        for char in plaintext:
            if char in 'æøåÆØÅ':
                byte_count += 1
        # AES only works with string lengths that are multiples of 16
        if byte_count % 16 != 0:
            missing_chars = 16 - byte_count % 16
            plaintext += padding[:missing_chars]

        ciphertext = self.cipher.encrypt(plaintext)

        return pickle.dumps((missing_chars, ciphertext))

    def unpack(self, pickled_tuple):
        tuple = pickle.loads(pickled_tuple)
        plaintext = self.cipher.decrypt(tuple[1]).decode()
        plaintext = plaintext[:len(plaintext) - tuple[0]] # Removes padding
        return plaintext


key = b'Sixteen byte keySixteen byte key'
cipher = AES.new(key, AES.MODE_ECB)
padding = 'acbdefghijklmnop'


def pack(plaintext):
    byte_count = len(plaintext)
    # AES module works with number of bytes not letters and
    # danish vowels use up two bytes instead of the usual one byte
    for char in plaintext:
        if char in 'æøåÆØÅ':
            byte_count += 1
    # AES only works with string lengths that are multiples of 16
    if byte_count % 16 != 0:
        missing_chars = 16 - byte_count % 16
        plaintext += padding[:missing_chars]

    ciphertext = cipher.encrypt(plaintext)
    return pickle.dumps((missing_chars, ciphertext))


def unpack(pickled_tuple):
    tuple = pickle.loads(pickled_tuple)
    plaintext = cipher.decrypt(tuple[1])
    plaintext = plaintext[:len(plaintext) - tuple[0]]
    return plaintext


plaintext = 'Hejsa med dig unge dansker æøå'
print(plaintext)

enc_msg = pack(plaintext)
print(enc_msg)


print(unpack(enc_msg))
