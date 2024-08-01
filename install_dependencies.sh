#!/bin/bash

#install conda
cd ..
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh

#create virtual environment for classifier
python3 -m venv hydraenv
source hydraenv/bin/activate
pip install -r ZooML/hydra_classifier/requirements.txt
deactivate

#clone megadetector
git clone https://github.com/agentmorris/MegaDetector
git clone https://github.com/ecologize/yolov5
cd MegaDetector

#create virtual environment for megadetector
source $ZOOML/../miniforge3/etc/profile.d/conda.sh
conda env create --file envs/environment-detector.yml
conda env create --file envs/environment-classifier.yml

