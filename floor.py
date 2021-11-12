# 2021-10-28 - hieuhihi
from shapely import geometry
from shapely.algorithms import polylabel
import math

from ancuong import wall_support, furniture_hardware, max_min, dim

class Floor(object):
    def __init__(self,msp,walls,in_wall_data,furniture_data,rooms):
        self.msp = msp
        self.walls = walls
        self.in_wall_data = in_wall_data
        self.furniture_data = furniture_data
        self.rooms = rooms

    def write_hatch(self,door_importer,dx=0,dy=0,distance=-120,color=1, mm=None):
        in_wall_room = []
        for wallData in self.in_wall_data:
            in_wall_room.append(wallData.attrib)
        for wallPointData in self.walls:
            point_data = wallPointData.attrib['points'].split('|')
            if mm is not None:
                point_data = wall_support.cut_wall(point_data, mm)
            if len(point_data) > 0:
                point_arr = []
                in_wall_id = []
                for i in point_data:
                    point_arr.append([float(i.split(',')[0]) + dx, float(i.split(',')[1]) + dy])
                for data in in_wall_room:
                    if data['wallUID'] == wallPointData.attrib['wallUID']:
                        if data not in in_wall_id:
                            in_wall_id.append(data)
                        x = float(data['PosX']) + dx
                        y = float(data['PosY']) + dy
                        cos_x_length = cos(data['XLength'], data['RotateZ'])
                        sin_x_length = sin(data['XLength'], data['RotateZ'])

                        if data['Type'] == 'BayWindow':
                            cos_y_width = cos(wallPointData.attrib['wallThick'], data['RotateZ'])
                            sin_y_width = sin(wallPointData.attrib['wallThick'], data['RotateZ'])
                            self.msp.add_line(
                                (x - cos_x_length - sin_y_width, y - sin_x_length + cos_y_width),
                                (x - cos_x_length - 7 * sin_y_width, y - sin_x_length + 7 * cos_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x + cos_x_length - sin_y_width, y + sin_x_length + cos_y_width),
                                (x + cos_x_length - 7 * sin_y_width, y + sin_x_length + 7 * cos_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x - cos_x_length - 7 * sin_y_width, y - sin_x_length + 7 * cos_y_width),
                                (x + cos_x_length - 7 * sin_y_width, y + sin_x_length + 7 * cos_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x - cos_x_length - sin_y_width - cos_y_width, y - sin_x_length + cos_y_width - sin_y_width),
                                (x - cos_x_length - 8 * sin_y_width - cos_y_width, y - sin_x_length + 8 * cos_y_width - sin_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x + cos_x_length - sin_y_width + cos_y_width, y + sin_x_length + cos_y_width + sin_y_width),
                                (x + cos_x_length - 8 * sin_y_width + cos_y_width, y + sin_x_length + 8 * cos_y_width + sin_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x - cos_x_length - 8 * sin_y_width - cos_y_width, y - sin_x_length + 8 * cos_y_width - sin_y_width),
                                (x + cos_x_length - 8 * sin_y_width + cos_y_width, y + sin_x_length + 8 * cos_y_width + sin_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x - cos_x_length - sin_y_width - 2 * cos_y_width, y - sin_x_length + cos_y_width - 2 * sin_y_width),
                                (x - cos_x_length - 9 * sin_y_width - 2 * cos_y_width, y - sin_x_length + 9 * cos_y_width - 2 * sin_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x + cos_x_length - sin_y_width + 2 * cos_y_width, y + sin_x_length + cos_y_width + 2 * sin_y_width),
                                (x + cos_x_length - 9 * sin_y_width + 2 * cos_y_width, y + sin_x_length + 9 * cos_y_width + 2 * sin_y_width),
                                dxfattribs={'color': '3'})
                            self.msp.add_line(
                                (x - cos_x_length - 9 * sin_y_width - 2 * cos_y_width, y - sin_x_length + 9 * cos_y_width - 2 * sin_y_width),
                                (x + cos_x_length - 9 * sin_y_width + 2 * cos_y_width, y + sin_x_length + 9 * cos_y_width + 2 * sin_y_width),
                                dxfattribs={'color': '3'})
                        else:
                            cos_y_width = cos(data['YWidth'], data['RotateZ'])
                            sin_y_width = sin(data['YWidth'], data['RotateZ'])
                            self.msp.add_line(
                                (x + cos_x_length - sin_y_width, y + sin_x_length + cos_y_width),
                                (x - cos_x_length - sin_y_width, y - sin_x_length + cos_y_width),
                                dxfattribs={'color': '3'})
                        self.msp.add_line(
                            (x - cos_x_length + sin_y_width, y - sin_x_length - cos_y_width),
                            (x - cos_x_length - sin_y_width, y - sin_x_length + cos_y_width),
                            dxfattribs={'color': '3'})
                        self.msp.add_line(
                            (x + cos_x_length + sin_y_width, y + sin_x_length - cos_y_width),
                            (x + cos_x_length - sin_y_width, y + sin_x_length + cos_y_width),
                            dxfattribs={'color': '3'})
                        self.msp.add_line(
                            (x + cos_x_length + sin_y_width, y + sin_x_length - cos_y_width),
                            (x - cos_x_length + sin_y_width, y - sin_x_length - cos_y_width),
                            dxfattribs={'color': '3'})
                        if data['Type'] == 'SingleDoor':
                            door_importer.import_block(block_name='left_door')
                            door_importer.import_block(block_name='right_door')
                            door_importer.finalize()
                            if data['RotateTimes'] == '2' or data['RotateTimes'] == '0':
                                self.msp.add_blockref('right_door', insert=(x, y), dxfattribs={
                                    'xscale': float(data['XLength']) / 10,
                                    'yscale': float(data['XLength']) / 10,
                                    'rotation': float(data['RotateZ']),
                                    'color': '3'})
                            if data['RotateTimes'] == '3' or data['RotateTimes'] == '1':
                                self.msp.add_blockref('left_door', insert=(x, y), dxfattribs={
                                    'xscale': float(data['XLength']) / 10,
                                    'yscale': float(data['XLength']) / 10,
                                    'rotation': float(data['RotateZ']),
                                    'color': '3'})
                        if data['Type'] == 'SafetyDoor':
                            door_importer.import_block(block_name='safety_door_left')
                            door_importer.import_block(block_name='safety_door_right')
                            door_importer.finalize()
                            if data['RotateTimes'] == '2' or data['RotateTimes'] == '0':
                                self.msp.add_blockref('safety_door_left', insert=(x, y), dxfattribs={
                                    'xscale': float(data['XLength']) / 10,
                                    'yscale': float(data['XLength']) / 10,
                                    'rotation': float(data['RotateZ'])})
                            if data['RotateTimes'] == '3' or data['RotateTimes'] == '1':
                                self.msp.add_blockref('safety_door_right', insert=(x, y), dxfattribs={
                                    'xscale': float(data['XLength']) / 10,
                                    'yscale': float(data['XLength']) / 10,
                                    'rotation': float(data['RotateZ'])})
                        if data['Type'] == 'DoubleDoor':
                            door_importer.import_block(block_name='double_door')
                            door_importer.finalize()
                            self.msp.add_blockref('double_door', insert=(x, y), dxfattribs={
                                'xscale': float(data['XLength']) / 10,
                                'yscale': float(data['XLength']) / 10,
                                'rotation': float(data['RotateZ'])})
                        if data['Type'] != 'DoorHole' and data['Type'] != 'BayWindow':
                            self.msp.add_line(
                                (x - cos_x_length, y - sin_x_length),
                                (x + cos_x_length, y + sin_x_length),
                                dxfattribs={'color': '3'})

                if len(in_wall_id) > 0 and len(point_data) > 0:

                    def get_key(elem):
                        return math.pow(point_arr[0][0] - float(elem['PosX']), 2) + math.pow(
                            point_arr[0][1] - float(elem['PosY']), 2)

                    in_wall_id = sorted(in_wall_id, key=get_key)

                    x = float(in_wall_id[0]['PosX']) + dx
                    y = float(in_wall_id[0]['PosY']) + dy
                    cos_x_length = cos(in_wall_id[0]['XLength'], in_wall_id[0]['RotateZ'])
                    sin_x_length = sin(in_wall_id[0]['XLength'], in_wall_id[0]['RotateZ'])
                    cos_wall_thick = cos(wallPointData.attrib['wallThick'], in_wall_id[0]['RotateZ'])
                    sin_wall_thick = sin(wallPointData.attrib['wallThick'], in_wall_id[0]['RotateZ'])

                    point_in_1 = near_point(point_arr[0],
                        near_point(point_arr[0],
                           (x - cos_x_length + sin_wall_thick, y - sin_x_length - cos_wall_thick),
                           (x + cos_x_length - sin_wall_thick, y + sin_x_length + cos_wall_thick)),
                        near_point(point_arr[0],
                           (x - cos_x_length - sin_wall_thick, y - sin_x_length + cos_wall_thick),
                           (x + cos_x_length + sin_wall_thick, y + sin_x_length - cos_wall_thick)))

                    point_in_2 = near_point(point_arr[3],
                        near_point(point_arr[3],
                           (x - cos_x_length + sin_wall_thick, y - sin_x_length - cos_wall_thick),
                           (x + cos_x_length - sin_wall_thick, y + sin_x_length + cos_wall_thick)),
                        near_point(point_arr[3],
                           (x - cos_x_length - sin_wall_thick, y - sin_x_length + cos_wall_thick),
                           (x + cos_x_length + sin_wall_thick, y + sin_x_length - cos_wall_thick)))

                    if not (x - cos_x_length < point_arr[0][0] < x + cos_x_length
                            or x - cos_x_length > point_arr[0][0] > x + cos_x_length
                            or y - sin_x_length < point_arr[0][1] < y + sin_x_length
                            or y - sin_x_length > point_arr[0][1] > y + sin_x_length):
                        dim.draw_dim(self.msp, [point_arr[0], point_in_1], distance, dimcolor=color)
                        self.msp.add_line(point_arr[0], point_in_1, dxfattribs={'color': '7'})
                        self.msp.add_line(point_in_2, point_arr[3], dxfattribs={'color': '7'})
                        self.msp.add_line(point_in_1, point_in_2, dxfattribs={'color': '7'})
                        self.msp.add_line(point_arr[0], point_arr[3], dxfattribs={'color': '7'})

                    x = float(in_wall_id[len(in_wall_id) - 1]['PosX']) + dx
                    y = float(in_wall_id[len(in_wall_id) - 1]['PosY']) + dy
                    cos_x_length = cos(in_wall_id[len(in_wall_id) - 1]['XLength'],
                                       in_wall_id[len(in_wall_id) - 1]['RotateZ'])
                    sin_x_length = sin(in_wall_id[len(in_wall_id) - 1]['XLength'],
                                       in_wall_id[len(in_wall_id) - 1]['RotateZ'])
                    cos_wall_thick = cos(wallPointData.attrib['wallThick'], in_wall_id[len(in_wall_id) - 1]['RotateZ'])
                    sin_wall_thick = sin(wallPointData.attrib['wallThick'], in_wall_id[len(in_wall_id) - 1]['RotateZ'])

                    point_in_1 = near_point(point_arr[1],
                        near_point(point_arr[1],
                           (x + cos_x_length + sin_wall_thick, y + sin_x_length - cos_wall_thick),
                           (x - cos_x_length - sin_wall_thick, y - sin_x_length + cos_wall_thick)),
                        near_point(point_arr[1],
                           (x + cos_x_length - sin_wall_thick, y + sin_x_length + cos_wall_thick),
                           (x - cos_x_length + sin_wall_thick, y - sin_x_length - cos_wall_thick)))

                    point_in_2 = near_point(point_arr[2],
                        near_point(point_arr[2],
                           (x + cos_x_length + sin_wall_thick, y + sin_x_length - cos_wall_thick),
                           (x - cos_x_length - sin_wall_thick, y - sin_x_length + cos_wall_thick)),
                        near_point(point_arr[2],
                           (x + cos_x_length - sin_wall_thick, y + sin_x_length + cos_wall_thick),
                           (x - cos_x_length + sin_wall_thick, y - sin_x_length - cos_wall_thick)))

                    if not (x - cos_x_length < point_arr[1][0] < x + cos_x_length
                            or x - cos_x_length > point_arr[1][0] > x + cos_x_length
                            or y - sin_x_length < point_arr[1][1] < y + sin_x_length
                            or y - sin_x_length > point_arr[1][1] > y + sin_x_length):
                        dim.draw_dim(self.msp, [point_in_1, point_arr[1]], distance, dimcolor=color)
                        self.msp.add_line(point_in_1, point_arr[1], dxfattribs={'color': '7'})
                        self.msp.add_line(point_arr[2], point_in_2, dxfattribs={'color': '7'})
                        self.msp.add_line(point_in_1, point_in_2, dxfattribs={'color': '7'})
                        self.msp.add_line(point_arr[1], point_arr[2], dxfattribs={'color': '7'})

                    if len(in_wall_id) > 1:
                        for x in range(len(in_wall_id) - 1):
                            rotate_z = float(in_wall_id[x]['RotateZ']) % 180
                            cos_x_length_start = cos(in_wall_id[x]['XLength'], rotate_z)
                            sin_x_length_start = sin(in_wall_id[x]['XLength'], rotate_z)
                            cos_wall_thick_start = cos(wallPointData.attrib['wallThick'], rotate_z)
                            sin_wall_thick_start = sin(wallPointData.attrib['wallThick'], rotate_z)

                            rotate_z = float(in_wall_id[x + 1]['RotateZ']) % 180
                            cos_x_length_end = cos(in_wall_id[x + 1]['XLength'], rotate_z)
                            sin_x_length_end = sin(in_wall_id[x + 1]['XLength'], rotate_z)
                            cos_wall_thick_end = cos(wallPointData.attrib['wallThick'], rotate_z)
                            sin_wall_thick_end = sin(wallPointData.attrib['wallThick'], rotate_z)

                            point_in_1 = near_point(point_arr[0],
                                far_point(point_arr[0],
                                  (float(in_wall_id[x]['PosX']) + cos_x_length_start + sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) + sin_x_length_start - cos_wall_thick_start),
                                  (float(in_wall_id[x]['PosX']) - cos_x_length_start + sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) - sin_x_length_start - cos_wall_thick_start)),
                                far_point(point_arr[0],
                                  (float(in_wall_id[x]['PosX']) + cos_x_length_start - sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) + sin_x_length_start + cos_wall_thick_start),
                                  (float(in_wall_id[x]['PosX']) - cos_x_length_start - sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) - sin_x_length_start + cos_wall_thick_start)))

                            point_in_2 = near_point(point_arr[0],
                                near_point(point_arr[0],
                                   (float(in_wall_id[x + 1]['PosX']) - cos_x_length_end + sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) - sin_x_length_end - cos_wall_thick_end),
                                   (float(in_wall_id[x + 1]['PosX']) + cos_x_length_end + sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) + sin_x_length_end - cos_wall_thick_end)),
                                near_point(point_arr[0],
                                   (float(in_wall_id[x + 1]['PosX']) - cos_x_length_end - sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) - sin_x_length_end + cos_wall_thick_end),
                                   (float(in_wall_id[x + 1]['PosX']) + cos_x_length_end - sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) + sin_x_length_end + cos_wall_thick_end)))

                            self.msp.add_line(point_in_1, point_in_2, dxfattribs={'color': '7'})
                            dim.draw_dim(self.msp,[point_in_1, point_in_2], distance, dimcolor=color)

                            point_out_1 = far_point(point_arr[0],
                                far_point(point_arr[0],
                                  (float(in_wall_id[x]['PosX']) + cos_x_length_start + sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) + sin_x_length_start - cos_wall_thick_start),
                                  (float(in_wall_id[x]['PosX']) - cos_x_length_start + sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) - sin_x_length_start - cos_wall_thick_start)),
                                far_point(point_arr[0],
                                  (float(in_wall_id[x]['PosX']) + cos_x_length_start - sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) + sin_x_length_start + cos_wall_thick_start),
                                  (float(in_wall_id[x]['PosX']) - cos_x_length_start - sin_wall_thick_start,
                                   float(in_wall_id[x]['PosY']) - sin_x_length_start + cos_wall_thick_start)))

                            point_out_2 = far_point(point_arr[0],
                                near_point(point_arr[0],
                                   (float(in_wall_id[x + 1]['PosX']) - cos_x_length_end + sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) - sin_x_length_end - cos_wall_thick_end),
                                   (float(in_wall_id[x + 1]['PosX']) + cos_x_length_end + sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) + sin_x_length_end - cos_wall_thick_end)),
                                near_point(point_arr[0],
                                   (float(in_wall_id[x + 1]['PosX']) - cos_x_length_end - sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) - sin_x_length_end + cos_wall_thick_end),
                                   (float(in_wall_id[x + 1]['PosX']) + cos_x_length_end - sin_wall_thick_end,
                                    float(in_wall_id[x + 1]['PosY']) + sin_x_length_end + cos_wall_thick_end)))

                            self.msp.add_line(point_out_1, point_out_2, dxfattribs={'color': '7'})
                else:
                    dim.draw_dim(self.msp,[point_arr[0], point_arr[1]], distance, dimcolor=color)
                    self.msp.add_line(point_arr[0], point_arr[1], dxfattribs={'color': '7'})
                    self.msp.add_line(point_arr[2], point_arr[3], dxfattribs={'color': '7'})
                    self.msp.add_line(point_arr[0], point_arr[3], dxfattribs={'color': '7'})
                    self.msp.add_line(point_arr[1], point_arr[2], dxfattribs={'color': '7'})

    def write_furniture(self,doc,category_id,attribute_importer):
        for furniture in self.furniture_data:
            x = float(furniture.attrib['PosX'])
            y = float(furniture.attrib['PosY'])
            h = float(furniture.attrib['Length'])
            w = float(furniture.attrib['Width'])
            rotate = float(furniture.attrib['RotateZ'])
            model_type = furniture.attrib['Type']
            if model_type == 'Part':
                self.draw_overview(x, y, h, w, rotate)
                continue
            # block name is material attribute in model info (Attribute in xml file)
            attribute = furniture.attrib['Attribute']
            # if attribute is empty or null draw overview by categoryId
            if attribute == '' or attribute == 'null':
                cate = furniture.attrib['categoryId']
                if cate in category_id:
                    attribute = category_id[cate]

            cos_x_length = cos(h, rotate)
            sin_x_length = sin(h, rotate)
            cos_y_width = cos(w, rotate)
            sin_y_width = sin(w, rotate)
            if attribute == '' or attribute == 'null':
                print("No attribute for {} use default overview".format(furniture.attrib['materialId']))
                self.msp.add_line(
                    (x - cos_x_length + sin_y_width, y - sin_x_length - cos_y_width),
                    (x - cos_x_length - sin_y_width, y - sin_x_length + cos_y_width),
                    dxfattribs={'color': '3'})
                self.msp.add_line(
                    (x + cos_x_length + sin_y_width, y + sin_x_length - cos_y_width),
                    (x + cos_x_length - sin_y_width, y + sin_x_length + cos_y_width),
                    dxfattribs={'color': '3'})
                self.msp.add_line(
                    (x + cos_x_length + sin_y_width, y + sin_x_length - cos_y_width),
                    (x - cos_x_length + sin_y_width, y - sin_x_length - cos_y_width),
                    dxfattribs={'color': '3'})
                self.msp.add_line(
                    (x + cos_x_length - sin_y_width, y + sin_x_length + cos_y_width),
                    (x - cos_x_length - sin_y_width, y - sin_x_length + cos_y_width),
                    dxfattribs={'color': '3'})
            else:
                print("Found materialId: {} Import: ".format(furniture.attrib['materialId']) + attribute)
                try:
                    attribute_importer.import_block(block_name=attribute)
                    attribute_importer.finalize()
                    furniture_hardware.add_block(self.msp, doc, attribute, (x, y), furniture)
                except:
                    print("Attribute: {} not found".format(attribute))

    def dim(self):
        print("Start dim")
        room_arr = []
        wall_arr = []
        if self.rooms:
            for room in self.rooms:
                room.attrib['wallRoom'] = []
                room_arr.append(room.attrib)
            for wall in self.walls:
                wall_arr.append(wall.attrib)
                for r in room_arr:
                    wall_id_arr = r['wallsUid'].split(',')
                    if wall.attrib['wallUID'] in wall_id_arr:
                        if float(wall.attrib['wallThick']) > 100:
                            r['wallRoom'].append(wall)
            top_point_arr = []
            bottom_point_arr = []
            left_point_arr = []
            right_point_arr = []
            for room in room_arr:
                if len(room['wallRoom']) == 0:
                    return
                for points in top_wall(room['wallRoom']):
                    for point in points.attrib['points'].split('|'):
                        top_point_arr.append(round(float(point.split(',')[0])))
                for points in bottom_wall(room['wallRoom']):
                    for point in points.attrib['points'].split('|'):
                        bottom_point_arr.append(round(float(point.split(',')[0])))
                for points in left_wall(room['wallRoom']):
                    for point in points.attrib['points'].split('|'):
                        left_point_arr.append(round(float(point.split(',')[1])))
                for points in right_wall(room['wallRoom']):
                    for point in points.attrib['points'].split('|'):
                        right_point_arr.append(round(float(point.split(',')[1])))

            top_point_arr = refresh_arr(top_point_arr)
            bottom_point_arr = refresh_arr(bottom_point_arr)
            left_point_arr = refresh_arr(left_point_arr)
            right_point_arr = refresh_arr(right_point_arr)
            if len(top_point_arr) > 0 and len(bottom_point_arr) > 0 and len(left_point_arr) > 0 and len(
                    right_point_arr) > 0:
                self.draw_dim_top_arr(top_point_arr,max_min.get_max(left_point_arr[len(left_point_arr) - 1],
                                        right_point_arr[len(right_point_arr) - 1]) + 1000)
                self.draw_dim_bottom_arr(bottom_point_arr, max_min.get_min(left_point_arr[0], right_point_arr[0]) - 1000)
                self.draw_dim_left_arr(left_point_arr, max_min.get_min(top_point_arr[0], bottom_point_arr[0]) - 1000)
                self.draw_dim_right_arr(right_point_arr,max_min.get_max(top_point_arr[len(top_point_arr) - 1],
                                        bottom_point_arr[len(bottom_point_arr) - 1]) + 1000)

    def add_room_name(self):
        for room in self.rooms:
            point_list = []
            points = room.findall('InnerPoints')[0].attrib['value'].split('|')
            if points == ['']:
                return
            for point in points:
                p = (float(point.split(',')[0]), float(point.split(',')[1]))
                point_list.append(p)
            polygon = geometry.LineString(point_list).buffer(10000)
            label = polylabel.polylabel(polygon, tolerance=10)
            room_name = room.attrib['name']
            attr = {
                'style': "h3d_style",
                'height': 150,
            }
            self.msp.add_text(room_name, dxfattribs=attr).set_pos((label.x - len(room_name) * 65, label.y - 75),
                                                             align='left')

    def draw_dim_top_arr(self, point_arr, T):
        for i in range(len(point_arr) - 1):
            if not math.fabs(point_arr[i] - point_arr[i + 1]) < 100:
                dim.draw_dim(self.msp, [(point_arr[i], T), (point_arr[i + 1], T)], 400, 200, 200, (600, 400))
        dim.draw_dim(self.msp, [(point_arr[0], T), (point_arr[len(point_arr) - 1], T)], 1000, 200, 200)

    def draw_dim_bottom_arr(self, point_arr, B):
        for i in range(len(point_arr) - 1):
            if not math.fabs(point_arr[i] - point_arr[i + 1]) < 50:
                dim.draw_dim(self.msp, [(point_arr[i], B), (point_arr[i + 1], B)], -400, 200, 200, (-600, -300))
        dim.draw_dim(self.msp, [(point_arr[0], B), (point_arr[len(point_arr) - 1], B)], -1000, 200, 200)

    def draw_dim_left_arr(self, point_arr, L):
        for i in range(len(point_arr) - 1):
            if not math.fabs(point_arr[i] - point_arr[i + 1]) < 50:
                dim.draw_dim(self.msp, [(L, point_arr[i]), (L, point_arr[i + 1])], 400, 200, 200, (-400, 500))
        dim.draw_dim(self.msp, [(L, point_arr[0]), (L, point_arr[len(point_arr) - 1])], 1000, 200, 200)

    def draw_dim_right_arr(self, point_arr, R):
        for i in range(len(point_arr) - 1):
            if not math.fabs(point_arr[i] - point_arr[i + 1]) < 50:
                dim.draw_dim(self.msp, [(R, point_arr[i]), (R, point_arr[i + 1])], -200, 200, 200, (250, -600))
        dim.draw_dim(self.msp, [(R, point_arr[0]), (R, point_arr[len(point_arr) - 1])], -700, 200, 200)

    def draw_overview(self, x, y, w, d, rotate, color=251):
        cos_rz = math.cos(rotate / 180 * math.pi)
        sin_rz = math.sin(rotate / 180 * math.pi)
        self.msp.add_polyline2d(
            [(x, y),
             (x + w * cos_rz, y + w * sin_rz),
             (x + w * cos_rz + d * sin_rz, y + w * sin_rz - d * cos_rz),
             (x + d * sin_rz, y - d * cos_rz),
             (x, y)],
            dxfattribs={'color': color})

def near_point(point1, point2, point3):
    distance12 = math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2)
    distance13 = math.pow(point1[0] - point3[0], 2) + math.pow(point1[1] - point3[1], 2)
    if distance12 < distance13:
        return point2
    else:
        return point3

def far_point(point1, point2, point3):
    distance12 = math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2)
    distance13 = math.pow(point1[0] - point3[0], 2) + math.pow(point1[1] - point3[1], 2)
    if distance12 < distance13:
        return point3
    else:
        return point2

def top_wall(wallData):
    hor_wall = horizontal_wall(wallData)
    top_wall_arr = []
    for wall in hor_wall:
        point = wall.attrib['points'].split('|')
        if (math.fabs(float(point[0].split(',')[0]) - float(point[1].split(',')[0])) < math.fabs(
                float(point[2].split(',')[0]) - float(
                    point[3].split(',')[0])) and float(point[0].split(',')[1]) < float(point[2].split(',')[1])) or (
                math.fabs(float(point[0].split(',')[0]) - float(point[1].split(',')[0])) > math.fabs(
            float(point[2].split(',')[0]) - float(
                point[3].split(',')[0])) and float(point[0].split(',')[1]) > float(point[2].split(',')[1])):
            top_wall_arr.append(wall)
    return top_wall_arr

def bottom_wall(wallData):
    horWall = horizontal_wall(wallData)
    bottomWallArr = []
    for wall in horWall:
        point = wall.attrib['points'].split('|')
        if (math.fabs(float(point[0].split(',')[0]) - float(point[1].split(',')[0])) > math.fabs(
                float(point[2].split(',')[0]) - float(
                    point[3].split(',')[0])) and float(point[0].split(',')[1]) < float(point[2].split(',')[1])) or (
                math.fabs(float(point[0].split(',')[0]) - float(point[1].split(',')[0])) < math.fabs(
            float(point[2].split(',')[0]) - float(
                point[3].split(',')[0])) and float(point[0].split(',')[1]) > float(point[2].split(',')[1])):
            bottomWallArr.append(wall)
    return bottomWallArr

def left_wall(wall_data):
    ver_wall = vertical_wall(wall_data)
    left_walls = []
    for wall in ver_wall:
        point = wall.attrib['points'].split('|')
        if (math.fabs(float(point[0].split(',')[1]) - float(point[1].split(',')[1])) < math.fabs(
                float(point[2].split(',')[1]) - float(
                    point[3].split(',')[1])) and float(point[0].split(',')[0]) > float(point[2].split(',')[0])) or (
                math.fabs(float(point[0].split(',')[1]) - float(point[1].split(',')[1])) > math.fabs(
            float(point[2].split(',')[1]) - float(
                point[3].split(',')[1])) and float(point[0].split(',')[0]) < float(point[2].split(',')[0])):
            left_walls.append(wall)
    return left_walls

def right_wall(wall_data):
    ver_wall = vertical_wall(wall_data)
    right_walls = []
    for wall in ver_wall:
        point = wall.attrib['points'].split('|')
        if (math.fabs(float(point[0].split(',')[1]) - float(point[1].split(',')[1])) > math.fabs(
                float(point[2].split(',')[1]) - float(
                    point[3].split(',')[1])) and float(point[0].split(',')[0]) > float(point[2].split(',')[0])) or (
                math.fabs(float(point[0].split(',')[1]) - float(point[1].split(',')[1])) < math.fabs(
            float(point[2].split(',')[1]) - float(
                point[3].split(',')[1])) and float(point[0].split(',')[0]) < float(point[2].split(',')[0])):
            right_walls.append(wall)
    return right_walls

def horizontal_wall(wall_data):
    data = []
    for wall in wall_data:
        if check(wall.attrib['startPoint'], wall.attrib['endPoint']):
            data.append(wall)
    return data

def vertical_wall(wall_data):
    data = []
    for wall in wall_data:
        if not check(wall.attrib['startPoint'], wall.attrib['endPoint']):
            data.append(wall)
    return data

def check(param, param1):
    a = param.split(',')
    b = param1.split(',')
    x = math.fabs(float(a[0]) - float(b[0]))
    y = math.fabs(float(a[1]) - float(b[1]))
    if x > y:
        return True
    return False

def refresh_arr(point_arr):
    point_arr.sort()
    list_remove = []
    for i in range(len(point_arr) - 2):
        if point_arr[i + 1] == point_arr[i]:
            list_remove.append(point_arr[i + 1])
    for i in list_remove:
        point_arr.remove(i)
    list_remove = []
    for i in range(len(point_arr) - 4):
        if math.fabs(point_arr[i + 1] - point_arr[i + 2]) < 100:
            if math.fabs(point_arr[i + 1] - point_arr[i]) > math.fabs(point_arr[i + 2] - point_arr[i + 3]):
                list_remove.append(point_arr[i + 2])
            else:
                list_remove.append(point_arr[i + 1])
    for i in list_remove:
        if i in point_arr:
            point_arr.remove(i)
    return point_arr

def cos(number,deg):
    return float(number) / 2 * math.cos(float(deg) / 180 * math.pi)

def sin(number,deg):
    return float(number) / 2 * math.sin(float(deg) / 180 * math.pi)
