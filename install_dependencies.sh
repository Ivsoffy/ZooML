#!/bin/bash

#install conda
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

#create virtual environment for classifier
pip install -r /content/ZooML/hydra_classifier/requirements.txt

#clone megadetector
git clone https://github.com/agentmorris/MegaDetector
git clone https://github.com/ecologize/yolov5

#create virtual environment for megadetector
source /content/miniforge3/etc/profile.d/conda.sh
conda env create --file /content/MegaDetector/envs/environment-detector.yml
conda env create --file /content/MegaDetector/envs/environment-classifier.yml

