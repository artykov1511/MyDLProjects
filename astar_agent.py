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
    
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = 0

        self.f = 0
        self.g = 0
        
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h

    def __eq__(self, other):
        return (self.player_row == other.player_row and self.player_col == other.player_col)



class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]


class AStarAgent(Agent):

    def __init__(self):
        super().__init__()
        
        #  g cost in A*
        #    IMPORTANT NOTE!!!
        #please fill values inside this array
        #as you perform the A* search!
        self.g_values = []
        
        
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
    
        
        
        
    def solve(self, level_matrix, player_row, player_column):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

       

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        
        
        level_height = len(initial_level_matrix)
        level_width = len(initial_level_matrix[0])
        
       
        #  initialize g values
        self.g_values = [ [self.INFINITY_COST]*level_width for i in range(level_height) ]
        
        #  initialize g of starting position 0
        self.g_values[player_row][player_column] = 0
        
        #  calculate heuristic value for starting position
        (apple_row, apple_column) = self.find_apple_position(initial_level_matrix)
        initial_heuristic = self.heuristic(player_row, player_column, apple_row, apple_column)
        
        print("A* solve() --- level size:", (level_height, level_width))
        print("A* solve() --- apple position:", (apple_row, apple_column))
        print("A* solve() --- initial_heuristic:", initial_heuristic)
        
        
        
        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """
        # Initialization 
        open_list = PriorityQueue()
        closed_list = []
        #parent_node = 0
        #depth = 0 #self.g_values[player_row][player_column]
        init_node = Node(0, initial_level_matrix, player_row, player_column, 0, 0)

        open_list.put(init_node, init_node.f)

        search = True
        level_matrix = initial_level_matrix
        while not open_list.empty(): #and search:
            # Choose the node with least f value
            current_node = open_list.get()
            level_matrix[current_node.player_row][current_node.player_col] = 'P'
            
            if current_node.chosen_dir != 0:
                move_sequence.append(current_node.chosen_dir)

            successors = []
            # Determine successors of the current node
            if (current_node.player_row + 1 < level_height-1) and (level_matrix[current_node.player_row + 1][current_node.player_col] != 'F') and (level_matrix[current_node.player_row + 1][current_node.player_col] != 'W'):
                p1 = Node(current_node, level_matrix, current_node.player_row+1, current_node.player_col, 1, 'D')
                successors.append(p1) 
            if (current_node.player_col + 1 < level_width-1) and (level_matrix[current_node.player_row][current_node.player_col+1] != 'W') and (level_matrix[current_node.player_row][current_node.player_col+1] != 'F'):
                p2 = Node(current_node, level_matrix, current_node.player_row, current_node.player_col+1, 1, 'R')
                successors.append(p2)
          
            if (current_node.player_row - 1 > 0) and (level_matrix[current_node.player_row - 1][current_node.player_col] != 'F') and (level_matrix[current_node.player_row - 1][current_node.player_col] != 'W'): 
                p3 = Node(current_node, level_matrix, current_node.player_row-1, current_node.player_col, 1, 'U')
                successors.append(p3)
            if (current_node.player_col - 1 > 0) and (level_matrix[current_node.player_row][current_node.player_col-1] != 'W') and (level_matrix[current_node.player_row][current_node.player_col-1] != 'F'):
                p4 = Node(current_node, level_matrix, current_node.player_row, current_node.player_col-1, 1, 'L')
                successors.append(p4)
           

            
            for i in successors:
                # If successor is goal, stop search
                if i.level_matrix[i.player_row][i.player_col] == 'A':
                    i.g = i.parent_node.g + i.depth
                    i.h = self.heuristic(i.player_row, i.player_col, apple_row, apple_column)
                    i.f = i.g + i.h
                    search = False
                    break
                
                i.g = i.parent_node.g + i.depth
                i.h = self.heuristic(i.player_row, i.player_col, apple_row, apple_column)
                i.f = i.g + i.h
                
                #sayac_closed_list = 0
                status = True
                for k in open_list.elements:
                    if (i.player_row == k[1].player_row) and (i.player_col == k[1].player_col) and (k[1].f < i.f):
                        status = False
                        break    
                    else:
                        status = True
                    
                if status == True:
                    for t in closed_list:
                        if (i.player_row == t.player_row) and (i.player_col == t.player_col) and (t.f < i.f):
                            status = False
                            break
                        else:
                            status = True


                if status == True:
                    open_list.put(i, i.f)
                    self.g_values[i.player_row][i.player_col] = i.g

            
            closed_list.append(current_node)
            
        
        

        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence
