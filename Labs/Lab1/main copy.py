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
# goal = WikiPage('https://en.wikipedia.org/wiki/New_York_City')
goal = WikiPage('https://en.wikipedia.org/wiki/Computation')

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
        return [start]
    # initialize queue and queue in the start
    frontier = Queue()
    frontier.put(start)
    
    reached = [start]
    
    while not frontier.empty():
        state = frontier.get()
        children = state.children
        for child in children:
            # print(f"child: {child}, goal: {goal}")
            if child == goal:
                return reached
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



# # YOUR SEARCH ALGORITHM CODE HERE
# # (print the discovered route when you find it)

# # instantiate an object representing a particular wiki page:
# page = WikiPage('https://en.wikipedia.org/wiki/Mount_Royal_University')


# # by default, the object is not expanded, meaning we don't know what its children are
# print(page)    # prints "Mount_Royal_University (not expanded)"


# # accessing the children attribute expands the page
# children = page.children  # returns a list of new WikiPage objects, accessible from page
# print(page)  # now prints "Mount_Royal_University (N children)"

# # calling get_ancestors() returns a list of pages along the path to the page
# child_0 = children[0]
# print("ANCESTORS")
# print(child_0.get_ancestors())  # prints a list of pages along the route

# # two page objects can be checked for equality
# destination = WikiPage("https://en.wikipedia.org/wiki/Artificial_intelligence")
# page == destination  # False


path = bfs(start, goal)

if path != False:
    print(path)



# Can you think of a search approach that could be faster than your implementation above?
# Describe it.