# Testing how it works
# Random Array of Two values between 0 and 1
#settings = [0.2, 0.7]
from translator import UniversalTranslator
import numpy as np

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=10) 

rng = np.random.default_rng()
settings=rng.random(size=2)

# reward = 0
# translated_string = translator.translate(settings)
# print(translated_string)
# segments = translated_string.split()
# for code in segments: 
#   if code.isalpha(): 
#     reward += 1  

# #print(f"{segments}\n")
# #print(f"Settings: {settings}")

# print(f"Amount of Segmented Words (Constant): {len(segments)}")

# print(f"Amount of characters {len(translated_string)}") 
# print(f"Amount of words decoded from Segment {reward}")
# print(f"Percentage of Words Decoded: {(reward / len(segments)) * 100}")

# 76% - [0.14726682, 0.5843318]
current = [0.2, 0.4]
choice = np.random.rand(len(settings)) * 0.085
print(choice) 
if np.random.random() > .5:
  next = current - choice
else: 
  next = current + choice  

print(next)