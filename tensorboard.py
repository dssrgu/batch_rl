import os

from slurm_launcher.sbatch_launcher import srun_gpuless_task

TENSORBOARD_DIR = os.path.dirname(os.path.abspath(__file__))+'/results/'


def run_tensorboard():
    srun_gpuless_task(
            cmd=r"""bash -c 'tensorboard --host=$(hostname).mllab.snu.ac.kr --port=0 --logdir={}'""".format(TENSORBOARD_DIR),
            partition='dept,titan,rtx2080,rtx3090',
            job_name='tensorboard',
    )

if __name__=='__main__':
    run_tensorboard()


