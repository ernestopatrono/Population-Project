# -*- coding: utf-8 -*-
"""
Population project
"""

# Aca voy a intentar
#Por ahora estoy  haciendo el codigo sin involucrar datos geograficos reales

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, binary_dilation

# crear una grid con cell values

GRID_SIZE = (60, 70)

#NUM_REGIONS representa ...
NUM_REGIONS = 2

#por ahora una grid de valores random en cada pixel, en vez d un mapa de poblacion
base_grid = np.random.rand(*GRID_SIZE)

#Create the region grid (each cell stores a region ID)
regions_grid = np.random.randint(1, NUM_REGIONS + 1, size=GRID_SIZE, dtype=np.uint8)

#pruebo definir una funcion para poder visualizar distintas grids juntas o separadas segun necesite
def visualize_grids(*grids, titles=None, cmap="tab10"):
    """
    Visualizes one or more grids.
    
    Parameters:
    - *grids: Multiple 2D NumPy arrays (grids) to visualize.
    - titles: List of titles for each grid (optional).
    - cmap: Colormap for visualization (default: 'tab10').
    """
    
    num_grids = len(grids)  # Count how many grids were provided

    if num_grids == 0:
        print("No grids provided for visualization.")
        return

    # Create subplots dynamically
    fig, axes = plt.subplots(1, num_grids, figsize=(6 * num_grids, 6))

    # Ensure axes is iterable (even if it's a single plot)
    if num_grids == 1:
        axes = [axes]

    # Loop through grids and display each one
    for i, grid in enumerate(grids):
        axes[i].imshow(grid, cmap=cmap, interpolation="nearest")
        # la interpolation podria ser 'none' en vez de 'nearest', creo.
        title = titles[i] if titles and i < len(titles) else f"Grid {i+1}"
        axes[i].set_title(title)
        axes[i].set_xticks([])
        axes[i].set_yticks([])

    # Add a shared color bar
    fig.colorbar(axes[0].imshow(grids[0], cmap=cmap), ax=axes, orientation="vertical", fraction=0.05, pad=0.05)

    plt.show()
    
#visualize_grids(base_grid, region_grid, titles=None, cmap="tab10")

#seteo una celda inicial donde empezaria a contar poblacion
SEED_CELL = (17,17)

seed_value = regions_grid[SEED_CELL]

#seteo un valor de "poblacion" que cada region debe tener
REGION_POP = 332

#lo siguiente es para probar la identificacion de el borde de una region:
def find_region_border(grid, region_value):
    # Step 1: Create a mask for the region (cells that have the same value)
    region_mask = grid == region_value
   
    # Step 2: Label connected regions in the mask
    labeled, num_features = label(region_mask)
   
    # Step 3: Dilate the region to expand it by one pixel
    dilated_region = binary_dilation(region_mask).astype(int)
    
    # Step 4: The border is the difference between the dilated region and the original region
    border_mask = dilated_region & ~region_mask
    
    # Get the coordinates of the border cells
    border_cells = np.argwhere(border_mask)
    
    return border_cells, border_mask

def find_region_containing_cell(grid, target_value, target_coords):
    """
    Finds the connected region that contains the target cell and its value.
    Also returns the border of that region if needed.
    """
    # Step 1: Create a mask for the target value
    region_mask = grid == target_value
    
    # Step 2: Label connected regions
    labeled, num_features = label(region_mask)
    
    # Step 3: Get the region label for the target cell
    target_label = labeled[target_coords[0], target_coords[1]]
    
    # Step 4: Find all cells that belong to the same region (same label)
    region_cells = (labeled == target_label)
    
    # Optionally, find the border of the region
    dilated_region = binary_dilation(region_cells)
    border_mask = dilated_region & ~region_cells
    
    return region_cells, border_mask, labeled

#para testear el border dettection arond la celda, doy el mismo valor a un rectangulo alreedor de la celda
region_size = 25
# Calculate the bounds, making sure they are clamped within the grid limits
start_row = max(SEED_CELL[0] - region_size // 2, 0)
end_row = min(SEED_CELL[0] + region_size // 2, regions_grid.shape[0])
start_col = max(SEED_CELL[1] - region_size // 2, 0)
end_col = min(SEED_CELL[1] + region_size // 2, regions_grid.shape[1])
# Assign value of the SEED to the rectangular region
regions_grid[start_row:end_row, start_col:end_col] = seed_value

region_cells, border_mask, labeled = find_region_containing_cell(regions_grid, seed_value, SEED_CELL)

# Step 2: Visualize the region and its border
bordered_region_grid = np.zeros_like(regions_grid)
bordered_region_grid[region_cells] = 1  # Mark the region cells with value 10
bordered_region_grid[border_mask] = 3  # Mark the border cells with value 5

visualize_grids(bordered_region_grid, titles=None, cmap="viridis")

#sugerencia para identificar el boundary de una region:
#For very sparse grids (where most cells have the same value), you might want to look into sparse matrices (e.g., using scipy.sparse) to reduce memory usage.