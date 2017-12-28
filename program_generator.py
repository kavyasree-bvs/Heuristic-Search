#!/usr/bin/python

import random
def generate_initial_state(n_blocks,n_stacks):
	A = 65
	blocks = []
	
	for i in range(n_blocks):
		blocks.append(A+i)
	random.shuffle(blocks)
	#print blocks

	initial_state =[]
	x = 0
	num = []
	for i in range(n_stacks):
		initial_state.append([])
		y = n_blocks-x
		if(i==n_stacks-1):
			z= n_blocks - x
		else:
			z = random.randint(0,y)
		#print z
		num.append(z)
		x = x+z
		for j in range(num[i]):
			initial_state[i].append(chr(blocks.pop()))

	return initial_state

def generate_goal_state(n_blocks,n_stacks):
	A = 65
	blocks = []
	
	for i in range(n_blocks):
		blocks.append(A+i)

	final_state =[]
	for i in range(n_stacks):
		final_state.append([])
	for j in range(n_blocks):
		final_state[0].append(chr(blocks[j]))
		
	return final_state