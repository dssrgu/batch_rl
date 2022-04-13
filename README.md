# offline_atari

Code to run REM with offline Atari data. This code is based on [REM](https://github.com/google-research/batch_rl).

## Installation

This installation procedure was tested in 4/4/2022.

### Setup Conda environment and intall tensorflow

1. Install latest Conda from https://www.anaconda.com/products/individual.

2. Run the following commands to create a new Conda environment and install Tensorflow:
```
conda create -n [ENV]
conda activate [ENV]
conda install -c conda-forge tensorflow==2.6.2 cudatoolkit==11.2
```

### Install packages

1. Install preliminary packages.

```
python -m pip install --upgrade pip
python -m pip install absl-py atari-py gin-config gym[atari,accept-rom-license] opencv-python
python -m pip install git+https://github.com/google/dopamine.git
```

## Reproducing results

To reproduce the results for an environment, run: 

```
python -um batch_rl.fixed_replay.train --env_name [ENV] --data_num [DATA_NUMBER]
```

This code was tested on 5 environments used in CQL: Asterix, Breakout, Qbert, Seaquest, and Pong.

Each environment contains 5 equally partitioned datasets, so you can set DATA_NUMBER between [1..5].

Experiment results are saved in ```./results``` folder.