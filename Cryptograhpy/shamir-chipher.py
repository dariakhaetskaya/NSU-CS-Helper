import random
import math

class ShamirChipher:
    def __init__(self, p):
        self.p = p
        self.ca = 0
        self.da = 0
        self.cb = 0
        self.db = 0

    @staticmethod
    def modpow(b, e, m):
        if m == 1:
            return 0
        result = 1
        base = b % m
        while e > 0:
            if e % 2 == 1:
                result = result*base % m
            e = int(e) >> 1
            base = base*base%m
        return result

    @staticmethod
    def randGcd1(b):
        rangeStart = 2
        rangeEnd = b - 1
        while True:
            num = random.randint(rangeStart, rangeEnd)
            if math.gcd(num, b) == 1:
                return num

    @staticmethod
    def fct(arr):
        global b
        if arr == []:
            return 'Null division', 0
        elif arr == [0.0]:
            return 0, b
        p = []
        q = []
        for i in range(len(arr)):
            q.append(0)
            p.append(0)
        p[0] = arr[0]
        p[1] = arr[0] * arr[1] + 1
        q[0] = 1
        q[1] = arr[1]
        for n in range(2,len(arr)):
            p[n] = arr[n] * p[n-1] + p[n-2]
            q[n] = arr[n] * q[n-1] + q[n-2]
        return p[-2], len(p)

    def gcdex(self, a, m, b = 1, d = 1):
        a //= d
        b //= d
        m //= d
        newM = m

        arr = []
        while m != 1:
            division = m // a
            arr.append(float(division))
            p = m
            m = a
            a = p - (p // a) * a

        pN_1, n = self.fct(arr)

        x0 = (((-1) ** (n - 1)) * pN_1 * b) % newM

        return int(x0)

    def generate_private_keys(self):
        self.ca = self.randGcd1(p - 1)
        self.da = self.gcdex(self.ca, p - 1)
        self.cb = self.randGcd1(p - 1)
        self.db = self.gcdex(self.cb, p - 1)
        print(f"ca = {self.ca}, da = {self.da}")
        print(f"cb = {self.cb}, db = {self.db}")

        print(f"checking {self.ca}*{self.da} mod({p-1}) = {self.modpow(self.ca*self.da, 1, p - 1)}")
        print(f"checking {self.cb}*{self.db} mod({p-1}) = {self.modpow(self.cb*self.db, 1, p - 1)}")

    def sendAtoB(self, m):
        x1 = self.modpow(m, self.ca, self.p)
        print("x1 = ", x1)
        x2 = self.modpow(x1, self.cb, self.p)
        print("x2 = ", x2)
        x3 = self.modpow(x2, self.da, self.p)
        print("x3 = ", x3)
        x4 = self.modpow(x3, self.db, self.p)
        print("decrypted message = ", x4)


if __name__== "__main__":
    
    p = input("Enter p or leave blank for default settings: ")
    if p.isdigit():
        p = int(p)
    else:
        p = 30803

    shamir = ShamirChipher(p)
    shamir.generate_private_keys()

    m = input("Enter message to send: ")
    if m.isdigit():
        m = int(m)
    else:
        print("Please enter integer number")
        exit(-1)
    shamir.sendAtoB(m)
