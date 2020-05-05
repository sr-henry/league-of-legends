import cv2
import time
import math
import win32api
import win32gui
import win32con
import numpy as np
from PIL import ImageGrab, Image
from pynput.mouse import Controller
from overlay import *

mouse = Controller()

lower = np.array([0, 2, 47])
upper = np.array([0, 11, 97])

kernel0 = np.ones((7,7), np.uint8)
kernel1 = np.ones((20,20), np.uint8)

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

def find_elements_on_screen(screen, lower, upper):
    mask = cv2.inRange(screen, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations = 1)
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
            _x, _y = (
                x + w + 49,
                y + h + 57
            )
            enemies.append((_x,_y))
    return enemies

def calculate_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x1-x2, y1-y2)

def lock_enemy(enemies):
    min_dist = 999
    min_enemy = None
    for enemy in enemies:
        dist = calculate_distance(win32api.GetCursorPos(), enemy)
        if dist < min_dist:
            min_dist = dist
            min_enemy = enemy
    if not min_enemy is None:
        mouse.position = min_enemy

def find_allies(screen):
    allies = []
    lower = np.array([35, 25, 0])
    upper = np.array([49, 35, 4])
    mask = cv2.inRange(screen, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations = 1)
    ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = ret[0] if len(ret) == 2 else ret[1]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if 8 <= approx.size <= 12:
            x, y, w, h = cv2.boundingRect(approx)
            _x, _y = (
                x + w - 2,
                y + h - 22
            )
            allies.append((_x,_y))
    return allies

def local_player(screen, players):
    life = np.array([41, 146, 66])
    player = None
    for x,y in players:
        if np.array_equal(screen[y][x], life):
            player = (
                x + 38,
                y + 79
            )
            break
    return player

if __name__ == "__main__":

    color = lambda rgb: "#%02x%02x%02x"%(rgb)

    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        img = get_screen()        

        enemies = find_enemies(img)

        allies = find_allies(img)

        e = local_player(img, allies)

        if not e is None:
            draw_center_square(e, 30, 0x00ff00ff)

        for i in enemies:
            draw_center_square(i, 30, 0x000000FF)

            draw_line(e,i, 0x000000FF)


        if win32api.GetAsyncKeyState(win32con.VK_SHIFT):
            lock_enemy(enemies)
            
        #cv2.imshow("frame", img)
        #cv2.imshow("mask", mask)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break 
   
            


    