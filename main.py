import time
import math
import cv2
import win32api
import win32con
import win32gui
import threading
import numpy as np

from wnd_cap import capture
from GDI import GDIDraw

class WndCap(threading.Thread):
    def __init__(self, hwnd):
        threading.Thread.__init__(self)
        self.on = True
        self.hwnd = hwnd
        self.img = None 

    def run(self):
        while self.on:
            self.img = cv2.cvtColor(capture(self.hwnd), cv2.COLOR_RGBA2RGB)

    def terminate(self):
        self.on = False

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = math.hypot(x, y)

    @property
    def ivalue(self):
        return int(self.x), int(self.y)

    @property
    def value(self):
        return self.x, self.y

    @property
    def unite(self):
        if self.h == 0:
            return Vec2(0, 0)
        return Vec2(self.x/self.h, self.y/self.h)

    @property
    def tan(self):
        if self.y == 0:
            return 0
        return self.x/self.y

    def dot(self, n):
        return Vec2(self.x * n, self.y * n)

    def __add__(self, v):
        return Vec2(self.x + v.x, self.y + v.y)
     
    def __sub__(self, v):
        return Vec2(self.x - v.x, self.y - v.y)

    def __mul__(self, v):
        return Vec2(self.x * v.x, self.y * v.y)
    
    def __str__(self):
        return '(%f : %f)'%(self.x, self.y)     

class Predictor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pred = None
        self.dt = 0.1
        self.pt = 0.3
        
    def run(self):
        while cap.on: 
            if not cap.img is None:
                e0 = min_entity(find_enemies(cap.img))
                time.sleep(self.dt)
                e1 = min_entity(find_enemies(cap.img))
                if e0 and e1:
                    d = e1 - e0
                    self.pred = e1 + d.unite.dot((d.h/self.dt)*self.pt)
                else:
                    self.pred = None

def find_color_contours(img, lower, upper):
    kernel0 = np.ones((4,4), np.uint8)
    kernel1 = np.ones((20,20), np.uint8)
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations = 1)
    ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return ret[0] if len(ret) == 2 else ret[1]
    
def find_enemies(img):
    enemies = []
    l = np.array([0, 2, 47])
    u = np.array([0, 11, 90])
    offsetx, offsety = 40, 57
    for cnt in find_color_contours(img, l, u):
        approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
        if approx.size == 8:
            x, y, w, h = cv2.boundingRect(approx)
            e = Vec2(x + w + offsetx, y + h + offsety)
            enemies.append(e)
    return enemies

def min_entity(entities):
    md = math.inf
    me = None
    m = Vec2(*win32api.GetCursorPos())
    for e in entities:
        d = (e-m).h
        if d < md:
            md = d
            me = e
    return me

def local_player(img):
    l = np.array([35, 25, 0])
    u = np.array([49, 35, 4])
    offsetx, offsety = 38, 60
    for cnt in find_color_contours(img, l, u):
        approx = cv2.approxPolyDP(cnt, 0.1*cv2.arcLength(cnt, True), True)
        if approx.size == 8:
            x, y, w, h = cv2.boundingRect(approx)
            _x, _y = (x + w, y + h)
            if np.array_equal(img[_y-22][_x-2], [33, 138, 49]):
                return Vec2(_x + offsetx, _y + offsety)
                
def evade(p0, p1, a):
    vec_d = p1-p0
    de = math.tan(a)*vec_d.h
    b = math.radians(180) - math.atan(vec_d.tan)        
    dy = de*math.sin(b)
    dx = de*math.cos(b)
    v = Vec2(dx,dy)
    return p1 + v

def move(x,y):
    x0, y0 = win32api.GetCursorPos()
    win32api.mouse_event(0x0001, x-x0, y-y0, 0, 0)
 
if __name__ == '__main__':
    
    gdi = GDIDraw()
        
    print('[@] League-of-Legends Skill-Shot AimBot')
        
    hwnd = win32gui.FindWindow(0, 'League of Legends (TM) Client')

    if not hwnd:
        print('[!] Game not found')
        quit()

    ## Window Capture
    cap = WndCap(hwnd)
    cap.setDaemon(True)
    cap.start()

    ## Moviment Predictor
    pre = Predictor()
    pre.setDaemon(True)
    pre.start()

    ## Evade angle
    alpha = 15

    while not win32api.GetAsyncKeyState(win32con.VK_HOME):            
        if not cap.img is None:

            e = min_entity(find_enemies(cap.img))
            p = local_player(cap.img)
 
            if win32api.GetAsyncKeyState(0x51) or\
                win32api.GetAsyncKeyState(0x57) or\
                win32api.GetAsyncKeyState(0x52):
                if e:
                    move(*e.value) 
            
            if p and e:
                gdi.circle(e.value, 30, 1, (255,0,255))
     
                gdi.line(p.value, e.value, 1, (255,255,255))

                if pre.pred:
                    gdi.line(e.value, pre.pred.ivalue, 1, (0,255,0))

                if win32api.GetAsyncKeyState(0x12):
                    evp = evade(e, p, math.radians(alpha))
                    evn = evade(e, p, -math.radians(alpha))
        
                    move(*min_entity([evp, evn]).ivalue)

                    win32api.mouse_event(0x0008, 0, 0, 0, 0)
                    win32api.mouse_event(0x0010, 0, 0, 0, 0)
            
    cap.terminate()
