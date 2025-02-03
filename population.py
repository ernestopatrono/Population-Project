# -*- coding: utf-8 -*-
"""
Population project
"""

#Aca voy a intentar

import numpy as np
import matplotlib.pyplot as plt


GRID_SIZE = (1000, 900)

grid = np.random.rand(*GRID_SIZE)

plt.imshow(grid, cmap='viridis', interpolation='nearest')
plt.colorbar()  # Adds a color bar to the side to show the value-to-color mapping
plt.title("Grid Visualization with Color Tones")
plt.show()