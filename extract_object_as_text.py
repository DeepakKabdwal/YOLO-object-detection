import os
from glob import glob
from functools import reduce
import pandas as pd
from xml.etree import ElementTree as et

# import all the .xml files into the xml_list
xml_list = glob('./dataset/*.xml')
# print(xml_list)

# replace \\ with / for proper path
xml_list = list(map(lambda x: x.replace('\\', '/'), xml_list))


# now read each xml file and from each xml file get
# filename, size(width, height), object(name, xmin, xmax, ymin, ymax)
def extract_object_info(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    file_name = root.find('filename').text
    # print(file_name)
    size = root.find('size')
    width = size.find('width').text
    height = size.find('height').text
    object_img = root.findall('object')
    parser = []
    for obj in object_img:
        name = obj.find('name').text
        bound = obj.find('bndbox')
        xmin = bound.find('xmin').text
        xmax = bound.find('xmax').text
        ymin = bound.find('ymin').text
        ymax = bound.find('ymax').text
        parser.append([file_name, width, height, name, xmin, xmax, ymin, ymax])
    return parser


parsed_list = list(map(extract_object_info, xml_list))

