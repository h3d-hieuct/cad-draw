# 2021-10-28 - hieuhihi
from ancuong import max_min

def get_mm_wall(wall_data,mm):
    min_point_all = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
    max_point_all = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
    for wallPointData in wall_data:
        point_data = wallPointData.attrib['points'].split('|')
        for i in cut_wall(point_data,mm):
            if min_point_all[0] > float(i.split(',')[0]):
                min_point_all[0] = float(i.split(',')[0])
            if max_point_all[0] < float(i.split(',')[0]):
                max_point_all[0] = float(i.split(',')[0])
            if min_point_all[1] > float(i.split(',')[1]):
                min_point_all[1] = float(i.split(',')[1])
            if max_point_all[1] < float(i.split(',')[1]):
                max_point_all[1] = float(i.split(',')[1])
    w = max_point_all[0] - min_point_all[0]
    h = max_point_all[1] - min_point_all[1]
    if w/260 > h/210:
        scale = w/260
    else:
        scale = h/210
    if scale < 16:
        scale = 16
    return [min_point_all,max_point_all,int(scale)+1]

def cut_wall(point_data,mm):
    min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
    max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
    for i in point_data:
        if min_point[0] > float(i.split(',')[0]):
            min_point[0] = float(i.split(',')[0])
        if max_point[0] < float(i.split(',')[0]):
            max_point[0] = float(i.split(',')[0])
        if min_point[1] > float(i.split(',')[1]):
            min_point[1] = float(i.split(',')[1])
        if max_point[1] < float(i.split(',')[1]):
            max_point[1] = float(i.split(',')[1])

    point_data_after_cut = []
    if max_point[1] > mm[0][1] - 300 > min_point[1] and min_point[0] > mm[0][0] - 400 and max_point[0] < mm[1][0] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[1]) < mm[0][1]:
                point_data_after_cut.append(p[0] + ',' + str(mm[0][1] - 200))
            else:
                point_data_after_cut.append(i)
    if max_point[1] > mm[1][1] + 300 > min_point[1] and min_point[0] > mm[0][0] - 400 and max_point[0] < mm[1][0] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[1]) > mm[1][1]:
                point_data_after_cut.append(p[0] + ',' + str(mm[1][1] + 200))
            else:
                point_data_after_cut.append(i)
    if mm[0][1] - 300 < min_point[1] and mm[1][1] + 300 > max_point[1] and min_point[0] > mm[0][0] - 400 and max_point[
        0] < mm[1][0] + 400:
        point_data_after_cut = []
        for i in point_data:
            point_data_after_cut.append(i)
    if mm[0][1] - 300 > min_point[1] and mm[1][1] + 300 < max_point[1] and min_point[0] > mm[0][0] - 400 and max_point[
        0] < mm[1][0] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[1]) < mm[0][1]:
                point_data_after_cut.append(p[0] + ',' + str(mm[0][1] - 200))
            elif float(p[1]) > mm[1][1]:
                point_data_after_cut.append(p[0] + ',' + str(mm[1][1] + 200))
            else:
                point_data_after_cut.append(i)

    if min_point[0] < mm[1][0] + 300 < max_point[0] and min_point[1] > mm[0][1] - 400 and max_point[1] < mm[1][1] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[0]) > mm[1][0]:
                point_data_after_cut.append(str(mm[1][0] + 200) + ',' + p[1])
            else:
                point_data_after_cut.append(i)
    if min_point[0] < mm[0][0] - 300 < max_point[0] and min_point[1] > mm[0][1] - 400 and max_point[1] < mm[1][1] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[0]) < mm[0][0]:
                point_data_after_cut.append(str(mm[0][0] - 200) + ',' + p[1])
            else:
                point_data_after_cut.append(i)
    if mm[0][0] - 300 < min_point[0] and mm[1][0] + 300 > max_point[0] and min_point[1] > mm[0][1] - 400 and max_point[
        1] < mm[1][1] + 400:
        point_data_after_cut = []
        for i in point_data:
            point_data_after_cut.append(i)
    if mm[0][0] - 300 > min_point[0] and mm[1][0] + 300 < max_point[0] and min_point[1] > mm[0][1] - 400 and max_point[
        1] < mm[1][1] + 400:
        point_data_after_cut = []
        for i in point_data:
            p = i.split(',')
            if float(p[0]) > mm[1][0]:
                point_data_after_cut.append(str(mm[1][0] + 200) + ',' + p[1])
            elif float(p[0]) < mm[0][0]:
                point_data_after_cut.append(str(mm[0][0] - 200) + ',' + p[1])
            else:
                point_data_after_cut.append(i)

    return point_data_after_cut
