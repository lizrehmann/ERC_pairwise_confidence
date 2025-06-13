#!/bin/bash
#SBATCH --job-name=conf_pair_job
#SBATCH --ntasks-per-node=24
#SBATCH --time=24:0:0
#SBATCH --output=conf_pair_job.out
#SBATCH --error=conf_pair_job.err
#SBATCH --mail-user=rehmanne@oregonstate.edu
#SBATCH --mail-type=END

#sbatch -p forsythe.q -A forsythe conf_pair_job.sh

python /scratch/rehmanne/ERC_pairwise_confidence/ERC_pairwise_confidence/confidence_pair.py