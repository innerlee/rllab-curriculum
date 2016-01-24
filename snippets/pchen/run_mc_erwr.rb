require_relative '../rocky/utils'

quantile = 1
seed = 1

params = {
  mdp: {
    # _name: "box2d.mountain_car_mdp",
    _name: "box2d.cartpole_mdp",
  },
  policy: {
    _name: "mean_std_nn_policy",
    std_trainable: false,
    initial_std: 1,
    hidden_sizes: [],
    std_sizes: []
  },
  baseline: {
    _name: "zero_baseline",
  },
  exp_name: "erwr_mc_seed_#{seed}",
  algo: {
    # _name: "ppo",
    # step_size: 0.1,
    # binary_search_penalty: false,

    # _name: "trpo",
    # step_size: 0.1,
    # backtrack_ratio: 0.8,
    # max_backtracks: 10,
    # cg_iters: 10,

    # _name: "cem",

    _name: "erwr",
    max_opt_itr: 10,
    best_quantile: 0.1,

    batch_size: 50000,
    whole_paths: true,
    max_path_length: 100,
    n_itr: 500,
    plot: true,
  },
  n_parallel: 2,
  # snapshot_mode: "none",
  seed: seed,
  plot: true,
}
command = to_command(params)
puts command
system(command)

