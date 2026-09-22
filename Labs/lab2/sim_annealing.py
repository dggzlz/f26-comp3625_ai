# function simulated_annealing(f, start, n) returns a solution state
# 	current ← start
# 	for T decreasing to 0 over n iterations:
# 		next ← a randomly selected successor of current
# 		ΔE ← f(next) - f(current)
# 		if ΔE < 0 then current ← next
# 		else current ← next with probability e-ΔE/T
