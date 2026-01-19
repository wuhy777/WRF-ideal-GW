import xarray as xr
import numpy as np

def write_input_terrain(ds):
	
	ter_high = ds['terrain_high_coarse'].values
	ter_low = ds['terrain_low_coarse'].values
	
	ny, nx = 501, 501
	ny_s, nx_s = ter_high.shape
	ter = np.full((ny, nx), ter_low)

	start_y = (ny - ny_s) // 2
	start_x = (nx - nx_s) // 2
	end_y = start_y + ny_s
	end_x = start_x + nx_s

	ter[start_y:end_y, start_x:end_x] += ter_high

	with open('input_terrain', 'w') as file:
		# Write the dimensions as the first line
		file.write(f"{nx} {ny}\n")
		
		# Write the terrain data
		np.savetxt(file, ter, fmt='%.4f', delimiter=' ')

	print("input_terrain file has been created.")

def write_input_sounding(ds):
	
	psfc = ds['psfc_low'].values / 100
	t2 = ds['t2_low'].values
	q2 = ds['q2_low'].values * 1000
	theta2 = t2 * (1000 / psfc) ** 0.286

	u = ds['ua_low'].values
	v = ds['va_low'].values
	t = ds['t_low'].values
	p = ds['pressure'].values / 100
	z = ds['geopt_low'].values / 9.81
	q = ds['q_low'].values * 1000
	theta = t * (1000 / p) ** 0.286

	with open('input_sounding', 'w') as file:
		# Write surface data
		file.write(f"{psfc:10.4f} {theta2:10.4f} {q2:10.4f}\n")

		# Write the profile data
		for k in range(len(p)):
			line = (
				f"{z[k]:10.4f} "
				f"{theta[k]:10.4f} "
				f"{q[k]:10.4f} "
				f"{u[k]:10.4f} "
				f"{v[k]:10.4f} "
			)
			file.write(line + "\n")

	print("input_sounding file has been created.")

def main():

	timeidx = 42
	south_north_idx = 17
	west_east_idx = 13
	ds = xr.open_dataset('/nfs/raid66/hywu/GWNN/data/04_gwnn_out/local/ds_train_2007_interp.nc').isel(time=timeidx, south_north=south_north_idx, west_east=west_east_idx)
	
	ds = ds.dropna(dim='pressure')
	write_input_terrain(ds)
	write_input_sounding(ds)
	
if __name__ == "__main__":
	main()
