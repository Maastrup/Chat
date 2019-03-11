from Crypto.Cipher import AES

key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_ECB)
padding = 'acbdefghijklmnop'

plaintext = 'Dette er en meget super sindsygt krypteret besked'

if len(plaintext) % 16 != 0:
    missing_chars = 16 - len(plaintext) % 16
    plaintext += padding[:missing_chars]

ciphertext = cipher.encrypt(plaintext)

print(ciphertext)

plaintext = cipher.decrypt(ciphertext).decode()
print(plaintext)

