import gymnasium as gym
import torch
import time



def evaluate_policy(env, model,turns = 3):
    scores = 0
    for j in range(turns):
        s, info = env.reset()
        
        done = False
        ep_r = 0
        steps = 0
        while not done:
            time.sleep(0.1)
            a = model.select_action(s, evaluate=True)
            # print('model 执行的操作：',a)
            s_prime, r, done,truncated, info = env.step(a)
            done = done or truncated
            ep_r += r
            steps += 1
            s = s_prime
        scores += ep_r
    
    return int(scores/turns)


#You can just ignore this funciton. Is not related to the RL.
def str2bool(v):
    '''transfer str to bool for argparse'''
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'True','true','TRUE', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'False','false','FALSE', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

class LinearSchedule(object):
    def __init__(self, schedule_timesteps, final_p, initial_p=1.0):
        """Linear interpolation between initial_p and final_p over
        schedule_timesteps. After this many timesteps pass final_p is
        returned.

        Parameters
        ----------
        schedule_timesteps: int
            Number of timesteps for which to linearly anneal initial_p
            to final_p
        initial_p: float
            initial output value
        final_p: float
            final output value
        """
        self.schedule_timesteps = schedule_timesteps
        self.final_p = final_p
        self.initial_p = initial_p

    def value(self, t):
        fraction = min(float(t) / self.schedule_timesteps, 1.0)
        return self.initial_p + fraction * (self.final_p - self.initial_p)
