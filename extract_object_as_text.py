import os
from glob import iglob
from functools import reduce
import pandas as pd
from xml.etree import ElementTree as et
from concurrent.futures import ThreadPoolExecutor


def extract_object_info(xml_file):
    tree = et.parse(xml_file)
    root = tree.getroot()
    file_name = root.find('filename').text
    size = root.find('size')
    width = float(size.find('width').text)
    height = float(size.find('height').text)
    data = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        bound = obj.find('bndbox')
        xmin = float(bound.find('xmin').text)
        xmax = float(bound.find('xmax').text)
        ymin = float(bound.find('ymin').text)
        ymax = float(bound.find('ymax').text)
        center_x = ((xmax + xmin) / 2) / width
        center_y = ((ymax + ymin) / 2) / height
        w = (xmax - xmin) / width
        h = (ymax - ymin) / height
        data.append([file_name, width, height, name, xmin, xmax, ymin, ymax, center_x, center_y, w, h])
    return data


def parse_xml_files(xml_files):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(extract_object_info, xml_files))
    return reduce(lambda x, y: x + y, results)


def convert_xml_to_yolo(xml_dir):
    xml_files = iglob(os.path.join(xml_dir, '*.xml'))
    data = parse_xml_files(xml_files)
    columns = ['filename', 'width', 'height', 'name', 'xmin', 'xmax', 'ymin', 'ymax', 'center_x', 'center_y', 'w', 'h']
    df = pd.DataFrame(data, columns=columns)
    cols_to_convert = ['width', 'height', 'xmin', 'xmax', 'ymin', 'ymax']
    df[cols_to_convert] = df[cols_to_convert].astype(float)
    return df


if __name__ == '__main__':
    xml_dir = './dataset/'
    df = convert_xml_to_yolo(xml_dir)


