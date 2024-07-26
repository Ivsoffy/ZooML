"""
#load model

from omegaconf import OmegaConf
from srcs.utils import instantiate
from efficientnet_pytorch import EfficientNet

checkpoint = torch.load('../../models/efficientnet_with_animals.pth')
loaded_config = OmegaConf.create(checkpoint['config'])

model = instantiate(loaded_config.arch)

state_dict = checkpoint['state_dict']
model.load_state_dict(state_dict)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()
"""
#inference
import torch
import numpy as np
import cv2


def inference(path, model):
    frame = cv2.imread(path)
    max_side = max(frame.shape[0:2])
    old_image_height, old_image_width, channels = frame.shape
    color = (255, 255, 255)

    padded = np.full((max_side, max_side, channels), color, dtype=np.uint8)
    padded[0:old_image_height,0:old_image_width] = frame

    image = cv2.resize(padded, (224, 224))
    image = cv2.resize(image, (224, 224))
    image = np.transpose(image, (2, 0, 1))
    image = torch.tensor(image).float()

    with torch.no_grad():
        predict = model(image.unsqueeze(0))
    predicted_conf = torch.nn.functional.softmax(predict, dim=-1).max(1)
    predicted_confs = torch.nn.functional.softmax(predict, dim=-1).cpu().numpy()
    classes = ['badger', 'bird', 'boar', 'brown_bear', 'deer', 'fox', 'hare', 'himalayan_bear', 'lynx', 'manul', 'marmot', 'raccoon_dog', 'snow_leopard', 'squirrel', 'weasel', 'wolf', 'wolverine']
    num_class = predicted_conf.indices[0]
    
    confidence = max(predicted_confs[0])
    predicted_class = classes[num_class]
    return (predicted_class, num_class, confidence)
