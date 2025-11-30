from collections import deque
from enum import Enum


class Direc(Enum):
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

    @staticmethod
    def opposite(direc):
        if direc == Direc.LEFT:
            return Direc.RIGHT
        if direc == Direc.RIGHT:
            return Direc.LEFT
        if direc == Direc.UP:
            return Direc.DOWN
        if direc == Direc.DOWN:
            return Direc.UP
        return Direc.NONE

class Coord:
    def __init__(self, x = -1, y = -1):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Coord({self.x},{self.y})"
    
    __repr__ = __str__

    def direc_to(self, adj_pos):
        """Return the direction of an adjacent Coord relative to self."""
        if self.x == adj_pos.x:
            diff = self.y - adj_pos.y
            if diff == 1:
                return Direc.LEFT
            if diff == -1:
                return Direc.RIGHT
        elif self.y == adj_pos.y:
            diff = self.x - adj_pos.x
            if diff == 1:
                return Direc.UP
            if diff == -1:
                return Direc.DOWN
        return Direc.NONE

    def adj(self, direc):
        """Return the adjacent Coord in a given direction. (Row, Col) format"""
        if direc == Direc.LEFT:
            return Coord(self.x, self.y - 1)
        elif direc == Direc.RIGHT:
            return Coord(self.x, self.y + 1)
        elif direc == Direc.UP:
            return Coord(self.x - 1, self.y)
        elif direc == Direc.DOWN:
            return Coord(self.x + 1, self.y)
        else:
            return None

    def all_adj(self):
        """Return a list of all the adjacent Coord."""
        adjs = []
        for direc in Direc:
            if direc != Direc.NONE:
                adjs.append(self.adj(direc))
        return adjs

    @staticmethod
    def manhattan_dist(p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)
    

class TableCell:
    def __init__(self):
        self.reset()

    def reset(self):
        # track shortest path
        self.parent = None
        self.dist = float('inf')

        # track longest path
        self.visit = False

    
class PathSolver():

    def __init__(self, snake_coords = None, grid_size = (5,5)):
        self.table = [
            [TableCell() for _ in range(grid_size[0])]
            for _ in range(grid_size[1])
        ]

        self.snake_coords = snake_coords

    # table reset
    def _reset_table(self):
        for row in self.table:
            for col in row:
                col.reset()

    # build path from src to des using self.table
    # returns directions to follow path
    def _build_path(self, src, des):
        dir_path = deque()

        tmp = des
        while tmp != src:
            parent = self.table[tmp.x][tmp.y].parent
            dir_path.appendleft(parent.direc_to(tmp))
            tmp = parent

        return dir_path
    
    # check in bounds and no collision
    # NOTE: assuming only obstacles are the snake body
    def is_safe(self, coord:Coord):
        
        # if coord == self.snake_coords[-1] and coord == self.snake_coords[1]:
        #     return False        

        return (0 <= coord.x < len(self.table)) and (0 <= coord.y < len(self.table[0])) and \
                not (coord in self.snake_coords)  # avoid collision w/ body

    # determine if coordinate is valid for path finding
    def _is_valid(self, coord:Coord):
        
        if not self.is_safe(coord):
            return False

        not_visited = not self.table[coord.x][coord.y].visit

        return not_visited

    # find shortest path from snake head to target_coord
    def shortest_path_to_coord(self, target_coord:Coord):
        self._reset_table()

        head_coord = self.snake_coords[0]
        
        self.table[head_coord.x][head_coord.y].dist = 0
        queue = deque()
        queue.append(head_coord)

        while queue:
            cur:Coord = queue.popleft()

            # print(f'cur: {cur}')
            if cur == target_coord:
                return self._build_path(head_coord, target_coord)
            
            # attempt to keep snake moving in same direction to avoid collision with itself
            if cur == head_coord:
                # direction determined by 2nd snake point
                first_direc = self.snake_coords[1].direc_to(head_coord)
            else:
                first_direc = self.table[cur.x][cur.y].parent.direc_to(cur)

            # TODO: better heuristic here?
            # add adjacent positions to queue, prioritizing continuing in same direction if possible
            adjs = cur.all_adj()
            for i, coord in enumerate(adjs):

                # orient adjs to add Coord that continues in same direction first
                if first_direc == cur.direc_to(coord):
                    adjs[0], adjs[i] = adjs[i], adjs[0]
                    break
            
            for coord in adjs:
                if self._is_valid(coord):
                    adj_cell = self.table[coord.x][coord.y]

                    # add unvisited cells to queue
                    if adj_cell.visit == False:
                        adj_cell.dist = self.table[cur.x][cur.y].dist + 1
                        adj_cell.parent = cur
                        adj_cell.visit = True
                        queue.append(coord)

        # no path found, return empty path
        return deque()  
    
    # find longest path from snake head to target_coord
    def longest_path_to_coord(self, target_coord:Coord):
        
        # get shortest path first, if none exists, return empty path
        path = self.shortest_path_to_coord(target_coord)
        if not path:
            return deque()

        self._reset_table()

         # mark all coords in shortest path as visited to avoid adding them to queue
        cur = self.snake_coords[0]
        self.table[cur.x][cur.y].visit = True
        for direc in path:
            cur = cur.adj(direc)
            self.table[cur.x][cur.y].visit = True
        
        # attempt extending path between each pair of coords in shortest path
        idx = 0
        cur = self.snake_coords[0]

        while True:
            cur_direc = path[idx]
            next_coord = cur.adj(cur_direc)

            # find detour around next_coord
            if cur_direc == Direc.RIGHT or cur_direc == Direc.LEFT:
                test_direcs = [Direc.UP, Direc.DOWN]
            else:   
                test_direcs = [Direc.LEFT, Direc.RIGHT]

            detour_found = False
            for test_direc in test_direcs:
                detour_coord = cur.adj(test_direc)
                after_detour = detour_coord.adj(test_direc)

                if self._is_valid(detour_coord) and self._is_valid(after_detour):
                    # mark detour coords as visited
                    self.table[detour_coord.x][detour_coord.y].visit = True
                    self.table[after_detour.x][after_detour.y].visit = True

                     # insert detour into path
                    path.insert(idx, test_direc)
                    path.insert(idx + 2, Direc.opposite(test_direc))

                    detour_found = True
                    break
            
            if not detour_found:
                idx += 1
                cur = next_coord

                if idx >= len(path):
                    break

        return path
