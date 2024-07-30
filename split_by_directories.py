import json
import os
import argparse
import sys
import shutil
from tqdm import tqdm


def create_directories(path, labels):
    set_labels = set([labels[key] for key in labels])
    for label in set_labels:
        if not os.path.exists(os.path.join(path, label)):
            os.mkdir(os.path.join(path, label))
        
        
def split_images(path_to_images, path_with_classes, images, labels):
    files = set([image['file'] for image in images])
    for image in tqdm(images):
        file = image['file']
        for detection in image['detections']:
            category = detection['category']
            name = labels[category]
            shutil.copy(os.path.join(path_to_images, file), os.path.join(path_with_classes, name, file))
        

def split_by_directories(path_to_images, path_to_json, path_with_classes):
    with open(path_to_json, 'r', encoding='utf-8') as f:
        js = json.load(f)
        
    labels = js['detection_categories']
    images = js['images']
    create_directories(path_with_classes, labels)
    split_images(path_to_images, path_with_classes, images, labels)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path_to_images',
        help='the path where the classified photos lie')
    parser.add_argument(
        'path_to_json_classifier',
        help='the path to the json file with the classification. it is created after using the detect and script classifier.sh in the ZooML/dataset/annotations folder')
    parser.add_argument(
        'path_with_classes',
        help='the path to the folders with categories')
    
    if len(sys.argv[1:]) != 3:
        parser.print_help()
        parser.exit()
        
    args = parser.parse_args()

    split_by_directories(args.path_to_images,
                         args.path_to_json_classifier,
                         args.path_with_classes)
    

if __name__ == '__main__':
    main()