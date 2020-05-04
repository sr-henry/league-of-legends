import win32api
import win32gui
import win32con
from time import sleep

window_name = "Fancy"

hwnd = win32gui.FindWindow(0, window_name)

if not hwnd:
    print("{} NOT FOUND".format(window_name))
    
hdc = win32gui.GetDC(hwnd)

enemy_color = 0x00ff1ac6

enemy_brush = win32gui.CreateSolidBrush(enemy_color)

screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

def draw_fill_rect(x, y, w, h):
    rect = (x, y, x + w, y + h)
    win32gui.FillRect(hdc, rect, enemy_brush)

def draw_border_box(x, y, w, h, t):
    draw_fill_rect(x, y, w, t)
    draw_fill_rect(x, y, t, h)
    draw_fill_rect((x + w), y, t, h)
    draw_fill_rect(x, (y + h), w+t, t)


def draw_center_square(point, side_size):
    x, y = point
    x,y = x - side_size//2, y - side_size//2
    draw_border_box(x, y, side_size, side_size, 3)

def draw_line(p1, p2):
    pen = win32gui.CreatePen(win32con.PS_SOLID, 2, enemy_color)
    hoPen = win32gui.SelectObject(hdc, pen)
    win32gui.MoveToEx(hdc, p1[0], p1[1])
    win32gui.LineTo(hdc, p2[0], p2[1])
    win32gui.DeleteObject(win32gui.SelectObject(hdc, hoPen))

if __name__ == "__main__":

    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        draw_center_square((500,500), 30)
    
    win32gui.DeleteDC(hdc)
        
