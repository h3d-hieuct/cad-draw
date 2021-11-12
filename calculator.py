# 2021-10-28 - hieuhihi
import math
import numpy as np

def rotate_part(part,rotate):
    result = []
    for point in part:
        if point['type'] == 0:
            if 'x' in point:
                result.append({'type':0,'data':re_rotate_XYZ(point['x'],point['y'],point['z'],rotate)})
            else:
                result.append({'type':0,'data':rotate_XYZ(point['data'][0], point['data'][1], point['data'][2], rotate)})
    return result

def rotate_tran(x, y, rotate):
    x1 = round(x * math.cos(rotate / 180 * math.pi) - y * math.sin(rotate / 180 * math.pi), 2)
    y1 = round(x * math.sin(rotate / 180 * math.pi) + y * math.cos(rotate / 180 * math.pi), 2)
    return [x1, y1]

def rotate_XYZ(x, y, z, rotate):
    rotate_x = rotate_tran(y, z, rotate[0])
    y = rotate_x[0]
    z = rotate_x[1]
    rotate_y = rotate_tran(z, x, rotate[1])
    z = rotate_y[0]
    x = rotate_y[1]
    rotate_z = rotate_tran(x, y, rotate[2])
    x = rotate_z[0]
    y = rotate_z[1]
    return [x, y, z]

def re_rotate_XYZ(x, y, z, rotate):
    rotate_z = rotate_tran(x, y, -rotate[2])
    x = rotate_z[0]
    y = rotate_z[1]
    rotate_y = rotate_tran(z, x, -rotate[1])
    z = rotate_y[0]
    x = rotate_y[1]
    rotate_x = rotate_tran(y, z, -rotate[0])
    y = rotate_x[0]
    z = rotate_x[1]
    return [x, y, z]

def generate_corner_point(cx, cy, start, angle, segment):
    result = []
    x = start[0]
    y = start[1]
    for i in range(int(segment) + 1):
        a_rad = np.deg2rad(-angle * i / segment)
        px = (x - cx) * np.cos(a_rad) - (y - cy) * np.sin(a_rad) + cx
        py = (x - cx) * np.sin(a_rad) + (y - cy) * np.cos(a_rad) + cy
        result.append((px, py))
    return result

def distance(point1, point2):
    if "x" and "y" in point1 and "x" and "y" in point2:
        return math.sqrt(math.pow(point1['x'] - point2['x'], 2) + math.pow(point1['y'] - point2['y'], 2))
    if "x" and "y" in point1 and "x" and "y" not in point2:
        return math.sqrt(math.pow(point1['x'] - point2[0], 2) + math.pow(point1['y'] - point2[1], 2))
    if "x" and "y" not in point1 and "x" and "y" in point2:
        return int(math.sqrt(math.pow(point1[0] - point2['x'], 2) + math.pow(point1[1] - point2['y'], 2)))
    else:
        return int(math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2)))

def x(num=0,scale=0):
    return 260 * 4 + 297 * num * (scale + 8)

def y(scale=0):
    return 210 * 4 + scale * 210
