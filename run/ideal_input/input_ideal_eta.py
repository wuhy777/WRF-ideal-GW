import xarray as xr
import numpy as np
from pathlib import Path

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

	rd = 287.04
	g = 9.81
	cp = 1004.6
	cv = 717.6
	rvovrd = 1.608

	u = ds['ua_low'].values
	v = ds['va_low'].values
	t = ds['t_low'].values
	p = ds['p_low'].values / 100 # convert to hPa
	z = ds['geopt_low'].values / g
	q = ds['q_low'].values * 1000 # convert to g/kg
	theta = t * (1000 / p) ** 0.286

	z0 = z[0]
	p0 = p[0] * 100 # convert back to Pa
	theta0 = theta[0]
	q0 = q[0] / 1000 # convert back to kg/kg

	qvf = 1.0 + rvovrd * q0
	rho0 = 100000 / (rd * theta0 * qvf) * (p0 / 100000)**(cv/cp)

	dp = - g * rho0 * z0 * (1 + q0)
	psfc = p0 - dp
	
	q2 = q0 * 1000
	theta2 = 100000 / (rd * rho0 * qvf) * (psfc / 100000)**(cv/cp)

	psfc = psfc / 100

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

	pathdir = Path('/nfs/raid66/hywu/GWNN/experiments/gwnn/20260117_local_phys/data')
	paths = sorted(list(pathdir.glob('GWNNout*00.nc')))
	paths_train_1 = paths[1344:2208] # 2007-12-01 to 2007-12-09
	paths_train_2 = paths[2304:3168] # 2007-12-11 to 2007-12-19
	paths_train_3 = paths[3264:4128] # 2007-12-21 to 2007-12-29
	paths_train = paths_train_1 + paths_train_2 + paths_train_3 # train set (2007-12 except 2007-12-10 2007-12-20 2007-12-30)
	
	timeidx = 320
	south_north_idx = 10
	west_east_idx = 13
	path = paths_train[timeidx]
	ds = xr.open_dataset(path).isel(time=0, south_north=south_north_idx, west_east=west_east_idx)
	
	write_input_terrain(ds)
	write_input_sounding(ds)
	
if __name__ == "__main__":
	main()
