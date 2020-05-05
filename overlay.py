import win32api
import win32gui
import win32con
from time import sleep

window_name = "OverlayFrame"

hwnd = win32gui.FindWindow(0, window_name)

if not hwnd:
    print("{} NOT FOUND".format(window_name))
    
hdc = win32gui.GetDC(hwnd)

enemy_color = 0x00ff1ac6

enemy_brush = win32gui.CreateSolidBrush(enemy_color)

def draw_fill_rect(x, y, w, h, color ):
    rect = (x, y, x + w, y + h)
    win32gui.FillRect(hdc, rect, color)

def draw_border_box(x, y, w, h, t, color):
    draw_fill_rect(x, y, w, t, color)
    draw_fill_rect(x, y, t, h, color)
    draw_fill_rect((x + w), y, t, h, color)
    draw_fill_rect(x, (y + h), w+t, t, color)

def draw_center_square(point, side_size, color):
    if point is None:
        return
    x, y = point
    x,y = x - side_size//2, y - side_size//2
    draw_border_box(x, y, side_size, side_size, 3, color)

def draw_line(p1, p2, color):
    if p1 is None or p2 is None:
        return
    pen = win32gui.CreatePen(win32con.PS_SOLID, 2, color)
    hoPen = win32gui.SelectObject(hdc, pen)
    win32gui.MoveToEx(hdc, p1[0], p1[1])
    win32gui.LineTo(hdc, p2[0], p2[1])
    win32gui.DeleteObject(win32gui.SelectObject(hdc, hoPen))

if __name__ == "__main__":

    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        draw_center_square((500,500), 30)
    
    win32gui.DeleteDC(hdc)
        
