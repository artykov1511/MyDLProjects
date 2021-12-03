import time
import random
from copy import deepcopy
from agent import Agent
from operator import attrgetter

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
        self.rhs_value = 0
        
    
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h 
    
    def __eq__(self, other):
        return (self.player_row, self.player_col) == (other.player_row, other.player_col)
        

       

class PriorityQueue: 
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority[0], priority[1], item))
    
    def get(self):
        return heapq.heappop(self.elements)[2]

    def exists(self, other):
        for m in self.elements:
            if m[2] == other:
                return True
            else:
                return False
    
    def update(self, s, priority):
        for m in self.elements:
            if m[2] == s:
                idx = self.elements.index(m)
                list(self.elements[idx])[0] = priority[0]  
                list(self.elements[idx])[1] = priority[1]
                heapq.heapify(self.elements)
                
    def remove(self, s):
        for m in self.elements:
            if m[2] == s:
                idx = self.elements.index(m)
                self.elements[idx] = self.elements[-1]
                self.elements.pop()
                heapq.heapify(self.elements)

class DStarLiteAgent(Agent):

    def __init__(self):
        super().__init__()
        
        
        self.initialized = False
        self.U = 0   # PRIORITY QUEUE
        self.s_start = 0
        self.s_goal = 0
        self.s_last = 0
        self.level_matrix = 0
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
    
    
        
        
    def solve(self, level_matrix, player_row, player_column, changed_row=None, changed_column=None):
        super().solve(level_matrix, player_row, player_column)
        move_sequence = []

       

        initial_level_matrix = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        self.print_level_matrix(initial_level_matrix)

        level_height = len(initial_level_matrix)
        level_width = len(initial_level_matrix[0])
        (apple_row, apple_column) = self.find_apple_position(initial_level_matrix)
        self.level_matrix = initial_level_matrix
        
        if (not self.initialized):
            self.s_start = Node(0, self.level_matrix, player_row, player_column, self.INFINITY_COST, 0, 0)
            
            self.s_last = self.s_start
            self.Initialize(initial_level_matrix, level_height, level_width, apple_row, apple_column, player_row, player_column)
            self.initialized = True
            
            self.Compute_Shortest_Path(move_sequence)
            while self.s_start != self.s_goal:
                succ = self.Calculate_Predecessors(self.s_start)
                #tmp = [1 + i.depth for i in succ]
                tmp1 = [self.g_values[i.player_row][i.player_col] + 1 for i in succ]
                tmp2 = succ[tmp1.index(min(tmp1))]
                self.s_start = tmp2 #min(succ, key=attrgetter('depth'))    # RETURNS THE ELELEMNT WITH MIN G VALUE
                if self.s_start.chosen_dir != 0:
                    move_sequence.append(self.s_start.chosen_dir)

              


                
                
                
        else:
            #  initialization phase is already performed
            #  this means solve() is called once again because there is
            #a change detected in the map
           # super().solve(level_matrix, player_row, player_column)
            for a in range(len(level_matrix)):
                for b in range(len(level_matrix[0])):
                    if level_matrix[a][b] == 'P':
                        self.s_start.player_row = a
                        self.s_start.player_col = b
                        
                        self.s_start.chosen_dir = 0
                        


            print("Solve called again because a new obstacle appeared at position:(", changed_row, ",", changed_column, ")")
            girdi = False
            sayac = 0
            while self.s_start != self.s_goal: 
                if sayac != 0:
                    succ = self.Calculate_Predecessors(self.s_start)
                    tmp1 = [self.g_values[i.player_row][i.player_col] + 1 for i in succ]
                    tmp2 = succ[tmp1.index(min(tmp1))]
                    self.s_start = tmp2 #min(succ, key=attrgetter('depth'))    # RETURNS THE ELELEMNT WITH MIN G VALUE
                
                if self.s_start.chosen_dir != 0:
                    move_sequence.append(self.s_start.chosen_dir)

                  
                if changed_row != -1 and not girdi:
                   
                    self.k_m = self.k_m + self.heuristic(self.s_last.player_row, self.s_last.player_col, self.s_start.player_row, self.s_start.player_col)
                    self.s_last = self.s_start
                    changed_node = Node(0, self.level_matrix, changed_row, changed_column, 0,0,0)
                    succ = self.Calculate_Predecessors(changed_node)
                    
                    for i in succ:
                        c_old = 1
                        c_new = self.INFINITY_COST
                        self.Update_Vertex(i)
                    girdi = True
                    self.Compute_Shortest_Path(move_sequence)
                sayac += 1
              
       
        return move_sequence
    
    

    def Initialize(self, level_matrix, level_height, level_width, apple_row, apple_column, player_row, player_col):
        self.U = PriorityQueue()
        self.k_m = 0
        self.g_values = [ [self.INFINITY_COST]*level_width for i in range(level_height) ]
        self.rhs_values = [ [self.INFINITY_COST]*level_width for i in range(level_height) ]
        self.rhs_values[apple_row][apple_column] = 0
        self.s_goal = Node(0, level_matrix, apple_row, apple_column, self.INFINITY_COST, 0, 0)                      # DEPTH, CHOSEN_DIR AND H_VALUE WAS SET TO ZERO. REVISE THIS!!!
        self.U.put(self.s_goal, self.Calculate_Key(self.s_goal))
    

    def Calculate_Key(self, s):
        s_start = self.s_start
        heuristic_start_s = self.heuristic(s_start.player_row, s_start.player_col, s.player_row, s.player_col)
        tempr1 = min(self.g_values[s.player_row][s.player_col], self.rhs_values[s.player_row][s.player_col]) + heuristic_start_s + self.k_m
        tempr2 = min(self.g_values[s.player_row][s.player_col], self.rhs_values[s.player_row][s.player_col]) 
        return [tempr1, tempr2]

    def Update_Vertex(self, u):
        if u != self.s_goal:
            succ = self.Calculate_Predecessors(u) 
            tmp = [1+self.g_values[i.player_row][i.player_col] for i in succ]
            self.rhs_values[u.player_row][u.player_col] = min(tmp)
    
        if self.U.exists(u):
            self.U.remove(u)
        if (self.g_values[u.player_row][u.player_col] != self.rhs_values[u.player_row][u.player_col]):            
             self.U.put(u, self.Calculate_Key(u))  
    def Compute_Shortest_Path(self, move_sequence):
    
        while (list(self.U.elements[0][0:2]) < self.Calculate_Key(self.s_start) ) or (self.rhs_values[self.s_start.player_row][self.s_start.player_col] != self.g_values[self.s_start.player_row][self.s_start.player_col]):
            k_old = [self.U.elements[0][0], self.U.elements[0][1]]
            u = self.U.get()
            k_new = self.Calculate_Key(u)
            if k_old < k_new:
                self.U.put(u, k_new)          
                  
            elif self.g_values[u.player_row][u.player_col] > self.rhs_values[u.player_row][u.player_col]:
                self.g_values[u.player_row][u.player_col] = self.rhs_values[u.player_row][u.player_col]
                
                for t in self.Calculate_Predecessors(u):
                    self.Update_Vertex(t)
                
            else:
                self.g_values[u.player_row][u.player_col] = self.INFINITY_COST
                pred_u = self.Calculate_Predecessors(u)
                pred_u.append(u)
                c_s_u = [1] * (len(pred_u)-1)
                c_s_u.append(0)
                for idx, el in enumerate(pred_u):
                    self.Update_Vertex(el)
            




    def Calculate_Predecessors(self, s):
        pred = []
        if self.level_matrix[s.player_row + 1][s.player_col] != 'W':
            s1 = Node(s, self.level_matrix, s.player_row + 1, s.player_col, s.depth+1, 'D', 0)   
            pred.append(s1)
        if self.level_matrix[s.player_row][s.player_col + 1] != 'W':
            s2 = Node(s, self.level_matrix, s.player_row, s.player_col+1, s.depth+1, 'R', 0)
            pred.append(s2)
        if self.level_matrix[s.player_row - 1][s.player_col] != 'W':
            s3 = Node(s, self.level_matrix, s.player_row-1, s.player_col, s.depth+1, 'U', 0)
            pred.append(s3)
        if self.level_matrix[s.player_row][s.player_col - 1] != 'W':
            s4 = Node(s, self.level_matrix, s.player_row, s.player_col-1, s.depth+1, 'L', 0)
            pred.append(s4)
        return pred
    


    

    def on_encounter_obstacle(self):
        
        pass
