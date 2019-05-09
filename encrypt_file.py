import cryptography
import sys


def dec_file(fn):
    return

def enc_file(data):
    fernet = Fernet(key)
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
    key = bb''
    fn = sys.argv[1]
    data=load_input(fn)
    enc_file(data)
    return

main();
