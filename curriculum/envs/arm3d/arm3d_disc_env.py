import random

import numpy as np

from rllab.core.serializable import Serializable
from rllab.envs.base import Step
from rllab.envs.mujoco.mujoco_env import MujocoEnv
from rllab.misc import autoargs
from rllab.misc import logger
from rllab.spaces.box import Box
from rllab.misc.overrides import overrides
from contextlib import contextmanager
from gym.utils import seeding
import pickle

class Arm3dDiscEnvllx(MujocoEnv, Serializable):
    FILE = "arm3d_disc.xml"
    # FILE = "arm3d_disc_test.xml"

    def __init__(self,envIdLLX=None,
                 init_solved=True,
                 kill_radius=0.4,
                 stepNumMax = 300,
                 sparse1_dis=0.1,
                 task2InitNoise=False,
                 *args, **kwargs):
        MujocoEnv.__init__(self, *args, **kwargs)

        Serializable.quick_init(self, locals())

        # self.init_qvel = np.zeros_like(self.init_qvel)
        # self.init_qacc = np.zeros_like(self.init_qacc)
        self.init_solved = init_solved
        self.kill_radius = kill_radius
        self.kill_outside = False
        self.envIdLLX = envIdLLX
        self.goalPostitionTask1 = None
        self.stepNumMax = stepNumMax #1111
        self.sparse1_dis=sparse1_dis
        self.task2InitNoise = task2InitNoise

    @overrides
    def get_current_obs(self):
        return np.concatenate([
            self.model.data.qpos.flat, #[:self.model.nq // 2],
            self.model.data.qvel.flat, #[:self.model.nq // 2],
            self.model.data.site_xpos[0], # disc position
        ])

    @contextmanager
    def set_kill_outside(self, kill_outside=True, radius=None):
        self.kill_outside = True
        old_kill_radius = self.kill_radius
        if radius is not None:
            self.kill_radius = radius
        try:
            yield
        finally:
            self.kill_outside = False
            self.kill_radius = old_kill_radius

    @property
    def start_observation(self):
        return np.copy(self.model.data.qpos).flatten()

    def reset(self, init_state=None, *args, **kwargs):
        # init_state = (0.387, 1.137, -2.028, -1.744, 2.029, -0.873, 1.55, 0, 0) # TODO: used for debugging only!
        # @llx-noise
        if init_state and self.task2InitNoise:
            init_state  += np.random.uniform(0,self.task2InitNoise,len(init_state))
            # print('add noise to task2'+str(self.task2InitNoise))
        ret = super(Arm3dDiscEnvllx, self).reset(init_state, *args, **kwargs)
        self.stepsNum = 0
        # self.current_goal = self.model.data.geom_xpos[-1][:2]
        # print(self.current_goal) # I think this is the location of the peg
        return ret

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # print(action.shape)
        done = False
        self.stepsNum +=1
        self.forward_dynamics(action)
        # @llx reward
        distance_to_goal = self.get_distance_to_goal()
        if self.rewardMode == 'sparse1':
            #0.005
            if distance_to_goal < self.sparse1_dis:
                done = True
                reward =  1
            else: reward = 0
        elif self.rewardMode == 'sparse2':
            # Difficlut to design the reward
            relativePosition = self.get_disc_position() - self.get_goal_position()
            # way 1
            if abs(relativePosition[0]) < 0.01 and  \
                abs(relativePosition[1]) < 0.01 and \
                    abs(relativePosition[2]) < 0.1:
                    done = True
                    reward =  1
            else: reward =  0
        else:
            reward = -distance_to_goal#*0.01


        # if distance_to_goal < 0.03:
        #     print("inside the PR2DiscEnv, the dist is: {}, goal_pos is: {}".format(distance_to_goal, self.get_goal_position()))
            # print("Qpos: " + str(self.model.data.qpos))

        ob = self.get_current_obs()
        # print(ob)
        # @llx move to the top
        # done = False

        if self.kill_outside and (distance_to_goal > self.kill_radius):
            print("******** OUT of region ********")
            done = True
        elif self.stepsNum>self.stepNumMax:
            done = True

        return Step(
            ob, reward, done,
        )


    def get_disc_position(self):
        return self.model.data.site_xpos[0]

    def get_goal_position(self):
        return self.model.data.site_xpos[1]
        # return self.model.data.xpos[-1] + np.array([0, 0, 0.05]) # this allows position to be changed todo: check this

    def get_vec_to_goal(self):
        disc_pos = self.get_disc_position()
        # @llx reward
        if self.envIdLLX == 1:
            return disc_pos - self.goalPostitionTask1
        else:
            return disc_pos - self.get_goal_position()

    def get_distance_to_goal(self):
        vec_to_goal = self.get_vec_to_goal()
        return np.linalg.norm(vec_to_goal)


    def set_state(self, qpos, qvel):
        #assert qpos.shape == (self.model.nq, 1) and qvel.shape == (self.model.nv, 1)
        self.model.data.qpos = qpos
        self.model.data.qvel = qvel
        # self.model._compute_subtree() #pylint: disable=W0212
        self.model.forward()


class Arm3dDiscEnv(MujocoEnv, Serializable):
    FILE = "arm3d_disc.xml"
    # FILE = "arm3d_disc_test.xml"

    def __init__(self,
                 init_solved=True,
                 kill_radius=0.4,
                 *args, **kwargs):
        MujocoEnv.__init__(self, *args, **kwargs)
        Serializable.quick_init(self, locals())

        # self.init_qvel = np.zeros_like(self.init_qvel)
        # self.init_qacc = np.zeros_like(self.init_qacc)
        self.init_solved = init_solved
        self.kill_radius = kill_radius
        self.kill_outside = False
        # print("yo!")

    @overrides
    def get_current_obs(self):
        return np.concatenate([
            self.model.data.qpos.flat, #[:self.model.nq // 2],
            self.model.data.qvel.flat, #[:self.model.nq // 2],
            self.model.data.site_xpos[0], # disc position
        ])

    @contextmanager
    def set_kill_outside(self, kill_outside=True, radius=None):
        self.kill_outside = True
        old_kill_radius = self.kill_radius
        if radius is not None:
            self.kill_radius = radius
        try:
            yield
        finally:
            self.kill_outside = False
            self.kill_radius = old_kill_radius

    @property
    def start_observation(self):
        return np.copy(self.model.data.qpos).flatten()

    def reset(self, init_state=None, *args, **kwargs):
        # init_state = (0.387, 1.137, -2.028, -1.744, 2.029, -0.873, 1.55, 0, 0) # TODO: used for debugging only!
        ret = super(Arm3dDiscEnv, self).reset(init_state, *args, **kwargs)
        # self.current_goal = self.model.data.geom_xpos[-1][:2]
        # print(self.current_goal) # I think this is the location of the peg
        return ret

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # print(action.shape)
        self.forward_dynamics(action)
        # @llx reward
        # distance_to_goal = self.get_distance_to_goal()
        # reward = -distance_to_goal
        # Difficlut to design the reward
         # @llx reward
        distance_to_goal = self.get_distance_to_goal()
        reward = -distance_to_goal


        # print(self.model.data.site_xpos[1])
        # print(self.model.data.qpos[-2:])

        # if distance_to_goal < 0.03:
        #     print("inside the PR2DiscEnv, the dist is: {}, goal_pos is: {}".format(distance_to_goal, self.get_goal_position()))
            # print("Qpos: " + str(self.model.data.qpos))

        ob = self.get_current_obs()
        # print(ob)
        done = False

        if self.kill_outside and (distance_to_goal > self.kill_radius):
            print("******** OUT of region ********")
            done = True

        return Step(
            ob, reward, done,
        )


    def get_disc_position(self):
        return self.model.data.site_xpos[0]

    def get_goal_position(self):
        return self.model.data.site_xpos[1]
        # return self.model.data.xpos[-1] + np.array([0, 0, 0.05]) # this allows position to be changed todo: check this

    def get_vec_to_goal(self):
        disc_pos = self.get_disc_position()
        goal_pos = self.get_goal_position()
        return disc_pos - goal_pos # note: great place for breakpoint!

    def get_distance_to_goal(self):
        vec_to_goal = self.get_vec_to_goal()
        return np.linalg.norm(vec_to_goal)


    def set_state(self, qpos, qvel):
        #assert qpos.shape == (self.model.nq, 1) and qvel.shape == (self.model.nv, 1)
        self.model.data.qpos = qpos
        self.model.data.qvel = qvel
        # self.model._compute_subtree() #pylint: disable=W0212
        self.model.forward()

    # def is_feasible(self, goal):
    #     return np.all(np.logical_and(self.goal_lb <= goal, goal <= self.goal_ub))
    #
    # @property
    # def goal_lb(self):
    #     return self.model.jnt_range[:self.model.nq // 2, 0]
    #
    # @property
    # def goal_ub(self):
    #     return self.model.jnt_range[:self.model.nq // 2, 1]
    #
    # @property
    # def goal_dim(self):
    #     return self.model.njnt // 2
