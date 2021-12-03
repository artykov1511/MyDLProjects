import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque


"""
  you may use the following Node class
  modify it if needed, or create your own
"""
class Node():
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, h_value):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = h_value
        
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h
        

       

class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class DStarLiteAgent(Agent):

    def __init__(self):
        super().__init__()
        
        
        self.initialized = False
        
        
        #  g cost in A*, 2d array of size [height][width] 
        #    IMPORTANT NOTE!!!
        #please fill values inside this array
        #as you perform the A* search!
        self.g_values = []
        
        #  rhs cost in D*, 2d array of size [height][width]
        #SAME AS G, FILL THESE VALUES IN YOUR CODE
        self.rhs_values = []
        
        
        #  a large enough value for initializing g values at the start
        self.INFINITY_COST = 2**10
        
    
    #  finds apple's position in the given level matrix
    #return a tuple of (row, column)
    def find_apple_position(self, level_matrix):
        for r in range(len(level_matrix)):
            for c in range(len(level_matrix[0])):
                if (level_matrix[r][c] == "A"):
                    return (r, c)
        
        return (-1, -1)
        
    
    #  calculates manhattan distance between player and apple
    #this function assumes there is only a single apple in the level
    def heuristic(self, player_row, player_column, apple_row, apple_column):
        return abs(player_row - apple_row) + abs(player_column - apple_column)
    
    
        
        
    def solve(self, level_matrix, player_row, player_column, changed_row, changed_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        self.print_level_matrix(initial_level_matrix)
        
        if (not self.initialized):
            #  first time calling D*lite agent solve()

            
            self.initialized = True
        else:
            #  initialization phase is already performed
            #  this means solve() is called once again because there is
            #a change detected in the map
            print("Solve called again because a new obstacle appeared at position:(", changed_row, ",", changed_column, ")")

            
            
            pass
        
        
        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        #move_sequence = ["U"]
        return move_sequence
    
    
    
    def on_encounter_obstacle(self):
        pass
