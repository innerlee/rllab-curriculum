# coding=utf-8
import time
import numpy as np
np.random.seed(0)
# Arm3dKeyEnv 的 render has nothing excluding black and white
from curriculum.envs.arm3d.arm3d_key_env import Arm3dKeyEnv

from curriculum.envs.arm3d.arm3d_move_peg_env import Arm3dMovePegEnv
from curriculum.envs.arm3d.arm3d_disc_env import Arm3dDiscEnv,Arm3dDiscEnvllx

import pickle
from copy import deepcopy
from curriculum.envs.start_env import generate_starts
from rllab.misc.instrument import VariantGenerator
# daxiaobi he shenti titiaoxian 
# 1　身体的扭动
# 2 dabi shangxia + shang - xia
# 4 xiaobi shangxia + xia - shang
# 3 shouwan niu dong + qian - hou
# 3+4 xiaobi qianhou -- qian
# 5 zhengshitu tiaozhengshouwan 
# 7 youshitu tiaozheng shouwan
# 6 niudong zuo you
# 6 shouwan niu dong + shang - xia  

start_goal = [0.56, 0.5, -1.5, -1.74429440, -0.6, -0.9, 1.75]
#start_goal = [0, 0, 0, -1.74429440, 0, 0, 0]
# start_goal = [0.386884635, 1.13705218, -2.02754147, -1.74429440, 2.02916096, -0.873269847, 1.54785694]


# blackground is black
# action is for the cylinder on the table
# env = Arm3dMovePegEnv()
# for i in range(100000):
#     env.step( np.random.rand(2) )
#     env.render()

tmp_env = Arm3dDiscEnv()
import numpy as np
for j in range(100):
    import pdb; pdb.set_trace()
    tmp_env.reset(init_state=start_goal+np.random.uniform(0,0.3,len(start_goal)))
    for i in range(20):
        tmp_env.render()

env =  Arm3dDiscEnvllx(stepNumMax=1000,sparse1_dis=0.01)
env.rewardMode = ''
tmp_env = Arm3dDiscEnv()
tmp_env.reset(init_state=start_goal)
print(env.get_distance_to_goal())

env =  Arm3dDiscEnvllx(envIdLLX=1,stepNumMax=1000,sparse1_dis=0.01)
env.goalPostitionTask1 = np.asarray(tmp_env.get_disc_position())
print(env.get_distance_to_goal())
import pdb; pdb.set_trace()


# blackground is white
# action is for the robot behind the table
# env = Arm3dDiscEnvllx(envIdLLX=1)
env = Arm3dDiscEnv()
# env.seed(0)
# env.reset()
# env.llx='test'

# with env.set_kill_outside():
# #import pdb; pdb.set_trace()
env.reset(init_state=start_goal)
# seed_starts = generate_starts(env, starts=[vv['start_goal']], horizon=10,  # this is smaller as they are seeds!
#                                     variance=vv['brownian_variance'], subsample=vv['num_new_starts'])  # , animated=True, speedup=1)

print(env.get_disc_position())
# [ 0.00249257  0.29855902 -0.14545976]
print(env.get_goal_position())
# [ 0.   0.3 -0.4]
env.goalPostitim = env.get_disc_position()
print(env.get_distance_to_goal())
#0.254556521293

# for i in range(150000):
#     i += 1
#     # import pdb; pdb.set_trace()
#     # obs = env.step( np.random.rand(7) )
#     # print(env.step(np.zeros(7))[1])
    
#     env.render()
# with open('test.pkl', 'wb') as f:
#     pickle.dump(env, f)
# print('save env ok')

# # env3 = deepcopy(env)

# with open('test.pkl', 'rb') as f:
#     env2 = pickle.load(f)
# for i in range(1000):
#     # env.step( np.random.rand(7) )
#     env2.render()
