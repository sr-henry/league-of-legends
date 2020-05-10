import win32api
import win32gui
import win32con

class GDIDraw(object):
    def __init__(self):
        self.window_name = "OverlayFrame"
        self.hwnd = win32gui.FindWindow(0, self.window_name)
        self.hdc = win32gui.GetDC(self.hwnd)
    
    def brush(self, color):
        return win32gui.CreateSolidBrush(win32api.RGB(*color))

    def fill_rect(self, x, y, w, h, brush):
        rect = (x, y, x + w, y + h)
        win32gui.FillRect(self.hdc, rect, brush)
    
    def rect(self, x, y, w, h, t, brush):
        self.fill_rect(x, y, w, t, brush)
        self.fill_rect(x, y, t, h, brush)
        self.fill_rect((x + w), y, t, h, brush)
        self.fill_rect(x, (y + h), w+t, t, brush)
    
    def square(self, point, side_size, brush):
        if point is None:
            return
        x, y = point
        x,y = x - side_size//2, y - side_size//2
        self.rect(x, y, side_size, side_size, 3, brush)
    
    def line(self, p1, p2, t, color):
        if p1 is None or p2 is None:
            return
        pen = win32gui.CreatePen(win32con.PS_SOLID, t, win32api.RGB(*color))
        hoPen = win32gui.SelectObject(self.hdc, pen)
        win32gui.MoveToEx(self.hdc, p1[0], p1[1])
        win32gui.LineTo(self.hdc, p2[0], p2[1])
        win32gui.DeleteObject(win32gui.SelectObject(self.hdc, hoPen))

    def circle(self, point, radius, t, color):
        if point is None:
            return
        x,y = point
        pen = win32gui.CreatePen(win32con.PS_SOLID, t, win32api.RGB(*color))
        hoPen = win32gui.SelectObject(self.hdc, pen)
        win32gui.Arc(self.hdc, x-radius, y-radius, x+radius, y+radius,0,0,0,0)
        win32gui.DeleteObject(win32gui.SelectObject(self.hdc, hoPen))
    
    def elipse(self, point, r_alpha, r_beta, t, color):
        if point is None:
            return
        x,y = point
        pen = win32gui.CreatePen(win32con.PS_SOLID, t, win32api.RGB(*color))
        hoPen = win32gui.SelectObject(self.hdc, pen)
        win32gui.Arc(self.hdc, x-r_alpha, y-r_beta, x+r_alpha, y+r_beta,0,0,0,0)
        win32gui.DeleteObject(win32gui.SelectObject(self.hdc, hoPen))
