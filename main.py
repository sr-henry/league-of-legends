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
        return '(%.3f:%.3f)'%(self.x, self.y)     

class Predictor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pred = Vec2(0,0)
        self.dt = 0.1
        self.pt = 0.25
        
    def run(self):
        while cap.on: 
            if not cap.img is None:
                e0 = min_entity(mouse(), find_enemies(cap.img))
                time.sleep(self.dt)
                e1 = min_entity(mouse(), find_enemies(cap.img))
                if e0 and e1:
                    d = e1 - e0
                    if d.h < 100:
                        self.pred = d.unite.dot((d.h/self.dt)*self.pt)
                    else:
                        self.pred = Vec2(0,0)
                else:
                    self.pred = Vec2(0,0)
                    
def move(x, y):
    x0, y0 = win32api.GetCursorPos()
    win32api.mouse_event(0x0001, x-x0, y-y0, 0, 0)

def mouse():
    return Vec2(*win32api.GetCursorPos())

def find_color_contours(img, lower, upper):
    kernel0 = np.ones((5,5), np.uint8)
    kernel1 = np.ones((20,20), np.uint8)
    mask = cv2.inRange(img, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel0)
    mask = cv2.dilate(mask, kernel1, iterations=1)
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

def min_entity(m, entities):
    md = math.inf
    me = None
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
            if np.array_equal(img[_y-22][_x-2], [41, 146, 66]):
                return Vec2(_x + offsetx, _y + offsety)

def find_minions(img):
    minions = []
    l = np.array([88, 81, 197])
    u = np.array([255,91,197])
    mask = cv2.inRange(img, l, u)
    mask = cv2.dilate(mask, np.ones((4,4), np.uint8), iterations=1)
    ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ret = ret[0] if len(ret) == 2 else ret[1]
    offsetx, offsety = 30, 32
    for c in ret:
        approx = cv2.approxPolyDP(c, 0.1*cv2.arcLength(c, True), True)
        x, y, w, h = cv2.boundingRect(approx)
        if approx.size == 4 and w <= 63: 
            _x, _y = x + offsetx, y + offsety
            if w <= 16:
                gdi.circle((_x,_y), 15, 2, (181,106,6))
            gdi.text(str(w), (_x,_y,_x,_y))
            minions.append((_x,_y))
    return mask
                
def evade(p0, p1, a):
    vec_d = p1-p0
    de = math.tan(a)*vec_d.h
    b = math.pi - math.atan(vec_d.tan)        
    dy = de*math.sin(b)
    dx = de*math.cos(b)
    v = Vec2(dx,dy)
    return p1 + v

def check_inside(c, r, p, t):
    rd = (p[0]-c[0])**2/r[0]**2 + (p[1]-c[1])**2/r[1]**2 
    if rd <= t:
        return True
    return False

def pid(err):
    global previous_error

    Kp, Ki, Kd = 1, 0, 0
    I = 0
    
    P = err
    I += previous_error
    D = err - previous_error

    pid_value = (Kp * P) + (Ki * I) + (Kd * D)    

    previous_error = err    

    return pid_value

    
def kite(aar, threshold_aar, dist_error):
    p = local_player(cap.img)

    if not p:
        return
    
    e = min_entity(mouse(), find_enemies(cap.img))
    if not e:
        return

    e += pre.pred
    p += offset 
    
    d = e - p

    a, b = aar
    m = d.tan
    c = math.sqrt((a*a - b*b))
    ec = c/a    

    k = math.atan(m)

    r = b/math.sqrt(1-(ec*math.cos(k + math.pi/2))**2)

    t = p + d.unite.dot(r)

    err = d.h - (t-p).h

    z = (p + d.unite.dot(pid(err))) 

    pid_distance = (p-z).h
   
    is_inside = check_inside(p.ivalue, aar, e.ivalue, threshold_aar)

    op = p+d.unite.dot(-r)
    
    ## normalizer
#    player_pred = p + pre.pred.dot(-1)
#    
#    cost = (-((player_pred - z).h**2)+(player_pred.h**2)+(z.h**2))/(2*player_pred.h*z.h)
#     
#    theta = math.acos(cost)
#    
#    print(math.degrees(theta))
#
#    gdi.line(p.ivalue, player_pred.ivalue, 2, (128,0,128))

    if pid_distance < dist_error and is_inside:
        # auto-atack
        pass        
     
    else:
        move(*z.ivalue)  
        win32api.mouse_event(0x0008, 0, 0, 0, 0)
        time.sleep(.1)
        win32api.mouse_event(0x0010, 0, 0, 0, 0)
            
#    gdi.circle(p.ivalue, dist_error, 2, (255,255,0))
#    gdi.elipse(p.ivalue, a, b, 2, (255,255,255))
#    gdi.line(p.ivalue, e.ivalue, 2, (255,255,255))
#    gdi.line(p.ivalue, z.ivalue, 2, (255,0,0))
#    gdi.circle(z.ivalue, 5, 4, (255,0,0))    
#    gdi.circle(op.ivalue, 5, 4, (255,255,0))    
#    gdi.circle(t.ivalue, 5, 4, (0,255,255))


if __name__ == '__main__':
    print('[@] Legit Hack League-of-Legends:: v.0')

    hwnd = win32gui.FindWindow(0, 'League of Legends (TM) Client')

    if not hwnd:
        print('[!] Game not found')
        quit()
        
    print('[HOME] - Exit')

    gdi = GDIDraw()

    cap = WndCap(hwnd)
    cap.setDaemon(True)
    cap.start()

    pre = Predictor()
    pre.setDaemon(True)
    pre.start()

    # line evade angle
    alpha = 20

    # auto-atack range Ezreal
    aarange = (290, 240)

    # fix local player for aa range
    offset = Vec2(3, 51)

    previous_error = 0
    
    while not win32api.GetAsyncKeyState(win32con.VK_HOME):            
        if not cap.img is None:

            if win32api.GetAsyncKeyState(0x51) or\
                win32api.GetAsyncKeyState(0x57) or\
                win32api.GetAsyncKeyState(0x52):
                e = min_entity(mouse(), find_enemies(cap.img))
                if e:
                    move(*(e + pre.pred).ivalue)

            if win32api.GetAsyncKeyState(0x20):
                kite(aarange, 1.4, 40)
    
    cap.terminate()
