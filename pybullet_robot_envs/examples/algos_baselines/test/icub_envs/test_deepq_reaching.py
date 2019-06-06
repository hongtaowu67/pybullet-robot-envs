#add parent dir to find package. Only needed for source code build, pip install doesn't need it.
import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(currentdir)
parentdir = os.path.dirname(os.path.dirname(currentdir))
os.sys.path.insert(0, parentdir)

from baselines import deepq

from pybullet_robot_envs.envs.icub_envs.icub_reach_gym_env import iCubReachGymEnv
from pybullet_robot_envs import robot_data


log_dir = '../pybullet_logs/icubreach_deepq'

def callback(lcl, glb):
  # stop training if reward exceeds 199
  is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
  if is_solved:
      print("is solved!")
  return is_solved


def main():

  use_IK = 1
  discreteAction = 1
  use_IK = 1 if discreteAction else use_IK

  icubenv = iCubReachGymEnv(urdfRoot=robot_data.getDataPath(), renders=True, useIK=use_IK, isDiscrete=discreteAction)

  act = deepq.learn(icubenv, network='mlp', total_timesteps=0, load_path=log_dir+"/model.pkl")
  print(act)

  while True:
    obs, done = icubenv.reset(), False
    print("===================================")
    print("obs")
    print(obs)
    episode_rew = 0
    while not done:
      #icubenv.render()
      action = act(obs[None])
      #print(action)
      obs, rew, done, _ = icubenv.step(action[0])
      episode_rew += rew
      print("Episode reward", episode_rew)

if __name__ == '__main__':
  main()