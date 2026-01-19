# %%
import numpy as np
import matplotlib.pyplot as plt

# %%
def save_terrain_to_file(terrain_array: np.ndarray, filename: str ='input_terrain'):
	"""
	Save a 2D terrain array to a text file.
	
	Parameters:
	terrain_array (np.ndarray): 2D array representing the terrain.
	filename (str): Name of the file to save the terrain data. Defaults to 'input_terrain'.
	"""
	
	# Check if the input is a 2D numpy array
	if terrain_array.ndim != 2:
		raise ValueError("Input terrain_array must be a 2D numpy array.")
	
	# Obtain the dimensions of the terrain array
	# Notice that numpy uses row-major order (rows, columns) -> (NY, NX)
	ny, nx = terrain_array.shape

	print(f"Terrain size: NX = {nx}, NY = {ny}")
	print(f"Saving terrain to file: {filename}")

	with open(filename, 'w') as file:
		# Write the dimensions as the first line
		file.write(f"{nx} {ny}\n")
		
		# Write the terrain data
		np.savetxt(file, terrain_array, fmt='%.4f', delimiter=' ')
	
	print("Terrain data saved successfully.")

# %%
if __name__ == "__main__":
	# Define terrain dimensions and resolution
	NX, NY = 501, 501
	delta = 4000 # units: meters
	# Create grid coordinates
	x = np.linspace(-(NX-1)*delta/2, (NX-1)*delta/2, NX)
	y = np.linspace(-(NY-1)*delta/2, (NY-1)*delta/2, NY)
	X, Y = np.meshgrid(x, y)
	
	# Generate a bell-shaped mountain
	sigma = 50000 # units: meters
	hm = 10 # units: meters
	z = hm * (1+((X/sigma)**2 + (Y/sigma)**2))**(-3/2)

	# Save the generated terrain to a file
	# save_terrain_to_file(z, filename='input_terrain')


