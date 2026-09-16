"""
Your name(s):
Diego Gonzalez Reyes - 201724348
Tarun Jaswal - 201720549
John Galang - 201719861
"""

from nodes import WikiPage
from queue import Queue

# change the start and destination pages as you like - see if your algorithm can find a route between them
start = WikiPage('https://en.wikipedia.org/wiki/Breadth-first_search')
# # goal = WikiPage('https://en.wikipedia.org/wiki/New_York_City')
goal = WikiPage('https://en.wikipedia.org/wiki/Computation')

# start = WikiPage('https://en.wikipedia.org/wiki/Mount_Royal_University')
# goal = WikiPage('https://en.wikipedia.org/wiki/Artificial_intelligence')

# What search algorithm are you using? Why?
# (your response here)
"""
We decided to do BFS, for a few reasons:

- because first of all, garuantees to find the shortest path, 
- We think the computation requires is minimal, so we dont wanna complicate ourselves, 
- we still think the memory requirements are still minimal.
"""

# Does your code work? (Verify the route found by your search algorithm)

def bfs(start, goal):
    if start == goal:
        return start
    # initialize queue and queue in the start
    frontier = Queue()
    frontier.put(start)
    
    reached = [start]
    
    while not frontier.empty():
        state = frontier.get()
        children = state.children
        for child in children:
            if child == goal:
                return child
            if child not in reached:
                reached.append(child)
                frontier.put(child)
    return False


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



# YOUR SEARCH ALGORITHM CODE HERE
# (print the discovered route when you find it)


path = bfs(start, goal)

print("\nPATH TO GET FROM START TO GOAL")
print(path.get_ancestors())
print("\nLENGTH OF THE PATH =", len(path.get_ancestors()))



# Can you think of a search approach that could be faster than your implementation above?
# Describe it.