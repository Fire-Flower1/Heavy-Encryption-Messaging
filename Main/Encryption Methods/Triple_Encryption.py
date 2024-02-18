from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class TripleEncryption:

    def __init__(self):
        self.salt = b'r\x83"\xc2\xad}\xb1\\\xc8\xda\xef\x8a%\x1a[\xa4\x96\xeb\x85\xbf\xcbol\xa2rE\x95\xb5b\x00kg'

        self.password = {
            "pass1": input("First Password? "),
            "pass2": input("Second Password? "),
            "pass3": input("Third Password? ")
        }

        self.key = {
            "key1": PBKDF2(self.password["pass1"], self.salt, dkLen=32),
            "key2": PBKDF2(self.password["pass2"], self.salt, dkLen=32),
            "key3": PBKDF2(self.password["pass3"], self.salt, dkLen=32)
        }

    def saveKey(self):

        if input(f"Would you like to save these keys (Key 1: {self.key['key1']}, Key 2: {self.key['key2']}, Key 3: {self.key['key3']}) to a file? Y/N ") == "Y":
            file_out = open(input("Where should I save them? "), "wb")
            file_out.write(f"Key 1: {self.key['key1']}, Key 2: {self.key['key2']}, Key 3: {self.key['key3']}".encode())
            file_out.close()
        else:
            print(f"Keys not saved, the keys are: Key 1: {self.key['key1']}, Key 2: {self.key['key2']}, Key 3: {self.key['key3']}")

    def encrypt(self, data):
        cipher1 = AES.new(self.key["key1"], AES.MODE_CBC)
        cipher2 = AES.new(self.key["key2"], AES.MODE_CBC)
        cipher3 = AES.new(self.key["key3"], AES.MODE_CBC)  # Fixed: Use "key3" for cipher3

        ciphered_data1 = cipher1.encrypt(pad(data, AES.block_size))
        ciphered_data2 = cipher2.encrypt(pad(ciphered_data1, AES.block_size))
        ciphered_data3 = cipher3.encrypt(pad(ciphered_data2, AES.block_size))

        # Separate IVs from each encryption operation
        iv1 = cipher1.iv
        iv2 = cipher2.iv
        iv3 = cipher3.iv

        # Concatenate IVs and ciphertexts
        encrypted_data = iv1 + iv2 + iv3 + ciphered_data3
        return encrypted_data

    def decrypt(self, cipher_data):
        iv1 = cipher_data[:16]  # IV for cipher1
        iv2 = cipher_data[16:32]  # IV for cipher2
        iv3 = cipher_data[32:48]  # IV for cipher3
        ciphertext1 = cipher_data[48:64]  # Ciphertext for cipher1
        ciphertext2 = cipher_data[64:80]  # Ciphertext for cipher2
        ciphertext3 = cipher_data[80:]  # Ciphertext for cipher3

        # Decrypt each ciphertext with its corresponding IV
        cipher1 = AES.new(self.key["key1"], AES.MODE_CBC, iv1)
        original_data1 = unpad(cipher1.decrypt(ciphertext1), AES.block_size)

        cipher2 = AES.new(self.key["key2"], AES.MODE_CBC, iv2)
        original_data2 = unpad(cipher2.decrypt(original_data1), AES.block_size)

        cipher3 = AES.new(self.key["key3"], AES.MODE_CBC, iv3)
        original_data3 = unpad(cipher3.decrypt(original_data2), AES.block_size)

        return original_data3  # Concatenate decrypted data


if __name__ == "__main__":
    encrypt = TripleEncryption()

    while True:
        q = input("Encrypt, Decrypt, or Quit? ")
        if q == "Encrypt":
            print(encrypt.encrypt(input("What to encrypt? ").encode()).hex())  # hex encode ciphertext
        elif q == "Decrypt":
            print(encrypt.decrypt(bytes.fromhex(input("Encrypted data? "))).decode())  # hex decode ciphertext before
            # decryption
        elif q == "Quit":
            break
        else:
            print("Incorrect input, it is case sensitive.")
