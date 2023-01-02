from decrypt import*
from encrypt import*
from usb_removable import *
def Run():
    print('1. Mã hóa')
    print('2. Giải mã')
    option = input('Nhập lựa chọn:')
    while 1:
        if option == '0':
            break
        if option == '1':
            runEncrypt()
            break
        elif option == '2':
            runDecrypt()
            break
        else:
            option = input('Lựa chọn không hợp lệ. Nhấn 0 để thoát hoặc nhập lại: ')

if __name__ == "__main__":
    USB()