import os
import xml.etree.ElementTree as ET

current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
config_file_path = os.path.join(parent_path, "..", "config.xml")
tree = ET.parse(config_file_path)

def read_config():
    file_path_array = []
    id_array = []
    fc_array = []
    pv_array = []
    root = tree.getroot()
    for child in root:
        for grandchild in child:
            if child.tag == "filepath":
                file_path_array.append(grandchild.text)
            elif child.tag == "id":
                id_array.append(grandchild.text)
            elif child.tag == "fc":
                fc_array.append(grandchild.text)
            elif child.tag == "pv":
                pv_array.append(grandchild.text)
    return file_path_array, id_array, fc_array, pv_array

def write_config(tag, text):
    print("write_config", tag, text)
    root = tree.getroot()
    new_ele = ET.Element("option")
    new_ele.text = text
    root.find(tag).append(new_ele)
    tree.write(config_file_path)