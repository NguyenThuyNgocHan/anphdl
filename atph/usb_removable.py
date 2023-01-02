import wmi
import runpy
c=wmi.WMI()
import win32com.client
from decrypt import*
from encrypt import*

def check_for_key(my_usb):
    for disk in c.Win32_LogicalDisk():
        my_usb_id=my_usb[0].upper()+':'
        #drive.type=2 la removable device
        if (disk.DriveType==2 and str(disk.Caption)==my_usb_id):
            return disk
    return 0
def load_key(usbDisk):
    port = usbDisk.DeviceID
    try:
      exec(open(f'{port}\\therest.py').read())
    except:
        print('Khong doc duoc file tu usb!')
def USB():

    my_usb = input("Nhap vao id USB cua ban (vi du: F): ")
    disk = check_for_key(my_usb)
    if(disk!=0):
        load_key(disk)
    else:
        print('Khong tim thay USB nao co id '+my_usb+ ', vui long cam usb vao \n')
    return
