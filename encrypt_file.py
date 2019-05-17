#useful guide: https://nitratine.net/blog/post/encryption-and-decryption-in-python/#encrypting-and-decrypting-files

from cryptography.fernet import Fernet
import sys

key = Fernet.generate_key()

#key = b'0xAA'
fernet = Fernet(key)

def akey():
	file = open('key.key', 'wb')
	file.write(key) # The key is type bytes still
	file.close()
	return

def dec_file():
    with open(sys.argv[2], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.decrypt(data)
    with open(sys.argv[3], 'wb') as f:
        f.write(encrypted)
    return

def enc_file(data):
    encr=fernet.encrypt(data)
    outf=sys.argv[2]
    with open(outf,'wb') as oof:
            oof.write(encr)
    return

def load_input(fn):
    #with open(fn) as ain:
    #    for item in ain:
    #        print(item);
    with open(fn,'rb') as ain:
        data=ain.read()
    return data

def main():
    akey()
    fn = sys.argv[1]
    print("loading input file")
    data=load_input(fn)
    print('encrypting file.')
    enc_file(data)
    print('decrypting file')
    dec_file()
    print('finished')
    return

main();