from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class SingleEncryption:

    def __init__(self, password):
        self.password = password
        self.salt = b'r\x83"\xc2\xad}\xb1\\\xc8\xda\xef\x8a%\x1a[\xa4\x96\xeb\x85\xbf\xcbol\xa2rE\x95\xb5b\x00kg'
        self.key = PBKDF2(self.password, self.salt, dkLen=32)

    def saveKey(self):

        if input(f"Would you like to save this key ({self.key}) to a file? Y/N ") == "Y":
            file_out = open(input("Where should I save it? "), "wb")
            file_out.write(self.key)
            file_out.close()
        else:
            print(f"Key not saved, the key is {self.key}")

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))
        return cipher.iv + ciphered_data  # concatenate IV and ciphertext

    def decrypt(self, cipher_data):
        iv = cipher_data[:16]  # separate IV...
        ciphertext = cipher_data[16:]  # ...and ciphertext
        cipher = AES.new(self.key, AES.MODE_CBC, iv)  # specify the IV from encryption
        original_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return original_data


if __name__ == "__main__":
    encrypt = SingleEncryption(input("Encryption password? "))
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
