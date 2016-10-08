import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Movement import *
from Unit import *
from HexagridHelper import *

import math
from collections import deque

class PEWPEWDIEBEEPBOOP:
    def getAction(self, pid, grids, units, memory):
        # Overhead, but not so much
        def init_memory():
            if 'explored' not in memory:
                memory['explored'] = grids
            if 'size' not in memory:
                height = len(grids)
                width = len(grids[0])
                memory['size'] = (width, height)
        init_memory()

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
            'se': LOWERRIGHT,
            'nw': UPPERLEFT,
            'w': LEFT,
            'sw': LOWERLEFT
            }
        directions = ('ne', 'e', 'se','sw', 'w', 'nw')

        def in_boundary(row, col):
            return 0 <= row < memory['size'][1] \
                and 0 <= col < memory['size'][0]

        def resolve(row, col, direction):
            remainder = row % 2
            delta = resolution[remainder][direction]
            new_row = row + delta[0]
            new_col = col + delta[1]
            if in_boundary(new_row, new_col):
                return (new_row, new_col)
            else: return (row, col)

        heatmap = []
        width, height = memory['size']
        explored = memory['explored']
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
                    if g < 9:
                        continue
                    if g == 9:
                        freebies.append((row, col))
                    elif g - 10 == pid:
                        ours.append((row, col))
                    else:
                        theirs.append((row, col))
                else: # Unexplored!
                    unexplored.append((row, col))

                u = units[row][col]
                if not isinstance(u, int): # Is not a unit!
                    if u.GetPlayerID() == pid:
                        us.append((row, col, u.GetUnitID() ))
                    else:
                        them.append((row, col))
        def _(x, denominator):
            return math.exp(-x**2./denominator)
        # Capture all freebies
        visited = {}
        for freebie_row, freebie_col in freebies:
            q = deque()
            q.append((freebie_row, freebie_col))
            visited[(freebie_row, freebie_col)] = 0
            while not q:
                row, col = q.popleft()
                distance = visited[(row, col)]
                heatmap[row][col] += _(distance, 1024.)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if (new_row, new_col) not in visited:
                        visited[(new_row, new_col)] = distance + 1
                        q.append((new_row, new_col))

        for unexplored_row, unexplored_col in unexplored:
            q = deque()
            q.append((freebie_row, freebie_col))
            visited[(freebie_row, freebie_col)] = 0
            while not q:
                row, col = q.popleft()
                distance = visited[(row, col)]
                heatmap[row][col] += _(distance, 256.)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if (new_row, new_col) not in visited:
                        visited[(new_row, new_col)] = distance + 1
                        q.append((new_row, new_col))

        for their_row, their_col in theirs:
            q = deque()
            q.append((freebie_row, freebie_col))
            visited[(freebie_row, freebie_col)] = 0
            while not q:
                row, col = q.popleft()
                distance = visited[(row, col)]
                heatmap[row][col] += _(distance, 64.)
                for direction in directions:
                    new_row, new_col = resolve(row, col, direction)
                    if (new_row, new_col) not in visited:
                        visited[(new_row, new_col)] = distance + 1
                        q.append((new_row, new_col))

        results = []
        # Your code here!
        final_position = set()
        for unit_row, unit_col, unit_id in us:
            direction_max = 'na'
            max_heat = -1e99
            for direction in directions:
                new_row, new_col = resolve(unit_row, unit_col, direction)
                if (new_row, new_col) not in final_position \
                    and heatmap[new_row][new_col] > max_heat:
                    max_heat = heatmap[new_row][new_col]
                    direction_max = direction
            result.append(Movement(unit_id, direction_mapper[direction_max]))
        return results

