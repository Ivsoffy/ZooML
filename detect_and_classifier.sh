#!/bin/bash

#initialize conda
source $ZOOPATH/../miniforge3/etc/profile.d/conda.sh
#initialize megadetector
export PYTHONPATH="$ZOOPATH/../MegaDetector:$ZOOPATH/../yolov5"


if [ "$#" == 2 ]
then
input_dir=$1
output_dir=$2
else
input_dir=$ZOOPATH/dataset/raw_images
output_dir=$ZOOPATH/dataset/output_images
fi 

#paths
path_json_detect_file=$ZOOPATH/dataset/annotations/raw_images_detect.json
path_final_json=$ZOOPATH/dataset/annotations/raw_images_classifier.json
logdir=$ZOOPATH/storage/logs/
crop_image_folder=$ZOOPATH/dataset/crop_images
weights=$ZOOPATH/models/efficientnet_with_animals.pth
path_to_label=$ZOOPATH/storage/TrapperAI_index.json

#envs
hydra_env=$ZOOPATH/../hydraenv/bin/activate

#python scripts
run_detector_batch=$ZOOPATH/../MegaDetector/megadetector/detection/run_detector_batch.py
crop_detections=$ZOOPATH/../MegaDetector/megadetector/classification/crop_detections.py
classifier=$ZOOPATH/hydra_classifier/classifier.py

#activate venv for megadetector
conda activate megadetector
#run megadetector
python3.8 $run_detector_batch MDV5A $input_dir $path_json_detect_file --output_relative_filenames --checkpoint_frequency 10000 --quiet --threshold 0.2 --include_image_size
#initialize for crops_detection.py
conda activate megaclassifier
#run crops detection
python3.9 $crop_detections -i $input_dir --save-full-images --square-crops -t 0.1 -n 6 --logdir $logdir $path_json_detect_file $crop_image_folder
conda deactivate
#activate venv for classifier
source $hydra_env
#run classifier
python3 $classifier $input_dir $crop_image_folder $output_dir $path_json_detect_file $path_final_json $weights $path_to_label