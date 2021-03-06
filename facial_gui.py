from __future__ import division
import cv2
import cv2.cv
import numpy as np
import sys
import os
#https://github.com/ageitgey/face_recognition
import face_recognition
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import base64
from sys import exit as exit
import hashlib, uuid


#key = Fernet.generate_key()
##key = b'0xAA'
#fernet = Fernet(key)

#password = b"password"
#salt = os.urandom(16)
#kdf = PBKDF2HMAC(
#    algorithm = hashes.SHA256(),
#    length = 32,
#    salt = salt,
#    iterations = 100000,
#    backend = default_backend()
#)
#key = base64.urlsafe_b64encode(kdf.derive(password))
#f = Fernet (key)


def akey():
    file = open('mykey.key', 'wb')
    file.write(key) # The key is type bytes still
    file.close()
    return


def dec_file(fn,f):
    apath = os.path.dirname(fn)
    base = os.path.basename(fn)
    abase = base.split("_")
    outf = apath + "/dec_" + abase[1]
    print('---------')
    print("File Decrypted To:")
    print(outf)
    print('---------')
    with open(fn, 'rb') as ain:
        data = ain.read()
    #f = Fernet(key)
    decr = f.decrypt(data)
    with open(outf, 'wb') as oof:
        oof.write(decr)
    return


def enc_file(fn,f):
    apath = os.path.dirname(fn)
    base = os.path.basename(fn)
    outf = apath + "/enc_" + base
    print('---------')
    print("File Encrypted To:")
    print(outf)
    print('---------')
    with open(fn, 'rb') as ain:
        data=ain.read()
    encr=f.encrypt(data)
    with open(outf, 'wb') as oof:
        oof.write(encr)
    return


def load_input(fn):
    #with open(fn) as ain:
    #    for item in ain:
    #        print(item);
    with open(fn,'rb') as ain:
        data=ain.read()
    return data


def detect_faces(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects


def gen_face(img, gray, face_cascade):
    rects_face = detect_faces(gray, face_cascade)
    r = rects_face
    ex_face = img[r[0][1]:r[0][3], r[0][0]:r[0][2]]
    return ex_face, r, rects_face


def SecondForm():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Second Form').Layout(layout)
    b, v = window.Read()

def init_encryption(password):
    try:
        #fh = open('./mykey.key', 'rb')
        #key = fh.read()  # The key will be type bytes
        #fh.close()
        #f = Fernet(key)

        fh = open('./salt.key', 'rb')
        salt=fh.read()
        fh.close()
        #password = fh.read()
        #password = b"password"
        #salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)

        print("key file exists")
        print("loading key from file.")
    except:
        ##key = Fernet.generate_key()
        ## with open('./mykey.key','wb') as fille:
        ##    fille.write(key)
        #fille = open('./mykey.key', 'wb')
        #fille.write(key)
        #fille.close()
        print("key file not found")
        print("new key generated.")
        #f = Fernet(key)

        ##fh = open('./salt.key', 'rb')
        # password = fh.read()
        #password = b"password"
        salt = os.urandom(16)
        bfile = open('./salt.key', 'wb')
        bfile.write(salt)
        bfile.close()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
    return f


def main():
    password = b""
    #f = init_encryption(password)
    passflag = 0
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Set Dev', '&Properties', 'E&xit' ]],
                ['&Edit', ['&Paste', ['Special', 'Normal',], 'Undo'],],
                ['&Toolbar', ['---', '&Set Facial Key', '&File To Encrypt', '&File To Decrypt']],
                ['&Help', '&About...'],]

    # define the window layout
    layout = [[sg.Menu(menu_def, tearoff=False, pad=(10,1))],
              [sg.Image(filename='', key='image'), sg.Output(size=(20, 2))],
              [sg.Text('Enter Password', size = (15,1))],
              [sg.ReadButton('Submit'), sg.InputText('', key='in1', do_not_clear=True, size=(15, 1))],
              [sg.ReadButton('Snapshot'), sg.ReadButton('Encrypt'), sg.ReadButton('Decrypt')]
              ]

    window = sg.Window("Facial Encryption GUI - OpenCV Integration",
                       default_element_size=(12, 1),
                       auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1))

    window.Layout(layout).Finalize()
    av = sys.argv[1]
    capdevice = int(av)
    keyfile = ''
    try:
        face_cascade = cv2.CascadeClassifier('/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(capdevice)
        keyflag = 0
        snapflag = 0
        decencflag = 0
        keyfilename = './me.jpg'
        try:
            known_image = face_recognition.load_image_file(keyfilename)
            keyflag = 1
        except:
            print('no default image file found.')
        while True:
            event, values = window.Read(timeout=0, timeout_key='timeout')
            if event == 'Snapshot':
                if passflag==1:
                    #filename = sg.PopupGetFile('Save Settings', save_as=True, no_window=True)
                    #window.SaveToDisk(filename)
                    # save(values)
                    if keyflag==1:
                        snapflag=1;
                    else:
                        print('---------')
                        print("Error Making Snapshot.")
                        print("Has the image key been set?")
                        print('---------')
                else:
                    print('Enter password.')
            elif event == 'About...':
                window.Disappear()
                sg.Popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...', grab_anywhere=True)
                window.Reappear()
            elif event == 'Set Facial Key':
                try:
                    keyfilename = sg.PopupGetFile('file to open', no_window=True)
                    print('---------')
                    print('Image Key Set.')
                    print(keyfilename)
                    print('---------')
                    keyflag=1
                except:
                    print("Error Setting Facial Key")
            elif event == 'Properties':
                SecondForm()
            elif event == 'Encrypt':
                if decencflag == 1:
                    in_encfilename = sg.PopupGetFile('file to open', no_window=True)
                    print("File Encrypted.", in_encfilename)
                    enc_file(in_encfilename,f)
                else:
                    print('No Facial Recognition.')
            elif event == 'Decrypt':
                if decencflag == 1:
                    in_decfilename = sg.PopupGetFile('file to open', no_window=True)
                    print("File Decrypted.", in_decfilename)
                    try:
                        dec_file(in_decfilename,f)
                    except:
                        print("Error decryptiing.")
                        print("Password probably incorrect.")
                else:
                    print('No Facial Recognition.')
            elif event == 'Submit':
                passflag=1
                query = values['in1'].rstrip()
                print("Password Entered.")
                #password = b"password"
                password = bytes(query)
                print(query)
                print(password)
                f = init_encryption(password)
            elif event in ['Exit', None]:
                print("Exit")
                break

            eva, frame = cap.read()
            iframe=frame.copy()

            if eva is True:
                frame = cv2.resize(frame, (480, 360), interpolation=cv2.INTER_AREA)
                height, width = frame.shape[:2]
                cv2.rectangle(frame, (int(5 * width / 16), int(1 / 8 * height)),
                              (int(11 / 16 * width), int(7 / 8 * height)), (0, 255, 0), 2)
                roi_frame = frame[int(1 / 8 * height):int(7 / 8 * height), int(5 * width / 16):int(11 / 16 * width)]
                roi_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
                roi_gray = cv2.equalizeHist(roi_gray)
                try:
                    ex_face, r, rects_face = gen_face(frame, roi_gray, face_cascade)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, 'Face Detected.', (10, int(1 / 16 * height)), font, .4, (0, 0, 255), 1, cv2.CV_AA)
                    if cv2.waitKey(1) & snapflag == 1:
                        snapflag = 0
                        known_image = face_recognition.load_image_file(keyfilename)
                        unknown_image = iframe.copy()
                        rhh_encoding = face_recognition.face_encodings(known_image)[0]
                        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
                        results = face_recognition.compare_faces([rhh_encoding], unknown_encoding)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        if results[0] == True:
                            print('---------')
                            print("Snapshot Taken.")
                            print('True Match.')
                            print('Files Can Be Encrypted or Decrypted.')
                            print('---------')
                            decencflag=1
                        else:
                            print('---------')
                            print('Snapshot Taken')
                            print('False Match.')
                            print('---------')
                except:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, 'No Face Detected.', (10, int(1 / 16 * height)), font, .4, (0, 0, 255), 1,
                                cv2.CV_AA)
            else:
                continue

            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window.FindElement('image').Update(data=imgbytes)
    except:
        print('Select Video Device')

main()