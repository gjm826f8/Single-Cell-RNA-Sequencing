import xml.etree.ElementTree as ET
tree = ET.parse('..\\config.xml')

def read_config():
    file_path_array = []
    id_array = []
    fc_array = []
    root = tree.getroot()
    for child in root:
        for grandchild in child:
            if child.tag == "filepath":
                file_path_array.append(grandchild.text)
            elif child.tag == "id":
                id_array.append(grandchild.text)
            elif child.tag == "fc":
                fc_array.append(grandchild.text)
    return file_path_array, id_array, fc_array

def write_config(tag, text):
    print("write_config", tag, text)
    root = tree.getroot()
    new_ele = ET.Element("option")
    new_ele.text = text
    root.find(tag).append(new_ele)
    tree.write("..\\config.xml")