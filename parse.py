# 2021-10-28 - hieuhihi
import calculator

def parse_unit(module,module_part_list,module_door_list,module_direction_list,module_info_list,module_model_list):
    name = module.attrib['name']
    info = module.find("Values")
    rotate = [float(info.attrib['RX']), float(info.attrib['RY']), float(info.attrib['RZ'])]
    elevation = float(info.attrib['PZ'])
    parts = module.findall("Part")
    model_list = module.findall("Model")
    model_data = []
    for model in model_list:
        if model.attrib['type'] == 'wash_basin':
            model_data.append({'type':'wash_basin','value':model.findall("Values")[0].attrib})
        if model.attrib['type'] == 'cooking_bench':
            model_data.append({'type':'cooking_bench','value':model.findall("Values")[0].attrib})
        if model.attrib['type'] == 'disinfection_cabinet':
            model_data.append({'type':'disinfection_cabinet','value':model.findall("Values")[0].attrib})
    material_list = parse_material(parts)
    accessory_list = parse_accessory(parts, module.findall("Accessories/Accessory"))
    module_info = {"name": name, "info": info, "rotate": rotate, "ele": elevation,
                   'material_cabinet': get_material(material_list[0]),
                   'material_door': get_material(material_list[1]),
                   'material_door_functor': get_material(material_list[2]),
                   'accessory_list': accessory_list}
    part_data = []
    doors_data = []
    direction = []
    for part in parts:
        parse_part_and_door(part_data, doors_data, model_data, direction, part, None, rotate)
    module_part_list.append(part_data)
    module_door_list.append(doors_data)
    module_direction_list.append(direction)
    module_info_list.append(module_info)
    module_model_list.append(model_data)

def parse_accessory(parts,accessories):
    result = []
    for accessory in accessories:
        flag = True
        for data in result:
            if data['name'] == accessory.attrib['materialName']:
                data['num'] = str(int(data['num']) + int(accessory.attrib['num']))
                flag = False
        if flag:
            result.append({'name':accessory.attrib['materialName'],'num':accessory.attrib['num']})
    for part in parts:
        if part.attrib['type'] == "functor":
            for accessory in part.findall('Accessories/Accessory'):
                flag = True
                for data in result:
                    if data['name'] == accessory.attrib['materialName']:
                        data['num'] =  str(int(data['num']) + int(accessory.attrib['num']))
                        flag = False
                if flag:
                    result.append({'name': accessory.attrib['materialName'], 'num': accessory.attrib['num']})
    return result

def get_material(material_list):
    result = ''
    sl = 0
    material_cv = {}
    for material in material_list:
        if not material['material'] in material_cv:
            material_cv[material['material']] = []
        material_cv[material['material']].append(material['name'])
    for i in material_cv:
        if sl < len(material_cv[i]):
            sl = len(material_cv[i])
            result = i
    return result

def parse_material(parts):
    material_cabinet = []
    material_door = []
    material_door_functor =[]
    for part in parts:
        if part.attrib['type'] == "cabinet_board":
            name = ''
            material_name = ''
            if 'name' in part.attrib:
                name = part.attrib['name']
            if "materialName" in part.attrib:
                material_name = part.attrib['materialName']
            material_cabinet.append({'name': name, 'material': material_name})
        if part.attrib['type'] == "swingDoorEntity":
            for door in part.findall("Part"):
                name = ''
                material_name = ''
                if 'name' in door.findall("Part")[0].attrib:
                    name = door.findall("Part")[0].attrib['name']
                if "materialName" in door.findall("Part")[0].attrib:
                    material_name = door.findall("Part")[0].attrib['materialName']
                elif "materialName" in door.findall("Part/Part")[0].attrib:
                    material_name = door.findall("Part/Part")[0].attrib['materialName']
                material_door.append({'name': name, 'material': material_name})
        if part.attrib['type'] == "functor":
            parse_material_functor(part,material_cabinet,material_door_functor)
    return [material_cabinet,material_door,material_door_functor]

def parse_material_functor(parts,material_cabinet,material_door_functor):
    for part in parts.findall("Part"):
        if part.attrib['type'] == "cabinet_board":
            name = ''
            material_name = ''
            if 'name' in part.attrib:
                name = part.attrib['name']
            if "materialName" in part.attrib:
                material_name = part.attrib['materialName']
            elif "materialName" in parts.attrib:
                material_name = parts.attrib['materialName']
            material_cabinet.append({'name': name, 'material': material_name})
        if part.attrib['type'] == "swingDoorEntity" or part.attrib['type'] == "door_board":
            for door in part.findall("Part"):
                name = ''
                material_name = ''
                if 'name' in door.findall("Part")[0].attrib:
                    name = door.findall("Part")[0].attrib['name']
                if "materialName" in door.findall("Part")[0].attrib:
                    material_name = door.findall("Part")[0].attrib['materialName']
                elif "materialName" in door.findall("Part/Part")[0].attrib:
                    material_name = door.findall("Part/Part")[0].attrib['materialName']
                material_door_functor.append({'name': name, 'material': material_name})
        if part.attrib['type'] == "functor":
            parse_material_functor(part,material_cabinet,material_door_functor)

def parse_part_and_door(part_data,doors_data,model_data,direction,part,functor_rotate=None,module_rotate=None):
    if part.attrib['type'] == "functor" or part.attrib['partNumber'] == 'TN_NHOM':
        values = part.findall("Values")[0].attrib
        rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
        for part_child in part.findall("Part"):
            parse_part_and_door(part_data,doors_data,[],direction,part_child,rotate,module_rotate)
        for model in part.findall("Model"):
            if model.attrib['type'] == "hardware":
                model_data.append({'type':'hardware',
                    'value':{'W':model.findall("Values")[0].attrib['W'],
                            'H':model.findall("Values")[0].attrib['H'],
                            'D':model.findall("Values")[0].attrib['D'],
                            'PX':float(model.findall("Values")[0].attrib['PX'])+float(values['PX']),
                            'PY':float(model.findall("Values")[0].attrib['PY'])+float(values['PY']),
                            'PZ':float(model.findall("Values")[0].attrib['PZ'])+float(values['PZ']),
                            'RX':model.findall("Values")[0].attrib['RX'],
                            'RY':model.findall("Values")[0].attrib['RY'],
                            'RZ':float(model.findall("Values")[0].attrib['RZ'])+float(values['RZ'])}})
    else:
        p = parse_part(part, functor_rotate, module_rotate)
        inner_p = parse_part(part, functor_rotate, module_rotate, True)
        d = parse_door(part,functor_rotate, module_rotate)
        if len(p[0]) > 0:
            part_data.append(p[0])
            direction.append(p[1])
        if len(inner_p[0]) > 0:
            part_data.append(inner_p[0])
            direction.append(inner_p[1])
        if len(d) > 0:
            doors_data.append(d)

def parse_part(part,functor_rotate,module_rotate,inner=False):
    result = []
    values = {}
    direction = []
    a = b = False
    part_rotate = None
    if part.attrib['type'] == "cabinet_board":
        if inner:
            face_board_global_p = part.findall("FaceBoard/InnerBorderLines/LineGlobleP/globalP")
        else:
            face_board_global_p = part.findall("FaceBoard/faceBoardGlobalP/globalP")
        if len(part.findall("Values")) > 0:
            values = part.findall("Values")[0].attrib
            # False ko xoay , van ngang
            a = part.attrib['grainDirection'] == 'vertical'
            b = part.attrib['sideGrainDirection'] == 'vertical'
        if len(face_board_global_p) == 0 :
            if inner:
                face_board_global_p = part.findall("Part/FaceBoard/InnerBorderLines/LineGlobleP/globalP")
            else:
                face_board_global_p = part.findall("Part/FaceBoard/faceBoardGlobalP/globalP")
            part_rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
            if len(part.findall("Part/Values")) > 0:
                values = part.findall("Part/Values")[0].attrib
                a = part.findall("Part")[0].attrib['grainDirection'] == 'vertical'
                b = part.findall("Part")[0].attrib['sideGrainDirection'] == 'vertical'
        result = parse_core(face_board_global_p, values,part_rotate, functor_rotate, module_rotate)

        direction = [a, b, b]
        rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
        direction = parse_direction(direction, rotate)
        if not part_rotate is None:
            direction = parse_direction(direction, part_rotate)
        if not functor_rotate is None:
            direction = parse_direction(direction, functor_rotate)
    return [result,direction]

def parse_door(part,functor_rotate, module_rotate):
    result = []
    values = {}
    if part.attrib['type'] == "swingDoorEntity" or part.attrib['type'] == 'door_board':
        part_rotate = [float(part.findall("Values")[0].attrib['RX']),float(part.findall("Values")[0].attrib['RY']),
                       float(part.findall("Values")[0].attrib['RZ'])]
        for p in part.findall("Part"):
            face_board_global_p = p.findall("Part/Part/FaceBoard/faceBoardGlobalP/globalP")
            if len(p.findall("Part/Part/Values")) > 0:
                values = p.findall("Part/Part/Values")[0].attrib
            if len(face_board_global_p) == 0:
                face_board_global_p = p.findall("Part/FaceBoard/faceBoardGlobalP/globalP")
                if len(p.findall("Part/Values")) > 0:
                    values = p.findall("Part/Values")[0].attrib
                if len(face_board_global_p) > 0:
                    info = p.attrib
                    for p1 in p.findall("Part"):
                        face_board_global_p = p1.findall("FaceBoard/faceBoardGlobalP/globalP")
                        a = p1.attrib['grainDirection'] == 'vertical'
                        b = p1.attrib['sideGrainDirection'] == 'vertical'
                        direction = [a, b, b]
                        rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
                        direction = parse_direction(direction, rotate)
                        if not part_rotate is None:
                            direction = parse_direction(direction, part_rotate)
                        if not functor_rotate is None:
                            direction = parse_direction(direction, functor_rotate)
                        result.append({"data":parse_core(face_board_global_p,values,part_rotate,functor_rotate,module_rotate)
                                ,"info":info,"direction":direction})
                else:
                    if len(p.findall("Part/Part/Part/Values")) > 0:
                        values = p.findall("Part/Part/Part/Values")[0].attrib
                    for p1 in p.findall("Part"):
                        for p2 in p1.findall("Part"):
                            info = p.attrib
                            for p3 in p2.findall("Part"):
                                face_board_global_p = p3.findall("FaceBoard/faceBoardGlobalP/globalP")
                                a = p3.attrib['grainDirection'] == 'vertical'
                                b = p3.attrib['sideGrainDirection'] == 'vertical'
                                direction = [a, b, b]
                                rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
                                direction = parse_direction(direction, rotate)
                                if not part_rotate is None:
                                    direction = parse_direction(direction, part_rotate)
                                if not functor_rotate is None:
                                    direction = parse_direction(direction, functor_rotate)
                                result.append({"data":parse_core(face_board_global_p,values,part_rotate,functor_rotate,module_rotate)
                                        ,"info":info,"direction":direction})
            else:
                for p1 in p.findall("Part"):
                    info = p.attrib
                    for p2 in p1.findall("Part"):
                        face_board_global_p = p2.findall("FaceBoard/faceBoardGlobalP/globalP")
                        a = p2.attrib['grainDirection'] == 'vertical'
                        b = p2.attrib['sideGrainDirection'] == 'vertical'
                        direction = [a, b, b]
                        rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
                        direction = parse_direction(direction, rotate)
                        if not part_rotate is None:
                            direction = parse_direction(direction, part_rotate)
                        if not functor_rotate is None:
                            direction = parse_direction(direction, functor_rotate)
                        result.append({"data":parse_core(face_board_global_p,values,part_rotate,functor_rotate,module_rotate)
                                ,"info":info,"direction":direction})
    return result

def parse_core(face_board_global_p,values,part_rotate,functor_rotate,module_rotate):
    result = []
    for global_p in face_board_global_p:
        x = float(global_p.attrib["x"])
        y = float(global_p.attrib["y"])
        z = float(global_p.attrib["z"])
        if global_p.attrib['type'] == "1":
            cx = float(global_p.attrib["cx"])
            cy = float(global_p.attrib["cy"])
            cz = float(global_p.attrib["cz"])
            segment = float(global_p.attrib["section"])
            angle = float(global_p.attrib["angle"])
            rotate = [float(values['RX']), float(values['RY']), float(values['RZ'])]
            xyz = calculator.re_rotate_XYZ(x, y, z, module_rotate)
            cxyz = calculator.re_rotate_XYZ(cx, cy, cz, module_rotate)
            if not functor_rotate is None:
                xyz = calculator.re_rotate_XYZ(xyz[0], xyz[1], xyz[2], functor_rotate)
                cxyz = calculator.re_rotate_XYZ(cxyz[0], cxyz[1], cxyz[2], functor_rotate)
            if not part_rotate is None:
                xyz = calculator.re_rotate_XYZ(xyz[0], xyz[1], xyz[2], part_rotate)
                cxyz = calculator.re_rotate_XYZ(cxyz[0], cxyz[1], cxyz[2], part_rotate)
            xyz = calculator.re_rotate_XYZ(xyz[0], xyz[1], xyz[2], rotate)
            cxyz = calculator.re_rotate_XYZ(cxyz[0], cxyz[1], cxyz[2], rotate)
            # r = helper.distance_f((cxyz[0], cxyz[1]), (xyz[0], xyz[1]))
            if cx == x and cy == y and cz == z:
                result.append({"x": x, "y": y, "z": z, 'type': 0})
            else:
                points = []
                corner_points = calculator.generate_corner_point(cxyz[0], cxyz[1], (xyz[0], xyz[1]),
                                                             angle, segment)
                for point in corner_points:
                    rotate_xyz = calculator.rotate_XYZ(point[0], point[1], xyz[2], rotate)
                    if not part_rotate is None:
                        rotate_xyz = calculator.rotate_XYZ(rotate_xyz[0], rotate_xyz[1], rotate_xyz[2], part_rotate)
                    if not functor_rotate is None:
                        rotate_xyz = calculator.rotate_XYZ(rotate_xyz[0], rotate_xyz[1], rotate_xyz[2], functor_rotate)
                    rotate_xyz = calculator.rotate_XYZ(rotate_xyz[0], rotate_xyz[1], rotate_xyz[2], module_rotate)
                    points.append({"x": rotate_xyz[0], "y": rotate_xyz[1], "z": rotate_xyz[2]})
                result.append({'type': 1, 'data': points})
        else:
            result.append({"x": x, "y": y, "z": z, 'type': 0})
    return result

def parse_direction(direction,rotate):
    if rotate[0] == 90 or rotate[0] == 270 or rotate[0] == -90 or rotate[0] == -270:
        direction = [direction[1],direction[0],not direction[2]]
    if rotate[1] == 90 or rotate[1] == 270 or rotate[1] == -90 or rotate[1] == -270:
        direction = [not direction[2],not direction[1],not direction[0]]
    if rotate[2] == 90 or rotate[2] == 270 or rotate[2] == -90 or rotate[2] == -270:
        direction = [not direction[0],direction[2],direction[1]]
    return direction

def parse_stone(xml,stone_data,sections_data,back_path):
    z = float(xml.attrib['groundHeightValue'])
    h = float(xml.attrib['tableThicknessValue'])

    points = xml.attrib["pathGeometryPoints"].split('|')
    for p in points:
        stone_data.append({'type': 0, 'x': float(p.split(',')[0]),
                           'y': float(p.split(',')[1]), 'z': z})
    for p in points:
        stone_data.append({'type': 0, 'x': float(p.split(',')[0]),
                           'y': float(p.split(',')[1]), 'z': z + h})

    l = len(xml.attrib['normalSectionsPoint'].split('|'))
    if l > 4:
        arr = xml.attrib['normalPoint'].split(',')
        edge = len(xml.findall("FrontPath")[0].attrib['points'].split('|')) - 1
        calculator_section(arr, sections_data, l, edge, z, h)

    l = len(xml.attrib['deleteSectionsPoint'].split('|'))
    if l > 4:
        arr = xml.attrib['deletePoint'].split(',')
        edge = len(xml.findall("BackPath")[0].attrib['points'].split('|')) - 1
        calculator_section(arr, sections_data, l, edge, z, h)

        z = z + h
        h = float(xml.attrib['backHeightValue'])
        points = xml.findall("BackPath")[0].attrib['points'].split('|')
        for p in points:
            back_path.append({'type': 0, 'x': float(p.split(',')[0]),
                              'y': float(p.split(',')[1]), 'z': z})
        points.reverse()
        for p in points:
            back_path.append({'type': 0, 'x': float(p.split(',')[0]),
                              'y': float(p.split(',')[1]), 'z': z})
        points.reverse()
        for p in points:
            back_path.append({'type': 0, 'x': float(p.split(',')[0]),
                              'y': float(p.split(',')[1]), 'z': z + h})
        points.reverse()
        for p in points:
            back_path.append({'type': 0, 'x': float(p.split(',')[0]),
                              'y': float(p.split(',')[1]), 'z': z + h})

def calculator_section(arr,sections_data,l,edge,z,h):
    for b in range(edge):
        lis = []
        for a in range(l):
            idx = (a + b * l) * 12
            lis.append({'type': 0, 'x': float(arr[idx]) / 0.1,
                        'y': float(arr[idx + 1]) / 0.1,
                        'z': float(arr[idx + 2]) / 0.1 + z + h})
        lis = lis + lis
        sections_data.append(lis)
    lis = []
    for a in range(l):
        idx = ( a + l + 4 * edge * l) * 3
        lis.append({'type': 0, 'x': float(arr[idx]) / 0.1,
                    'y': float(arr[idx + 1]) / 0.1,
                    'z': float(arr[idx + 2]) / 0.1 + z + h})
    lis = lis + lis
    sections_data.append(lis)