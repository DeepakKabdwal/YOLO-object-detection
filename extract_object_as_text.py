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
data = reduce(lambda x, y: x + y, parsed_list)

# convert it all into a pandas dataframe
df = pd.DataFrame(data, columns=['filename', 'width', 'height', 'name', 'xmin', 'xmax', 'ymin', 'ymax'])

# print(df.info())

# all the data is of type object, but we need width height xmin xmax ymin ymax as integer so conversion
cols = ['width', 'height', 'xmin', 'xmax', 'ymin', 'ymax']
df[cols] = df[cols].astype(float)

<<<<<<< Updated upstream
# get yolo labels from this data
df['center_x'] = ((df['xmax'] + df['xmin']) / 2) / df['width']
df['center_y'] = ((df['ymax'] + df['ymin']) / 2) / df['height']
df['w'] = (df['xmax'] - df['xmin']) / df['width']
df['h'] = (df['ymax'] - df['ymin']) / df['height']
=======
if __name__ == '__main__':
    xml_dir = './dataset/'
    df = convert_xml_to_yolo(xml_dir)

images = df['filename'].unique()
#print(len(images))
images_df = pd.DataFrame(images, columns=['FileNames'])
# we need test and train split of 80% to 20%
#print(images_df.head())
images_train = tuple(images_df.sample(frac=0.8)['FileNames'])    #randomly take 80% of the dataframe
#rest 20% as test images

# NEVER train on test images
images_test = tuple(images_df.query(f'FileNames not in {images_train}')['FileNames'])
# print(len(images_df))
# print(len(images_train))
# print(len(images_test))
#dataframes made for training and testing
train_df = df.query(f'filename in {images_train}')
test_df = df.query(f'filename in {images_test}')

#print(train_df.head())

#encode the label names as we can't train on text values


>>>>>>> Stashed changes

# print(df.info())
