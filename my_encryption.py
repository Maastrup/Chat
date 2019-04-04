from Crypto.Cipher import AES
import secrets
import random
import pickle
import sys


# Rabin Miller testen, probabilistic
def rabin_miller(p, k):
    # Opskriv 2^t * r = p - 1 så r er ulige
    r = p - 1
    s = 0
    while r % 2 == 0:
        s += 1
        """ bitshifting to the right divides r by 2 but
            preserves int-type, floats screws up the test
            by lowering precision """
        r = r >> 1

    for i in range(k):
        a = random.randrange(2, p - 1)
        x = pow(a, r, p) # svarer til a**r % p
        if x != 1 and x != p - 1:
            j = 1
            while j < s and x != p - 1:
                x = pow(x, 2, p) # x**2 % p

                if x == 1: # IKKE et primtal
                    return False

                j += 1
            # IKKE et primtal
            if x != p - 1:
                return False
    return True


def gen_big_prime():
    p = 0
    count = 0

    while True:
        p = secrets.randbits(1024)

        if p % 2 == 0:
            p -= 1
        # # If prime table reveals compositness start over
        # if not prime_table_test(p):
        #     memo.append(p)
        #     continue
        if rabin_miller(p, 5):
            break

        count += 1

    print('Found a prime in {} tries'.format(count))
    return p


def gen_base():
    return secrets.randbits(128)


def prime_factors(s, n):
    while n % 2 == 0: # if LSB is 1
        s.append(2)
        n = n >> 1 # We are sure n can be divided by 2 and through >> 1 we preserve n's int-status

    print('')

    i = 3
    while n > 1:
        if n % i == 0:
            s.append(i)
            n //= i
        else:
            i += 2


def pack(plaintext, key):
    cipher = AES.new(key, AES.MODE_EAX)
    byte_string = bytes(plaintext, 'utf-8')

    ciphertext, tag = cipher.encrypt_and_digest(byte_string)
    print('\nSent:', ciphertext.hex())

    return pickle.dumps((cipher.nonce, ciphertext, tag))


def unpack(pickled_tuple, key):
    try:
        nonce, ciphertext, tag = pickle.loads(pickled_tuple)
        print('\nReceived:', ciphertext.hex())
    except EOFError:
        print('Program is closing')
        return
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except ValueError:
        print('MAC check failed')
        return -1
    except KeyError:
        print('Incorrect decryption')
        return -1


""" Testing """
