import math

import calculator
import const
import dim
import furniture_hardware
import max_min
import parse
import table_infor
import wall_support
from floor import Floor
from pnpoly import Point

class Cabinet(object):

    module_missing = []
    id_name_pos = []

    def __init__(self, msp, module_part_list, module_door_list, module_direction_list, module_info_list, module_model_list, stone_data=None,
                 sections_data=None, back_path=None, doc5=None, doc6=None, doc7=None):
        self.msp = msp
        self.module_part_list = module_part_list
        self.module_door_list = module_door_list
        self.module_direction_list = module_direction_list
        self.module_info_list = module_info_list
        self.module_model_list = module_model_list
        self.stone_data = stone_data
        self.sections_data = sections_data
        self.back_path = back_path
        self.doc5 = doc5
        self.doc6 = doc6
        self.doc7 = doc7

    def draw_cabinet(self):
        for i in range(len(self.module_part_list)):
            part_data = self.module_part_list[i]
            door_data = self.module_door_list[i]
            direction_data = self.module_direction_list[i]
            module_info = self.module_info_list[i]
            print(module_info['name'])
            print(module_info['rotate'])
            rotate = module_info['rotate']
            self.draw_door_module(door_data, rotate, self.draw_module(part_data,door_data,direction_data,rotate, i, 0), i, 0)
            self.draw_door_module(door_data, rotate, self.draw_module(part_data,door_data,direction_data,rotate, i, 1), i, 1)
            self.draw_door_module(door_data, rotate, self.draw_module(part_data,door_data,direction_data,rotate, i, 2), i, 2)
            self.draw_door_module(door_data, rotate, self.draw_module(part_data,door_data,direction_data,rotate, i, 3), i, 3)
            self.msp.add_blockref('KT', insert=(0, -6000 * i), dxfattribs={
                'xscale': 25,
                'yscale': 25})
            self.msp.add_blockref('KT', insert=(8000, -6000 * i), dxfattribs={
                'xscale': 25,
                'yscale': 25})
            table_infor.write_info(self.msp, module_info, [11500, -6000 * i])

    def draw_cabinet_cupboard(self, wall_data):
        mm = max_min.get_mm_location(self.module_part_list)
        wall_location = calculate_wall_location(wall_data[0], mm)
        mm_wall = wall_support.get_mm_wall(wall_data[0], mm)
        # calculator_index_module(self.module_part_list)
        floor = Floor(self.msp, wall_data[0], wall_data[1], None, None)
        floor.write_hatch([], -mm_wall[0][0] + calculator.x(), -mm_wall[1][1] - calculator.y(), 480, 250, mm)
        #[[location 1 góc 0][location 2 góc 90][location 3 góc -90][location 4 góc 180]]
        # 3 array con là ứng với ele 0 , 1400, 2200
        module_part_location = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        module_door_location = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        module_direction_location = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        module_info_location = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        module_model_location = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
        module_after_sort_location_1 = [[], [], [], [], []]
        module_after_sort_location_2 = [[], [], [], [], []]
        module_after_sort_location_3 = [[], [], [], [], []]
        module_after_sort_location_4 = [[], [], [], [], []]
        module_above_after_sort_location_1 = [[], [], [], [], []]
        module_above_after_sort_location_2 = [[], [], [], [], []]
        module_above_after_sort_location_3 = [[], [], [], [], []]
        module_above_after_sort_location_4 = [[], [], [], [], []]
        module_top_after_sort_location_1 = [[], [], [], [], []]
        module_top_after_sort_location_2 = [[], [], [], [], []]
        module_top_after_sort_location_3 = [[], [], [], [], []]
        module_top_after_sort_location_4 = [[], [], [], [], []]

        def location_append(l, part, door, direction, info, m):
            idx = 0
            if info['ele'] > 2000:
                idx = 2
            elif info['ele'] > 1400:
                idx = 1
            module_part_location[l][idx].append(part)
            module_door_location[l][idx].append(door)
            module_direction_location[l][idx].append(direction)
            module_info_location[l][idx].append(info)
            module_model_location[l][idx].append(m)

        has_two_type_cabinet = has_three_type_cabinet = location_1 = location_2 = location_3 = location_4 = False

        print("mặt bằng")
        self.msp.add_blockref('KT', insert=(- 297 * (mm_wall[2] + 8), -calculator.h),
                         dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})
        table_infor.write_info(self.msp, self.module_info_list[0], [- 297 * (mm_wall[2] + 8), -calculator.h],
                               2600 / 2995 * (mm_wall[2] + 8) / 10)
        self.msp.add_blockref('KT', insert=(0, -calculator.h), dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})

        for i in range(len(self.module_part_list)):
            part_data = self.module_part_list[i]
            door_data = self.module_door_list[i]
            direction_data = self.module_direction_list[i]
            module_info = self.module_info_list[i]
            model_data = self.module_model_list[i]
            num = 0
            if module_info['ele'] > 2000:
                num = 2
                has_three_type_cabinet = True
            elif module_info['ele'] > 1400:
                num = 1
                has_two_type_cabinet = True
            min_middle = self.draw_module(part_data,door_data,rotate_direction(direction_data,module_info), [0, 0, 0], 0, 4,
                [mm_wall[0][0] - calculator.x(num, mm_wall[2]), mm_wall[1][1] + calculator.y()])
            self.draw_door_module(door_data, [0, 0, 0], [
                [mm_wall[0][0] - calculator.x(num, mm_wall[2]), mm_wall[1][1] + calculator.y(), min_middle[0][2]], [],[]], 0, 4)
            point = [min_middle[0][0] - mm_wall[0][0] + calculator.x(num, mm_wall[2]),
                     min_middle[0][1] - mm_wall[1][1] - calculator.y()]
            # self.msp.add_text(module_info['name'], dxfattribs={'style': "h3d_style", 'height': 60, 'layer': const.LAYER_7}).set_pos(
            #     (point[0] + 50, point[1] + 50))
            self.id_name_pos.append({'id':module_info,'pos':(point[0] + 50, point[1] + 50)})
            dim.draw_dim(self.msp, [(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])],
                50, 50, 20, (0, 0), 7, 250, 10, 20)
            dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]),
                (min_middle[1][0] - min_middle[0][0] + point[0], min_middle[1][1] - min_middle[0][1] + point[1])],
                50, 50, 20, (0, 0), 7, 250, 10, 20)

            point = [min_middle[0][0] - mm_wall[0][0] + calculator.x(num, mm_wall[2]),
                     min_middle[0][1] - mm_wall[1][1] - calculator.y()]
            h = min_middle[1][1] - min_middle[0][1]
            w = min_middle[1][0] - min_middle[0][0]

            if math.fabs(module_info['rotate'][2]) < 5:
                location_append(0, part_data, door_data, direction_data, module_info, model_data)
                w = 0
                location_1 = True
            if math.fabs(module_info['rotate'][2] - 90) < 5:
                location_append(1, part_data, door_data, direction_data, module_info, model_data)
                w = h = 0
                location_2 = True
            if math.fabs(module_info['rotate'][2] + 90) < 5:
                location_append(2, part_data, door_data, direction_data, module_info, model_data)
                location_3 = True
            if math.fabs(module_info['rotate'][2] + 180) < 5 or math.fabs(module_info['rotate'][2] - 180) < 5:
                location_append(3, part_data, door_data, direction_data, module_info, model_data)
                h = 0
                location_4 = True

            if len(model_data) > 0:
                for model in model_data:
                    px = float(model['value']['PX'])
                    py = -float(model['value']['PY'])
                    cos_rz = math.cos(module_info['rotate'][2] / 180 * math.pi)
                    sin_rz = math.sin(module_info['rotate'][2] / 180 * math.pi)
                    if model['type'] == 'wash_basin':
                        model['value']['RZ'] = module_info['rotate'][2]
                        furniture_hardware.add_block(self.msp, self.doc5, 'chau 1_b', (
                            point[0] + w + px * cos_rz + py * sin_rz,
                            point[1] + h + px * sin_rz - py * cos_rz), model['value'], True)
                    if model['type'] == 'cooking_bench':
                        model['value']['RZ'] = module_info['rotate'][2]
                        furniture_hardware.add_block(self.msp, self.doc6, 'A$C74A327AC', (
                            point[0] + w + px * cos_rz + py * sin_rz,
                            point[1] + h + px * sin_rz - py * cos_rz), model['value'], True)
                    if model['type'] == 'disinfection_cabinet':
                        model['value']['RZ'] = module_info['rotate'][2]
                        furniture_hardware.add_block(self.msp, self.doc7, 'A$C06C54A8D', (
                            point[0] + w + px * cos_rz + py * sin_rz,
                            point[1] + h + px * sin_rz - py * cos_rz), model['value'], True)
                    if model['type'] == 'hardware':
                        model['value']['RZ'] = module_info['rotate'][2]
                        furniture_hardware.add_block(self.msp, self.doc5, 'chau 1_b', (
                            point[0] + w + px * cos_rz + py * sin_rz,
                            point[1] + h + px * sin_rz - py * cos_rz), model['value'], True)

        num = 0
        if has_two_type_cabinet:
            num = num + 1
            self.msp.add_blockref('KT', insert=(297 * (mm_wall[2] + 8), -calculator.h),
                             dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})
            floor.write_hatch([], -mm_wall[0][0] + calculator.x(num,mm_wall[2]), -mm_wall[1][1] - calculator.y(), 480, 250,mm)
        if has_three_type_cabinet:
            num = num + 1
            self.msp.add_blockref('KT', insert=(297 * (mm_wall[2] + 8)*num, -calculator.h),
                             dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})
            floor.write_hatch([], -mm_wall[0][0] + calculator.x(num,mm_wall[2]), -mm_wall[1][1] - calculator.y(), 480, 250,mm)

        print("mặt đứng")
        if location_1:
            num = num + 1
            module_after_sort_location_1 = self.draw_front_location(module_part_location, module_door_location, module_direction_location,
                    module_info_location, module_model_location, mm_wall[2], num,[wall_location[1], wall_location[2]], 1)
            module_above_after_sort_location_1 = sort_module_index(module_part_location[0][1], module_door_location[0][1], module_direction_location[0][1],
                            module_info_location[0][1], module_model_location[0][1], 1)
            module_top_after_sort_location_1 = sort_module_index(module_part_location[0][2], module_door_location[0][2], module_direction_location[0][2],
                            module_info_location[0][2], module_model_location[0][2], 1)
        if location_3:
            num = num + 1
            module_after_sort_location_3 = self.draw_front_location(module_part_location, module_door_location, module_direction_location,
                    module_info_location, module_model_location, mm_wall[2], num, [wall_location[0], wall_location[3]], 3)
            module_above_after_sort_location_3 = sort_module_index(module_part_location[2][1], module_door_location[2][1],
                    module_direction_location[2][1], module_info_location[2][1], module_model_location[2][1], 3)
            module_top_after_sort_location_3 = sort_module_index(module_part_location[2][2], module_door_location[2][2],
                    module_direction_location[2][2], module_info_location[2][2], module_model_location[2][2], 3)
        if location_2:
            num = num + 1
            module_after_sort_location_2 = self.draw_front_location(module_part_location, module_door_location, module_direction_location,
                    module_info_location, module_model_location, mm_wall[2], num, [wall_location[3], wall_location[0]], 2)
            module_above_after_sort_location_2 = sort_module_index(module_part_location[1][1], module_door_location[1][1],
                    module_direction_location[1][1], module_info_location[1][1], module_model_location[1][1], 2)
            module_top_after_sort_location_2 = sort_module_index(module_part_location[1][2], module_door_location[1][2],
                    module_direction_location[1][2], module_info_location[1][2], module_model_location[1][2], 2)
        if location_4:
            num = num + 1
            module_after_sort_location_4 = self.draw_front_location(module_part_location, module_door_location, module_direction_location,
                    module_info_location, module_model_location, mm_wall[2], num, [wall_location[2], wall_location[1]], 4)
            module_above_after_sort_location_4 = sort_module_index(module_part_location[3][1], module_door_location[3][1],
                    module_direction_location[3][1], module_info_location[3][1], module_model_location[3][1], 4)
            module_top_after_sort_location_4 = sort_module_index(module_part_location[3][2], module_door_location[3][2],
                    module_direction_location[3][2], module_info_location[3][2], module_model_location[3][2], 4)

        module_index =  module_after_sort_location_2[3] + module_after_sort_location_1[3] + \
                        module_after_sort_location_3[3] + module_after_sort_location_4[3] + \
                        module_above_after_sort_location_2[3] + module_above_after_sort_location_1[3] + \
                        module_above_after_sort_location_3[3] + module_above_after_sort_location_4[3] + \
                        module_top_after_sort_location_2[3] + module_top_after_sort_location_1[3] + \
                        module_top_after_sort_location_3[3] + module_top_after_sort_location_4[3]

        print("mặt cắt")
        module_after_sort = [
            module_after_sort_location_2[0] + module_after_sort_location_1[0] +
            module_after_sort_location_3[0] + module_after_sort_location_4[0],
            module_after_sort_location_2[1] + module_after_sort_location_1[1] +
            module_after_sort_location_3[1] + module_after_sort_location_4[1],
            module_after_sort_location_2[2] + module_after_sort_location_1[2] +
            module_after_sort_location_3[2] + module_after_sort_location_4[2],
            module_after_sort_location_2[3] + module_after_sort_location_1[3] +
            module_after_sort_location_3[3] + module_after_sort_location_4[3],
            module_after_sort_location_2[4] + module_after_sort_location_1[4] +
            module_after_sort_location_3[4] + module_after_sort_location_4[4]]

        for i in range(math.ceil(len(module_after_sort[0]) / 3)):
            num = num + 1
            self.msp.add_blockref('KT', insert=(297 * (mm_wall[2] + 8) * num, -calculator.h),
                             dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})
            module = [module_after_sort[0][i * 3], module_after_sort[1][i * 3], module_after_sort[2][i * 3],
                      module_after_sort[3][i * 3], module_after_sort[4][i * 3]]
            location = check_location_index(module)
            mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
            self.draw_side(module, module_part_location[location], module_door_location[location], module_direction_location[location],
                module_info_location[location], mm, 0, num, mm_wall[2], wall_location[location])

            if i * 3 + 1 < len(module_after_sort[0]):
                module = [module_after_sort[0][i * 3 + 1], module_after_sort[1][i * 3 + 1],
                          module_after_sort[2][i * 3 + 1], module_after_sort[3][i * 3 + 1], module_after_sort[4][i * 3 + 1]]
                location = check_location_index(module)
                mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
                self.draw_side(module, module_part_location[location], module_door_location[location], module_direction_location[location],
                    module_info_location[location], mm, 1, num, mm_wall[2], wall_location[location])

            if i * 3 + 2 < len(module_after_sort[0]):
                module = [module_after_sort[0][i * 3 + 2], module_after_sort[1][i * 3 + 2],
                          module_after_sort[2][i * 3 + 2], module_after_sort[3][i * 3 + 2], module_after_sort[4][i * 3 + 2]]
                location = check_location_index(module)
                mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
                self.draw_side(module, module_part_location[location], module_door_location[location], module_direction_location[location],
                    module_info_location[location], mm, 2, num, mm_wall[2], wall_location[location])

        module_above_after_sort_location_1 = self.check_duplicate(module_above_after_sort_location_1)
        module_above_after_sort_location_2 = self.check_duplicate(module_above_after_sort_location_2)
        module_above_after_sort_location_3 = self.check_duplicate(module_above_after_sort_location_3)
        module_above_after_sort_location_4 = self.check_duplicate(module_above_after_sort_location_4)

        module_after_sort = [
            module_above_after_sort_location_2[0] + module_above_after_sort_location_1[0] +
            module_above_after_sort_location_3[0] + module_above_after_sort_location_4[0],
            module_above_after_sort_location_2[1] + module_above_after_sort_location_1[1] +
            module_above_after_sort_location_3[1] + module_above_after_sort_location_4[1],
            module_above_after_sort_location_2[2] + module_above_after_sort_location_1[2] +
            module_above_after_sort_location_3[2] + module_above_after_sort_location_4[2],
            module_above_after_sort_location_2[3] + module_above_after_sort_location_1[3] +
            module_above_after_sort_location_3[3] + module_above_after_sort_location_4[3],
            module_above_after_sort_location_2[4] + module_above_after_sort_location_1[4] +
            module_above_after_sort_location_3[4] + module_above_after_sort_location_4[4]]
        for i in range(math.ceil(len(module_after_sort[0]) / 3)):
            num = num + 1
            self.msp.add_blockref('KT', insert=(297 * (mm_wall[2] + 8) * num, -calculator.h),
                                  dxfattribs={'xscale': mm_wall[2] + 8, 'yscale': mm_wall[2] + 8})
            module = [module_after_sort[0][i * 3], module_after_sort[1][i * 3], module_after_sort[2][i * 3],
                      module_after_sort[3][i * 3], module_after_sort[4][i * 3]]
            location = check_location_index(module)
            mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
            self.draw_side_above(module, module_part_location[location], module_door_location[location],
                           module_direction_location[location],
                           module_info_location[location], mm, 0, num, mm_wall[2], wall_location[location])

            if i * 3 + 1 < len(module_after_sort[0]):
                module = [module_after_sort[0][i * 3 + 1], module_after_sort[1][i * 3 + 1],
                          module_after_sort[2][i * 3 + 1], module_after_sort[3][i * 3 + 1],
                          module_after_sort[4][i * 3 + 1]]
                location = check_location_index(module)
                mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
                self.draw_side_above(module, module_part_location[location], module_door_location[location],
                               module_direction_location[location],
                               module_info_location[location], mm, 1, num, mm_wall[2], wall_location[location])

            if i * 3 + 2 < len(module_after_sort[0]):
                module = [module_after_sort[0][i * 3 + 2], module_after_sort[1][i * 3 + 2],
                          module_after_sort[2][i * 3 + 2], module_after_sort[3][i * 3 + 2],
                          module_after_sort[4][i * 3 + 2]]
                location = check_location_index(module)
                mm = max_min.get_mm_location([module[0]], module[3]['rotate'][2], [0, 90, 90])
                self.draw_side_above(module, module_part_location[location], module_door_location[location],
                               module_direction_location[location],
                               module_info_location[location], mm, 2, num, mm_wall[2], wall_location[location])
        self.write_idx_name(self.id_name_pos,module_index)
        calculator.h += (mm_wall[2]+8) * 210

    def check_duplicate(self,module_above_list):
        module_list =  [[], [], [], [], []]
        for i in range(len(module_above_list[3])):
            if get_info(module_above_list[3][i]) not in self.module_missing:
                module_list[0].append(module_above_list[0][i])
                module_list[1].append(module_above_list[1][i])
                module_list[2].append(module_above_list[2][i])
                module_list[3].append(module_above_list[3][i])
                module_list[4].append(module_above_list[4][i])
        return module_list

    def draw_front_location(self,module_part_location, module_door_location,module_direction_location,
                            module_info_location, module_model_location,scale, num, wall_local, location):
        main = location - 1
        left = 0
        right = 0
        rz = 0
        xy = 0
        if location == 1:
            left = 1
            right = 2
            xy = 1
        if location == 2:
            left = 3
            rz = 90
        if location == 3:
            right = 3
            rz = -90
        if location == 4:
            left = 2
            right = 1
            xy = 1
            rz = 180
        self.msp.add_blockref('KT', insert=(297 * (scale + 8) * num, -calculator.h),dxfattribs={'xscale': scale + 8, 'yscale': scale + 8})
        mm = max_min.get_mm_location(
            module_part_location[main][0] + module_part_location[main][1] + module_part_location[main][2] +
            module_part_location[left][0] + module_part_location[left][1] + module_part_location[left][2] +
            module_part_location[right][0] + module_part_location[right][1] + module_part_location[right][2], rz)
        self.draw_wall_in_front_location(mm, scale, num, wall_local)
        self.draw_front_location_with_ele(module_part_location, module_door_location,module_direction_location, module_info_location
                                          , module_model_location, mm, num, scale, location, main, left, right, xy, rz, 0)
        self.draw_front_location_with_ele(module_part_location, module_door_location,module_direction_location, module_info_location
                                          , module_model_location, mm, num, scale, location, main, left, right, xy, rz, 1)
        self.draw_front_location_with_ele(module_part_location, module_door_location,module_direction_location, module_info_location
                                          , module_model_location, mm, num, scale, location, main, left, right, xy, rz, 2)

        self.draw_module([self.stone_data],[],[], [0, 0, rz], 0, 5,
                         [mm[0][0] - calculator.x(num,scale), 0 + calculator.y(scale)], {'layer': const.LAYER_9})
        for section in self.sections_data:
            self.draw_module([section],[],[], [0, 0, rz], 0, 5,
                             [mm[0][0] - calculator.x(num,scale), 0 + calculator.y(scale)], {'layer': const.LAYER_9})
        self.draw_module([self.back_path],[],[], [0, 0, rz], 0, 5,
                         [mm[0][0] - calculator.x(num,scale), 0 + calculator.y(scale)], {'layer': const.LAYER_9})
        return sort_module_index(module_part_location[main][0], module_door_location[main][0],module_direction_location[main][0],
                                module_info_location[main][0], module_model_location[main][0], location)

    def draw_front_location_with_ele(self,module_part_location,module_door_location,module_direction_location,module_info_location,module_model_location ,
                                     mm, num, scale, location, main, left, right, xy, rz ,ele):
        mm_location_1 = max_min.get_mm_location(module_part_location[main][ele])
        mm_location_2 = max_min.get_mm_location(module_part_location[left][ele])
        mm_location_3 = max_min.get_mm_location(module_part_location[right][ele])
        tb = (mm_location_1[0][xy] + mm_location_1[1][xy]) / 2
        self.draw_front_location_main(module_part_location[main][ele], module_door_location[main][ele],module_direction_location[main][ele],
            module_info_location[main][ele], module_model_location[main][ele], mm, num, scale, rz)
        self.draw_front_location_extra(module_part_location[left][ele], module_door_location[left][ele],module_direction_location[left][ele],
            module_info_location[left][ele], mm, num, scale, mm_location_2[1][xy], tb, location)
        self.draw_front_location_extra(module_part_location[right][ele], module_door_location[right][ele],module_direction_location[right][ele],
            module_info_location[right][ele], mm, num, scale, mm_location_3[1][xy], tb, location)

    def draw_front_location_main(self, module_part_location, module_door_location,module_direction_location, module_info_location,
                                 module_model_location, mm, num, scale, RZ):
        for i in range(len(module_part_location)):
            part_data = module_part_location[i]
            door_data = module_door_location[i]
            direction_data = module_direction_location[i]
            module_info = module_info_location[i]
            model_data = module_model_location[i]
            self.draw_module_in_front_location(part_data, door_data,direction_data, module_info, model_data, mm, num, scale, RZ)

    def draw_front_location_extra(self, module_part_location, module_door_location,module_direction_location, module_info_location, mm, num, scale,
                                  check1, check2, location):
        for i in range(len(module_part_location)):
            part_data = module_part_location[i]
            door_data = module_door_location[i]
            direction_data = module_direction_location[i]
            module_info = module_info_location[i]
            mm_module = max_min.get_mm_location([part_data])
            if location == 3:
                if check1 == mm_module[1][0] and mm_module[1][0] > check2:
                    self.draw_module_in_front_location(part_data, door_data, direction_data, module_info, [], mm, num, scale, -90)
            elif location == 2:
                if check1 == mm_module[0][0] and mm_module[0][0] < check2:
                    self.draw_module_in_front_location(part_data, door_data, direction_data, module_info, [], mm, num, scale, 90)
            elif location == 1:
                if check1 == mm_module[1][1] and mm_module[1][1] > check2:
                    self.draw_module_in_front_location(part_data, door_data, direction_data, module_info, [], mm, num, scale, 0)

    def draw_module_in_front_location(self, part_data, door_data, direction_data, module_info, model_data, mm, num, scale, RZ):
        min_middle = self.draw_module(part_data,door_data,direction_data, [0, 0, RZ], 0, 5,[mm[0][0] - calculator.x(num,scale), 0 + calculator.y(scale)])
        self.draw_door_module(door_data, [0, 0, RZ],
            [[mm[0][0] - calculator.x(num,scale), 0 + calculator.y(scale), min_middle[0][2]],[], []], 0, 5)
        point = [min_middle[0][0] - mm[0][0] + calculator.x(num,scale), min_middle[0][1] - calculator.y(scale)]
        self.id_name_pos.append({'id': module_info, 'pos': (point[0] + 50, point[1] + 50)})
        dim.draw_dim(self.msp, [(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])], 50,
                    50, 20, (0, 0), 7, 250, 10, 20)
        dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]), (min_middle[1][0] - min_middle[0][0] + point[0],
                    min_middle[1][1] - min_middle[0][1] + point[1])], 120, 50, 20, (0, 0), 7, 250, 10, 20)
        if len(model_data) > 0:
            if min_middle[0][1] > float(module_info['info'].attrib['PZ']):
                point[1] = float(module_info['info'].attrib['PZ'])- calculator.y(scale)
            for model in model_data:
                if model['type'] == 'wash_basin':
                    model['value']['RZ'] = 0
                    d = model['value']['D']
                    model['value']['D'] = model['value']['H']
                    model['value']['H'] = d
                    furniture_hardware.add_block(self.msp, self.doc5, 'chauf', (
                    point[0] + float(model['value']['PX']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'cooking_bench':
                    model['value']['RZ'] = 0
                    d = model['value']['D']
                    model['value']['D'] = model['value']['H']
                    model['value']['H'] = d
                    furniture_hardware.add_block(self.msp, self.doc6, 'A$C706F0BD6', (
                    point[0] + float(model['value']['PX']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'disinfection_cabinet':
                    model['value']['RZ'] = 0
                    d = model['value']['D']
                    model['value']['D'] = model['value']['H']
                    model['value']['H'] = d
                    furniture_hardware.add_block(self.msp, self.doc7, 'A$C3E5D6D2C', (
                    point[0] + float(model['value']['PX']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'hardware':
                    model['value']['RZ'] = 0
                    d = model['value']['D']
                    model['value']['D'] = model['value']['H']
                    model['value']['H'] = d
                    furniture_hardware.add_block(self.msp, self.doc5, 'chauf', (
                    point[0] + float(model['value']['PX']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)

    def draw_side(self, module, module_part_location, module_door_location, module_direction_location, module_info_location, mm, idx, num, scale,
                  wall_location):
        print(module[3]['name'])
        self.draw_wall_in_front_location(mm, scale, num, [wall_location, False], idx)
        min_middle = self.draw_module(module[0],module[1],module[2], module[3]['rotate'], 0, 6,
                                 [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)])
        self.draw_door_module(module[1], module[3]['rotate'], [
            [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale), min_middle[0][2]], [], []], 0, 6)
        point = [min_middle[0][0] - mm[0][0] + calculator.x(num,scale) + 2000 * idx, min_middle[0][1] - calculator.y(scale)]

        if len(self.stone_data) > 0:
            stone = split_stone(module[0], self.stone_data)
            if len(stone[0])!=0:
                self.draw_module([stone[0]],[],[], module[3]['rotate'], 0, 6,
                    [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)], {'layer': const.LAYER_9})

                for section in self.sections_data:
                    if check_normal_section(section,stone[1]):
                        self.draw_module([section],[],[], module[3]['rotate'], 0, 6,
                            [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)], {'layer': const.LAYER_9})

        self.id_name_pos.append({'id': module[3], 'pos': (point[0] + 50, point[1] + 50)})
        dim.draw_dim(self.msp,[(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])], 50, 50,
                     20, (0, 0), 7, 250, 10, 20)
        dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]),
                    (min_middle[1][0] - min_middle[0][0] + point[0],min_middle[1][1] - min_middle[0][1] + point[1])],
                     120, 50, 20, (0, 0), 7, 250, 10, 20)

        if len(module[4]) > 0:
            for model in module[4]:
                if min_middle[0][1] > float(module[3]['info'].attrib['PZ']):
                    point[1] = float(module[3]['info'].attrib['PZ'])-calculator.y(scale)
                if model['type'] == 'wash_basin':
                    model['value']['W'] = model['value']['H']
                    furniture_hardware.add_block(self.msp, self.doc5, 'chauL', (
                    point[0] - float(model['value']['PY']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'cooking_bench':
                    model['value']['W'] = model['value']['H']
                    furniture_hardware.add_block(self.msp, self.doc6, 'A$C3A237A13', (
                    point[0] - float(model['value']['PY']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'disinfection_cabinet':
                    model['value']['W'] = model['value']['H']
                    furniture_hardware.add_block(self.msp, self.doc7, 'A$C51AB1ED8', (
                    point[0] - float(model['value']['PY']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)
                if model['type'] == 'hardware':
                    model['value']['W'] = model['value']['H']
                    furniture_hardware.add_block(self.msp, self.doc5, 'chauL', (
                    point[0] - float(model['value']['PY']), point[1] + float(model['value']['PZ'])),
                                                 model['value'], True)

        mm_module_main = max_min.get_mm_location([module[0]], module[3]['rotate'][2])
        for ele in [1,2]:
            module_list_above = []
            module_part_with_ele = module_part_location[ele]
            module_door_with_ele = module_door_location[ele]
            module_direction_with_ele = module_direction_location[ele]
            module_info_with_ele = module_info_location[ele]
            for i in range(len(module_part_with_ele)):
                part_data = module_part_with_ele[i]
                module_info = module_info_with_ele[i]
                mm_module = max_min.get_mm_location([part_data], module_info['rotate'][2])
                if mm_module[0][0] <= mm_module_main[0][0] < mm_module_main[1][0] <= mm_module[1][0]:
                    module_list_above.append({'idx': i, 'distance': 999})
                elif mm_module_main[0][0] <= mm_module[0][0] < mm_module[1][0] <= mm_module_main[1][0]:
                    module_list_above.append({'idx': i, 'distance': 999})
                else:
                    if mm_module_main[0][0] < mm_module[0][0] < mm_module_main[1][0]:
                        module_list_above.append({'idx': i, 'distance': mm_module_main[1][0] - mm_module[0][0]})
                    if mm_module_main[0][0] < mm_module[1][0] < mm_module_main[1][0]:
                        module_list_above.append({'idx': i, 'distance': mm_module[1][0] - mm_module_main[0][0]})

            i = -1
            if len(module_list_above) > 2:
                for module_idx in range(len(module_list_above)-1):
                    if module_list_above[module_idx]['idx'] == module_list_above[module_idx + 1]['idx']:
                        i = module_idx
            if len(module_list_above) == 2:
                if module_list_above[0]['distance'] < module_list_above[1]['distance']:
                    i = module_list_above[1]['idx']
                else:
                    i = module_list_above[0]['idx']
            if len(module_list_above) == 1:
                i = module_list_above[0]['idx']
            if i != -1:
                part_data = module_part_with_ele[i]
                door_data = module_door_with_ele[i]
                direction_data = module_direction_with_ele[i]
                module_info = module_info_with_ele[i]
                min_middle = self.draw_module(part_data, door_data, direction_data, module_info['rotate'], 0, 6,
                    [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)])
                self.draw_door_module(door_data, module_info['rotate'], [
                    [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale), min_middle[0][2]], [], []], 0, 6)
                point = [min_middle[0][0] - mm[0][0] + calculator.x(num,scale) + 2000 * idx, min_middle[0][1] - calculator.y(scale)]
                # self.msp.add_text(module_info['name'], dxfattribs={'style': "h3d_style", 'height': 60, 'layer': const.LAYER_7}).set_pos(
                #     (point[0] + 50, point[1] + 50))
                self.id_name_pos.append({'id': module_info, 'pos': (point[0] + 50, point[1] + 50)})
                dim.draw_dim(self.msp, [(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])], 50,
                    50, 20, (0, 0), 7, 250, 10, 20)
                dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]),
                    (min_middle[1][0] - min_middle[0][0] + point[0], min_middle[1][1] - min_middle[0][1] + point[1])],
                    50, 50, 20, (0, 0), 7, 250, 10, 20)
                self.module_missing.append(get_info(module_info))

    def draw_side_above(self, module, module_part_location, module_door_location, module_direction_location, module_info_location, mm, idx, num, scale,
                  wall_location):
        print(module[3]['name'])
        self.draw_wall_in_front_location(mm, scale, num, [wall_location, False], idx)
        min_middle = self.draw_module(module[0],module[1],module[2], module[3]['rotate'], 0, 6,
                                 [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)])
        self.draw_door_module(module[1], module[3]['rotate'], [
            [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale), min_middle[0][2]], [], []], 0, 6)
        point = [min_middle[0][0] - mm[0][0] + calculator.x(num,scale) + 2000 * idx, min_middle[0][1] - calculator.y(scale)]

        # self.msp.add_text(module[3]['name'], dxfattribs={'style': "h3d_style", 'height': 60, 'layer': const.LAYER_7}).set_pos(
        #     (point[0] + 50, point[1] + 50))
        self.id_name_pos.append({'id': module[3], 'pos': (point[0] + 50, point[1] + 50)})
        dim.draw_dim(self.msp, [(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])], 50, 50,
            20, (0, 0), 7, 250, 10, 20)
        dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]),
            (min_middle[1][0] - min_middle[0][0] + point[0], min_middle[1][1] - min_middle[0][1] + point[1])],
            120, 50, 20, (0, 0), 7, 250, 10, 20)
        mm_module_main = max_min.get_mm_location([module[0]], module[3]['rotate'][2])

        module_list_above = []
        module_part_with_ele = module_part_location[2]
        module_door_with_ele = module_door_location[2]
        module_direction_with_ele = module_direction_location[2]
        module_info_with_ele = module_info_location[2]
        for i in range(len(module_part_with_ele)):
            part_data = module_part_with_ele[i]
            module_info = module_info_with_ele[i]
            mm_module = max_min.get_mm_location([part_data], module_info['rotate'][2])
            if mm_module[0][0] <= mm_module_main[0][0] < mm_module_main[1][0] <= mm_module[1][0]:
                module_list_above.append({'idx': i, 'distance': 999})
            elif mm_module_main[0][0] <= mm_module[0][0] < mm_module[1][0] <= mm_module_main[1][0]:
                module_list_above.append({'idx': i, 'distance': 999})
            else:
                if mm_module_main[0][0] < mm_module[0][0] < mm_module_main[1][0]:
                    module_list_above.append({'idx': i, 'distance': mm_module_main[1][0] - mm_module[0][0]})
                if mm_module_main[0][0] < mm_module[1][0] < mm_module_main[1][0]:
                    module_list_above.append({'idx': i, 'distance': mm_module[1][0] - mm_module_main[0][0]})

        i = -1
        if len(module_list_above) > 2:
            for module_idx in range(len(module_list_above)-1):
                if module_list_above[module_idx]['idx'] == module_list_above[module_idx + 1]['idx']:
                    i = module_idx
        if len(module_list_above) == 2:
            if module_list_above[0]['distance'] < module_list_above[1]['distance']:
                i = module_list_above[1]['idx']
            else:
                i = module_list_above[0]['idx']
        if len(module_list_above) == 1:
            i = module_list_above[0]['idx']
        if i != -1:
            part_data = module_part_with_ele[i]
            door_data = module_door_with_ele[i]
            direction_data = module_direction_with_ele[i]
            module_info = module_info_with_ele[i]
            min_middle = self.draw_module(part_data, door_data, direction_data, module_info['rotate'], 0, 6,
                [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale)])
            self.draw_door_module(door_data, module_info['rotate'], [
                [mm[0][0] - calculator.x(num,scale) - 2000 * idx, 0 + calculator.y(scale), min_middle[0][2]], [], []], 0, 6)
            point = [min_middle[0][0] - mm[0][0] + calculator.x(num,scale) + 2000 * idx, min_middle[0][1] - calculator.y(scale)]
            # self.msp.add_text(module_info['name'], dxfattribs={'style': "h3d_style", 'height': 60, 'layer': const.LAYER_7}).set_pos(
            #     (point[0] + 50, point[1] + 50))
            self.id_name_pos.append({'id': module_info, 'pos': (point[0] + 50, point[1] + 50)})
            dim.draw_dim(self.msp, [(point[0], point[1]), (point[0], min_middle[1][1] - min_middle[0][1] + point[1])], 50,
                50, 20, (0, 0), 7, 250, 10, 20)
            dim.draw_dim(self.msp, [(point[0], min_middle[1][1] - min_middle[0][1] + point[1]),
                (min_middle[1][0] - min_middle[0][0] + point[0], min_middle[1][1] - min_middle[0][1] + point[1])],
                50, 50, 20, (0, 0), 7, 250, 10, 20)

    def draw_wall_in_front_location(self, mm, scale, num, wall_local, idx=0):
        left_point = [calculator.x(num,scale) + 2000 * idx, -(scale+4) * 210 - calculator.h]
        right_point = [calculator.x(num,scale) - mm[0][0] + mm[1][0] + 2000 * idx, -(scale+4) * 210 - calculator.h]
        if wall_local[0]:
            polyline_arr = [left_point, [left_point[0], left_point[1] + 3000],
                [left_point[0] - 240, left_point[1] + 3000], [left_point[0] - 240, left_point[1]]]
            hatch = self.msp.add_hatch(dxfattribs = {'layer':const.LAYER_5})
            hatch.paths.add_polyline_path(polyline_arr)
            hatch.set_pattern_fill('ANSI32', scale=5, color=250)
            self.msp.add_polyline3d(polyline_arr, dxfattribs={'layer': const.LAYER_2})
        if wall_local[1]:
            polyline_arr = [right_point, [right_point[0], right_point[1] + 3000],
                [right_point[0] + 240, right_point[1] + 3000], [right_point[0] + 240, right_point[1]]]
            hatch = self.msp.add_hatch(dxfattribs = {'layer':const.LAYER_5})
            hatch.paths.add_polyline_path(polyline_arr)
            hatch.set_pattern_fill('ANSI32', scale=5, color=250)
            self.msp.add_polyline3d(polyline_arr, dxfattribs={'layer': const.LAYER_2})
        self.msp.add_line((left_point[0] - 240, left_point[1]), (right_point[0] + 240, right_point[1]), dxfattribs={'layer':const.LAYER_5})

    def draw_module(self,module_data,door_data,direction_data, rotate, idx, face, mm=None, dxfattribs=None):
        face_rotate = get_face_info(face, idx)[0]
        delta = get_face_info(face, idx)[1]
        min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
        max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
        module_after_rotate = []
        for part in module_data:
            if len(part) > 0:
                part_after_rotate = calculator.rotate_part(part,rotate,face_rotate)
                max_min.get_min_point_part(part_after_rotate, min_point)
                max_min.get_max_point_part(part_after_rotate, max_point)
                module_after_rotate.append(part_after_rotate)
        if face != 0 and face != 4 and face != 5 and face != 6:
            dim.draw_dim(self.msp, [(delta[0], delta[1]), (delta[0], max_point[1] - min_point[1] + delta[1])], 50, 50, 20,
                (0, 0), 7, 7, 10, 20)
            dim.draw_dim(self.msp, [(delta[0], max_point[1] - min_point[1] + delta[1]),
                (max_point[0] - min_point[0] + delta[0], max_point[1] - min_point[1] + delta[1])], 50, 50, 20, (0, 0), 7, 7, 10, 20)
        middle_point = []
        if face == 3:
            middle_point = get_middle_point(module_after_rotate, min_point)
            middle_point.sort()
            middle_point = middle_point[1:len(middle_point) - 1]
        module_after_move = []
        for part in module_after_rotate:
            if face == 4 or face == 5 or face == 6:
                part_after_move = move_origin(part, [mm[0] - delta[0], mm[1] - delta[1], min_point[2]])
            else:
                part_after_move = move_origin(part, [min_point[0] - delta[0], min_point[1] - delta[1], min_point[2]])
            module_after_move.append(part_after_move)
        module_after_move_old = module_after_move.copy()
        module_after_move.sort(key=maxZ)

        max_min_list = []
        for doors in door_data:
            for door in doors:
                if len(door) > 0:
                    after_rotate = calculator.rotate_part(door['data'], rotate, face_rotate)
                    if face == 4 or face == 5 or face == 6:
                        after_move = move_origin(after_rotate, [mm[0] - delta[0], mm[1] - delta[1], min_point[2]])
                    else:
                        after_move = move_origin(after_rotate, [min_point[0] - delta[0], min_point[1] - delta[1], min_point[2]])
                    max_min_list.append(max_min.get_max_min_point_part(after_move))
        module_after_move.reverse()
        dxfattribs_list = calculator_dxfattribs(module_after_move,max_min_list)
        dxfattribs_list.reverse()
        module_after_move.reverse()
        for part_after_move in module_after_move:
            if face == 3 and len(middle_point) > 0:
                self.draw_part_with_middle_point(part_after_move, middle_point, dxfattribs_list[module_after_move.index(part_after_move)],
                    direction_data[module_after_move_old.index(part_after_move)][2])
                if len(middle_point) == 1:
                    dim.draw_dim(self.msp, [(delta[0] + 1000, delta[1]),
                        (delta[0] + 1000, max_point[1] - min_point[1] + delta[1])], 50, 50, 20, (0, 0), 7, 7, 10, 20)
                    dim.draw_dim(self.msp, [(delta[0] + 1000, max_point[1] - min_point[1] + delta[1]),
                        (max_point[0] - min_point[0] + delta[0] + 1000, max_point[1] - min_point[1] + delta[1])],
                        50, 50, 20, (0, 0), 7, 7, 10, 20)
                elif len(middle_point) == 2:
                    dim.draw_dim(self.msp, [(delta[0] + 1000, delta[1]),
                        (delta[0] + 1000, max_point[1] - min_point[1] + delta[1])], 50, 50, 20, (0, 0), 7, 7, 10, 20)
                    dim.draw_dim(self.msp, [(delta[0] + 1000, max_point[1] - min_point[1] + delta[1]),
                        (max_point[0] - min_point[0] + delta[0] + 1000, max_point[1] - min_point[1] + delta[1])],
                        50, 50, 20, (0, 0), 7, 7, 10, 20)
                    dim.draw_dim(self.msp, [(delta[0] + 2000, delta[1]),
                        (delta[0] + 2000, max_point[1] - min_point[1] + delta[1])], 50, 50, 20, (0, 0), 7, 7, 10, 20)
                    dim.draw_dim(self.msp, [(delta[0] + 2000, max_point[1] - min_point[1] + delta[1]),
                        (max_point[0] - min_point[0] + delta[0] + 2000, max_point[1] - min_point[1] + delta[1])],
                        50, 50, 20, (0, 0), 7, 7, 10, 20)
            else:
                if dxfattribs is None:
                    if face == 0:
                        self.draw_part_3D(part_after_move, {'layer': const.LAYER_1})
                    else:
                        layer = dxfattribs_list[module_after_move.index(part_after_move)]
                        self.draw_part(part_after_move, layer)
                        mm = max_min.get_max_min_point_part(part_after_move)
                        if (face == 1 or face == 4) and layer == {'layer': const.LAYER_1}:
                            if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                self.draw_direction(direction_data[module_after_move_old.index(part_after_move)][0],
                                                    ((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                        if (face == 2 or face == 5) and layer == {'layer': const.LAYER_1}:
                            if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                self.draw_direction(direction_data[module_after_move_old.index(part_after_move)][1],
                                                    ((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                        if face == 6 and layer == {'layer': const.LAYER_1}:
                            if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                self.draw_direction(direction_data[module_after_move_old.index(part_after_move)][2],
                                                    ((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                else:
                    self.draw_part(part_after_move, dxfattribs)
        return [min_point, max_point, middle_point]

    def draw_door_module(self, module_data, rotate, min_middle, idx, face):
        min_point = min_middle[0]
        middle_point = min_middle[2]
        face_rotate = get_face_info(face, idx)[0]
        delta = get_face_info(face, idx)[1]
        for parts in module_data:
            for part in parts:
                if len(part) > 0:
                    door_data = part['data']
                    door_info = part['info']
                    part_after_rotate = calculator.rotate_part(door_data,rotate,face_rotate)
                    part_after_move = move_origin(part_after_rotate, [min_point[0] - delta[0], min_point[1] - delta[1], min_point[2]])
                    mm = max_min.get_max_min_point_part(part_after_move)
                    if not door_info is None and face!=0:
                        self.draw_door_open_direction(float(door_info['openDirection']), mm[1][0], mm[1][1], mm[0][0], mm[0][1])
                    if face == 3 and len(middle_point) > 0:
                        self.draw_part_with_middle_point(part_after_move, middle_point, {'layer': const.LAYER_4})
                    else:
                        if len(part_after_move) > 0:
                            if face == 0:
                                self.draw_part_3D(part_after_move, {'layer': const.LAYER_4})
                            else:
                                if face == 1 or face == 4:
                                    if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                        self.draw_direction(part['direction'][0],((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                                if face == 2 or face == 5:
                                    if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                        self.draw_direction(part['direction'][1],((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                                if face == 6:
                                    if math.fabs(mm[0][0] - mm[1][0]) > 50 and math.fabs(mm[0][1] - mm[1][1]) > 50:
                                        self.draw_direction(part['direction'][2],((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2))
                                self.draw_part(part_after_move, {'layer': const.LAYER_4})

    def draw_door_open_direction(self, direction, max_x, max_y, min_x, min_y):
        if math.fabs(max_x - min_x) < 50 or math.fabs(max_y - min_y) < 50:
            return
        if direction == 4: # mở trái
            self.msp.add_polyline2d([(max_x, max_y), (min_x, (max_y - min_y) / 2 + min_y), (max_x, min_y)],
                               dxfattribs = {'layer':const.LAYER_5})
        elif direction == 6: # mở phải
            self.msp.add_polyline2d([(min_x, max_y), (max_x, (max_y - min_y) / 2 + min_y), (min_x, min_y)],
                               dxfattribs = {'layer':const.LAYER_5})
        elif direction == 5: # mở trước
            self.msp.add_polyline2d([(min_x, (max_y - min_y) / 2 + min_y), ((max_x - min_x) / 2 + min_x, max_y),
                                (max_x, (max_y - min_y) / 2 + min_y), ((max_x - min_x) / 2 + min_x, min_y),
                                (min_x, (max_y - min_y) / 2 + min_y)],
                               dxfattribs = {'layer':const.LAYER_5})
        elif direction == 8: # mở lên trên
            self.msp.add_polyline2d([(min_x, min_y), ((max_x - min_x) / 2 + min_x, max_y), (max_x, min_y)],
                               dxfattribs = {'layer':const.LAYER_5})
        elif direction == 2:
            print('mở từ dưới')

    def draw_part_with_middle_point(self, part_after_move, middle_point, dxfattribs,direction=None):
        min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
        max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
        for point in part_after_move:
            if point['type'] == 0:
                max_min.get_max_point_3d(max_point, point['data'])
                max_min.get_min_point_3d(min_point, point['data'])
            if point['type'] == 1:
                for p in point['data']:
                    max_min.get_max_point_3d(max_point, p)
                    max_min.get_min_point_3d(min_point, p)
        if len(middle_point) == 1:
            if max_point[2] >= middle_point[0] >= min_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
                    self.draw_direction(direction,
                        ((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
                self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)
            elif middle_point[0] >= max_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,
                        ((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
            elif min_point[2] >= middle_point[0]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)
        elif len(middle_point) == 2:
            if max_point[2] >= middle_point[1] >= middle_point[0] >= min_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
                    self.draw_direction(direction,
                        ((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                    self.draw_direction(direction,
                        ((max_point[0] + min_point[0]) / 2 + 2000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-2000, 0, 0]), dxfattribs)
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
                self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)
            elif max_point[2] >= middle_point[1] >= min_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
                self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)
            elif max_point[2] >= middle_point[0] >= min_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2 + 2000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-2000, 0, 0]), dxfattribs)
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
            elif middle_point[1] >= max_point[2] >= min_point[2] >= middle_point[0]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction, ((max_point[0] + min_point[0]) / 2 + 1000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-1000, 0, 0]), dxfattribs)
            elif middle_point[0] >= max_point[2]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2 + 2000, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [-2000, 0, 0]), dxfattribs)
            elif min_point[2] >= middle_point[1]:
                if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                    self.draw_direction(direction,((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
                self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)
        else:
            if math.fabs(max_point[0] - min_point[0]) > 50 and math.fabs(max_point[1] - min_point[1]) > 50 and dxfattribs == {'layer': const.LAYER_1}:
                self.draw_direction(direction, ((max_point[0] + min_point[0]) / 2, (max_point[1] + min_point[1]) / 2))
            self.draw_part(move_origin(part_after_move, [0, 0, 0]), dxfattribs)

    def draw_part(self, part_after_move, dxfattribs):
        main_polygon = []
        opposite_polygon = []
        face_polygon = []
        num = int(len(part_after_move) / 2)
        for i in range(num):
            main_polygon.append(part_after_move[i])
            opposite_polygon.append(part_after_move[num + i])
        main_polygon.append(part_after_move[0])
        opposite_polygon.append(part_after_move[num])
        if main_polygon[0] == opposite_polygon[0] and main_polygon[num] == opposite_polygon[num]:
            for i in range(num+1):
                face_polygon.append(main_polygon[i]['data'])
            self.msp.add_polyline3d(face_polygon, dxfattribs=dxfattribs)
        else:
            for i in range(num):
                if main_polygon[i]['type'] == 0 and main_polygon[i + 1]['type'] == 0:
                    face_polygon.append(main_polygon[i]['data'])
                    face_polygon.append(opposite_polygon[i]['data'])
                    face_polygon.append(opposite_polygon[i + 1]['data'])
                    face_polygon.append(main_polygon[i + 1]['data'])
                    face_polygon.append(main_polygon[i]['data'])
                elif main_polygon[i]['type'] == 0 and main_polygon[i + 1]['type'] == 1:
                    face_polygon.append(main_polygon[i]['data'])
                    face_polygon.append(opposite_polygon[i]['data'])
                    face_polygon.append(opposite_polygon[i + 1]['data'][0])
                    face_polygon.append(main_polygon[i + 1]['data'][0])
                    face_polygon.append(main_polygon[i]['data'])
                elif main_polygon[i]['type'] == 1 and main_polygon[i + 1]['type'] == 0:
                    for point in main_polygon[i]['data']:
                        face_polygon.append(point)
                    face_polygon.append(main_polygon[i + 1]['data'])
                    face_polygon.append(opposite_polygon[i + 1]['data'])
                    for point in opposite_polygon[i]['data'][::-1]:
                        face_polygon.append(point)
                    face_polygon.append(main_polygon[i]['data'][0])
                    for point in main_polygon[i]['data']:
                        face_polygon.append(point)
                elif main_polygon[i]['type'] == 1 and main_polygon[i + 1]['type'] == 1:
                    for point in main_polygon[i]['data']:
                        face_polygon.append(point)
                    face_polygon.append(main_polygon[i + 1]['data'][0])
                    face_polygon.append(opposite_polygon[i + 1]['data'][0])
                    for point in opposite_polygon[i]['data'][::-1]:
                        face_polygon.append(point)
                    face_polygon.append(main_polygon[i]['data'][0])
                    for point in main_polygon[i]['data']:
                        face_polygon.append(point)
            self.msp.add_polyline3d(face_polygon, dxfattribs=dxfattribs)

    def draw_part_3D(self, part_after_move, dxfattribs):
        main_polygon = []
        opposite_polygon = []
        num = int(len(part_after_move) / 2)
        for i in range(num):
            main_polygon.append(part_after_move[i])
            opposite_polygon.append(part_after_move[num + i])
        main_polygon.append(part_after_move[0])
        opposite_polygon.append(part_after_move[num])

        face_polygon_1 = []
        face_polygon_2 = []
        for i in range(num):
            if main_polygon[i]['type'] == 1:
                for point in main_polygon[i]['data']:
                    face_polygon_1.append(point)
            else:
                face_polygon_1.append(main_polygon[i]['data'])
            if opposite_polygon[i]['type'] == 1:
                for point in opposite_polygon[i]['data']:
                    face_polygon_2.append(point)
            else:
                face_polygon_2.append(opposite_polygon[i]['data'])
        self.draw_mesh(face_polygon_1, dxfattribs)
        self.draw_mesh(face_polygon_2, dxfattribs)

        for i in range(num):
            if main_polygon[i]['type'] == 0 and main_polygon[i + 1]['type'] == 0:
                face_polygon = [main_polygon[i]['data'], opposite_polygon[i]['data'],
                    opposite_polygon[i + 1]['data'], main_polygon[i + 1]['data']]
                self.draw_mesh(face_polygon, dxfattribs)
            elif main_polygon[i]['type'] == 0 and main_polygon[i + 1]['type'] == 1:
                face_polygon = [main_polygon[i]['data'], opposite_polygon[i]['data'],
                    opposite_polygon[i + 1]['data'][0], main_polygon[i + 1]['data'][0]]
                self.draw_mesh(face_polygon, dxfattribs)
            elif main_polygon[i]['type'] == 1 and main_polygon[i + 1]['type'] == 0:
                face_polygon = []
                for point in main_polygon[i]['data']:
                    face_polygon.append(point)
                face_polygon.append(main_polygon[i + 1]['data'])
                face_polygon.append(opposite_polygon[i + 1]['data'])
                for point in opposite_polygon[i]['data'][::-1]:
                    face_polygon.append(point)
                self.draw_mesh(face_polygon, dxfattribs)
            elif main_polygon[i]['type'] == 1 and main_polygon[i + 1]['type'] == 1:
                face_polygon = []
                for point in main_polygon[i]['data']:
                    face_polygon.append(point)
                face_polygon.append(main_polygon[i + 1]['data'][0])
                face_polygon.append(opposite_polygon[i + 1]['data'][0])
                for point in opposite_polygon[i]['data'][::-1]:
                    face_polygon.append(point)
                self.draw_mesh(face_polygon, dxfattribs)
                face_polygon = [main_polygon[i]['data'][-1],main_polygon[i + 1]['data'][0],
                                opposite_polygon[i + 1]['data'][0],opposite_polygon[i]['data'][-1]]
                self.draw_mesh(face_polygon, dxfattribs)


    def draw_mesh(self,face_polygon,dxfattribs):
        faces = []
        for i in range(len(face_polygon)):
            faces.append(i)
        mesh = self.msp.add_mesh(dxfattribs=dxfattribs)
        with mesh.edit_data() as mesh_data:
            mesh_data.vertices = face_polygon
            mesh_data.faces = [faces]

    def draw_direction(self,direction,point):
        if direction:
            self.msp.add_polyline2d([(point[0] - 20, point[1] - 60),
                (point[0], point[1] - 100), (point[0], point[1] + 100),(point[0] + 30, point[1] + 60)],dxfattribs = {'layer':const.LAYER_5})
        else:
            self.msp.add_polyline2d([(point[0] - 60, point[1] + 20),
                (point[0] - 100, point[1]), (point[0] + 100, point[1]),(point[0] + 60, point[1] - 20)],dxfattribs = {'layer':const.LAYER_5})

    def write_idx_name(self,id_name_pos,module_index):
        for data in id_name_pos:
            self.msp.add_text(str(module_index.index(data['id'])+1)+'.'+data['id']['name'],
                dxfattribs={'style': "h3d_style", 'height': 60, 'layer': const.LAYER_7}).set_pos(data['pos'])

def get_face_info(face, idx):
    face_rotate = []
    delta = []
    if face == 0:
        face_rotate = [-50, 40, 28.35]
        delta = [1000, -idx * 6000 - 5250 + 1000]
    if face == 1:
        face_rotate = [0, 0, 0]
        delta = [8500, -idx * 6000 - 5250 / 2 + 500]
    if face == 2:
        face_rotate = [-90, 0, 0]
        delta = [8500, -idx * 6000 - 5250 + 500]
    if face == 3:
        face_rotate = [0, 90, 90]
        delta = [11500, -idx * 6000 - 5250 + 500]
    if face == 4:
        face_rotate = [0, 0, 0]
        delta = [0, 0]
    if face == 5:
        face_rotate = [-90, 0, 0]
        delta = [0, 0]
    if face == 6:
        face_rotate = [0, 90, 90]
        delta = [0, 0]
    return [face_rotate, delta]

def move_origin(part,min_point):
    result = []
    for point in part:
        if point['type'] == 0:
            a = [0, 0, 0]
            a[0] = point['data'][0] - min_point[0]
            a[1] = point['data'][1] - min_point[1]
            a[2] = point['data'][2] - min_point[2]
            result.append({'type':0,'data':a})
        if point['type'] == 1:
            data = []
            for p in point['data']:
                a = [0, 0, 0]
                a[0] = p[0] - min_point[0]
                a[1] = p[1] - min_point[1]
                a[2] = p[2] - min_point[2]
                data.append(a)
            result.append({'type': 1, 'data': data})
    return result

def get_middle_point(module_data, min_point_module):
    result = []
    for part in module_data:
        min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
        max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
        for point in part:
            if point['type'] == 0:
                max_min.get_max_point_3d(max_point, point['data'])
                max_min.get_min_point_3d(min_point, point['data'])
            if point['type'] == 1:
                for p in point['data']:
                    max_min.get_max_point_3d(max_point, p)
                    max_min.get_min_point_3d(min_point, p)
        if (max_point[2] - min_point[2]) < 30 and (max_point[1] - min_point[1]) > 1000:
            result.append((max_point[2] + min_point[2]) / 2 - min_point_module[2])
    return result

def calculate_wall_location(wall_data, mm):
    wall_location_1 = wall_location_2 = wall_location_3 = wall_location_4 = False
    for wallPointData in wall_data:
        min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
        max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
        point_data = wallPointData.attrib['points'].split('|')
        for i in point_data:
            if min_point[0] > float(i.split(',')[0]):
                min_point[0] = float(i.split(',')[0])
            if max_point[0] < float(i.split(',')[0]):
                max_point[0] = float(i.split(',')[0])
            if min_point[1] > float(i.split(',')[1]):
                min_point[1] = float(i.split(',')[1])
            if max_point[1] < float(i.split(',')[1]):
                max_point[1] = float(i.split(',')[1])
        if math.fabs(min_point[1] - mm[1][1]) < 20:
            wall_location_1 = True
        if math.fabs(max_point[0] - mm[0][0]) < 20:
            wall_location_2 = True
        if math.fabs(min_point[0] - mm[1][0]) < 20:
            wall_location_3 = True
        if math.fabs(max_point[1] - mm[0][1]) < 20:
            wall_location_4 = True
    return [wall_location_1,wall_location_2,wall_location_3,wall_location_4]

def sort_module_index(module_part_location,module_door_location,module_direction_location,module_info_location,module_model_location,location):
    module_part = []
    module_door = []
    module_direction = []
    module_info = []
    module_model = []
    list_min = []
    len_module = len(module_part_location)
    for i in range(len_module):
        part_data = module_part_location[i]
        mm_module = max_min.get_mm_location([part_data])
        if location == 2 or location == 3:
            list_min.append(mm_module[0][1])
        else:
            list_min.append(mm_module[0][0])
    list_min.sort()
    if location == 3 or location == 4:
        list_min.reverse()
    for i in range(len_module):
        for j in range(len_module):
            part_data = module_part_location[j]
            mm_module = max_min.get_mm_location([part_data])
            if (list_min[i] == mm_module[0][0] and (location == 1 or location == 4)) or (list_min[i] == mm_module[0][1] and (location == 2 or location == 3)):
                module_part.append(part_data)
                module_door.append(module_door_location[j])
                module_direction.append(module_direction_location[j])
                module_info.append(module_info_location[j])
                module_model.append(module_model_location[j])
    return [module_part,module_door,module_direction,module_info,module_model]

def check_location_index(module):
    location = -1
    if math.fabs(module[3]['rotate'][2]) < 5:
        location = 0
    if math.fabs(module[3]['rotate'][2]-90) < 5:
        location = 1
    if math.fabs(module[3]['rotate'][2]+90) < 5:
        location = 2
    if math.fabs(module[3]['rotate'][2]+180) < 5 or math.fabs(module[3]['rotate'][2] - 180) < 5:
        location = 3
    return location

def split_stone(module,stone):
    mm = max_min.get_mm_location([module])
    tb = ((mm[0][0] + mm[1][0]) / 2, (mm[0][1] + mm[1][1]) / 2)
    num = int(len(stone) / 2)
    result = []
    poly_for_check = []
    for i in range(num):
        poly_for_check.append(stone[i])
    for i in range(3):
        poly_for_check.append(stone[i])
    for i in range(num):
        poly_for_check.append(stone[i+num])
    for i in range(3):
        poly_for_check.append(stone[i+num])
    for i in range(num):
        min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
        max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
        polygon = []
        for p in poly_for_check[i:i+4]:
            if p['x'] > max_point[0]:
                max_point[0] = p['x']
            if p['y'] > max_point[1]:
                max_point[1] = p['y']
            if p['x'] < min_point[0]:
                min_point[0] = p['x']
            if p['y'] < min_point[1]:
                min_point[1] = p['y']
            polygon.append((p['x'], p['y']))
        point = Point(tb)
        if (max_point[0]-min_point[0]<1000 or max_point[1]-min_point[1]<1000) and point.InPolygon(polygon,False):
            result = poly_for_check[i:i+4]+poly_for_check[num+3+i:num+3+i+4]
            return [result,[min_point,max_point]]
    return [result,[]]

def check_normal_section(normal_section,mm):
    min_point = [max_min.DEFAULT_MIN, max_min.DEFAULT_MIN, max_min.DEFAULT_MIN]
    max_point = [max_min.DEFAULT_MAX, max_min.DEFAULT_MAX, max_min.DEFAULT_MAX]
    for p in normal_section:
        if p['x'] > max_point[0]:
            max_point[0] = p['x']
        if p['y'] > max_point[1]:
            max_point[1] = p['y']
        if p['x'] < min_point[0]:
            min_point[0] = p['x']
        if p['y'] < min_point[1]:
            min_point[1] = p['y']
    if (math.fabs(mm[0][0] - min_point[0]) < 10 or math.fabs(mm[1][0] - min_point[0]) < 10 or math.fabs(
            mm[0][0] - max_point[0]) < 10 or math.fabs(mm[1][0] - max_point[0]) < 10) and (math.fabs(
            mm[0][1] - min_point[1]) < 10 or math.fabs(mm[1][1] - min_point[1]) < 10 or math.fabs(
            mm[0][1] - max_point[1]) < 10 or math.fabs(mm[1][1] - max_point[1]) < 10):
        return True
    return False

def maxZ(part):
    max_z = max_min.DEFAULT_MAX
    for point in part:
        if point['type'] == 0:
            if point['data'][2] > max_z:
                max_z = point['data'][2]
    return max_z

def calculator_dxfattribs(module_after_move,max_min_list):
    result = []
    for part in module_after_move:
        mm = max_min.get_max_min_point_part(part)
        impact = False
        for max_min_point in max_min_list:
            if (mm[0][0] < max_min_point[1][0] and max_min_point[0][0] < mm[1][0] and mm[0][1] < max_min_point[1][1] and max_min_point[0][1] < mm[1][1]) or (
                    mm[1][0] > max_min_point[0][0] and max_min_point[1][0] > mm[0][0] and mm[1][1] > max_min_point[0][1] and max_min_point[1][1] > mm[0][1]) or (
                    mm[0][0] < max_min_point[1][0] and max_min_point[0][0] < mm[1][0] and mm[1][1] > max_min_point[0][1] and max_min_point[1][1] > mm[0][1]) or (
                    mm[1][0] > max_min_point[0][0] and max_min_point[1][0] > mm[0][0] and mm[0][1] < max_min_point[1][1] and max_min_point[0][1] < mm[1][1]):
                if mm[1][2] < max_min_point[1][2]:
                    impact = True
        if impact:
            result.append({'layer': const.LAYER_3})
        else:
            result.append({'layer': const.LAYER_1})
        max_min_list.append(mm)
    return result

def get_info(module_info):
    return module_info['name']+module_info['info'].attrib['PX']+module_info['info'].attrib['PY']+module_info['info'].attrib['PZ']

def rotate_direction(direction_data,module_info):
    result = []
    for direction in direction_data:
        result.append(parse.parse_direction(direction,module_info['rotate']))
    return result