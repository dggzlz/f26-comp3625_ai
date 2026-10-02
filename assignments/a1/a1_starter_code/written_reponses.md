Write your answers to the following questions in this file, *after* completing everything else.

# 1) How many settings must be evaluated to *exhaustively* search for the best set (e.g. through some kind of brute-force search). State your assumptions and explain how you arrived at your answer. How does your solution compare to this (quantitatively)?

if we think about the problem, there are k possible values for the knobs, and we can have n knobs. Putting that in mathematical terms, this algorithm would take k^n settings to solve the problem. for a brute-force algorithm, if we don't set up the problem to be discrete, there would be an infinite number of values to select from, therefore take infinite time to solve the problem. in our case, our solution uses solves the problem by trying a random set of parameters multiple times, and for GA, we only need to run the algorithm by population size and number of generations (e.g., population size (p) = 100, and generations (g) = 50, then p * g = 5000). 

# 2) Why is the 10-knob problem harder than the 2-knob problem? (It may help you to know that the *mechanics* of both problems were the same: the relationship between settings and performance had the same general characteristics, there were just more settings to tune in the 10-knob problem).

Well, you can treat a search as a dimensional space. Inside a dimension we would need to compute a coordinate for n dimensions. For this we would need to compute a set of coordinates (e,g. [x, y, z, w, p,..., n]). The bigger the dimension, the more coordinates we need to compute. Time complexity then becomes O(k^n) and it will run exponentially. We know exponential time becomes really slow already with n=3, so to make that problem to run n=10 naturally takes longer to compute.

# 3) If your program was seen as an "agent program", which of the agent types discussed in class would it be?

In this case, we don't have a clear goal, and we are trying to maximize something, so this program would behave as an utility agent. 
Based on the slides we can describe P.E.A.S.:

- Performance: in this case we are trying to maximize translation rate, we can use this for the utility function.
- Environment: we can describe the knobs as the environment, where n knobs = n dimensions.
- Actuators: the agent can try many different settings for the knobs.
- Sensors: the agent can perceive the world by testing different settingws and getting back the decoding rate.

Based on this and since we don't have a clear goal, and we are trying to maximize something, so this program would behave as an utility agent.

# 4) it's often said that the simplest solution is the best. How well would a basic hill-climbing search perform in this problem? Justify your answer using your findings or plots from part 1 (you can answer this question whether or not you used hill-climbing as your approach). 

When looking at the plots, you can notice other maximas (local maximas) present in the plain. a basic hill-climbing solution would find one maxima look around, see that there isn't anything else around and stop the search, when in fact there are other better solutions.

# 5) When you moved from the 2- to the 10-knob problem, did you change your search algorithm? Why or why not?

We have a simulated annealing search algorithm for part 1 and it works really good. However; we had to move to a Genetic algorithm approach as simulated annealing was not working for the 10-knob problem. It all comes down to the dimension the problem presents. Simulated annealing follows one point in the space, by making the space bigger, the code just doesn't work. Genetic algorithms works really good in this case because you're throwing multiple points into the space.