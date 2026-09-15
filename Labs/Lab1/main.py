# COMP 3625: Artificial Intelligence
# Lab 1 - Search
# Instructor: Eric Chalmers
# Author: Diego Gonzalez Reyes
# Student ID: 201724348
# Mount Royal University
from queue import Queue

#===========Task 1: Identify a suitable search algorithm=========
"""
To me, Breadth-first search (BFS) is the most suitable search algorithm for this problem. 
BFS explores all the nodes at the present depth level before moving on to the nodes at the next depth level. 
Because this is a six degrees of separation problem, BFS is sufficient for both speed and space.
"""

#==========Task 2: Implement a search algorithm==============

def bfs():
    return
# function breadth_first_search(problem) -> goal_state or failure
# 	if problem.is_goal(problem.initial) then return problem.initial
# 	frontier ← a FIFO queue
# 	frontier.add(problem.initial)
# 	reached ← {problem.initial)
# 	while not frontier.empty()
# 		state ← frontier.pop()
# 		for each child in expand(state)
# 			if problem.is_goal(child) then return child
# 			if child not in reached then
# 				reached.add(child)
# 				frontier.add(child)
# return failure	