from decimal import Decimal
import random


class RSA:
    def __init__(self, p, q):
        self.N = p * q
        self.PHI = (p - 1) * (q - 1)

    @staticmethod
    def modpow(b, e, m):
        if m == 1:
            return 0
        result = 1
        base = b % m
        while e > 0:
            if e % 2 == 1:
                result = result*base % m
            e = Decimal(int(e) >> 1)
            base = base*base%m
        return result

    def get_key_pair(self):
        """
        Function to generate public and private keys
        - Choose two distinct prime numbers p and q
        - Compute p * q, it is a modulus in both keys,
        - Calculate  Carmichael's totient function(Euler`s totient) phi.
        It's a number of positive integers smaller than n which are coprime to n,
        - Choose c such that c and phi are coprime,
        - Find multiplicative inverse using extended Euclidean algorithm
        to find d,
        :return (c, n) - public key, (d, n) - private key
        """
        c = 3

        g, _, _ = self.extended_gcd(c, self.PHI)
        while g != 1:
            e = random.randrange(2, self.PHI)
            g, _, _ = self.extended_gcd(c, self.PHI)

        d, x, _ = self.extended_gcd(c, self.PHI)

        if x < 0:
            d = x + self.PHI
        else:
            d = x

        return (c, self.N), (d, self.N)

    @staticmethod
    def extended_gcd(a, b):
        """
        Extended Euclidean algorithm implementation
        :param a: first input for a*x + b*y = gcd
        :param b: second input for a*x + b*y = gcd
        :return: greatest common divisor, Bézout coefficients
        """
        x, old_x = 0, 1
        y, old_y = 1, 0

        while b != 0:
            quotient = a // b
            a, b = b, a - quotient * b
            old_x, x = x, old_x - quotient * x
            old_y, y = y, old_y - quotient * y

        return a, old_x, old_y

    def encrypt(self, key, byte_sequence):
        """
        Produces encrypted message from plaintext(in bytes)
        :param key: key for encryption(RSA - public, PSA signature - private)
        :param byte_sequence: input message in bytes
        :return: encrypted message by RSA
        """
        print(byte_sequence)
        exponent, mod = key
        self.divide_chunks(byte_sequence, 2)
        cipher = [self.modpow(ord(b), exponent, mod) for b in byte_sequence]
        return cipher

    @staticmethod
    def decrypt(key, ciphertext):
        """
        Produces decrypted message from encrypted(ciphertext)
        :param key: key for encryption(RSA - private, PSA signature - public)
        :param ciphertext: message to decrypt
        :return: decrypted message
        """
        exponent, mod = key
        plain = [chr(pow(char, exponent, mod)) for char in ciphertext]
        return ''.join(plain)

    @staticmethod
    def divide_chunks(arr, n):
        """
        Break a list into chunks of size N
        :param arr: list of bytes
        :param n: size of chunks
        :return: divided list
        """
        return [arr[i:i + n] for i in range(0, len(arr), n)]


if __name__== "__main__":
        """ Small test with simple string for checking of RSA DS """
        alice_p = 131
        alice_q = 227

        bob_p = 113
        bob_q = 281

        message = "Hello Bob, let's go to sauna"

        alice_rsa = RSA(alice_p, alice_q)
        bob_rsa = RSA(bob_p, bob_q)


        alice_public, alice_private = alice_rsa.get_key_pair()
        bob_public, bob_private = bob_rsa.get_key_pair()

        encrypted_msg = alice_rsa.encrypt(bob_public, message)
        print("Alice sends Bob message: ", message)
        print("Bob gets: ", encrypted_msg)
        decrypted_msg = bob_rsa.decrypt(bob_private, encrypted_msg)
        print("Bob decrypted: ", decrypted_msg)