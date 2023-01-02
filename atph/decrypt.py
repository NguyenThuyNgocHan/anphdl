import os
#from decrypt import*
from encrypt import*
from cryptography.fernet import Fernet
import base64
import hashlib
import numpy as np
import string, random, time
import os
import shutil
import csv

def decrypt_data(data,password):
    key = gen_fernet_key(password.encode('utf-8'))
    cipher = Fernet(key)
    print(cipher)
    print(data)
    print(cipher.decrypt(data).decode())
    decrypted = cipher.decrypt(data).decode()
    return decrypted

#Hàm đọc nội dung mã hóa được lưu ở nhiều file khác nhau
def readData(directory):
    fileName = directory+'/'+directory
    allData =b''
    f = open(fileName,'rb')
    if f:
        data = f.read()
        len_filename=6+len(directory)
        allData += data[44:-len_filename]
        FN = data[-len_filename:].decode()
        if (len(FN)!=6+len_filename):
            return allData
        while (len(data)>150):
            f = open(FN)
            if f:
                data = f.read()
                print(data)
                FN = data[-len_filename:]
                temp=(data[0:-len_filename]) #noi dung file ma hoa khong chua ten file ke tiep
                allData += temp.encode()
                print(temp.encode())
                print(allData)
    return allData


#Hàm lấy mật khẩu động
def getPassDong():
    t = time.localtime()
    return time.strftime("%H", t) + time.strftime("%M", t)

#hàm kiểm tra mật khẩu động
## password  = 3 ký từ đầu ngẫu nhiên + giờ(24h)(2 ký tự) + 1 dãy ký tự ngẫu nhiên + phút(2 ký tự) + 3 ký tự ngẫu nhiên
def checkPassDong(password):
    password = password[:-3]
    realPassword = password[3:5] + password[-2:]
    print(realPassword , getPassDong())
    if realPassword == getPassDong():
        return True
    return False

#Hàm kiểm tra mật khẩu của 1 file đã mã hóa
def checkPassword(fileName, password):
    f = open(fileName+'/'+ fileName)
    data = f.read()
    data = data[0:44]
    if data.encode() == gen_fernet_key(password.encode('utf-8')):
        return True
    return False
#----
def checkMode(a,b,c,n):
    return (a+b)%n == c

def passMode(password):
    while len(password) % 3 != 1:
        password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
        if password == '0':
            return
    n = int(password[0])
    for i in range(1, len(password), 3):
        while checkMode(int(password[i]),int(password[i+1]),int(password[i+2]),n) == False:
            password = input('Mật khẩu không hợp lệ. Nhấn 0 để thoát hoặc nhập lại mật khẩu: ')
            if password == '0':
                return

#Hàm xóa tất cả file chứa nội dung mã hóa sau khi file đó được giải mã
def removeFile(fileName):
    fileName = 'encr/' + fileName
    file= open(fileName, 'r')
    data = file.read()
    nextFile = data[-10:]
    file.close()
    os.remove(fileName)
    while 1:
        try :
            file= open(nextFile + '.txt', 'r')
            data = file.read()
            file.close()
            os.remove(nextFile + '.txt')
            nextFile = data[-10:]
        except IOError:
            return

#Hàm tiến hành giải mã
def runDecrypt():
    folder = input('Nhập tên folder chứa các file đã mã hóa:')
    while checkFileExists(folder,folder) == False:
        fileName = input('File không tồn tại hoặc chưa được mã hóa. Nhập 0 để thoát hoặc nhập lại tên file: ')
        if fileName == 0:
            return
    password = input('Nhập mật khẩu để mã hóa:')
    # while checkPassword(fileName,password) == False:
    #     password = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
    #     if password == '0':
    #         return
    #
    # OTP = input('Nhập mật khẩu động để tiếp tục: ')
    # while checkPassDong(OTP) == False:
    #     OTP = input('Mật khẩu sai. Nhấn 0 để thoát hoặc nhập lại: ')
    #     if OTP == '0':
    #         return

    # passmode = input('Nhập mật khẩu số để tiếp tục:')
    # passMode(passmode)
    data = readData(folder)
    print(data)
    de_data = decrypt_data(data,password)
    print("67890-0987657890")
    print(de_data)
    deFileName = input('Nhập tên file để lưu nọi dung giải mã:')
    f=open(deFileName,"a")
    f.writelines(de_data)
    f.close()
    removeFile(folder)
    print('Giải mã thành công.')
