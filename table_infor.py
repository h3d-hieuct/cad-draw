def write_info(msp,module_info,idx,scale = 1):
    attr   = {'style': "h3d_style",'height': 30 * scale,'color': 251}
    attr_1 = {'style': "h3d_style",'height': 30 * scale,'width': 0.7,'color': 251}
    attr_2 = {'style': "h3d_style",'height': 50 * scale,'color': 3}
    attr_3 = {'style': "h3d_style",'height': 50 * scale,'color': 251}
    attr_4 = {'style': "h3d_style",'height': 30 * scale,'width': 0.5,'color': 251}
    attr_5 = {'style': "h3d_style",'height': 30 * scale,'width': 0.6,'color': 251}
    attr_6 = {'style': "h3d_style",'height': 50 * scale,'width': 0.8,'color': 40}
    def insert_row(point_idx):
        result = insert_column(point_idx, 250 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 250 * scale, point_idx[1]], 350 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 600 * scale, point_idx[1]], 600 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 1200 * scale, point_idx[1]], 300 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 1500 * scale, point_idx[1]], 300 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 1800 * scale, point_idx[1]], 300 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 2100 * scale, point_idx[1]], 588 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 2688 * scale, point_idx[1]], 300 * scale, 90 * scale)
        return result
    def insert_row_1(point_idx):
        result = insert_column(point_idx, 250 * scale, 90 * scale)
        result = result + insert_column([point_idx[0] + 250 * scale, point_idx[1]], 2738 * scale, 90 * scale)
        return result
    def insert_column(point_idx,x,y):
        result = [[point_idx[0],point_idx[1]-y],[point_idx[0]+x,point_idx[1]-y],[point_idx[0]+x,point_idx[1]]]
        return result

    table = [[idx[0] + 2988 * scale, idx[1]], idx]
    table = table + insert_column(idx, 2988 * scale, 2030 * scale) + [idx]
    if scale==1:
        table = table + insert_column(idx, 600 * scale, 90 * scale)
        table = table + insert_column([idx[0] + 600 * scale, idx[1]], 1200 * scale, 90 * scale)
        table = table + insert_column([idx[0] + 1800 * scale, idx[1]], 300 * scale, 90 * scale)
        table = table + insert_column([idx[0] + 2100 * scale, idx[1]], 888 * scale, 90 * scale) + [idx]
        table = table + insert_column([idx[0], idx[1] - 90 * scale], 2988 * scale, 90 * scale) + [[idx[0], idx[1] - 90 * scale]]
    else:
        table = table + insert_column(idx, 2988 * scale, 90 * scale) + [idx]
    table = table + insert_column([idx[0], idx[1] - 180 * scale], 1800 * scale, 140 * scale)
    table = table + insert_column([idx[0] + 1800 * scale, idx[1] - 180 * scale], 1188 * scale, 140 * scale) + [[idx[0], idx[1] - 180 * scale]]
    table = table + insert_row([idx[0], idx[1] - 320 * scale]) + [[idx[0], idx[1] - 320 * scale]]
    table = table + insert_row([idx[0], idx[1] - 410 * scale]) + [[idx[0], idx[1] - 410 * scale]]
    table = table + insert_row([idx[0], idx[1] - 500 * scale]) + [[idx[0], idx[1] - 500 * scale]]
    table = table + insert_row([idx[0], idx[1] - 590 * scale]) + [[idx[0], idx[1] - 590 * scale]]
    table = table + insert_row([idx[0], idx[1] - 680 * scale]) + [[idx[0], idx[1] - 680 * scale]]
    table = table + insert_row([idx[0], idx[1] - 770 * scale]) + [[idx[0], idx[1] - 770 * scale]]
    table = table + insert_column([idx[0], idx[1] - 860 * scale], 600 * scale, 90 * scale)
    table = table + insert_column([idx[0] + 600 * scale, idx[1] - 860 * scale], 2388 * scale, 90 * scale)+ [[idx[0], idx[1] - 860 * scale]]
    table = table + insert_column([idx[0], idx[1] - 950 * scale], 2988 * scale, 90 * scale) + [[idx[0], idx[1] - 950 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1040 * scale]) + [[idx[0], idx[1] - 1040 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1130 * scale]) + [[idx[0], idx[1] - 1130 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1220 * scale]) + [[idx[0], idx[1] - 1220 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1310 * scale]) + [[idx[0], idx[1] - 1310 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1400 * scale]) + [[idx[0], idx[1] - 1400 * scale]]
    table = table + insert_column([idx[0], idx[1] - 1490 * scale], 2988 * scale, 90 * scale) + [[idx[0], idx[1] - 1490 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1580 * scale]) + [[idx[0], idx[1] - 1580 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1670 * scale]) + [[idx[0], idx[1] - 1670 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1760 * scale]) + [[idx[0], idx[1] - 1760 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1850 * scale]) + [[idx[0], idx[1] - 1850 * scale]]
    table = table + insert_row_1([idx[0], idx[1] - 1940 * scale]) + [[idx[0], idx[1] - 1940 * scale]]

    msp.add_polyline2d(table,dxfattribs={'color':251})

    if scale == 1:
        msp.add_text('MÃ SẢN PHẨM', dxfattribs=attr).set_pos([idx[0] + 120 * scale, idx[1] - 60 * scale])
        msp.add_text('SỐ LƯỢNG', dxfattribs=attr).set_pos([idx[0] + 1830 * scale, idx[1] - 60 * scale])
    msp.add_text('THÔNG TIN VẬT LIỆU', dxfattribs=attr_2).set_pos([idx[0] + 1300 * scale, idx[1] - 160 * scale])
    msp.add_text('VẬT LIỆU ĐỒNG MÀU', dxfattribs=attr_3).set_pos([idx[0] + 530 * scale, idx[1] - 280 * scale])
    msp.add_text('VẬT LIỆU KHÁC MÀU', dxfattribs=attr_3).set_pos([idx[0] + 2050 * scale, idx[1] - 280 * scale])
    msp.add_text('NHÓM', dxfattribs=attr).set_pos([idx[0] + 55 * scale, idx[1] - 380 * scale])
    msp.add_text('HẠNG MỤC', dxfattribs=attr).set_pos([idx[0] + 300 * scale, idx[1] - 380 * scale])
    msp.add_text('MÃ VẬT TƯ(loại ván + mặt 1/ mặt 2)', dxfattribs=attr_1).set_pos([idx[0] + 650 * scale, idx[1] - 380 * scale])
    msp.add_text('MÀU CHỈ CẠNH', dxfattribs=attr_1).set_pos([idx[0] + 1230 * scale, idx[1] - 380 * scale])
    msp.add_text('MÀU CHỈ CẠNH TRƯỚC', dxfattribs=attr_4).set_pos([idx[0] + 1520 * scale, idx[1] - 380 * scale])
    msp.add_text('CHI TIẾT KHÁC MÀU', dxfattribs=attr_5).set_pos([idx[0] + 1815 * scale, idx[1] - 380 * scale])
    msp.add_text('MÃ VẬT TƯ(loại ván + mặt 1/ mặt 2)', dxfattribs=attr_1).set_pos([idx[0] + 2150 * scale, idx[1] - 380 * scale])
    msp.add_text('MÀU CHỈ CẠNH', dxfattribs=attr_1).set_pos([idx[0] + 2720 * scale, idx[1] - 380 * scale])
    msp.add_text('VẬT LIỆU', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 470 * scale])
    msp.add_text('THÙNG TỦ', dxfattribs=attr).set_pos([idx[0] + 280 * scale, idx[1] - 470 * scale])
    msp.add_text('VẬT LIỆU', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 560 * scale])
    msp.add_text('CÁNH', dxfattribs=attr).set_pos([idx[0] + 280 * scale, idx[1] - 560 * scale])
    msp.add_text('VẬT LIỆU', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 650 * scale])
    msp.add_text('MẶT HỘC KÉO', dxfattribs=attr).set_pos([idx[0] + 280 * scale, idx[1] - 650 * scale])
    msp.add_text('VẬT LIỆU', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 740 * scale])
    msp.add_text('VẬT LIỆU', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 830 * scale])
    msp.add_text('TIÊU CHUẨN DÁN CẠNH', dxfattribs=attr).set_pos([idx[0] + 40 * scale, idx[1] - 920 * scale])
    msp.add_text('THÔNG TIN PHỤ KIỆN', dxfattribs=attr_2).set_pos([idx[0] + 1300 * scale, idx[1] - 1020 * scale])
    msp.add_text('PHỤ KIỆN', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1100 * scale])
    msp.add_text('PHỤ KIỆN', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1190 * scale])
    msp.add_text('PHỤ KIỆN', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1280 * scale])
    msp.add_text('PHỤ KIỆN', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1370 * scale])
    msp.add_text('PHỤ KIỆN', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1460 * scale])
    msp.add_text('THÔNG TIN THIẾT BỊ', dxfattribs=attr_2).set_pos([idx[0] + 1300 * scale, idx[1] - 1560 * scale])
    msp.add_text('THIẾT BỊ', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1640 * scale])
    msp.add_text('THIẾT BỊ', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1730 * scale])
    msp.add_text('THIẾT BỊ', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1820 * scale])
    msp.add_text('THIẾT BỊ', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 1910 * scale])
    msp.add_text('THIẾT BỊ', dxfattribs=attr).set_pos([idx[0] + 25 * scale, idx[1] - 2000 * scale])
    if scale == 1:
        msp.add_text(
            module_info['name'] + '_' + module_info['info'].attrib['W'] + 'x' + module_info['info'].attrib['D'] + 'x' +
            module_info['info'].attrib['H'], dxfattribs=attr_6).set_pos([idx[0] + 900 * scale, idx[1] - 65 * scale])
    msp.add_text(module_info['material_cabinet'], dxfattribs=attr_6).set_pos([idx[0] + 650 * scale, idx[1] - 480 * scale])
    msp.add_text(module_info['material_door'], dxfattribs=attr_6).set_pos([idx[0] + 650 * scale, idx[1] - 570 * scale])
    msp.add_text(module_info['material_door_functor'], dxfattribs=attr_6).set_pos([idx[0] + 650 * scale, idx[1] - 660 * scale])
    if len(module_info['accessory_list'])>5:
        module_info['accessory_list'] = module_info['accessory_list'][0:4]
    for accessory in module_info['accessory_list']:
        msp.add_text(accessory['name'], dxfattribs=attr_6).set_pos([idx[0] + 280 * scale, idx[1] - 1120 * scale - 90 * scale * module_info['accessory_list'].index(accessory)])