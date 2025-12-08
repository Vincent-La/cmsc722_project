# Snake HTN Planner With GTPyhop

Experimenting with PDDL and Hierarchical Task Network Planners for a classic Snake game environment

## Snake Environment

+ Adapted Snake enivornment from `pddlgym`
  + [PDDL domain file](pddlgym/pddlgym/pddl/snake.pddl)
  + [PDDL problem files](pddlgym/pddlgym/pddl/snake)

## Planning Models
+ Fast Foward (FF) Planner
  + Using the pddlgym_planners implmentation at [ff.py](pddlgym_planners/pddlgym_planners/ff.py)

+ Hierarchical Task Network (HTN) Planner
  + Implementation at [htn.py](htn.py)
  + Utilizes GTPyhop, methods and actions defined in [gtpyhop_snake_methods.py](gtpyhop_snake_methods.py)

+ Plan + Act w/ Snake Environment
  + [plan_act.py](plan_act.py) implements a Run-Lazy-Lookahead algorithm for planning and acting


## Experimental Results

See experiment results overview [here](experiments/README.md)

## Final Report

See final report [here](./CMSC722_final_report.pdf)

## Installation
```
conda create -n SNAKE_HTN python==3.10 -y
pip install -r requirements.txt
pip install -e pddlgym/
pip install -e pddlgym_planners/
```



