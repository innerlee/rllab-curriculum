"""
Test whatever you want here
"""

import logging
import os,sys
import numpy as np
import itertools

from rllab.envs.sliding_mem_env import SlidingMemEnv
from sandbox.pchen.dqn.envs.atari import AtariEnvCX

sys.path.append('.')

from sandbox.pchen.async_rl.async_rl.agents.a3c_agent import A3CAgent
from sandbox.pchen.async_rl.async_rl.agents.dqn_agent import DQNAgent, Bellman
from sandbox.pchen.async_rl.async_rl.algos.a3c_ale import A3CALE
from sandbox.pchen.async_rl.async_rl.algos.dqn_ale import DQNALE
from sandbox.pchen.async_rl.async_rl.utils.get_time_stamp import get_time_stamp
from sandbox.pchen.async_rl.async_rl.utils.ec2_instance import instance_info, subnet_info
from sandbox.pchen.async_rl.async_rl.bonus_evaluators.ale_hashing_bonus_evaluator import ALEHashingBonusEvaluator
from sandbox.pchen.async_rl.async_rl.preprocessor.image_vectorize_preprocessor import ImageVectorizePreprocessor
from sandbox.pchen.async_rl.async_rl.hash.sim_hash import SimHash

from rllab.misc import logger
from rllab.misc.instrument import run_experiment_lite, stub
from rllab import config

stub(globals())
from rllab.misc.instrument import VariantGenerator, variant

class VG(VariantGenerator):
    @variant
    def seed(self):
        return [42, 2222, 333333333333333]

    @variant
    def total_t(self):
        return [7 * 3*10**6]

    @variant
    def n_processes(self):
        return [18, 9]

    # @variant
    # def entropy_bonus(self):
    #     return [0.01]

    @variant
    def target_update_frequency(self):
        yield 40000

    @variant
    def eps_test(self):
        yield 0.01

    @variant
    def eval_frequency(self, target_update_frequency):
        # yield target_update_frequency * 1
        yield target_update_frequency * 7

    @variant
    def game(self, ):
        # return ["pong", "beam_rider", "breakout", "qbert", "space_invaders"]
        return ["pong", "breakout", ]

    @variant
    def n_step(self, ):
        return [5,]

    @variant
    def share_model(self, n_step):
        return [n_step == 1]

    @variant
    def bellman(self, ):
        # return ["q"]
        return [Bellman.sarsa]

vg = VG()
variants = vg.variants(randomized=False)

print(len(variants))

for v in variants[:]:
    locals().update(v)

    # Problem setting
    eval_n_runs = 15

    # The meat ---------------------------------------------
    # env = AtariEnv(
    #     rom_filename=os.path.join(rom_dir,game+".bin"),
    #     plot=plot,
    #     record_ram=record_ram,
    # )
    env = AtariEnvCX(
        game=game,
        obs_type="image"
    )
    env = SlidingMemEnv(env)

    agent = DQNAgent(
        # n_actions=env.number_of_actions,
        env=env,
        target_update_frequency=target_update_frequency,
        eps_test=eps_test,
        t_max=n_step,
        share_model=share_model,
    )
    algo = DQNALE(
        total_steps=total_t,
        n_processes=n_processes,
        env=env,
        agent=agent,
        eval_frequency=eval_frequency,
        eval_n_runs=eval_n_runs,
    )

    # sys stuff
    comp_cores = int(18 / n_processes)
    config.ENV = dict(
        MKL_NUM_THREADS=comp_cores,
        NUMEXPR_NUM_THREADS=comp_cores,
        OMP_NUM_THREADS=comp_cores,
    )
    run_experiment_lite(
        algo.train(),
        exp_prefix="0914_n_step_dqn_sarsa_fixed",
        seed=v["seed"],
        variant=v,
        # mode="local",
        #
        # mode="local_docker",

        mode="lab_kube",
        n_parallel=0,
        use_gpu=False,
        node_selector={
            "aws/type": "c4.8xlarge",
        },
        resources=dict(
            requests=dict(
                cpu=17.1,
            ),
            limits=dict(
                cpu=17.1,
            )
        )
    )

