import os
from glob import iglob
from functools import reduce
import pandas as pd
from xml.etree import ElementTree as et
from concurrent.futures import ThreadPoolExecutor
from shutil import move


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

def label_encoding(df):
              'bottle':9, 'sheep':10, 'diningtable':11, 'horse':12, 'motorbike':13, 'sofa':14, 'cow':15, 'car':16, 'cat':17,
              'bus':18, 'pottedplant':19}
    df.loc[:, 'id'] = df.loc[:, 'name'].apply(lambda x: labels[x])
    return df


if __name__ == '__main__':
    xml_dir = './dataset/'
    df = convert_xml_to_yolo(xml_dir)


# get yolo labels from this data
df['center_x'] = ((df['xmax'] + df['xmin']) / 2) / df['width']
df['center_y'] = ((df['ymax'] + df['ymin']) / 2) / df['height']
df['w'] = (df['xmax'] - df['xmin']) / df['width']
df['h'] = (df['ymax'] - df['ymin']) / df['height']

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
train_df = label_encoding(train_df)
test_df = label_encoding(test_df)

train_folder = 'dataset/train'
test_folder = 'dataset/test'

os.mkdir(train_folder)
os.mkdir(test_folder)
cols = ['filename', 'id', 'center_x', 'center_y', 'w', 'h']
training_group_by_obj = train_df[cols].groupby('filename')
testing_group_by_obj = test_df[cols].groupby('filename')

def save_data(filename, folder_path, group_obj):
    src = os.path.join('dataset', filename)
    dst = os.path.join(folder_path, filename)
    move(src, dst)

    text_filename = os.path.join(folder_path,
                                 os.path.splitext(filename)[0] + '.txt')
    group_obj.get_group(filename).set_index('filename').to_csv(text_filename, sep=' ',
                                                               index=False, header = False)
#moving training and testing files to respective directories
filename_series = pd.Series(list(training_group_by_obj.groups.keys()))
filename_series_test = pd.Series(list(testing_group_by_obj.groups.keys()))
filename_series.apply(save_data, args=(train_folder, training_group_by_obj))
filename_series_test.apply(save_data, args=(test_folder, testing_group_by_obj))






