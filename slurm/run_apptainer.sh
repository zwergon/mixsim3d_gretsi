#!/bin/bash

HOME=${WORK}/lecomtje

SIF_IMAGE=${HOME}/drp3d.sif
apptainer exec \
    --env PYTHONPATH=${HOME}/mixsim3d \
    --env PYTORCH_DIST_USE_IPV6=0 \
    -B /network/r11pocdrp/data/heatmap:/dataset \
    ${SIF_IMAGE} \
    "$@"
