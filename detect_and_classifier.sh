#!/bin/bash

#initialize conda
source data/storage/miniforge/etc/profile.d/conda.sh #надо чето переделать
#initialize megadetector
export PYTHONPATH="$HOME/MegaDetector:$HOME/mega/yolov5"

#paths
path_input_dir=dataset/raw_images
path_json_detect_file=dataset/annotations/raw_images_detect.json
path_final_json=dataset/annotations/raw_images_classifier.json
logdir=storage/logs/
crop_image_folder=dataset/crop_images
output_dir=dataset/output_images
weights=models/efficientnet_with_animals.pth
path_to_label=storage/TrapperAI_index.json
#envs
hydra_env=../hydraenv/bin/activate
#python scripts
run_detector_batch=../MegaDetector/megadetector/detection/run_detector_batch.py
crop_detections=../MegaDetector/megadetector/classification/crop_detections.py
classifier=hydra_classifier/classifier.py

#activate venv for megadetector
conda activate cameratraps-detector
#run megadetector
python3.8 $run_detector_batch MDV5A $path_input_dir $path_json_detect_file --output_relative_filenames --checkpoint_frequency 10000 --quiet --threshold 0.2 --include_image_size
#initialize for crops_detection.py
conda activate cameratraps-classifier
#run crops detection
python3.9 $crop_detections -i $path_input_dir --save-full-images --square-crops -t 0.1 -n 6 --logdir $logdir $path_json_detect_file $crop_image_folder
conda deactivate
#activate venv for classifier
source $hydra_env
#run classifier
python3 $classifier $path_input_dir $crop_image_folder $output_dir $path_json_detect_file $path_final_json $weights $path_to_label



