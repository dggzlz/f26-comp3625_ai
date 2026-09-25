from translator import UniversalTranslator
import numpy as np

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

# demo of how to use the UniversalTranslator object. You can delete these lines
# sample_settings = [0.2, 0.5]
# translated_string = translator.translate(sample_settings)
# print(translated_string) 

# print total number of settings evaluated
#print(f'# settings tried: {translator.n_settings_tried()}')

#Simulated Annealing 

# Random Array of Two values between 0 and 1
rng = np.random.default_rng()
settings = rng.random(size=2)
#settings = [0.2, 0.7]

reward = 0
translated_string = translator.translate(settings)
segments = translated_string.split()

for code in segments: 
  if code.isalpha(): 
    reward += 1  

print(f"{segments}\n")

print(f"Settings: {settings}")

#Item Count
print(f"Amount of Segmented Words (Constant): {len(segments)}")

#Character Count
print(f"Amount of characters {len(translated_string)}") 

print(f"Amount of words decoded from Segment {reward}")

print(f"Percentage of Words Decoded: {(reward / len(segments)) * 100}")