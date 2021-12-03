import time
import random
from copy import deepcopy
from agent import Agent


#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque

#from queue import PriorityQueue

COUNT = 0

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

        self.f = depth + h_value
        self.counter = 0
        
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h and self.h < other.h #self.h < other.h and self.counter > other.counter #
    
    def __eq__(self, other):
        return (self.player_row, self.player_col) == (other.player_row, other.player_col)



class PriorityQueue: 
    def __init__(self):
        self.elements = []
        
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        global COUNT
        COUNT += 1
        item.counter = COUNT
        heapq.heappush(self.elements, (priority[0], priority[1], item))
    
    def get(self):
        return heapq.heappop(self.elements)[2]


class AStarAgent(Agent):

    def __init__(self):
        super().__init__()
        
        #  g cost in A*
        #    IMPORTANT NOTE!!!
        #please fill values inside this array
        #as you perform the A* search!
        self.g_values = []
        #self.s_start = 0
        
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
        s_start = Node(0, initial_level_matrix, player_row, player_column, 0, 0, initial_heuristic)
        open_list.put(s_start, (s_start.f, s_start.h))

        search = True
        level_matrix = initial_level_matrix
        
        while not open_list.empty() and search:
            # Choose the node with least f value
            current_node = open_list.get()
            self.expanded_node_count += 1
        
           
            # Update the level matrix
            level_matrix[current_node.player_row][current_node.player_col] = 'P'
            
            # Update g values
            self.g_values[current_node.player_row][current_node.player_col] = current_node.depth
            
            if current_node.chosen_dir != 0:
                move_sequence.append(current_node.chosen_dir)

            successors = []
            # Determine successors of the current node
            if  (level_matrix[current_node.player_row + 1][current_node.player_col] != 'W'):  # (current_node.player_row + 1 < level_height-1) 
                p1 = Node(current_node, level_matrix, current_node.player_row+1, current_node.player_col, current_node.depth+1, 'D', 0)
                successors.append(p1) 
            if (level_matrix[current_node.player_row][current_node.player_col+1] != 'W'):  # (current_node.player_col + 1 < level_width-1) and 
                p2 = Node(current_node, level_matrix, current_node.player_row, current_node.player_col+1, current_node.depth+1, 'R', 0)
                successors.append(p2)
          
            if (level_matrix[current_node.player_row - 1][current_node.player_col] != 'W'):  # (current_node.player_row - 1 > 0) and 
                p3 = Node(current_node, level_matrix, current_node.player_row-1, current_node.player_col, current_node.depth+1, 'U', 0)
                successors.append(p3)
            if (level_matrix[current_node.player_row][current_node.player_col-1] != 'W'):  # (current_node.player_col - 1 > 0) and 
                p4 = Node(current_node, level_matrix, current_node.player_row, current_node.player_col-1, current_node.depth+1, 'L', 0)
                successors.append(p4)
           
	        			
            self.generated_node_count += len(successors)
            self.maximum_node_in_memory_count += len(open_list.elements)
            
            for i in successors:
                # If successor is goal, stop search
                if level_matrix[i.player_row][i.player_col] == 'A':
                    move_sequence.append(i.chosen_dir)
                    search = False
                    break
		   
               
                
                if i not in closed_list:
                    i.f = i.depth = self.INFINITY_COST
                if i.depth > current_node.depth + 1:
                    i.depth = current_node.depth + 1
                    i.h = self.heuristic(i.player_row, i.player_col, apple_row, apple_column)
                    open_list.put(i, (i.f, i.h))    
                

            
            closed_list.append(current_node)
                                


		
		
		   

       
	 
	        
	       
            
            
            
        
        

        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence
