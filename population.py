# -*- coding: utf-8 -*-

"""
Trying to recreate this:
https://www.vox.com/2015/5/27/8668967/world-population-map
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, binary_dilation

def population():
    '''
    Loads the 2d array to use as base.
    '''
    data = np.load('array_from_tif.npy')
    return data

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
    
def visualize_overlay(base_grid, overlay_grid,
base_cmap="Greys", overlay_cmap="viridis",
overlay_alpha=0.5, title="Overlay Plot"):
    """
    Displays base_grid and overlay_grid on top of each other.
    Parameters:
    base_grid (np.ndarray): The background dataset.
    overlay_grid (np.ndarray): The dataset to overlay on top of the base.
    base_cmap (str): Colormap for the base grid.
    overlay_cmap (str): Colormap for the overlay grid.
    overlay_alpha (float): Transparency level for the overlay (0.0 to 1.0).
    title (str): Title for the plot.
    """

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8,8))
    
    # Display the base grid. (This layer is fully opaque.)
    base_im = ax.imshow(base_grid, cmap=base_cmap)
    
    # Overlay the second grid on top with specified transparency.
    overlay_im = ax.imshow(overlay_grid, cmap=overlay_cmap, alpha=overlay_alpha)
    
    # Optionally add a title and colorbars for clarity
    ax.set_title(title)
    plt.colorbar(base_im, ax=ax, fraction=0.046, pad=0.04, label="Base Values")
    plt.colorbar(overlay_im, ax=ax, fraction=0.046, pad=0.04, label="Overlay Values")
    
    plt.show()
    
def find_region_containing_cell(grid, target_value, target_coords):
    """
    Finds the connected region that contains the target cell and its value.
    Also returns the border of that region if needed.
    """
    #sugerencia para identificar el boundary de una region:
    #For very sparse grids (where most cells have the same value), you might want to look into sparse matrices (e.g., using scipy.sparse) to reduce memory usage.
 
    
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
    #Nota: esta dilatacion es en cruz, nosea no agrega esquinas diagonales, mas adelante puedo implelentar que agregue pi/4 de las esuqinas que encuentre.
    #Tambien tengo que considerar el area terrestre que cada celda cubre y quizas ajustar la dilatacion de acuerdo con eso asi es realmente uniforme.
    
    border_mask = dilated_region & ~region_cells

    return region_cells, border_mask, labeled

def find_pixel(boundary, field, population):
    rows, cols = np.where(boundary)
    #aca elijo tomar el pixel con el valor base mas cercano a cierto dado como argumento
    selected_floats = field[rows, cols]
    valid_floats = selected_floats[~np.isnan(selected_floats)]
    deviations = np.abs(valid_floats - population)
    index_min_dev_previo = np.argmin(deviations)
    float_indicado = valid_floats[index_min_dev_previo]
    index_min_dev = np.where(selected_floats == float_indicado)[0][0]
    coordinates = rows[index_min_dev], cols[index_min_dev]
    return coordinates

if __name__ == '__main__':
    
    data = population()
    GRID_SIZE = data.shape
    base_grid = data

    #seteo una celda inicial donde empezaria a contar poblacion
    SEED_CELL = (131,111)
    
    #seteo un valor de "poblacion" que cada region debe tener
    REGION_POP = base_grid[SEED_CELL]
    
    #Create the region grid (each cell stores a region ID)
    regions_grid = np.zeros_like(base_grid)
    
    seed_value = 1
    regions_grid[SEED_CELL] = seed_value
    
    region_cells, border_mask, labeled = find_region_containing_cell(regions_grid, seed_value, SEED_CELL)
    
    value_region = seed_value
    value_border = seed_value + 1  
    
    #intento loopearlo
    i=0
    density = REGION_POP
    while True:
        #print(density)
        i+=1
        pops = base_grid[region_cells]
        density = np.mean(pops)
        new_pixel = find_pixel(border_mask, base_grid, density)
        if np.isnan(base_grid[new_pixel]):
            print('NaN',base_grid[new_pixel])
            print('density= ',density)
            break
        #print(new_pixel)
        #print(base_grid[new_pixel])
        regions_grid[new_pixel] = value_region
        #print(density)
        region_cells, border_mask, labeled = find_region_containing_cell(regions_grid, seed_value, SEED_CELL)
        if np.any(np.isnan(base_grid[region_cells])):
            print('el borde detector me esta definiendo la region agregando algun nan')
        regions_grid[region_cells] = value_region  # Mark the region cells with value 10
        regions_grid[border_mask] = value_border  # Mark the border cells with value 5
        if i%15 == 0:
            visualize_overlay(base_grid, regions_grid)
            #visualize_grids(base_grid, regions_grid, titles=None, cmap="cividis")
            