import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *

import math
import time
from collections import deque

class exploreBeforeAttack:
    def getAction(self, pid, grids, units, memory):
        start_time = time.time()
        # Overhead, but not so much
        def init_memory():
            if 'explored' not in memory:
                memory['explored'] = grids
            if 'size' not in memory:
                height = len(grids)
                width = len(grids[0])
                memory['size'] = (width, height)
        init_memory()
        LOS = 3
        width, height = memory['size']
        explored = memory['explored']
        explore_targets = [
            # (int(0.10*height), int(0.10*width)),
            # (int(0.10*height), int(0.5*width)),
            # (int(0.10*height), int(0.9*width)),
            # (int(0.5*height), int(0.10*width)),
            # (int(0.5*height), int(0.5*width)),
            # (int(0.5*height), int(0.9*width)),
            # (int(0.9*height), int(0.10*width)),
            # (int(0.9*height), int(0.5*width)),
            # (int(0.9*height), int(0.9*width)),
            (LOS, LOS),
            (LOS, width / 2),
            (LOS, width - LOS),
            (height / 2, LOS),
            (height / 2, width / 2),
            (height / 2, width - LOS),
            (height - LOS, LOS),
            (height - LOS, width / 2),
            (height - LOS, width - LOS),
            (height / 2, 2),
            (height / 2, width - 3),
            ]

        UNEXPLORED = -1
        WALL = 1
        # Another overhead, but meh
        resolution = [{
            'ne': (-1, 0),
            'e': (0, 1),
            'se': (1, 0),
            'nw': (-1, -1),
            'w': (0, -1),
            'sw': (1, -1),
            },
            {
            'ne': (-1, 1),
            'e': (0, 1),
            'se': (1, 1),
            'nw': (-1, 0),
            'w': (0, -1),
            'sw': (1, 0),
            }]
        direction_mapper = {
            'na': IDLE,
            'ne': UPPERRIGHT,
            'e': RIGHT,
            'se': DOWNRIGHT,
            'nw': UPPERLEFT,
            'w': LEFT,
            'sw': DOWNLEFT
            }
        directions = ('ne', 'e', 'se','sw', 'w', 'nw')

        def in_boundary(row, col):
            return 0 <= row < memory['size'][1] \
                and 0 <= col < memory['size'][0] \
                and explored[row][col] != WALL

        def resolve(row, col, direction):
            remainder = row % 2
            delta = resolution[remainder][direction]
            new_row = row + delta[0]
            new_col = col + delta[1]
            if in_boundary(new_row, new_col):
                return (new_row, new_col)
            else: return (row, col)

        heatmap = []
        us = []
        them = []
        ours = []
        theirs = []
        freebies = []
        unexplored = []
        for row in range(height):
            heatmap.append([])
            for col in range(width):
                heatmap[row].append(0.)
                g = grids[row][col]
                if g != -1: # Explored!
                    explored[row][col] = g
                e = explored[row][col]
                if e < 9:
                    pass
                elif e == 9:
                    freebies.append((row, col))
                elif e - 10 == pid:
                    ours.append((row, col))
                else:
                    theirs.append((row, col))

                u = units[row][col]
                if not isinstance(u, int): # Is not a unit!
                    if u.GetPlayerID() == pid:
                        us.append((row, col, u.GetUnitID() ))
                    else:
                        them.append((row, col))

                if e == -1:
                    unexplored.append((row, col))

        def _(x, denominator):
            return math.exp(-x**2./denominator)
        def __(x):
            return 1./math.sqrt(x+1.)
        def ___(x):
            return 1./(x+1.)
        # Capture all freebies
        for freebie_row, freebie_col in freebies:
            visited = [[-1] * width for i in range(height)]
            q = deque()
            q.append((freebie_row, freebie_col))
            visited[freebie_row][freebie_col] = 0
            while q:
                row, col = q.popleft()
                distance = visited[row][col]
                # heatmap[row][col] += _(distance, 1024.)
                heatmap[row][col] += ___(distance)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if explored[new_row][new_col] != WALL \
                        and visited[new_row][new_col] == -1:
                        visited[new_row][new_col] = distance + 1
                        q.append((new_row, new_col))

        # for unexplored_row, unexplored_col in unexplored:
        for target_row, target_col in explore_targets:
            if explored[target_row][target_col] != UNEXPLORED \
                or explored[target_row][target_col] == WALL:
                continue

            visited = [[-1] * width for i in range(height)]
            q = deque()
            q.append((target_row, target_col))
            visited[target_row][target_col] = 0
            while q:
                row, col = q.popleft()
                distance = visited[row][col]
                # heatmap[row][col] += _(distance, 256.)
                heatmap[row][col] += ___(distance)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if explored[new_row][new_col] != WALL \
                        and visited[new_row][new_col] == -1:
                        visited[new_row][new_col] = distance + 1
                        q.append((new_row, new_col))
            # One point of interest at a time
            break

        for their_row, their_col in theirs:
            visited = [[-1] * width for i in range(height)]
            q = deque()
            q.append((their_row, their_col))
            visited[their_row][their_col] = 0
            while q:
                row, col = q.popleft()
                distance = visited[row][col]
                # heatmap[row][col] += _(distance, 64.)
                heatmap[row][col] += ___(distance)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if explored[new_row][new_col] != WALL \
                        and visited[new_row][new_col] == -1:
                        visited[new_row][new_col] = distance + 1
                        q.append((new_row, new_col))
        # print len(us)
        # print heatmap[17][-4:]
        # print heatmap[18][-4:]
        # print heatmap[19][-4:]
        # print grids[17][-5:], explored[17][-5:]
        # print grids[18][-5:], explored[18][-5:]
        # print grids[19][-5:], explored[19][-5:]
        results = []
        # Your code here!
        final_position = set()
        for unit_row, unit_col, unit_id in us:
            direction_max = 'na'
            row_max = unit_row
            col_max = unit_col
            max_heat = heatmap[unit_row][unit_col]
            for direction in directions:
                new_row, new_col = resolve(unit_row, unit_col, direction)
                # print unit_row, unit_col, row_max, col_max, direction_max, max_heat, new_row, new_col, heatmap[new_row][new_col], (new_row, new_col) not in final_position, explored[new_row][new_row], grids[new_row][new_col]
                if (new_row, new_col) not in final_position \
                    and explored[new_row][new_col] != WALL \
                    and heatmap[new_row][new_col] > max_heat:
                    # print 'Update!'
                    max_heat = heatmap[new_row][new_col]
                    row_max = new_row
                    col_max = new_col
                    direction_max = direction
            final_position.add((row_max, col_max))
            results.append(Movement(unit_id, direction_mapper[direction_max]))
        print explored[height / 2][LOS]
        print '%.9fs' % (time.time() - start_time)
        return results
