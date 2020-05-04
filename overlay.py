import win32api
import win32gui
import win32con
from time import sleep

window_name = "League of Legends (TM) Client"

hwnd = win32gui.FindWindow(0, window_name)

if not hwnd:
    print("{} NOT FOUND".format(window_name))
    
hdc = win32gui.GetDC(0)

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

if __name__ == "__main__":
    draw_border_box(100, 400, 40, 100, 3)