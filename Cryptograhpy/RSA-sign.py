from hashlib import sha256
from RSA import RSA


class RSASignature:
    """Class produce and represents RSA digital signature."""

    def __init__(self, message, rsa):
        """
        Initialization of RSA signature algorithm.
        :param message: plain text(input in bytes)
        :param rsa: RSA algorithm implementation
        """
        self.message = message
        self.rsa = rsa
        self.public, self.private = self.rsa.get_key_pair()

    def encrypt_message(self):
        """
        Produces signature from a given hash.
        :return: encrypted hash / RSA digital signature
        """
        print("Generating your public & private keypairs now")
        print("Your public key is ", self.public, " and your private key is ", self.private)

        hashed = self.hash_function()
        encrypted_msg = self.rsa.encrypt(self.private, hashed)

        print("Your encrypted hashed message is: ")
        print(''.join(map(lambda x: str(x), encrypted_msg)))
        return encrypted_msg

    def decrypt_message(self, encrypted_msg):
        """
        Performs decryption of RSA digital signature.
        :param encrypted_msg:  RSA digital signature that will be converted into hash
        :return: decrypted hash
        """
        print("Decrypting message with public key ", self.public, " . . .")
        decrypted_msg = self.rsa.decrypt(self.public, encrypted_msg)

        print("Verification process...")
        return self.verify(decrypted_msg)

    def hash_function(self):
        """
        Simple hash function(SHA256 from hashlib) of message in bytes
        :return: hashed message in hex
        """
        hashed = sha256(self.message).hexdigest()
        return hashed

    def verify(self, received_hashed):
        """
        Verifying signature
        :param received_hashed: output from decrypt method
        :return: boolean flag of verification process
        """
        our_hashed = self.hash_function()
        if received_hashed == our_hashed:
            print("Verification successful: ", )
            print(received_hashed, " = ", our_hashed)
            return True
        else:
            print("Verification failed:(")
            print(received_hashed, " != ", our_hashed)
            return False


if __name__== "__main__":
        """ Small test with simple string for checking of RSA DS """
        p = 11
        q = 17

        message = b"Hello Bob, let's go to sauna"

        rsa = RSA(p, q)

        signature = RSASignature(message, rsa)
        cipher = signature.encrypt_message()
        print(signature.decrypt_message(cipher))