import pddlgym
import imageio
from pddlgym_planners.fd import FD


def main():
    env = pddlgym.make("PDDLEnvSnake-v0")

    obs, debug_info = env.reset()
    img = env.render()
    imageio.imsave("frame1.png", img)
    action = env.action_space.sample(obs)
    obs, reward, done, truncated, debug_info = env.step(action)
    img = env.render()
    imageio.imsave("frame2.png", img)

    # See `pddl/sokoban.pddl` and `pddl/sokoban/problem3.pddl`.

    # TODO: FD plannes  doesn't seem to work with snake...
    # env = pddlgym.make("PDDLEnvSokoban-v0")
    # env = pddlgym.make("PDDLEnvSnake-v0")

    # env.fix_problem_index(0)
    # obs, debug_info = env.reset()
    # print(f'DEBUG info: {debug_info}')
    # planner = FD()
    # plan = planner(env.domain, obs)
    # for act in plan:
    #     print("Obs:", obs)
    #     print("Act:", act)
    #     obs, reward, done, truncated, debug_info = env.step(act)
    # print("Final obs, reward, done:", obs, reward, done)


if __name__ == "__main__":
    main()
