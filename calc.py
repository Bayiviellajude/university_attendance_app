import math
import random

# Define RSA encryption functions
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime_number(min_value, max_value):
    p = random.randint(min_value, max_value)
    while not is_prime(p):
        p = random.randint(min_value, max_value)
    return p

def generate_key_pair():
    p = generate_prime_number(100, 1000)
    q = generate_prime_number(1000, 10000)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(1, phi - 1)
    d = pow(e, -1, phi)
    return ((n, e), (n, d))

def encrypt(plaintext, public_key):
    n, e = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

def decrypt(ciphertext, private_key):
    n, d = private_key
    plaintext = [chr(pow(char, d, n)) for char in ciphertext]
    return "".join(plaintext)

# Main program
print("Welcome to RSA encryption and decryption program!")
while True:
    action = input("Enter 'e' to encrypt or 'd' to decrypt: ")
    if action == 'e':
        plaintext = input("Enter the plaintext you want to encrypt: ")
        public_key, _ = generate_key_pair()
        ciphertext = encrypt(plaintext, public_key)
        print("The ciphertext is:", ciphertext)
    elif action == 'd':
        ciphertext = input("Enter the ciphertext you want to decrypt: ")
        _, private_key = generate_key_pair()
        plaintext = decrypt(ciphertext, private_key)
        print("The plaintext is:", plaintext)
    else:
        print("Invalid input. Please enter 'e' to encrypt or 'd' to decrypt.")
