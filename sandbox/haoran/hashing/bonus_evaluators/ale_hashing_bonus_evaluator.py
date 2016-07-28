import numpy as np
from rllab.misc import logger
from sandbox.haoran.hashing.hash.sim_hash import SimHash
from sandbox.haoran.hashing.bonus_evaluators.base import BonusEvaluator

class ALEHashingBonusEvaluator(BonusEvaluator):
    """
    Uses a hash function to store states of state-action pairs counts.
    Then assign bonus reward to under-explored states or state-action pairs.
    Input states might be pre-processed versions of raw states.
    """
    def __init__(
            self,
            state_dim,
            num_actions,
            img_preprocessor=None,
            hash_list=[],
            count_mode="s",
            bonus_mode="s_next",
            bonus_coeff=1.0,
            state_bonus_mode="1/n_s",
            state_action_bonus_mode="log(n_s)/n_sa",
        ):
        self.state_dim = state_dim
        if img_preprocessor is not None:
            assert img_preprocessor.output_dim == state_dim
            self.img_preprocessor = img_preprocessor
        else:
            self.img_preprocessor = None
        for hash in hash_list:
            assert hash.item_dim == state_dim
        self.num_actions = num_actions
        self.hash_list = hash_list

        self.count_mode = count_mode
        # Default: SimHash
        sim_hash_args = {
            "dim_key":128, "bucket_sizes":None
        }
        if count_mode == "s":
            if len(hash_list) == 0:
                hash = SimHash(state_dim,**sim_hash_args)
                hash.reset()
                hash_list.append(hash)
            assert len(hash_list) == 1
        elif count_mode == "sa":
            if len(hash_list) == 0:
                for i in xrange(num_actions):
                    hash = SimHash(state_dim,**sim_hash_args)
                    hash.reset()
                    hash_list.append(hash)
            assert len(hash_list) == num_actions
        else:
            raise NotImplementedError

        self.bonus_mode = bonus_mode
        self.bonus_coeff = bonus_coeff
        self.state_bonus_mode = state_bonus_mode
        self.state_action_bonus_mode = state_action_bonus_mode
        self.epoch_hash_count_list = [] # record the hash counts of all state (state-action) they are *updated* (not evaluated) in this epoch
        self.epoch_bonus_list = [] # record the bonus given throughout the epoch

    def preprocess(self,states):
        if self.img_preprocessor is not None:
            states = self.img_preprocessor.process(states)
        return states

    def update(self, states, actions):
        """
        Assume that actions are integers.
        """
        states = self.preprocess(states)
        if self.count_mode == "s":
            self.hash_list[0].inc_hash(states)
        elif self.count_mode == "sa":
            for s,a in zip(states,actions):
                s = s.reshape((1,len(s)))
                self.hash_list[a].inc_hash(s)
        else:
            raise NotImplementedError

    def evaluate(self, states, actions, next_states):
        """
        Compute a bonus score.
        """
        if self.bonus_mode == "s":
            states = self.preprocess(states)
            counts = self.hash_list[0].query_hash(states)
            bonus = self.compute_state_bonus(counts)
        elif self.bonus_mode == "sa":
            states = self.preprocess(states)
            # for each state, query the state-action count for each possible action
            counts = [
                [
                    hash.query_hash(s.reshape((1,len(s)))).ravel()
                    for hash in self.hash_list
                ]
                for s in states
            ]
            self.compute_state_action_bonus(counts, actions)
        elif self.bonus_mode == "s_next":
            next_states = self.preprocess(next_states)
            counts = self.hash_list[0].query_hash(next_states)
            bonus = self.compute_state_bonus(counts)
        else:
            raise NotImplementedError

        self.epoch_hash_count_list += list(counts)
        self.epoch_bonus_list += list(bonus)

        return bonus

    def compute_state_bonus(self,state_counts):
        if self.state_bonus_mode == "1/n_s":
            bonus = 1./np.maximum(1.,state_counts)
        elif self.state_bonus_mode == "1/sqrt(n_s)":
            bonus = 1./np.sqrt(np.maximum(1., state_counts))
        else:
            raise NotImplementedError
        bonus *= self.bonus_coeff
        return bonus

    def compute_state_action_bonus(self, state_action_counts, actions):
        raise NotImplementedError

    def count(self,states,actions):
        states = self.preprocess(states)
        if self.count_mode == "s":
            counts = self.hash_list[0].query_hash(states)
        elif self.count_mode == "sa":
            counts = [
                int(self.hash_list[a].query_hash(s.reshape((1,len(s)))))
                for s,a in zip(states,actions)
            ]
        else:
            raise NotImplementedError
        return counts

    def reset(self):
        for hash in self.hash_list:
            hash.reset()

    def finish_epoch(self,epoch,phase):
        # record counts
        if self.count_mode == "s":
            logger.record_tabular_misc_stat("%sStateCount"%(phase),self.epoch_hash_count_list)
        else:
            raise NotImplementedError

        # record bonus
        logger.record_tabular_misc_stat("%sBonusReward"%(phase),self.epoch_bonus_list)

        self.epoch_hash_count_list = []
        self.epoch_bonus_list = []

    def log_diagnostics(self, paths):
        pass
