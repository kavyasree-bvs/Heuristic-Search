#!/usr/bin/python

import sys
import copy
from program_generator import generate_initial_state
from program_generator import generate_goal_state
from operator import itemgetter

old_stdout = sys.stdout
log_file = open("message.log","w")
sys.stdout = log_file

n_blocks = int(sys.argv[1])
n_stacks = int(sys.argv[2])

def print_state(state):
	for i in range(n_stacks):
		print i+1, '|',
		for j in range(len(state[i])):
			print state[i][j],
		print ''
	print ''

class Node:
	def traceback(self): 
		if(self.parent!=None):
			self.parent.traceback()

		for i in range(n_stacks):
			print i+1, '|',
			for j in range(len(self.state[i])):
				print self.state[i][j],
			print ''
		print ''

	def __init__(self, parent_node, current_state):
	    self.parent = parent_node
	    self.state = current_state
	    if(self.parent==None):
	    	self.depth = 0
	    else:
	    	self.depth = self.parent.depth + 1

initial_state = generate_initial_state(n_blocks, n_stacks)
#initial_state= [['B'],['C', 'E'],['A', 'D']]
goal_state = generate_goal_state(n_blocks, n_stacks)

print 'initial state:'
print_state(initial_state)

def is_goal_state_reached(curr_state):
	if(curr_state == goal_state):
		return 1
	return 0

#Get coords
def get_coords(state):
	l = []
	for k in range(n_blocks):
		l.append([])
	for i in range(len(state)):
		for j in range(len(state[i])):
			for k in range(n_blocks):
				if(k == ord(state[i][j]) - 65):
					l[k]= [i,j]
	return l

goal_coords = get_coords(goal_state)

def h_1(state):
	coords = get_coords(state)
	h=0
	for i in range(len(coords)):
		if(coords[i] != goal_coords[i]):
			h=h+1
	return h

def h_2(state):
	coords = get_coords(state)
	h=0
	for i in range(len(coords)):
		if(coords[i] != goal_coords[i]):
			h=h+1
		if(i > 0 and i < len(coords) - 1):
			below = 0
			x=coords[i][0]
			y=coords[i][1]

			left = coords[i-1]
			right = coords[i+1]

			#check if below
			if(left == [x,y-1] or right == [x,y+1]):
				h = h
			else:
				h = h + 2
			#check if above
	return h

def h_3(state):
	coords = get_coords(state)
	#print 'coords', coords
	h=0
	for i in range(len(coords)):
		if(coords[i] != goal_coords[i]):
			h=h+1
		
		if(i > 0):
			# For example i ==> C
			desired_below_index = i - 1 # B
			'''
			print 'desired_below_index', desired_below_index
			print 'Present coordinates of i', coords[i]
			print 'Desired coordinates of i-1', goal_coords[desired_below_index] 
			print 'Present coordinates of i-1', coords[desired_below_index] #current coordinates of B
			'''

			# To Do: Figure out if currently B is exactly beneath C or not
			#Present coordinates of C
			curr_x = coords[i][0]
			curr_y = coords[i][1]

			#Present coordinates of B
			present_below_coords_x = coords[desired_below_index][0]
			present_below_coords_y = coords[desired_below_index][1]

			#Desired coordinates of B 
			desired_below_coords_x = goal_coords[desired_below_index][0]
			desired_below_coords_y = goal_coords[desired_below_index][1]
			
			#This heuristic adds 2 for every block that is not currently directly
			#on top of the block on which it has to be in the goal 
			#state or if there is such a block somewhere below it (in the same pile). 
			
			#Matters only if in the same row
			if(desired_below_coords_x == present_below_coords_x):
				#print '1'
				if(present_below_coords_y != curr_y -1):
					#print '2'
					if(present_below_coords_y < curr_y-1):
						#print '3'
						h = h+2
			else:
				h = h + 2
	return h	

def h_4(state):
	#Heuristic 4 - this heuristic is 
	#twice the number of blocks that must be moved once plus 
	#four times the number of blocks that must be moved twice. 
	
	#A block that must be moved once is a block that is currently on a block different to the block 
	#upon which it rests in the goal state or a block that has such a block somewhere below it in the same pile. 
	
	#A block that must be moved twice is a block that is currently on the block upon which it must be placed in the goal state, 
	#but that block is a block that must be moved or if there exists a block that must be moved twice somewhere below it (in the same pile).
	coords = get_coords(state)
	#print 'coords', coords
	h=0
	n_1 = 0
	n_2 = 0
	#for i in range(n_stacks):
		#if(coords[	])
	for i in range(len(coords)):
		if(coords[i] != goal_coords[i]):
			h=h+1
		
		if(i > 0 and i < len(coords) - 1):
			below = 0
			x=coords[i][0]
			y=coords[i][1]

			left = coords[i-1]
			right = coords[i+1]

			#check if below
			if(left == [x,y-1] or right == [x,y+1]):
				h = h
			else:
				h = h + 2
			#check if above
			''''''
		if(i > 0):
			# For example i ==> C
			desired_below_index = i - 1 # B

			# To Do: Figure out if currently B is exactly beneath C or not
			#Present coordinates of C
			curr_x = coords[i][0]
			curr_y = coords[i][1]

			#Present coordinates of B
			present_below_coords_x = coords[desired_below_index][0]
			present_below_coords_y = coords[desired_below_index][1]

			#Desired coordinates of B 
			desired_below_coords_x = goal_coords[desired_below_index][0]
			desired_below_coords_y = goal_coords[desired_below_index][1]

			#Matters only if in the same row
			if(desired_below_coords_x == present_below_coords_x):
				#print '1'
				if(present_below_coords_y != curr_y -1):
					#print '2'
					if(present_below_coords_y < curr_y-1):
						#print '3'
						#h = h+2
						n_1 = n_1 + 1
				else:
					#A block that must be moved twice is a block that is currently on the block upon which it must be placed in the goal state,
					if(coords[desired_below_index] != goal_coords[desired_below_index]):
						#but that block is a block that must be moved
						n_2 = n_2 +1
					else:
						#if there exists a block that must be moved twice somewhere below it (in the same pile).
						ii = desired_below_index
						cont = 1
						if(cont and ii > 0):
							# For example i ==> C
							desired_below_index_1 = ii - 1 # B

							# To Do: Figure out if currently B is exactly beneath C or not
							#Present coordinates of C
							curr_x_1 = coords[ii][0]
							curr_y_1 = coords[ii][1]

							#Present coordinates of B
							present_below_coords_x_1 = coords[desired_below_index_1][0]
							present_below_coords_y_1 = coords[desired_below_index_1][1]

							#Desired coordinates of B 
							desired_below_coords_x_1 = goal_coords[desired_below_index_1][0]
							desired_below_coords_y_1 = goal_coords[desired_below_index_1][1]

							#Matters only if in the same row
							if(desired_below_coords_x_1 == present_below_coords_x_1):
								#print '1'
								if(present_below_coords_y_1 != curr_y_1 -1):
									#print '2'
									if(present_below_coords_y_1 < curr_y_1-1):
										#print '3'
										#h = h+2
										n_2 = n_2 +1
										cont = 0
							else:
								n_2 = n_2 + 1
								cont = 0


			# placed exactly below
			#else:
			#	n_1 = n_1 +1
				#h = h + 2
	h = h + 2 * n_1 + 4 * n_2
	return h


def h_manhattan(state):
	coords = get_coords(state)
	h=0
	for i in range(len(coords)):
		if(coords[i] != goal_coords[i]):
			h = h + abs(coords[i][0] - goal_coords[i][0]) + abs(coords[i][1] - goal_coords[i][1])
	return h

def first_stack_check(state):
	coords = get_coords(state)
	cont = 1
	for i in range(len(state[0])):
		if(cont and coords[i] == goal_coords[i]):
			cont = 1
		else:
			cont = 0
	return cont

def successor(curr_node):
	curr_state = curr_node.state
	g_n = curr_node.depth +1 #because we are generating its children
	#print g_n
	states= []
	states_temp =[]
	for i in range(n_stacks):
		if(i==0 and first_stack_check(curr_state)):
			#skip the popping
			continue
		state_1 = copy.deepcopy(curr_state)
		if(len(state_1[i]) != 0):
			temp = state_1[i].pop()
			for j in range(n_stacks):
				state_2 = copy.deepcopy(state_1)
				if(j!=i):
					state_2[j].append(temp)
					#print 'here:',states_temp
					if(state_2 not in states_temp):
						states.append([state_2, g_n + h_4(state_2)])
						states_temp.append(state_2)

					if(is_goal_state_reached(state_2)):
						#print states
						return states
	#print states
	return states

#BFS
'''
states = []
nodes = []
states.append(initial_state)
Root = Node(None, initial_state)
nodes.append(Root)
i = 0
curr_state=initial_state
curr_node=Root
max_queue_size=0
max_queue_size = max(max_queue_size,len(states))
while(is_goal_state_reached(curr_state) == 0 or i > len(states)-1):
	max_queue_size = max(max_queue_size,len(states))
	print 'it=', i, ',', 'queue=', len(states), ',', 'depth= ', curr_node.depth
	print 'curr_state: ', curr_state
	print 'queue: \n', states, '\n'
	next_states = successor(curr_node)
	for j in range(len(next_states)):
		temp = next_states.pop(0)
		temp_node = Node(curr_node, temp[0])
		if(temp[0] not in states):
			states.append(temp[0])
			nodes.append(temp_node)
	#print i
	i = i+1
	curr_state = states[i]
	curr_node = nodes[i]
if(is_goal_state_reached(curr_state)):
	print 'success!', 'depth=', curr_node.depth, ',', 'total_goal_tests=', i, ',', 'max_queue_size=', max_queue_size
	print 'solution path:'
	curr_node.traceback()	
else:
	print 'error in finding goal path'
'''

#Out of place Algo
i = 0
max_queue_size = 0
states = []
nodes = []
pq = []
Root = Node(None, initial_state)
states.append(initial_state)
nodes.append(Root)
pq.append([initial_state, 0 + h_4(initial_state)])
max_queue_size = max(max_queue_size,len(pq))
curr_state = pq.pop(0)
curr_node = Root

node_count = 0
# Do until goal state is reached or queue becomes empty
while(is_goal_state_reached(curr_state[0]) == 0):
	#print 'curr_state', curr_state
	max_queue_size= max(max_queue_size,len(pq))
	print 'it=', i, ',', 'queue=', len(pq), ',', 'f=g+h=', curr_state[1], ',', 'depth= ', curr_node.depth
	next_states = successor(curr_node)
	#print 'next_states', next_states
	next_states = sorted(next_states, key = itemgetter(1))

	for j in range(len(next_states)):
		temp = next_states.pop(0)
		temp_node = Node(curr_node, temp[0])
		#print 'temp[0]',temp[0]
		#print 'states', states
		if(temp[0] not in states):
			states.append(temp[0])
			pq.append(temp)
			nodes.append(temp_node)
			node_count = node_count + 1
	pq = sorted(pq, key = itemgetter(1))
	#print 'pq', pq
	i = i+1
	#if(len(pq) != 0 ):
	curr_state = pq.pop(0)
	index=states.index(curr_state[0])
	curr_node = nodes[index]
	#else:
	#	break
	#print 'curr_state[0]', curr_state[0]

if(is_goal_state_reached(curr_state[0])):
	print 'success!', 'depth=', curr_node.depth, ',', 'total_goal_tests=', i, ',', 'max_queue_size=', max_queue_size
	print 'solution path:'
	curr_node.traceback()	
else:
	print 'error in finding goal path'

sys.stdout = old_stdout
log_file.close()
'''
if(is_goal_state_reached(curr_state[0])):
	print n_blocks, n_stacks, curr_node.depth, i, max_queue_size
	#print 'solution path:'
	#curr_node.traceback()	
else:
	print 'error in finding goal path'
'''