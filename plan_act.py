import pddlgym
import gym
import imageio
from pddlgym_planners.ff import FF  # FastForward
from pddlgym_planners.fd import FD  # FastDownward
from htn import HTN  # Hierarchical Task Network planner
import os
import shutil
from argparse import ArgumentParser

''' Parse command-line arguments '''
def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--env', type=str, default='PDDLEnvSnake-v0', choices = ['PDDLEnvSnake-v0'], help='The PDDLGym environment to use.')
    parser.add_argument('--prob_idx', type = int, default=0, help='Problem index to eval on')
    # TODO: add HTN planner
    parser.add_argument('--planner', type=str, choices=['ff', 'fd', 'htn'], default='ff', help='The planner to use: ff (FastForward) or fd (FastDownward).')
    parser.add_argument('--exp_dir', type=str, default='./experiments', help='Directory to save experiment outputs.')
    return parser.parse_args()

''' Initialize the specified planner '''
def init_planner(env, args):

    planner_name = args.planner
    prob_idx = args.prob_idx

    if planner_name == 'ff':
        return FF()
    # TODO: this one seems to crash
    elif planner_name == 'fd':
        return FD()
    elif planner_name == 'htn':
        return HTN(env, prob_idx)
    else:
        raise ValueError(f"Unknown planner: {planner_name}")
    

def main(args):

    output_dir = f'{args.exp_dir}/p{args.prob_idx}'
    # clean up dir for new results
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    

    env = pddlgym.make(args.env)
    env.fix_problem_index(args.prob_idx)

    # render env and save initial state as image
    obs, debug_info = env.reset()
    img = env.render()
    imageio.imsave(os.path.join(output_dir, f"{args.env}_step_00.png"), img)

    planner = init_planner(env, args)
    plan = planner(env.domain, obs)

    state_index = 1
    for action in plan:
        print(action)
        print("Obs:", obs)
        print("Act:", action)
        obs, reward, done, truncated, debug_info = env.step(action)

        img = env.render()
        imageio.imsave(os.path.join(output_dir, f"{args.env}_step_{state_index:04d}.png"), img)
        state_index += 1


    print("Final obs, reward, done:", obs, reward, done)
    print("\n------------------")

    with open(os.path.join(output_dir, "plan.txt"), "w") as f:
        for action in plan:
            f.write(f"{action}\n")

    print("Statistics:", planner.get_statistics())

    with open(os.path.join(output_dir, "statistics.txt"), "w") as f:
        f.write(str(planner.get_statistics()))

    # create animation with imagemagick
    os.system(f"magick -delay 30 {output_dir}/*.png {output_dir}/animation.gif")


if __name__ == "__main__":
    args = parse_args()
    main(args)
    