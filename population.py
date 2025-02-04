# -*- coding: utf-8 -*-
"""
Population project
"""

# Aca voy a intentar

import numpy as np
import matplotlib.pyplot as plt

# crear una grid con cell values

GRID_SIZE = (1000, 900)

NUM_REGIONS = 11

grid = np.random.rand(*GRID_SIZE)

# visualizar la grid  y sus cell values
plt.imshow(grid, cmap='viridis', interpolation='nearest')
# la interpolation podria ser 'none' en vez de 'nearest', creo.

plt.colorbar()  # Adds a color bar to the side to show the value-to-color mapping
plt.title("Grid Visualization with Color Tones")
plt.show()

#Create the region grid (each cell stores a region ID)
region_grid = np.random.randint(1, NUM_REGIONS + 1, size=GRID_SIZE, dtype=np.uint8)