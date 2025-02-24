# coding=utf-8
# Copyright 2021 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""The entry point for running experiments with fixed replay datasets.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools
import json
import os
import datetime



from absl import app
from absl import flags
from batch_rl.fixed_replay import run_experiment
from batch_rl.fixed_replay.agents import dqn_agent
from batch_rl.fixed_replay.agents import multi_head_dqn_agent
from batch_rl.fixed_replay.agents import quantile_agent
from batch_rl.fixed_replay.agents import rainbow_agent
from dopamine.discrete_domains import run_experiment as base_run_experiment
from dopamine.discrete_domains import train as base_train  # pylint: disable=unused-import
import tensorflow.compat.v1 as tf

flags.DEFINE_string('env', 'Pong', 'Name of the environment.')
flags.DEFINE_string('method', 'cql', 'Name of the method (e.g. cql, rem).')
flags.DEFINE_integer('data_num', 1, 'Dataset number (1..5).')
flags.DEFINE_integer('replay_capacity', 1000000, 'replay buffer capacity. set to 1000000 for full data. 100000 for 10% data. 10000 for 1% data.')
flags.DEFINE_float('min_q_weight', 1.0, 'min_q_weight for CQl. set to 1.0 for 10% data and 4.0 for 1% data.')
flags.DEFINE_string('agent', 'multi_head_dqn', 'Name of the agent.')
flags.DEFINE_string('replay_dir', None, 'Directory from which to load the replay data (to be set automatically)')
flags.DEFINE_string('init_checkpoint_dir', None, 'Directory from which to load '
                    'the initial checkpoint before training starts.')


FLAGS = flags.FLAGS



def create_agent(sess, environment, replay_data_dir, summary_writer=None):
  """Creates a DQN agent.

  Args:
    sess: A `tf.Session`object  for running associated ops.
    environment: An Atari 2600 environment.
    replay_data_dir: Directory to which log the replay buffers periodically.
    summary_writer: A Tensorflow summary writer to pass to the agent
      for in-agent training statistics in Tensorboard.

  Returns:
    A DQN agent with metrics.
  """
  if FLAGS.agent == 'dqn':
    agent = dqn_agent.FixedReplayDQNAgent
  elif FLAGS.agent == 'c51':
    agent = rainbow_agent.FixedReplayRainbowAgent
  elif FLAGS.agent == 'quantile':
    agent = quantile_agent.FixedReplayQuantileAgent
  elif FLAGS.agent == 'multi_head_dqn':
    agent = multi_head_dqn_agent.FixedReplayMultiHeadDQNAgent
  else:
    raise ValueError('{} is not a valid agent name'.format(FLAGS.agent))

  return agent(sess, num_actions=environment.action_space.n,
               replay_data_dir=replay_data_dir, summary_writer=summary_writer,
               init_checkpoint_dir=FLAGS.init_checkpoint_dir)




def main(unused_argv):
  # update flags
  FLAGS.method = FLAGS.method.lower()
  if FLAGS.method == 'rem':
    FLAGS.gin_files = ['batch_rl/fixed_replay/configs/rem.gin']
    FLAGS.agent = 'multi_head_dqn'
  elif FLAGS.method == 'cql':
    FLAGS.gin_files = ['batch_rl/fixed_replay/configs/cql.gin']
    FLAGS.gin_bindings.append(f'FixedReplayQuantileAgent.min_q_weight = {FLAGS.min_q_weight}')
    FLAGS.agent = 'quantile'
  else:
    raise NotImplementedError
  FLAGS.base_dir = os.path.join(
    './results',
    f'{FLAGS.env}_{FLAGS.data_num}_{FLAGS.method}_' +  datetime.datetime.utcnow().strftime('run_%Y_%m_%d_%H_%M_%S')
  )
  FLAGS.replay_dir = f'/data_large/readonly/atari/{FLAGS.env}/{FLAGS.data_num}'
  FLAGS.gin_bindings.append(f'atari_lib.create_atari_environment.game_name = "{FLAGS.env}"')
  FLAGS.gin_bindings.append(f'WrappedFixedReplayBuffer.replay_capacity = {FLAGS.replay_capacity}')
  # do not update flags after this!

  tf.logging.set_verbosity(tf.logging.INFO)
  base_run_experiment.load_gin_configs(FLAGS.gin_files, FLAGS.gin_bindings)
  replay_data_dir = os.path.join(FLAGS.replay_dir, 'replay_logs')
  create_agent_fn = functools.partial(
      create_agent, replay_data_dir=replay_data_dir)
  runner = run_experiment.FixedReplayRunner(FLAGS.base_dir, create_agent_fn)
  runner.run_experiment()


if __name__ == '__main__':
  app.run(main)
