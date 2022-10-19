from decimal import Decimal
import random

def bprint(decimal):
    print(bin(decimal)[2:])

class MiniPoker:
    def __init__(self, p, cards):
        self.p = p
        self.cards = cards
        self.rs = []
        self.R = []
        for i in range(len(cards)):
            self.rs.append(random.randrange(1, self.p // 4))
            self.R.append(bin(self.rs[i])[2:] + cards[i])

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
        """
        c = random.randrange(2, self.p - 1)

        g, _, _ = self.extended_gcd(c, self.p - 1)
        while g != 1:
            c = random.randrange(2, self.p - 1)
            g, _, _ = self.extended_gcd(c, self.p - 1)

        d, x, _ = self.extended_gcd(c, self.p - 1)

        if x < 0:
            d = x + self.p - 1
        else:
            d = x

        return (d, c)

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

    def calculate_x(self, private):
        x = []

        for R in self.R:
            x.append(self.modpow(int(R, 2), private, self.p))
        random.shuffle(x)
        return x

    def calculate_y(self, private, cards):
        y = []
        for card in cards:
            y.append(self.modpow(card, private, self.p))
        random.shuffle(y)
        return y


if __name__== "__main__":
        """ Small test with simple string for checking of RSA DS """
        p = 23
        cards = ['00', '01', '10']
        cards_names = {'00':"A", '01':"B", '10':"C"}
        print("cards: ", cards_names)

        message = "Hello Bob, let's go to sauna"

        poker = MiniPoker(p, cards)

        alice_public, alice_private = poker.get_key_pair()
        bob_public, bob_private = poker.get_key_pair()

        alice_public, alice_private = 15, 3
        bob_public, bob_private = 9, 5

        xs = poker.calculate_x(alice_private)
        bob_choice = random.choice(xs)
        Alices_card = poker.modpow(bob_choice, alice_public, p)
        print("Alice gets card:", cards_names[bin(Alices_card)[-2:]])
        xs.remove(bob_choice)

        alice_choice = random.choice(poker.calculate_y(bob_private, xs))
        card = poker.modpow(alice_choice, alice_public, p)
        Bobs_card = poker.modpow(card, bob_public, p)
        print("Bob gets card: ", cards_names[bin(Bobs_card)[-2:]])