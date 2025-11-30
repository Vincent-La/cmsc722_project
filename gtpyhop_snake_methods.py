from path_finding import Coord, PathSolver

'''
    Utils
'''
def pyhop_to_coord(pyhop_pos:str):
    split = pyhop_pos.split('-')
    return Coord(int(split[0][-1]), int(split[1][-1]))

def coord_to_pyhop(coord:Coord):
    return f'pos{coord.x}-{coord.y}'

def get_all_active_food(state):
    return [key for key,val in state.ispoint.items() if val]

def get_snake_head(state):
    snake_head = [key for key,val in state.headsnake.items() if val]
    assert len(snake_head) == 1, "Error: Multiple snake heads found"
    return snake_head[0]

def get_snake_coords(state):
    coords = []
    cur = get_snake_head(state)
    while cur is not None:
        coords.append(pyhop_to_coord(cur))
        cur = state.nextsnake[cur]
    return coords

def get_next_spawnpoints(state):
    # only one spawnpoint/nextspawnpoint active at a time
    spawnpoint = [s for s,v in state.spawn.items() if v][0]
    nextspawnpoint = state.nextspawn[spawnpoint]
    return spawnpoint, nextspawnpoint

# create gtpyhop action to move snake to given coord
def make_move_action_to_coord(state, snake_coords, coord:Coord):

    newhead = coord_to_pyhop(coord)
    head = coord_to_pyhop(snake_coords[0])

    # check if coord is occupied by food
    if not state.ispoint[newhead]:

        head = coord_to_pyhop(snake_coords[0])
        newtail = coord_to_pyhop(snake_coords[-2])
        tail = coord_to_pyhop(snake_coords[-1])

        return ('move', head, newhead, tail, newtail)
    
    # no more food spawns
    elif state.spawn['dummypoint']:
        return ('move_and_eat_no_spawn', head, newhead)

    # food spawns available 
    else:
        spawnpoint, nextspawnpoint = get_next_spawnpoints(state)
        return ('move_and_eat_spawn', head, newhead, spawnpoint, nextspawnpoint)

def check_multigoal_achieved(state, multigoal):
    for goal_k, goal_v in multigoal.ispoint.items():
        state_v = state.ispoint[goal_k]
        if state_v != goal_v:
            return False
    return True



'''
    Actions
'''

# NOTE: not bothering to check types since everything is_a coord

def move(state, head, newhead, tail, newtail):
    
    if state.headsnake[head] and \
       newhead in state.isadjacent[head] and \
       state.tailsnake[tail] and \
       state.nextsnake[newtail] == tail and \
       not state.blocked[newhead] and \
       not state.ispoint[newhead]:

        state.blocked[newhead] = True
        state.headsnake[newhead] = True
        state.nextsnake[newhead] = head
        state.headsnake[head] = False
        state.blocked[tail] = False
        state.tailsnake[tail] = False
        state.nextsnake[newtail] = None
        state.tailsnake[newtail] = True

        return state


# eat food and spawn new food
def move_and_eat_spawn(state, head, newhead, spawnpoint, nextspawnpoint):
    

    print("\nmove_and_eat_spawn called")

    if state.headsnake[head] and \
       newhead in state.isadjacent[head] and \
       not state.blocked[newhead] and \
       state.ispoint[newhead] and \
       state.spawn[spawnpoint] and \
       state.nextspawn[spawnpoint] == nextspawnpoint and \
       spawnpoint != 'dummypoint':
        
        state.blocked[newhead] = True
        state.headsnake[newhead] = True
        state.nextsnake[newhead] = head
        state.headsnake[head] = False
        state.ispoint[newhead] = False
        state.ispoint[spawnpoint] = True
        state.spawn[spawnpoint] = False
        state.spawn[nextspawnpoint] = True

        return state

# eat food but no new spawn
def move_and_eat_no_spawn(state, head, newhead):

    # print("\nmove_and_eat_no_spawn called")
    # print(f'{state.headsnake[head]}')
    
    if state.headsnake[head] and \
       newhead in state.isadjacent[head] and \
       not state.blocked[newhead] and \
       state.ispoint[newhead] and \
       state.spawn['dummypoint']:
        
        state.blocked[newhead] = True
        state.headsnake[newhead] = True
        state.nextsnake[newhead] = head
        state.headsnake[head] = False
        state.ispoint[newhead] = False

        return state
    

'''
    Methods
'''

# unigoal to collect food at food_coord
# pyhop check is setting ispoint[food_coord] to False == val
def m_get_food_unigoal(state, food_point, val):
    print(f'\nm_get_food_unigoal called for food at {food_point}')

    # unigoal acheived
    if state.ispoint[food_point] == val:
        return []

    # determine snake coords
    snake_coords = get_snake_coords(state)
    
    # create path solver
    ps = PathSolver(snake_coords, grid_size=(state.grid_size, state.grid_size))
    food_coord = pyhop_to_coord(food_point)
    tail_coord:Coord = snake_coords[-1]
    head_coord:Coord = snake_coords[0]

    # take step towards food if path exists
    path_to_food = ps.shortest_path_to_coord(food_coord)

    print(f'path_to_food:{path_to_food}')
    # print(f'make_move_action_to_coord: {make_move_action_to_coord(state, snake_coords, next_coord)}')


   # no need to worry about deadlock if this is the final food piece
    final_food = (len(get_all_active_food(state)) == 1) and state.spawn['dummypoint']
    print(f'FINAL FOOD STATUS: {final_food}')
    next_coord = None
    if path_to_food and final_food:
        print("UNSAFE STEP TOWARDS FOOD")
        # step towards food
        next_coord = head_coord.adj(path_to_food[0])

    # check if path to tail exists (to avoid deadlock)
    else:
        
        # try to take path with less turns to tail
        consistent_dir = snake_coords[-2].direc_to(tail_coord)
        adjs = tail_coord.all_adj()
        for i in range(len(adjs)):
            if tail_coord.direc_to(adjs[i]) == consistent_dir:
                adjs[0], adjs[i] = adjs[i], adjs[0]
                break
        
   
        for adj in adjs:
            if ps.is_safe(adj):
                
                # check if we can go towards food without getting stuck
                if path_to_food:
                    future_head = head_coord.adj(path_to_food[0])
                    future_snake_coords = [future_head] + snake_coords
                    ps.snake_coords = future_snake_coords

                    path_to_tail = ps.longest_path_to_coord(adj)

                    if len(path_to_tail) >= 1:
                        print('took SAFE step towards food')
                        next_coord = head_coord.adj(path_to_food[0])
                        break 
                
                # step towards tail from current state
                else:
                    ps.snake_coords = snake_coords
                    path_to_tail = ps.longest_path_to_coord(adj)
               
                    if len(path_to_tail) >= 1:
                        next_coord = head_coord.adj(path_to_tail[0])
                        print('took step towards tail')
                        break

                    # # safe step towards food
                    # if path_to_food:
                    #     next_coord = head_coord.adj(path_to_food[0])
                    #     print('took step towards food')

                    # step towards tail
                    # else:
                    #     next_coord = head_coord.adj(path_to_tail[0])
                    #     print('took step towards tail')
                    
                    # break
        
    # step away from food to open up a path
    if next_coord is None:
        max_dist = -1
        for adj in head_coord.all_adj():
            # edge case where we need to step away from food to avoid deadlock
            if ps.is_safe(adj) and adj != food_coord:
                dist = Coord.manhattan_dist(adj, food_coord)
                if dist > max_dist:
                    max_dist = dist
                    next_coord = adj

                    print('took randomish action')
    
    # no valid actions...
    if next_coord is None:
        print(f'no next_coord found...\nadj:{head_coord.all_adj()}\nbody: {snake_coords}')
        return []

    return [make_move_action_to_coord(state, snake_coords, next_coord), ('ispoint', food_point, val)]

  

def m_get_all_food_multigoal(state, multigoal):
    print(f'multigoal: {multigoal.ispoint}')
    print("m_get_all_food_multigoal method called")
    print('all active food:', get_all_active_food(state))
    print('snake head:', get_snake_head(state))
    # print(f'snake coords:', get_snake_coords(state))

    # check if multigoal achieved!
    if check_multigoal_achieved(state, multigoal):
        return []

    # TODO: determine optimal food ordering sequence to minimize moves

    # return []
    print(f'headsnake: {state.headsnake}')
    # print(state.isadjacent[state.headsnake])

    # determine manhattan distances to all food points
    snake_coords = get_snake_coords(state)
    head_coord = snake_coords[0]
    food_coords = [pyhop_to_coord(food) for food in get_all_active_food(state)]

    min_dist = float('inf')
    closest_food = None

    for food_coord in food_coords:

        # try to avoid pursuing a food that is currently occupied by the snake body
        if food_coord not in snake_coords:
            dist = Coord.manhattan_dist(head_coord, food_coord)

            if dist < min_dist:
                min_dist = dist
                closest_food = food_coord
    
    if not closest_food:
        closest_food = food_coords[0]
    
    # greedily pursue unigoal towards closest food
    closest_food = coord_to_pyhop(closest_food)
    return [('ispoint', closest_food, False), multigoal]
    

