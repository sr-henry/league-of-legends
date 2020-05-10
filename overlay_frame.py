import wx
import win32api
import win32gui
import win32con

w = win32api.GetSystemMetrics(0)
h = win32api.GetSystemMetrics(1)

fuchsia = (255, 0, 128)

class FancyFrame(wx.Frame):
    def __init__(self):
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER )
        wx.Frame.__init__(self, None, title='OverlayFrame', style = style, size= wx.Size(w,h))
        self.SetBackgroundColour(fuchsia)
        win32gui.SetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.GetHandle(), win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.GetHandle(), win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
        
        self.timer=wx.Timer(self)

        self.timer.Start(125)
    
        self.Bind(wx.EVT_TIMER, self.evt_timer)

        self.Show()

    def evt_timer(self,event):  
        self.Refresh()

app = wx.App()

FancyFrame()

app.MainLoop()
 
