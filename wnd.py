import win32gui
import win32con
import win32ui
import threading
import numpy as np
from cv2 import cvtColor, COLOR_RGBA2RGB

class WndCap(threading.Thread):
    def __init__(self, hwnd):
        threading.Thread.__init__(self)
        self.on = True
        self.hwnd = hwnd
        self.img = None 

    def run(self):
        while self.on:
            self.img = cvtColor(capture(self.hwnd), COLOR_RGBA2RGB)

    def terminate(self):
        self.on = False


def capture(hwnd):
    _,_,w,h = win32gui.GetClientRect(hwnd)
    hdc = win32gui.GetWindowDC(hwnd)
    dc = win32ui.CreateDCFromHandle(hdc)
    mdc = dc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(dc, w, h)
    mdc.SelectObject(bmp)
    mdc.BitBlt((0,0), (w,h), dc, (0,0), win32con.SRCCOPY)
    img = np.frombuffer(bmp.GetBitmapBits(True), dtype='uint8')
    img.shape = (h, w, 4)
    dc.DeleteDC()
    mdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hdc)
    win32gui.DeleteObject(bmp.GetHandle())
    return img


if __name__ == '__main__':
    import cv2
    hwnd = win32gui.FindWindow(0,'League of Legends (TM) Client')
    print(hwnd)
    while True:
        img = capture(hwnd)
        cv2.imshow('wnd', img)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break
