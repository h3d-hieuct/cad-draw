# 2021-10-28 - hieuhihi
import calculator
DEFAULT_MAX = -9999999999999999999999999999
DEFAULT_MIN = 99999999999999999999999999999

def get_mm_location(module_part_location, rotate=0, rotate_face=None):
    min_point = [DEFAULT_MIN, DEFAULT_MIN, DEFAULT_MIN]
    max_point = [DEFAULT_MAX, DEFAULT_MAX, DEFAULT_MAX]
    for module_part in module_part_location:
        for part in module_part:
            part = rotate_part(part,[0,0,rotate])
            if rotate_face is not None:
                part = rotate_part(part,rotate_face)
            get_max_point_part(part,max_point)
            get_min_point_part(part,min_point)
    return [min_point,max_point]

def rotate_part(part,rotate):
    result = []
    for point in part:
        if point['type'] == 0:
            if 'x' in point:
                result.append({'type':0,'data':calculator.re_rotate_XYZ(point['x'],point['y'],point['z'],rotate)})
            else:
                result.append({'type':0,'data':calculator.rotate_XYZ(point['data'][0], point['data'][1], point['data'][2], rotate)})
    return result

def get_max_point_3d(max_point, point):
    if point[0] > max_point[0]:
        max_point[0] = point[0]
    if point[1] > max_point[1]:
        max_point[1] = point[1]
    if point[2] > max_point[2]:
        max_point[2] = point[2]

def get_min_point_3d(min_point, point):
    if min_point[0] > point[0]:
        min_point[0] = point[0]
    if min_point[1] > point[1]:
        min_point[1] = point[1]
    if min_point[2] > point[2]:
        min_point[2] = point[2]

def get_min_point_part(part,min_point):
    for point in part:
        if point['type'] == 0:
            if 'data' in point:
                get_min_point_3d(min_point, point['data'])
                # if min_point[0]>point['data'][0]:
                #     min_point[0] = point['data'][0]
                # if min_point[1]>point['data'][1]:
                #     min_point[1] = point['data'][1]
                # if min_point[2]>point['data'][2]:
                #     min_point[2] = point['data'][2]

def get_max_point_part(part,max_point):
    for point in part:
        if point['type'] == 0:
            if 'data' in point:
                get_max_point_3d(max_point, point['data'])
                # if min_point[0]<point['data'][0]:
                #     min_point[0] = point['data'][0]
                # if min_point[1]<point['data'][1]:
                #     min_point[1] = point['data'][1]
                # if min_point[2]<point['data'][2]:
                #     min_point[2] = point['data'][2]

def get_max_point(points):
    value_x = points[0][0]
    value_y = points[0][1]
    for point in points:
        if value_x < point[0]:
            value_x = point[0]
        if value_y < point[1]:
            value_y = point[1]
    return value_x, value_y

def get_min_point(points):
    value_x = points[0][0]
    value_y = points[0][1]
    for point in points:
        if value_x > point[0]:
            value_x = point[0]
        if value_y > point[1]:
            value_y = point[1]
    return value_x, value_y

def get_max(point1, point2):
    if point1 > point2:
        return point1
    else:
        return point2

def get_min(point1, point2):
    if point1 < point2:
        return point1
    else:
        return point2


def get_max_min_point_part(part):
    min_point = [DEFAULT_MIN, DEFAULT_MIN, DEFAULT_MIN]
    max_point = [DEFAULT_MAX, DEFAULT_MAX, DEFAULT_MAX]
    get_max_point_part(part, max_point)
    get_min_point_part(part, min_point)
    return [min_point,max_point]