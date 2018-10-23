import os
import random

os.environ['THEANO_FLAGS'] = 'floatX=float32,device=cpu'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import argparse
import sys
from multiprocessing import cpu_count
from rllab.misc.instrument import run_experiment_lite
from rllab.misc.instrument import VariantGenerator
from rllab import config

from curriculum.experiments.starts.arm3d.arm3d_key.arm3d_key_brownian_algo import run_task

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--ec2', '-e', action='store_true', default=False, help="add flag to run in ec2")
    parser.add_argument('--clone', '-c', action='store_true', default=False,
                        help="add flag to copy file and checkout current")
    parser.add_argument('--local_docker', '-d', action='store_true', default=False,
                        help="add flag to run in local dock")
    parser.add_argument('--type', '-t', type=str, default='', help='set instance type')
    parser.add_argument('--price', '-p', type=str, default='', help='set betting price')
    parser.add_argument('--subnet', '-sn', type=str, default='', help='set subnet like us-west-1a')
    parser.add_argument('--name', '-n', type=str, default='', help='set exp prefix name and new file name')
    parser.add_argument('--debug', action='store_true', default=False, help="run code without multiprocessing")
    args = parser.parse_args()

    # setup ec2
    subnets = [
        'ap-south-1a', 'ap-south-1b', 'ap-southeast-1a', 'ap-southeast-1b'
    ]
    ec2_instance = args.type if args.type else 'm4.10xlarge'
    # configure instan
    info = config.INSTANCE_TYPE_INFO[ec2_instance]
    config.AWS_INSTANCE_TYPE = ec2_instance
    config.AWS_SPOT_PRICE = str(info["price"])
    n_parallel = int(info["vCPU"] / 2)  # make the default 4 if not using ec2
    if args.ec2:
        mode = 'ec2'
    elif args.local_docker:
        mode = 'local_docker'
        n_parallel = cpu_count() if not args.debug else 1
    else:
        mode = 'local'
        n_parallel = cpu_count() if not args.debug else 1
        # n_parallel = multiprocessing.cpu_count()

    exp_prefix = 'start-brownian-arm3d-key-largeBS-rerun'

    vg = VariantGenerator()
    vg.add('start_size', [7])  # this is the ultimate start we care about: getting the pendulum upright
    vg.add('start_goal', lambda start_size: [(1.55, 0.4, -3.75, -1.15, 1.81, -2.09, 0.05)] if start_size == 7 else
           [(1.55, 0.4, -3.75, -1.15, 1.81, -2.09, 0.05, 0, 0, 0, 0, 0, 0, 0)])
    vg.add('ultimate_goal',
           [(0.0, 0.3, -0.7,  # first point --> hill
             0.0, 0.3, -0.4,  # second point --> top
             -0.15, 0.3, -0.55)])  # third point --> side
    vg.add('goal_size', [9])
    vg.add('kill_radius', [None])
    vg.add('terminal_eps', [0.03])
    vg.add('ctrl_cost_coeff', [0])
    # brownian params
    vg.add('seed_with', ['all_previous', 'only_goods'])  # good from brown, onPolicy, previousBrown (ie no good)
    # vg.add('seed_with', ['only_goods'])  # good from brown, onPolicy, previousBrown (ie no good)
    vg.add('brownian_horizon', lambda seed_with: [50] if seed_with == 'on_policy' else [50])
    vg.add('brownian_variance', [1])
    vg.add('regularize_starts', [0])
    # goal-algo params
    vg.add('min_reward', [0.1])
    vg.add('max_reward', [0.9])
    vg.add('distance_metric', ['L2'])
    vg.add('extend_dist_rew', [False])
    vg.add('inner_weight', [0])
    vg.add('goal_weight', lambda inner_weight: [1000] if inner_weight > 0 else [1])
    vg.add('persistence', [1])
    vg.add('n_traj', [3])  # only for labeling and plotting (for now, later it will have to be equal to persistence!)
    vg.add('with_replacement', [True])
    vg.add('use_trpo_paths', [True])
    # replay buffer
    vg.add('replay_buffer', [True])
    vg.add('coll_eps', lambda terminal_eps: [terminal_eps])
    vg.add('num_new_starts', [600])
    vg.add('num_old_starts', [300])
    # sampling params
    vg.add('horizon', [500])
    vg.add('outer_iters', [5000])
    vg.add('inner_iters', [2])  # again we will have to divide/adjust the
    vg.add('pg_batch_size', [50000])
    # policy initialization
    vg.add('output_gain', [0.1])
    vg.add('policy_hidden_sizes', [(64, 64)])
    vg.add('policy_init_std', [1])
    vg.add('learn_std', [False])
    vg.add('adaptive_std', [False])
    vg.add('discount', [0.995])
    vg.add('baseline', ['g_mlp'])

    vg.add('seed', range(100, 1000, 100))

    # Launching
    print("\n" + "**********" * 10 + "\nexp_prefix: {}\nvariants: {}".format(exp_prefix, vg.size))
    print('Running on type {}, with price {}, parallel {} on the subnets: '.format(config.AWS_INSTANCE_TYPE,
                                                                                   config.AWS_SPOT_PRICE, n_parallel), *subnets)

    for vv in vg.variants():
        if mode in ['ec2', 'local_docker']:
            # choose subnet
            subnet = random.choice(subnets)
            config.AWS_REGION_NAME = subnet[:-1]
            config.AWS_KEY_NAME = config.ALL_REGION_AWS_KEY_NAMES[
                config.AWS_REGION_NAME]
            config.AWS_IMAGE_ID = config.ALL_REGION_AWS_IMAGE_IDS[
                config.AWS_REGION_NAME]
            config.AWS_SECURITY_GROUP_IDS = \
                config.ALL_REGION_AWS_SECURITY_GROUP_IDS[
                    config.AWS_REGION_NAME]
            config.AWS_NETWORK_INTERFACES = [
                dict(
                    SubnetId=config.ALL_SUBNET_INFO[subnet]["SubnetID"],
                    Groups=config.AWS_SECURITY_GROUP_IDS,
                    DeviceIndex=0,
                    AssociatePublicIpAddress=True,
                )
            ]
            
            # @llx
            # run_task is the algorithm to train agent
            run_experiment_lite(
                # use_cloudpickle=False,
                stub_method_call=run_task,
                variant=vv,
                mode=mode,
                # Number of parallel workers for sampling
                n_parallel=n_parallel,
                # Only keep the snapshot parameters for the last iteration
                snapshot_mode="last",
                seed=vv['seed'],
                # plot=True,
                exp_prefix=exp_prefix,
                # exp_name=exp_name,
                # for sync the pkl file also during the training
                sync_s3_pkl=True,
                # sync_s3_png=True,
                sync_s3_html=True,
                # # use this ONLY with ec2 or local_docker!!!
                pre_commands=[
                    'export MPLBACKEND=Agg',
                    'pip install --upgrade pip',
                    'pip install --upgrade -I tensorflow',
                    'pip install git+https://github.com/tflearn/tflearn.git',
                    'pip install dominate',
                    'pip install multiprocessing_on_dill',
                    'pip install scikit-image',
                    'conda install numpy -n rllab3 -y',
                ],
            )
            if mode == 'local_docker':
                sys.exit()
        else:
            run_experiment_lite(
                # use_cloudpickle=False,
                stub_method_call=run_task,
                variant=vv,
                mode='local',
                n_parallel=n_parallel,
                # Only keep the snapshot parameters for the last iteration
                snapshot_mode="last",
                seed=vv['seed'],
                exp_prefix=exp_prefix,
                # exp_name=exp_name,
            )
