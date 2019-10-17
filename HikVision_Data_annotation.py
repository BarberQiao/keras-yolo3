import xml.etree.ElementTree as ET

def get_all_class_name_by_image_ID_list(image_ids):
    classes_dict = dict()
    for image_id in image_ids:
        xml_file_path = 'HeiBeiHikvision/Annotations/%s.xml' % (image_id)
        in_file = open(xml_file_path)
        tree = ET.parse(in_file)
        root = tree.getroot()
        for obj in root.iter('object'):
            tmp_cls = obj.find('name').text
            if not classes_dict.keys().__contains__(tmp_cls):
                classes_dict[tmp_cls] = 1
            else:
                classes_dict[tmp_cls] += 1
    return classes_dict


def convert_annotation_write_lines(image_id, list_file, object_class_list, standard_classes):

    xml_file_path = 'HeiBeiHikvision/Annotations/%s.xml'%(image_id)
    in_file = open(xml_file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()
    finded_set = set()

    training_set_need = False
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls in object_class_list:
            training_set_need = True
            break
    if training_set_need:
        list_file.write('HeiBeiHikvision/JPEGImages/%s.jpg' % (image_id))
        show_list = list()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls in standard_class:
                cls_id = standard_classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text),int(xmlbox.find('ymax').text))
                list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
                finded_set.add(cls)
                show_list.append(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        print("add: ", 'HeiBeiHikvision/JPEGImages/%s.jpg' % (image_id)," ".join(show_list))
        list_file.write('\n')
    return finded_set

image_ids = open(r'HeiBeiHikvision/train.txt').read().strip().split()
output_train_file_path = r'HeiBeiHikvision/train_processed.txt'
output_class_txt_path = r"HeiBeiHikvision/HikVision_classes.txt"
list_file = open(output_train_file_path, 'w')
all_class = get_all_class_name_by_image_ID_list(image_ids)

find_class_dict = dict()
for each_class, tmp_count in all_class.items():
    if tmp_count > 100:
        find_class_dict[each_class] = 0
standard_class = list(find_class_dict.keys())

for image_id in image_ids:
    print(image_id, " start ", find_class_dict)
    finded_set = convert_annotation_write_lines(image_id, list_file, list(find_class_dict.keys()), standard_class)
    print(image_id, "return set: ", finded_set, find_class_dict)
    for each_cls in finded_set:
        if each_cls in find_class_dict:
            find_class_dict[each_cls] += 1
            if find_class_dict[each_cls] > 20:
                print(image_id, "Delete key: ", each_cls, "count: ", find_class_dict[each_cls], find_class_dict)
                del find_class_dict[each_cls]
                print(image_id, "Deleted key: ", each_cls, find_class_dict)
list_file.close()

with open(output_train_file_path, "r") as f:
    data = f.readlines()
print(data)
print(len(data))
print("standard: ", standard_class)
write_class = open(output_class_txt_path, 'w')
for tmp_class in standard_class:
    write_class.write(tmp_class)
    write_class.write('\n')
write_class.close()