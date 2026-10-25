"""
Your name(s):
Edwin Pang           - 201729758
John Galang          - 201719861
Tarun Jaswal         - 201720549
Diego Gonzalez Reyes - 201724348
"""

from nodes import WikiPage
from queue import Queue

# change the start and destination pages as you like - see if your algorithm can find a route between them
start = WikiPage('https://en.wikipedia.org/wiki/Breadth-first_search')
goal = WikiPage('https://en.wikipedia.org/wiki/Partial_differential_equation')

# What search algorithm are you using? Why?
# (your response here)
"""
We decided to use BFS, for a few reasons:

- Because first of all, garuantees to find the shortest path. 
- We think the computation required is minimal, so we don't wanna complicate ourselves with more complex algorithms. 
- We also considered DFS, but as mentioned in class DFS can get stuck in cycles
  and the problem's structure is not of a tree.
"""

# Does your code work? (Verify the route found by your search algorithm)
"""
YES, we tested our implementation multiple times, with different start & goal values, 
and verified the routes taken by the agent.
"""

# YOUR SEARCH ALGORITHM CODE HERE
# (print the discovered route when you find it)
def bfs(start, goal):
    if start == goal:
        return start
    
    # initialize queue
    frontier = Queue()
    frontier.put(start)
    
    reached = [start]
    
    while not frontier.empty():
        state = frontier.get() # pop next item in queue
        children = state.children
        for child in children:
            if child == goal:
                return child
            if child not in reached:
                reached.append(child)
                frontier.put(child)
    return WikiPage(state=None)

route = bfs(start, goal)

if route.state != None:
    print("\nROUTE TO GET FROM START TO GOAL")
    print(route.get_ancestors())
    print("\nLENGTH OF THE ROUTE =", len(route.get_ancestors()))

# Can you think of a search approach that could be faster than your implementation above?
# Describe it.

"""
A faster implementation would be to use bidirectional BFS, meaning we search starting from both the start and goal,
hoping that both would intersect to find a common page to each other which would still return the shortest path.
This would technically cut the time to half at worst case. 
"""