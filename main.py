import argparse
import json
import logging
import os
import time
import xml.etree.ElementTree as ET
import ezdxf
import requests
from ezdxf.addons import Importer

from ancuong import parse
from ancuong.cabinet import Cabinet
from ancuong.floor import Floor

logging.getLogger().setLevel(logging.CRITICAL)
DEFAULT_MAX = -9999999999999999999999999999
DEFAULT_MIN = 99999999999999999999999999999
doc = ezdxf.new()
msp = doc.modelspace()
msp.units = 7
doc.styles.new('h3d_style', dxfattribs={'font': 'times.ttf'})
xml_content = ""
job_type = ""
export_id = ""
base_path = ""

def server():
    global xml_content, job_type, export_id, base_path
    parser = argparse.ArgumentParser()
    parser.add_argument("jobType", help='Export job type')
    parser.add_argument("xmlContent", help='Xml Content')
    parser.add_argument("export_id", help='Id')
    args = parser.parse_args()
    xml_content = args.xmlContent
    job_type = args.jobType
    export_id = args.export_id
    base_path = "/worker/flamenco-worker-linux/flamenco_worker/cad/"

def local():
    global xml_content, job_type, export_id, base_path
    base_path = ""
    job_type = "floor"
    job_type = "cabinet"
    xml_content = "https://api.house3d.net/web/data/cad.h3d/202106/07/h3d_cad_1623056892.xml"
    xml_content = 'as7.xml'
    export_id = "1"

# to debug on local change this value to False
is_production_environment = False

if is_production_environment:
    print("====== ON PRODUCTION ======")
    server()
else:
    print("====== ON LOCAL ======")
    local()

if job_type == "floor":
    material_attribute_path = base_path + "attribute.json"
    if os.path.isfile(material_attribute_path):
        with open(material_attribute_path) as material_attribute:
            category_id = json.load(material_attribute)
    else:
        print("Cannot find material attribute template - path: {}".format(material_attribute_path))

    door_template_path = base_path + "template/door.dxf"
    if os.path.isfile(door_template_path):
        doc2 = ezdxf.readfile(door_template_path)
        door_importer = Importer(doc2, doc)
        door_importer.finalize()
    else:
        print("Cannot find door template - path: {}".format(door_template_path))

    material_template_path = base_path + "template/material.dxf"
    if os.path.isfile(material_template_path):
        doc1 = ezdxf.readfile(material_template_path)
        attribute_importer = Importer(doc1, doc)
        attribute_importer.finalize()
    else:
        print("Cannot find material template - path: {}".format(material_template_path))

if job_type == 'cabinet':
    cabinet_template_path = base_path + "template/cabinet.dxf"
    cabinet_1_template_path = base_path + "template/chau2.dxf"
    cabinet_2_template_path = base_path + "template/bep.dxf"
    cabinet_3_template_path = base_path + "template/lo.dxf"
    if os.path.isfile(cabinet_template_path):
        doc3 = ezdxf.readfile(cabinet_template_path)
        cabinet_importer = Importer(doc3, doc)
        cabinet_importer.finalize()

        doc4 = ezdxf.readfile("template/khungten.dxf")
        importer = Importer(doc4, doc)
        importer.import_block('KT')
        importer.finalize()
    else:
        print("Cannot find door template - path: {}".format(cabinet_template_path))

    if os.path.isfile(cabinet_1_template_path):
        doc5 = ezdxf.readfile(cabinet_1_template_path)
        cabinet_importer = Importer(doc5, doc)
        cabinet_importer.import_block(block_name='chau 1_b')
        cabinet_importer.import_block(block_name='chauL')
        cabinet_importer.import_block(block_name='chauf')
        cabinet_importer.finalize()

    if os.path.isfile(cabinet_2_template_path):
        doc6 = ezdxf.readfile(cabinet_2_template_path)
        cabinet_importer = Importer(doc6, doc)
        cabinet_importer.import_block(block_name='A$C74A327AC')
        cabinet_importer.import_block(block_name='A$C706F0BD6')
        cabinet_importer.import_block(block_name='A$C3A237A13')
        cabinet_importer.finalize()

    if os.path.isfile(cabinet_3_template_path):
        doc7 = ezdxf.readfile(cabinet_3_template_path)
        cabinet_importer = Importer(doc7, doc)
        cabinet_importer.import_block(block_name='A$C06C54A8D')
        cabinet_importer.import_block(block_name='A$C3E5D6D2C')
        cabinet_importer.import_block(block_name='A$C51AB1ED8')
        cabinet_importer.finalize()

    direction_path = base_path + 'template/direction.dxf'
    if os.path.isfile(direction_path):
        direction_f = ezdxf.readfile(direction_path)
        direction_importer = Importer(direction_f, doc)
        direction_importer.import_block('direction')
        direction_importer.finalize()
    else:
        print("Cannot find direction template - path: {}".format(direction_path))

def parse_xml(xml, job):
    if xml.find("http") > -1:
        if xml.find("https") < 0:
            xml = xml.replace("http", "https")

        print("xml content: {}".format(xml))
        r = requests.get(xml)
        xml = r.content

        # xml = urllib.request.urlopen(xml).read()
        tree = ET.fromstring(xml)
    else:
        tree = ET.parse(xml)
    if job.find("cabinet") > -1:
        cabinet = tree.findall("CabinetLayout")
        for child in cabinet:
            if "type" in child.attrib:
                parse_data(child, child.attrib['type'])
                # globals()["parse_" + child.attrib['type'] + "_xml"](child, job)
    if job.find("floor") > -1:
        parse_wall_data(tree)

def parse_wall_data(tree):
    print("parse_wall_data")
    walls = tree.findall("HouseType/Walls/Wall")
    inner_points = tree.findall("Room/InnerPoints")
    wall_info = tree.findall("Room/WallInfo")
    data_cabinet = tree.findall("Part/Values")
    rooms = tree.findall("HouseType/Rooms/Room")
    in_wall_data = tree.findall("HouseType/InWallDatas/InWallData")
    all_inner_wall_data = []
    all_wall_data = []
    print(in_wall_data)
    for i in inner_points:
        all_inner_wall_data.append(i.attrib['value'].split('|'))
    for i in wall_info:
        all_wall_data.append(i.attrib['value'].split('|'))

    furniture_data = tree.findall("Furniture/FurnitureData")

    floor = Floor(msp,walls,in_wall_data,furniture_data,rooms)
    floor.write_hatch(door_importer)
    floor.write_furniture(doc1,category_id,attribute_importer)
    floor.dim()
    floor.add_room_name()

def parse_data(xml, sub_app):
    if sub_app != 'cupboard':
        module_part_list = []
        module_door_list = []
        module_info_list = []
        module_model_list = []
        for module in xml.findall("Part"):
            if module.attrib['type'] == 'unit':
                parse.parse_unit(module,module_part_list,module_door_list,module_info_list,module_model_list)
            elif module.attrib['type'] == 'group':
                for unit in module.findall('Part'):
                    print('------------group--------------')
                    # parse_unit(unit, module_part_list, module_door_list, module_info_list)
        cabinet = Cabinet(msp,module_part_list,module_door_list,module_info_list,module_model_list)
        cabinet.draw_cabinet()
    else:
        stone_data = []
        sections_data = []
        back_path = []
        if len(xml.findall("Table")):
            parse.parse_stone(xml.findall("Table")[0],stone_data,sections_data,back_path)

        modules = xml.findall("Part")
        room_ids = []
        moduleWithID = {}
        for module in modules:
            if module.attrib['RoomUID'] not in room_ids and module.attrib['RoomUID'] != "-1":
                room_ids.append(module.attrib['RoomUID'])
        for roomID in room_ids:
            for module in modules:
                if roomID == module.attrib['RoomUID']:
                    if roomID not in moduleWithID:
                        moduleWithID[roomID] = [module]
                    else:
                        moduleWithID[roomID].append(module)
        for ids in moduleWithID:
            wall = []
            in_wall_data = []
            rooms = xml.findall("Room")
            for r in rooms:
                if r.attrib["uid"] == ids:
                    wall = r.findall("Walls/Wall")
                    in_wall_data = r.findall("InWallData")
            module_part_list = []
            module_door_list = []
            module_info_list = []
            module_model_list = []
            for module in moduleWithID[ids]:
                if module.attrib['type'] == 'unit':
                    parse.parse_unit(module, module_part_list, module_door_list, module_info_list, module_model_list)
                elif module.attrib['type'] == 'group':
                    for unit in module.findall('Part'):
                        print('------------group--------------')
                        # parse_unit(unit, module_part_list, module_door_list, module_info_list)
            wall_data = [wall, in_wall_data]
            cabinet = Cabinet(msp, module_part_list, module_door_list, module_info_list, module_model_list,stone_data,sections_data,back_path,doc5,doc6,doc7)
            cabinet.draw_cabinet_cupboard(wall_data)

def save_file():
    if not os.path.isdir("../output"):
        os.makedirs("../output")
    file_name = "output/" + str(round(time.time() * 1000)) + "_info.dxf"
    doc.saveas(file_name)
    print("Save file {} success".format(file_name))
    return file_name

def upload_file(file_name):
    if not is_production_environment:
        print("In local don't upload any files")
        return
    print("Start upload file")
    url = "https://api.house3d.net/web/api/queues/upload-cad/{}"
    f = open(file_name, 'rb')
    files = {'file': (file_name, f)}
    headers = {
        "Authorization": "Bearer 4t7fB5LM6rTUMgMBgz2Pps8fe6VzDt4EJ9P3Zu6Q47EJ3D6hBAzBYG6pXFaLfVzg4An8TdgET9EMKmg7GEbmgTS7Ud6AQHk48P3C2yT"}
    response = requests.post(url.format(export_id), headers=headers,
                             files=files)
    print("Response: {}".format(response.text))
    f.close()
    os.remove(file_name)

parse_xml(xml_content, job_type)
file = save_file()
upload_file(file)
