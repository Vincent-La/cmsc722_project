#!/bin/bash

python plan_act.py --env PDDLEnvSnake-v0 \
                   --prob_idx 2 \
                   --planner htn \
                   --exp_dir experiments/PDDLEnvSnake-v0/HTN

