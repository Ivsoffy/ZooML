#!/bin/bash

#install megadetector
cd ..
python3 -m venv hydraenv
source hydraenv/bin/activate
pip install -r ZooML/hydra_classifier/requirements.txt
deactivate
git clone https://github.com/agentmorris/MegaDetector
git clone https://github.com/ecologize/yolov5
cd MegaDetector
conda env create --file envs/environment-detector.yml
conda env create --file envs/environment-classifier.yml

