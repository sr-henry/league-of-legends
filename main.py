import cv2
import win32api
import win32gui
import win32con
import numpy as np
from PIL import ImageGrab, Image
import time
import math
from pynput.mouse import Controller

window_name = "League of Legends (TM) Client"
hwnd = win32gui.FindWindow(0, window_name)
hdc = win32gui.GetDC(hwnd)

mouse = Controller()

lower = np.array([0, 2, 47])
upper = np.array([0, 11, 97])

kernel0 = np.ones((7,7), np.uint8)
kernel1 = np.ones((20,20), np.uint8)

w = win32api.GetSystemMetrics(0)
h = win32api.GetSystemMetrics(1)

print(w,h)

def nothing(x):
    pass

def pil_2_cv(pil_img):
    img = np.array(pil_img)
    img = img[:,:,::-1].copy()
    return img

def get_screen():
    pil_img = ImageGrab.grab().convert('RGB')
    return pil_2_cv(pil_img)

def screen_filter(screen):
    lb = cv2.getTrackbarPos("L-B", "trackbar")
    lg = cv2.getTrackbarPos("L-G", "trackbar")
    lr = cv2.getTrackbarPos("L-R", "trackbar")
    ub = cv2.getTrackbarPos("U-B", "trackbar")
    ug = cv2.getTrackbarPos("U-G", "trackbar")
    ur = cv2.getTrackbarPos("U-R", "trackbar")
    lower = np.array([lr, lg, lb])
    upper = np.array([ur, ug, ub])
    mask = cv2.inRange(screen, lower, upper)
    return mask


def find_enemies(screen):
    enemies = []
    mask = cv2.inRange(screen, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations = 1)
    ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = ret[0] if len(ret) == 2 else ret[1]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if 8 <= approx.size <= 12:
            x, y, w, h = cv2.boundingRect(approx)
            _x = x + w + 49
            _y = y + h + 57
            enemies.append((_x,_y))
    return mask, enemies

def calculate_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x1-x2, y1-y2)


def lock_enemy(enemies):
    min_dist = 999999999999
    min_enemy = None
    for enemy in enemies:
        dist = calculate_distance(win32api.GetCursorPos(), enemy)
        if dist < min_dist:
            min_dist = dist
            min_enemy = enemy
    if not min_enemy is None:
        mouse.position = min_enemy

""" cv2.namedWindow("trackbar")
cv2.createTrackbar("L-B", "trackbar", 0, 255, nothing)
cv2.createTrackbar("L-G", "trackbar", 0, 255, nothing)
cv2.createTrackbar("L-R", "trackbar", 0, 255, nothing)
cv2.createTrackbar("U-B", "trackbar", 0, 255, nothing)
cv2.createTrackbar("U-G", "trackbar", 0, 255, nothing)
cv2.createTrackbar("U-R", "trackbar", 0, 255, nothing) """

if __name__ == "__main__":
    
    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        img = get_screen()        

        mask, enemies = find_enemies(img)

        for e in enemies:
            cv2.circle(img, e, 35, (255,0,255),thickness=3)

        if win32api.GetAsyncKeyState(win32con.VK_MENU):
            lock_enemy(enemies)
            
        #cv2.imshow("frame", img)
        #cv2.imshow("mask", mask)

        #if cv2.waitKey(25) & 0xFF == ord('q'):
            #cv2.destroyAllWindows()
            #break 
   
            


    