# 2021-10-28 - hieuhihi

from ancuong import  max_min

def add_block(msp, doc, block_name, position, furniture_info, is_cabinet=False):
    block_name = str(block_name).lower()
    block_data_entities = doc.blocks.block_records.entries[block_name].entity_space.entities
    max_point_arr = []
    min_point_arr = []
    for entity in block_data_entities:
        if entity.DXFTYPE == 'LWPOLYLINE':
            temp = []
            lwpoints = entity.lwpoints
            for point in lwpoints:
                x = point[0]
                y = point[1]
                temp.append([x, y])
            max_point_arr.append(max_min.get_max_point(temp))
            min_point_arr.append(max_min.get_min_point(temp))
        # if entity.dxftype() == 'ELLIPSE':
        #     points = []
        #     segment = 10
        #     delta = math.fabs(entity.dxf.end_param - entity.dxf.start_param) / segment
        #     b = math.sqrt(
        #         entity.dxf.major_axis[0] * entity.dxf.major_axis[0] + entity.dxf.major_axis[1] * entity.dxf.major_axis[
        #             1])
        #     a = b / entity.dxf.ratio
        #     for i in range(segment):
        #         p1 = [a * math.cos(entity.dxf.start_param + i * delta) + entity.dxf.center[0],
        #               b * math.sin(entity.dxf.start_param + i * delta) + entity.dxf.center[1]]
        #         points.append(p1)
        #     max_point_arr.append(get_max_point(points))
        #     min_point_arr.append(get_min_point(points))
        if entity.dxftype() == 'LINE':
            max_point_arr.append(
                max_min.get_max_point([(entity.dxf.start[0], entity.dxf.start[1]), (entity.dxf.end[0], entity.dxf.end[1])]))
            min_point_arr.append(
                max_min.get_min_point([(entity.dxf.start[0], entity.dxf.start[1]), (entity.dxf.end[0], entity.dxf.end[1])]))
        if entity.dxftype() == 'ARC':
            max_point_arr.append(max_min.get_max_point(
                [(entity.start_point[0], entity.start_point[1]), (entity.end_point[0], entity.end_point[1])]))
            min_point_arr.append(max_min.get_min_point(
                [(entity.start_point[0], entity.start_point[1]), (entity.end_point[0], entity.end_point[1])]))
    max_point = max_min.get_max_point(max_point_arr)
    min_point = max_min.get_min_point(min_point_arr)
    w = max_point[0] - min_point[0]
    h = max_point[1] - min_point[1]
    if is_cabinet:
        msp.add_blockref(block_name, insert=position, dxfattribs={
            'xscale': float(furniture_info.attrib['W']) / w,
            'yscale': float(furniture_info.attrib['D']) / h,
            'rotation': furniture_info.attrib['RZ']})
    else:
        msp.add_blockref(block_name, insert=position, dxfattribs={
            'xscale': float(furniture_info.attrib['Length']) / w,
            'yscale': float(furniture_info.attrib['Width']) / h,
            'rotation': furniture_info.attrib['RotateZ']})