import pddlgym
import gym
import imageio
from pddlgym_planners.ff import FF  # FastForward
from pddlgym_planners.fd import FD  # FastDownward
from htn import HTN  # Hierarchical Task Network planner
import os
from argparse import ArgumentParser

''' Parse command-line arguments '''
def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--env', type=str, default='PDDLEnvSnake-v0', help='The PDDLGym environment to use.')
    # TODO: add HTN planner
    parser.add_argument('--planner', type=str, choices=['ff', 'fd', 'htn'], default='ff', help='The planner to use: ff (FastForward) or fd (FastDownward).')
    parser.add_argument('--exp_dir', type=str, default='./experiments', help='Directory to save experiment outputs.')
    return parser.parse_args()

''' Initialize the specified planner '''
def init_planner(planner_name, env, problem_name):
    if planner_name == 'ff':
        return FF()
    # TODO: this one seems to crash
    elif planner_name == 'fd':
        return FD()
    elif planner_name == 'htn':
        return HTN(env, problem_name)
    else:
        raise ValueError(f"Unknown planner: {planner_name}")
    

def main(args):
    os.makedirs(args.exp_dir, exist_ok=True)
    env = pddlgym.make(args.env)

    # render env and save initial state as image
    obs, debug_info = env.reset()
    img = env.render()
    imageio.imsave(os.path.join(args.exp_dir, f"{args.env}_step_00.png"), img)

    planner = init_planner(args.planner, env, args.env)
    plan = planner(env.domain, obs)

    state_index = 1
    for action in plan:
        print(action)
        print("Obs:", obs)
        print("Act:", action)
        obs, reward, done, truncated, debug_info = env.step(action)

        img = env.render()
        imageio.imsave(os.path.join(args.exp_dir, f"{args.env}_step_{state_index:02d}.png"), img)
        state_index += 1


    print("Final obs, reward, done:", obs, reward, done)
    print("\n------------------")

    print("Statistics:", planner.get_statistics())

    # create animation with imagemagick
    os.system(f"magick -delay 30 {args.exp_dir}/* {args.exp_dir}/animation.gif")


if __name__ == "__main__":
    args = parse_args()
    main(args)
    