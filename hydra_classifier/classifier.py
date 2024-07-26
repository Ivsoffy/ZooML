#load model
import torch
from omegaconf import OmegaConf
from srcs.utils import instantiate
# from efficientnet_pytorch import EfficientNet
from tqdm import tqdm
import argparse
import sys
from pathlib import Path


def load_model(weights):
    checkpoint = torch.load(weights)
    loaded_config = OmegaConf.create(checkpoint['config'])

    model = instantiate(loaded_config.arch)

    state_dict = checkpoint['state_dict']
    model.load_state_dict(state_dict)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    model.eval()
    return model


import os
import json

from draw_box import draw_labels
from inference import inference

#CROPPED_DIR = '/data/dataset/crop_valid'
#INPUT_DIR = '/data/dataset/valid'
#OUPUT_DIR = '/data/dataset/files_with_boxes'
#JSON_FILE = '/data/dataset/annotations/val_out_md.json'
#OUTPUT_JSON_FILE = '/data/dataset/annotations/delete.json'
#WEIGHTS = '/data/models/efficientnet_with_animals.pth'

def add_classification_label(js, path_to_label):
    with open(path_to_label, 'r', encoding='utf-8') as f:
        label = json.load(f)
    js['detection_categories'] = label

def create_draw_images(input_dir, cropped_dir, output_dir, json_file, output_json_file, weights, label_file):
    model = load_model(weights)
    with open(json_file, 'r', encoding='utf-8') as f:
        js = json.load(f)
        
    images = js['images']
    detector = js['info']['detector']

    if not Path(output_dir).exists():
        os.mkdir(output_dir)

    add_classification_label(js, label_file)
    labels = js['detection_categories']

    for image in tqdm(images):
        
        name = image['file']
        detections = image['detections']
        width = image['width']
        height = image['height']
        
        for i in range(len(detections)):
            detection = detections[i]
            if i < 10:
                str_i = f'0{i}'
            else:
                str_i = f'{i}'
            path = os.path.join(cropped_dir, f'{name}___crop{str_i}_{detector}.jpg')
            if not Path(path).exists():
                #print(path + " is not exists")
                continue

            animal = inference(path, model)
            detection['category'] = str(animal[1].item())
            detection['conf'] = str(animal[2])

        
        full_image_path = os.path.join(input_dir, name)
        draw_labels(full_image_path, detections, output_dir, labels, name, width, height)
            
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(js, fp=f, indent=2)  

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_dir',
        help = 'The path to the directory where the original photos are stored')
    parser.add_argument(
        'cropped_dir',
        help = 'The path to the directory where cropped photos are stored')
    parser.add_argument(
        'output_dir',
        help = 'The path to the directory where framed photos will be saved')
    parser.add_argument(
        'json_detector_file',
        help = 'The path to the MD format json file')
    parser.add_argument(
        'final_json_file',
        help = 'The path where the json file with the classification will be saved')
    parser.add_argument(
        'weights',
        help = 'The path to the weights of the model (Efficientnet)')
    parser.add_argument(
        'label',
        help = 'The path to the label with categories'
    )
    if len(sys.argv[1:]) != 7:
        parser.print_help()
        parser.exit()
        
    args = parser.parse_args()
    
    create_draw_images(args.input_dir, 
                       args.cropped_dir, 
                       args.output_dir, 
                       args.json_detector_file, 
                       args.final_json_file, 
                       args.weights,
                       args.label)
        
    
if __name__ == '__main__':
    main()