import GTPyhop.gtpyhop as gtpyhop
import pddlgym
from gtpyhop_snake_methods import *
import time


class HTN:
    def __init__(self, env, prob_idx):
        self._env = env
        self.stats = {}
        self._init_domain(prob_idx)
        self._declare_gtpyhop_methods()

    def __call__(self, domain, obs):
        # NOTE set to 0 for performance
        gtpyhop.verbose = 0
        # output plan regardless of success
        # gtpyhop.verify_goals = False

        start = time.time()
        result = gtpyhop.find_plan(self.initial, [self.multigoal])
        end = time.time()

        self.stats['total_time'] = f"{end - start:.6f}"
        self.stats['plan_length'] = len(result)

        result = self.convert_htn_plan_to_pddlgym(result)
        return result
    
    def convert_htn_plan_to_pddlgym(self, result):
        name_to_predicate = {pred.name: pred for pred in self._env.action_predicates}
        return [pddlgym.structs.Literal(name_to_predicate[act[0].replace('_', '-')], list(act[1:])) for act in result]

    def get_statistics(self):
        # Placeholder for returning planner statistics
        return self.stats
    

    def _declare_gtpyhop_methods(self):
        gtpyhop.declare_actions(move, move_and_eat_spawn, move_and_eat_no_spawn)
        gtpyhop.declare_unigoal_methods('ispoint', m_get_food_unigoal)
        gtpyhop.declare_multigoal_methods(m_get_all_food_multigoal)
        

    def _init_domain(self, prob_idx):

        domain = gtpyhop.Domain(f'Snake_p{prob_idx}')

        if prob_idx == 0:
            rigid = gtpyhop.State('rigid relations')

            # snake domain is only coordinates/fields according to problem size
            # p01/pddl is a 5x5 grid, so coords are (0,0) to (4,4)
            size = 5
            coords = []
            for i in range(size):
                for j in range(size):
                    coord = f'pos{i}-{j}'
                    coords.append(coord)

            coords.append('dummypoint')

            rigid.types = {
                'coord': coords,
            }

            # define initial state for p01

            initial = gtpyhop.State('state0')
            initial.grid_size = size

            # point adjacency relations
            isadjacent = {'dummypoint': []}

            for i in range(size):
                for j in range(size):
                    coord = f'pos{i}-{j}'
                    adjacent_coords = []
                    # up
                    if i > 0:
                        adjacent_coords.append(f'pos{i-1}-{j}')
                    # down
                    if i < size - 1:
                        adjacent_coords.append(f'pos{i+1}-{j}')
                    # left
                    if j > 0:
                        adjacent_coords.append(f'pos{i}-{j-1}')
                    # right
                    if j < size - 1:
                        adjacent_coords.append(f'pos{i}-{j+1}')
                    isadjacent[coord] = adjacent_coords

            initial.isadjacent = isadjacent

            # snake spawn + point spawns
            # set initial tail position
            tailsnake  = 'pos3-0'
            initial.tailsnake = {tailsnake: True} | {coord: False for coord in rigid.types['coord'] if coord != tailsnake}

            # set initial head position
            headsnake = 'pos4-0'
            initial.headsnake = {headsnake: True} | {coord: False for coord in rigid.types['coord'] if coord != headsnake}

            # initial nextsnake position
            nextsnake = {headsnake: tailsnake}
            initial.nextsnake = nextsnake | {coord: None for coord in rigid.types['coord'] if coord not in nextsnake.keys()}

            # set blocked positions (obstacles + snake spawnpoints)
            # NOTE: no obstacles in p01
            blocked_pos = []
            blocked_pos.extend([tailsnake, headsnake])
            initial.blocked = {coord: True for coord in blocked_pos} | {coord: False for coord in rigid.types['coord'] if coord not in blocked_pos}
            
            # set initial food spawn
            spawn = 'pos2-0'
            initial.spawn = {spawn: True} | {coord: False for coord in rigid.types['coord'] if coord != spawn}

            # nextspawn relations
            nextspawn = {
                'pos1-0' :'dummypoint',
                'pos2-0' :'pos1-4',
                'pos1-4' :'pos1-1',
                'pos1-1' :'pos0-1',
                'pos0-1' :'pos3-3',
                'pos3-3' :'pos4-2',
                'pos4-2' :'pos3-4',
                'pos3-4' :'pos0-0',
                'pos0-0' :'pos1-2',
                'pos1-2' :'pos1-0'
            }

            initial.nextspawn = nextspawn | {coord: None for coord in rigid.types['coord'] if coord not in nextspawn.keys()}

            # ispoint
            ispoint = ['pos0-4', 'pos3-1', 'pos1-3', 'pos2-4', 'pos4-1']
            initial.ispoint = {coord: True for coord in ispoint} | {coord: False for coord in rigid.types['coord'] if coord not in ispoint}

            self.initial = initial
            self.multigoal = gtpyhop.Multigoal('multigoal')
            self.multigoal.ispoint = {
                'pos0-4': False,
                'pos3-1': False,
                'pos1-3': False,
                'pos2-4': False,
                'pos4-1': False,
                'pos2-0': False,
                'pos1-4': False,
                'pos1-1': False,
                'pos0-1': False,
                'pos3-3': False,
                'pos4-2': False,
                'pos3-4': False,
                'pos0-0': False,
                'pos1-2': False,
                'pos1-0': False,
            }

        # same as p0 but with less initial food spawns
        elif prob_idx == 1:
            rigid = gtpyhop.State('rigid relations')

            # snake domain is only coordinates/fields according to problem size
            # p01/pddl is a 5x5 grid, so coords are (0,0) to (4,4)
            size = 5
            coords = []
            for i in range(size):
                for j in range(size):
                    coord = f'pos{i}-{j}'
                    coords.append(coord)

            coords.append('dummypoint')

            rigid.types = {
                'coord': coords,
            }

            # define initial state for p01

            initial = gtpyhop.State('state0')
            initial.grid_size = size

            # point adjacency relations
            isadjacent = {'dummypoint': []}

            for i in range(size):
                for j in range(size):
                    coord = f'pos{i}-{j}'
                    adjacent_coords = []
                    # up
                    if i > 0:
                        adjacent_coords.append(f'pos{i-1}-{j}')
                    # down
                    if i < size - 1:
                        adjacent_coords.append(f'pos{i+1}-{j}')
                    # left
                    if j > 0:
                        adjacent_coords.append(f'pos{i}-{j-1}')
                    # right
                    if j < size - 1:
                        adjacent_coords.append(f'pos{i}-{j+1}')
                    isadjacent[coord] = adjacent_coords

            initial.isadjacent = isadjacent

            # snake spawn + point spawns
            # set initial tail position
            tailsnake  = 'pos3-0'
            initial.tailsnake = {tailsnake: True} | {coord: False for coord in rigid.types['coord'] if coord != tailsnake}

            # set initial head position
            headsnake = 'pos3-1'
            initial.headsnake = {headsnake: True} | {coord: False for coord in rigid.types['coord'] if coord != headsnake}

            # initial nextsnake position
            nextsnake = {headsnake: tailsnake}
            initial.nextsnake = nextsnake | {coord: None for coord in rigid.types['coord'] if coord not in nextsnake.keys()}

            # set blocked positions (obstacles + snake spawnpoints)
            # NOTE: no obstacles in p01
            blocked_pos = []
            blocked_pos.extend([tailsnake, headsnake])
            initial.blocked = {coord: True for coord in blocked_pos} | {coord: False for coord in rigid.types['coord'] if coord not in blocked_pos}
            
            # set initial food spawn
            spawn = 'pos2-0'
            initial.spawn = {spawn: True} | {coord: False for coord in rigid.types['coord'] if coord != spawn}

            # nextspawn relations
            nextspawn = {
                # 'pos1-2' :'dummypoint',
                'pos2-0' :'pos1-4',
                'pos1-4' :'pos1-1',
                'pos1-1' :'pos0-1',
                'pos0-1' :'pos3-3',
                'pos3-3' :'pos4-2',
                'pos4-2' :'pos1-2',
                # 'pos3-4' :'pos0-0',
                # 'pos0-0' :'pos1-2',
                'pos1-2' :'dummypoint'
            }

            initial.nextspawn = nextspawn | {coord: None for coord in rigid.types['coord'] if coord not in nextspawn.keys()}

            # ispoint
            ispoint = ['pos0-4']
            initial.ispoint = {coord: True for coord in ispoint} | {coord: False for coord in rigid.types['coord'] if coord not in ispoint}

            self.initial = initial
            self.multigoal = gtpyhop.Multigoal('multigoal')
            self.multigoal.ispoint = {
                'pos0-4': False,
                'pos2-0': False,
                'pos1-4': False,
                'pos1-1': False,
                'pos0-1': False,
                'pos3-3': False,
                'pos4-2': False,
                # 'pos3-4': False,
                # 'pos0-0': False,
                'pos1-2': False,
                # 'pos1-0': False,
            }

        else:
            raise NotImplementedError("Only PDDLEnvSnake-v0 is implemented")
        

