import os
from cryptography.fernet import Fernet
import base64
import hashlib
import numpy as np
import string, random, time
import os
import csv
from create_hiden_folder import *

def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def encrypt_data(data,password):
    key = gen_fernet_key(password.encode('utf-8'))
    cipher = Fernet(key)
    encryptMessage = cipher.encrypt(data)
    extraByte = np.random.bytes(np.random.randint(1,10))
    print (encryptMessage)
    return encryptMessage + extraByte + str(len(extraByte)).encode('utf-8')

#Hàm sinh ngẫu nhiên tên file có 5 ký tự (VD:ahdns)
def generateFileName(dic):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return dic + '/' + result_str

#Hàm ghi dữ liệu vào nhiều file khác nhau, mỗi file chứa 50 ký tự. Các file được lưu vào folder en_file
#File ghi 50 ký tự đầu có tên do người dùng nhập vào
#Các file sau có tên do chương trình random và được lưu vào cuối nội dung file trước đó
#Cách làm này tương tự như Danh sách liên kết
def writeData(dir,data):
    fileName = dir + '/'+dir
    with open(fileName, 'ab+') as encrypted_file:
        if len(data) <= 150:
            encrypted_file.write(data[0:len(data)])
            return
        encrypted_file.write(data[0:150])
        newFile = generateFileName(dir).encode()
        encrypted_file.write(newFile)
        newFile =newFile.decode()
        # tạo file mới có tên random
    data = data[150:] #xóa 50 byte đầu của data
    while (len(data) / 150 > 1):
        with open(newFile, 'ab+') as encrypted_file:
            encrypted_file.write(data[0:150])
            newFile = generateFileName(dir).encode()
            encrypted_file.write(newFile)
            newFile =newFile.decode()
            data = data[150:] #xóa 50 byte đầu của data
    with open(newFile, 'ab+') as encrypted_file:
        encrypted_file.write(data)


#Hàm mã hóa file với password được cung cấp
def encrypt(fileName,enFileName,password):
    while 1:
        try:
            file= open(fileName, 'rb')
        except IOError:
            fileName = input("Khong the mo file nhan 0 de thoat, hoac nhap ten file moi: ")
            if (fileName == '0'):
                return
        data = file.read()
        key = gen_fernet_key(password.encode('utf-8'))
        print("**************************88")
        print(encrypt_data(data,password))
        encrypted = key + encrypt_data(data,password)
        #hàm ghi data vào nhiều file
        writeData(enFileName,encrypted)
        return

#Hàm kiểm tra một file có được mã hóa chưa (được lưu trong file public.csv)
def checkFileExists(direct,fileName):
    try :
        open(direct +'/'+ fileName)
        return True
    except IOError:
        return False

#Hàm tiến hành mã hóa
def runEncrypt():
    fileName = input('Nhập tên file cần mã hóa:')
    directory = input('Nhập tên folder lưu dữ liệu mã hóa:')
    cre_hidden(directory)
    password = input('Nhập mật khẩu để mã hóa file:')
    encrypt(fileName,directory,password)