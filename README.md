# Offline Atari

Code to run REM and CQL with offline Atari data. This code is based on [REM](https://github.com/google-research/batch_rl) and [CQL](https://github.com/aviralkumar2907/CQL).

## Installation

This installation procedure was tested in 4/4/2022.

### Setup Conda environment and intall tensorflow

1. Install latest Conda from https://www.anaconda.com/products/individual.

2. Run the following commands to create a new Conda environment and install Tensorflow:
```
conda create -n [CONDA_ENV]
conda activate [CONDA_ENV]
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

### Run experiments

To reproduce the results for CQL or REM, run: 

```
python -um batch_rl.fixed_replay.train --env [ENV] --data_num [DATA_NUMBER] --method [METHOD] --replay_capacity [REPLAY_CAPACITY] --min_q_weight [MIN_Q_WEIGHT]
```

Descriptions:
```

--env:  environment name (Asterix, Breakout, Qbert, Seaquest, or Pong)

--data_num: dataset number (1 ~ 5)

--method: method name (cql or rem)

--replay_capacity: replay buffer capacity. arange this to train on a subset of the full data. 1000000 denotes the full data. Hence, 100000 ==> 10% data / 10000 ==> 1% data

--min_q_weight: Optional parameter for CQL. set to 1.0 for 10% data and 4.0 for 1% data.
```

This code was tested on 5 environments used in CQL: Asterix, Breakout, Qbert, Seaquest, and Pong, on 10% data (--replay_capacity 100000).

Each environment contains 5 equally partitioned datasets, so you can set DATA_NUMBER between [1..5].

Experiment results are saved in ```./results``` folder.


### Check with tensorboard

To visualize your runs with tensorboard, run:

```
python tensorboard.py
```
