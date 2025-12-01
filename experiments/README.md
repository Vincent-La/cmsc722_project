# Experiments Overview

+ Red = snake head
+ Green = snake body
+ Yellow = snake tail
+ White = food
+ Black = empty cell

## Problem p0 (5x5, multifood)

#### Problem Initial State
![](./PDDLEnvSnake-v0/FF/p0/PDDLEnvSnake-v0_step_00.png)


| Planner                         | Plan Length | Planner Total Time (s) | Rendered Plan |
| -------                         | ----------- |   ---------------      | ------------- |
|  Fast-Forward (FF)              |     29      |       0.1              | ![](./PDDLEnvSnake-v0/FF/p0/animation.gif)  | 
|  Hiearchical Task Network (HTN) |     27      |     0.008530           | ![](./PDDLEnvSnake-v0/HTN/p0/animation.gif) |

## Problem p1 (5x5, single food)

#### Problem Initial State
![](./PDDLEnvSnake-v0/FF/p1/PDDLEnvSnake-v0_step_00.png)

| Planner                         | Plan Length | Planner Total Time (s) | Rendered Plan |
| -------                         | ----------- |   ---------------      | ------------- |
|  Fast-Forward (FF)              |     41      |       0.03             | ![](./PDDLEnvSnake-v0/FF/p1/animation.gif)  | 
|  Hiearchical Task Network (HTN) |     47      |     0.015784           | ![](./PDDLEnvSnake-v0/HTN/p1/animation.gif) |

## Problem p2 (7x7, multifood)

#### Problem Initial State
![](./PDDLEnvSnake-v0/FF/p2/PDDLEnvSnake-v0_step_00.png)

| Planner                         | Plan Length | Planner Total Time (s) | Rendered Plan |
| -------                         | ----------- |   ---------------      | ------------- |
|  Fast-Forward (FF)              |     41      |       0.11             | ![](./PDDLEnvSnake-v0/FF/p2/animation.gif)  | 
|  Hiearchical Task Network (HTN) |     35      |     0.020910           | ![](./PDDLEnvSnake-v0/HTN/p2/animation.gif) |

## Problem p3 (7x7, single food)

#### Problem Initial State
![](./PDDLEnvSnake-v0/FF/p3/PDDLEnvSnake-v0_step_00.png)

| Planner                         | Plan Length | Planner Total Time (s) | Rendered Plan |
| -------                         | ----------- |   ---------------      | ------------- |
|  Fast-Forward (FF)              |     74      |       0.88             | ![](./PDDLEnvSnake-v0/FF/p3/animation.gif)  | 
|  Hiearchical Task Network (HTN) |     76      |     0.046762           | ![](./PDDLEnvSnake-v0/HTN/p3/animation.gif) |

## Problem p4 (7x7, single food)
+ More diffiult version of p3

#### Problem Initial State
![](./PDDLEnvSnake-v0/FF/p4/PDDLEnvSnake-v0_step_00.png)

| Planner                         | Plan Length             | Planner Total Time (s) | Rendered Plan  |
| -------                         | -----------             |   ---------------      | -------------  |
|  Fast-Forward (FF)              |     No Plan Found!      |     No Plan Found!     | No Plan Found! | 
|  Hiearchical Task Network (HTN) |     118                 |     0.075316           | ![](./PDDLEnvSnake-v0/HTN/p4/animation.gif) |

