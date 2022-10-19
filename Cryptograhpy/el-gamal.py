from decimal import Decimal
import random

class ElGamal:
    def __init__(self):
        self.p = 30803
        self.g = 2

    @staticmethod
    def modpow(b, e, m):
        if m == 1:
            return 0
        result = 1
        base = b % m
        while e > 0:
            if e % 2 == 1:
                result = result * base % m
            e = Decimal(int(e) >> 1)
            base = base * base % m
        return result

    def get_key_pair(self):
        """
        Function to generate public and private keys
        :return c - public key, d - private key
        """
        rangeStart = 2
        rangeEnd = self.p - 1
        c = random.randint(rangeStart, rangeEnd)
        d = self.modpow(self.g, c, self.p)

        return (d, c)

    def encrypt(self, public, m):
        """
        
        :return: encrypted message by El Gamal chiper
        """
        rangeStart = 2
        rangeEnd = self.p - 1
        r = random.randint(rangeStart, rangeEnd)

        k = self.modpow(self.g, r, self.p)
        x = self.modpow(m * pow(public, r), 1, self.p)

        return (k, x)

    def decrypt(self, private, m):
        k, x = m
        decrypted = self.modpow(x * pow(k, (self.p - 1) - private), 1, self.p)
        return decrypted


if __name__== "__main__":
        """ Small test with simple string for checking of RSA DS """
        e = ElGamal()

        alice_public, alice_private = e.get_key_pair()
        bob_public, bob_private = e.get_key_pair()

        message = 3243

        print("Alice sends Bob message: ", message)
        encrypted_msg = e.encrypt(bob_public, message)
        print("Bob gets: ", encrypted_msg)
        decrypted_msg = e.decrypt(bob_private, encrypted_msg)
        print("Bob decrypted: ", decrypted_msg)