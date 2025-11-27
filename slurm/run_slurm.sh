#!/bin/bash
#SBATCH -N 2
#SBATCH -n 8
#SBATCH --ntasks-per-node=4
#SBATCH -J Python_drp3d
#SBATCH --exclusive
#SBATCH -p gpgpu
#SBATCH --gres=gpu:4
#SBATCH --wckey=xgk15001
#SBATCH --time=00:30:00
#SBATCH --output=log.%j.out
#SBATCH --error=error.%j.err

HOME=${WORK}/lecomtje
SIF_IMAGE=${HOME}/drp3d.sif

# Passe les variables Slurm nécessaires à Apptainer

export NCCL_DEBUG=INFO
export NCCL_IB_DISABLE=1
export NCCL_P2P_DISABLE=1


srun apptainer exec --nv \
    --env PYTHONPATH=/mixsim3d \
    -B ${HOME}/mixsim3d:/mixsim3d \
    ${SIF_IMAGE} \
    python3 -u /mixsim3d/tests/rank.py
