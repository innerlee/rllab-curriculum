#/bin/bash
cp ~/.mujoco/mjkey.txt ./mjpro131/bin/
cp ~/.mujoco/mjkey.txt ./vendor/mujoco/
# source activate cpu_rllab #rllab_goal_rl
source activate rllab_goal_rl
# python testArm3d.py

#10.23 
# python -m baselines.run --render  --ps _TfRunningMeanStd_ecoef0.01_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 6 --save_path ./result/1023Experiments \
# python -m baselines.run --render  --ps _TfRunningMeanStd_ecoef0.01_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 2 --save_path ./result/1023Experiments \
python -m baselines.run --render  --ps _TfRunningMeanStd_ecoef0.00_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 2 --save_path ./result/1023Experiments \

#play
# play will meet wrong when the load_num_env is not equal with num_env
# so if you want to play, please set the load_num_env and num_env same, and make num_timesteps
python -m baselines.run --num_env_play 2  --play --render  --ps _TfRunningMeanStd_ecoef0.01_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=0 --seed 0 --num_env 2 --save_path ./result/test/2 \
--load_num_env 6 --load_path ./result/1022Experiments --load_num 02400 

#10.22
# python -m baselines.run --num_env_play 2  --play --record  --ps _TfRunningMeanStd_ecoef0.01_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 6 --save_path ./result/test
# python -m baselines.run --num_env_play 1  --play --record  --ps _TfRunningMeanStd_ecoef0.00  --stepNumMax 1111 --env arm3d_task2 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 3 --save_path ./result/1022Experiments
# SET ENV
# python -m baselines.run --num_env_play 3  --play --record  --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=4e7 --seed 0 --num_env 9 --save_path ./result/1022Experiments

# change load_path and add load_num
# change load_num_env for the loaded model not the new model
#10.19
# python -m baselines.run \
# --stepNumMax 1111 --env arm3d_task1  --reward_scale 1 --normalize \
# --seed 0 --num_env 2 --save_path ./result/test \
# --num_env_play 2  --play --render \
# --alg=ppo2 --network=mlp --num_timesteps=1 \
# --ps _TfRunningMeanStd_ecoef0.00 #--render 
# --load_num_env 1 --load_path ./result/1019Experiments --load_num 03900 \

# python -m baselines.run --render --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 9 --save_path ./result/1019Experiments
# python -m baselines.run --render --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 9 --save_path ./result/1019Experiments
# python -m baselines.run --render --ps _TfRunningMeanStd_ecoef0.01_removeTotalTask  --stepNumMax 1111 --env arm3d_task12 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 6 --save_path ./result/1019Experiments
# python -m baselines.run --render --ps _TfRunningMeanStd_ecoef0.00  --stepNumMax 1111 --env arm3d_task2 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 3 --save_path ./result/1019Experiments

# 10.18
# python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01 --sparse1_dis 0.3 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1018Experiments  
# python -m baselines.run --load_num_env 2 --render --load_path 01700 --ps _TfRunningMeanStd_ecoef0.01 --sparse1_dis 0.2 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1018Experiments  
# python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01 --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Exp1018Experimentseriments  
# python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1500 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1018Experiments 

# 10.17
# set ent_coef
    # python -m baselines.run --load_num_env 2 --render --load_path 03900 --ps _TfRunningMeanStd_ecoef0.00  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 2 --save_path ./result/test 
    # ## sparse
        # python -m baselines.run --load_num_env 2 --render --load_path 03900  --ps _TfRunningMeanStd_ecoef0.00 --sparse1_dis 1 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
        # python -m baselines.run --load_num_env 2 --render --load_path 01650 --ps _TfRunningMeanStd_ecoef0.01 --sparse1_dis 1 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
        # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.00 --sparse1_dis 0.7 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
        # python -m baselines.run --load_num_env 2 --render --load_path 01400 --ps _TfRunningMeanStd_ecoef0.00 --sparse1_dis 0.5 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
        # python -m baselines.run --load_num_env 2s --load_path 00250 --render --ps _TfRunningMeanStd_ecoef0.00 --sparse1_dis 0.3 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
    # ## dense baseline
    # python -m baselines.run --load_num_env 2 --render --load_path 03850 --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments 
    # ## for less steps
        # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 900 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments   
        # python -m baselines.run --load_num_env 2 --render --load_path 03700 --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 700 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments   
        # python -m baselines.run baselines.run --load_num_env 2 --render --load_path 03900 --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 500 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments   
    # # test 2 env
        # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 2 --save_path ./result/1017Experiments 
    # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.03  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
    # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.05  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
    # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.07  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
    # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.1  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  
    # python -m baselines.run --ps _TfRunningMeanStd_ecoef0.3  --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e9 --seed 0 --num_env 16 --save_path ./result/1017Experiments  

#play
# python -m baselines.run --ps _TfRunningMeanStd_test maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  
# python -m baselines.run --load_path 00600 --render --ps _TfRunningMeanStd --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  
# 10.16 after meeting
# set noReNor
# python -m baselines.run --ps _TfRunningMeanStd_noReNor --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task2 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016Experiments_2  
# GPU 0
# python -m baselines.run --ps _TfRunningMeanStd_noReNor maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  
# # restore noReNor
# GPU 1
# python -m baselines.run --ps _TfRunningMeanStd maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  
# # set ent_coef
# GPU 2
# python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  
# python -m baselines.run --ps _TfRunningMeanStd_ecoef0.01 --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task2 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016Experiments_2  
# # restore ent_coef
# GPU 3
# python -m baselines.run --ps _TfRunningMeanStd --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task1 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 16 --save_path ./result/1016Experiments_2  

# 10.16-test
# python -m baselines.run --ps _TfRunningMeanStd --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task2 --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016test  

# 10.16-1
# recurrent sparse1 task2
# python -m baselines.run --sparse1_dis 0.1 maxSteps --stepNumMax 1111 --env arm3d_task2  --render --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016Experiments_1  
# python -m baselines.run --sparse1_dis 0.05 maxSteps --stepNumMax 1111 --env arm3d_task2  --render --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/test  

# recurrent task12
# python -m baselines.run --sparse1_dis 0.05 maxSteps --stepNumMax 1111 --env arm3d_task12  --render --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016Experiments_1  
# python -m baselines.run --sparse1_dis 0.1maxSteps --stepNumMax 1111 --env arm3d_task12  --render --normalize --reward_scale 1 --rewardModeForArm3d sparse1 --alg=ppo2 --network=mlp --num_timesteps=2e7 --seed 0 --num_env 2 --save_path ./result/1016Experiments_1  
#_NoReNormalizing
# _maxSteps_300 