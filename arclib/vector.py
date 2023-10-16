
def isnum(x):
    return isinstance(x, (float, int))

class vec2:
    def __init__(self, x=None, y=None):
        self.__reg()
        if isnum(x) and isnum(y):
            self.x = x
            self.y = y
        elif x == y == None:
            return
        else:
            raise TypeError('x or y is None or not number.')
        
    @staticmethod   
    def parse(t):
        return vec2(float(t[0]), float(t[1]))

    def __reg(self):
        self.x = 0
        self.y = 0

    def __add__(self, v):
        if isnum(v):
            return vec2(self.x + v, self.y + v)
        return vec2(self.x + v.x, self.y + v.y)

    def __sub__(self, v):
        if isnum(v):
            return vec2(self.x - v, self.y - v)
        return vec2(self.x - v.x, self.y - v.y)

    def __mul__(self, v):
        if isnum(v):
            return vec2(self.x * v, self.y * v)
        return vec2(self.x * v.x, self.y * v.y)

    def __truediv__(self, v):
        if isnum(v):
            return vec2(self.x / v, self.y / v)
        return vec2(self.x / v.x, self.y / v.y)

    def __list__(self):
        return [float(self.x), float(self.y)]

    def __str__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f})'

    def __repr__(self) -> str:
        return f'vec2{self.__str__()}'

class vec3:
    def __init__(self, x=None, y=None, z=None):
        self.__reg()
        if isnum(x) and isnum(y):
            self.x = x
            self.y = y
            if isnum(z):
                self.z = z
        elif x == y == z == None:
            return
        else:
            raise TypeError('x or y or z is None or not number.')

    @staticmethod   
    def parse(t):
        return vec3(float(t[0]), float(t[1]), float(t[2]))
    
    def __reg(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __add__(self, v):
        if isnum(v):
            return vec2(self.x + v, self.y + v, self.z + v)
        return vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        if isnum(v):
            return vec2(self.x - v, self.y - v, self.z - v)
        return vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, v):
        if isnum(v):
            return vec2(self.x * v, self.y * v, self.z * v)
        return vec3(self.x * v.x, self.y * v.y, self.z * v.z)

    def __truediv__(self, v):
        if isnum(v):
            return vec3(self.x / v, self.y / v, self.z / v)
        return vec3(self.x / v.x, self.y / v.y, self.z / v.z)
    
    def __list__(self):
        return [float(self.x), float(self.y), float(self.z)]

    def __str__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f}, {self.z:.3f})'

    def __repr__(self) -> str:
        return f'vec3{self.__str__()}'
