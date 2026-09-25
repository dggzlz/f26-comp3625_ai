from translator import UniversalTranslator
import numpy as np


# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

# demo of how to use the UniversalTranslator object. You can delete these lines
sample_settings = list(np.random.uniform(0, 1, size=2))
translated_string = mysim_annealing(translator.translate, sample_settings)
print(translated_string)

# print total number of settings evaluated
print(f'# settings tried: {translator.n_settings_tried()}')