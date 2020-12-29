import math

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
