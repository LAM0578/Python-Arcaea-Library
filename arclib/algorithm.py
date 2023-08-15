import math
from .vector import vec2, vec3

# ARC

_HALF_PI = 1.5707963267948966

def straight(a, b, t):
    return a + (b - a) * t

def sineIn(a, b, t):
    return a + (b - a) * (1 - math.cos(t * _HALF_PI))

def sineOut(a, b, t):
    return a + (b - a) * math.sin(t * _HALF_PI)

def bezier(a, b, t):
    return a + (b - a) * ((3 * t - math.pow(2 * t, 2)) * t)

_ARC_X_FUNCTION = {
    's': straight,
    'si': sineIn,
    'sisi': sineOut,
    'siso': sineOut,
    'so': sineOut,
    'sosi': sineIn,
    'soso': sineIn,
    'b': bezier
}

_ARC_Y_FUNCTION = {
    's': straight,
    'si': straight,
    'sisi': sineOut,
    'siso': sineOut,
    'so': straight,
    'sosi': sineIn,
    'soso': sineIn,
    'b': bezier
}

_ARC_EASING = ['s', 'si', 'so', 'b', 'sisi', 'siso', 'sosi', 'soso']

def checkEasing(s):
    return s in _ARC_EASING

def calculate_x(start:float, end:float, arcEasing:str, t:float):
    if checkEasing(arcEasing):
        return _ARC_X_FUNCTION[arcEasing](start, end, t)
    return straight(start, end, t)

def calculate_y(start:float, end:float, arcEasing:str, t:float):
    if checkEasing(arcEasing):
        return _ARC_Y_FUNCTION[arcEasing](start, end, t)
    return straight(start, end, t)

def calculate(start:vec2, end:vec2, arcEasing:str, t:float):
    return vec2(calculate_x(start.x, end.x, arcEasing, t), calculate_y(start.y, end.y, arcEasing, t))

# CAMERA

def cubicIn(a, b, t):
    return a + (b - a) * (t ** 3)

def cubicOut(a, b, t):
    return a + (b - a) * ((t - 1) ** 3 + 1)
    
_CAMERA_EASING = ['reset', 'l', 's', 'qi', 'qo']

_CAMERA_FUNCTION = {
    'l': straight, # Linear
    's': straight, # Straight
    'qi': cubicIn, # Cubic In
    'qo': cubicOut # Cubic Out
}

def checkCameraEasing(e):
    return e in _CAMERA_EASING

def calculateCamera(start:vec3, end:vec3, cameraEasing:str, t:float):
    if checkCameraEasing(cameraEasing):
        return vec3(
            _CAMERA_FUNCTION[cameraEasing](start.x, end.x, t),
            _CAMERA_FUNCTION[cameraEasing](start.y, end.y, t),
            _CAMERA_FUNCTION[cameraEasing](start.z, end.z, t)
        )
    return vec3()
