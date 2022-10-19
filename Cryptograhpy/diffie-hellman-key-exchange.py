from decimal import *

def verify(n):
    if n.isdigit():
        return Decimal(n)
    print("Secret must be a number")
    exit(-1)


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

class DHKeyExchange:
    def __init__(self, p, g):
        self.p = p
        self.g = g

    def generate_public_key(self, a):
        return modpow(self.g, a, self.p)

    def generate_private_key(self, peer_public_key, a):
        return modpow(peer_public_key, a, self.p)


if __name__== "__main__":
    
    p = input("Enter p or leave blank for default settings: ")
    if p.isdigit():
        p = Decimal(p)
    else:
        p = Decimal('30803')

    g = input("Enter g or leave blank for default settings: ")
    if g.isdigit():
        g = Decimal(g)
    else:
        g = Decimal('2')
    
    diffie_hellman = DHKeyExchange(p, g)

    a = verify(input("Enter secret for Alice: "))
    alice_public_key = diffie_hellman.generate_public_key(a)
    print("Alice's public key:", alice_public_key)

    b = verify(input("Enter secret for Bob: "))
    bob_public_key = diffie_hellman.generate_public_key(b)
    print("Bob's public key:", bob_public_key)

    private_key = diffie_hellman.generate_private_key(alice_public_key, b)
    print("Shared private key is: ", private_key)
    print(diffie_hellman.generate_private_key(bob_public_key, a))