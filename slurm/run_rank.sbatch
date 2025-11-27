#!/bin/bash
#SBATCH --job-name=rank_test
#SBATCH --output=rank_test_%j.out
#SBATCH --error=rank_test_%j.err
#SBATCH --ntasks=6             # nombre de processus (un par CPU)
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00        # temps max
#SBATCH --partition=debug      # ta partition
#SBATCH --nodes=1


# Afficher info sur le job
echo "SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"
echo "SLURM_NTASKS: $SLURM_NTASKS"
echo "SLURM_PROCID: $SLURM_PROCID"
echo "SLURM_LOCALID: $SLURM_LOCALID"


# Lancer le script Python avec torch.distributed (CPU backend)
srun bash -c ' 
docker run --rm --gpus all \
    -v /home/jef/repositories/mixsim3d_gretsi/:/mixsim3d \
    -e PYTHONPATH=/mixsim3d \
    -e MASTER_ADDR=rank_0 \
    -e MASTER_PORT=12345 \
    -e BACKEND='gloo' \
    -e SLURM_PROCID \
    -e SLURM_NTASKS \
    --name=rank_${SLURM_PROCID} --network ranknet \
    drp3d:cuda12.6 python3 -u /mixsim3d/tests/rank.py
'