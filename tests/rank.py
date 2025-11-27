import os
import socket
import torch
import torch.distributed as dist
from drp.utils.hostlist import expand_hostlist

def main():
    
   
    # Récupère les variables Slurm
    rank = int(os.environ['SLURM_PROCID'])  # Rank local sur le nœud
    world_size = int(os.environ['SLURM_NTASKS'])  # Nombre total de processus


    if rank == 0:
        for k,v in os.environ.items():
            if "SLURM" in k or 'NCCL' in k:
                print(k, v)

    # Adresse IP du nœud maître (premier nœud de la liste)
    master_addr = os.environ['MASTER_ADDR']
    master_port = os.environ['MASTER_PORT']
    backend = os.environ['BACKEND']
    # Initialise le backend distribué (NCCL pour GPU, GLOO pour CPU)
     
    init_str = f'tcp://{os.environ["MASTER_ADDR"]}:{os.environ["MASTER_PORT"]}'

    print(f"Rank {rank} attempting to connect to {init_str}", flush=True)

    dist.init_process_group(
        backend=backend,  # ou 'gloo' pour CPU
        init_method=init_str,
        rank=rank,
        world_size=world_size
    )

    # Exemple d'utilisation du rank
    print(f"Hello from rank {rank} of {world_size}")

    # Ton code distribué ici...
    dist.barrier()  # Synchronisation

if __name__ == "__main__":
    main()
