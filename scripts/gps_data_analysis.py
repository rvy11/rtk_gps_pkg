#!/usr/bin/python3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot
import numpy as np
import csv
import argparse
from scipy import stats

if __name__ == "__main__":
	time = []
	utm_north = []
	utm_east = []
	parser = argparse.ArgumentParser(description="Analyze GPS data")
	parser.add_argument("path", help="path to GPS data CSV file")
	parser.add_argument("-d", help="plot dimension", default="2")
	args = parser.parse_args()

	with open(args.path) as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			time.append(row['%time'])
			utm_north.append(row['field.utm_north'])
			utm_east.append(row['field.utm_east'])

	north = np.array(list(map(float, utm_north)))
	east = np.array(list(map(float, utm_east)))
	time = np.array(list(map(float, time))) / 1_000_000_000

	print("north mean:", np.mean(north))
	print("north std:", np.std(north))
	print("east mean:", np.mean(east))
	print("east std:", np.std(east))

	print("north diff:", np.max(north)-np.min(north))
	print("east diff:", np.max(east)-np.min(east))


	# 42.339637, -71.088449, 327959, 4689599
	# 42.337210, -71.090214, 327807, 4689333
	# tru_east = 327959-np.mean(east)
	# tru_north = 4689599-np.mean(north)
	tru_east = 327807-np.mean(east)
	tru_north = 4689333-np.mean(north)

	print("true east diff:", tru_east)
	print("true north diff:", tru_north)

	north = north - np.min(north)
	east = east - np.min(east)
	time = time - np.min(time)
	
	slope, intercept, r_value, p_value, std_err = stats.linregress(east, north)
	print("linear regression: slope = %.4f, intercept = %.4f, r_value = %.4f, p_value = %.4f, std_err = %.4f" % (slope, intercept, r_value, p_value, std_err))

	y_line = intercept+slope*east

	y_err = north - y_line
	print("min %.4f, max %.4f"%(min(y_err), max(y_err)))

	dim = int(args.d)
	fig = plot.figure()
	if dim == 3:
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(east, north, time)
		# ax.plot(east, intercept+slope*east, '-')
		ax.set_xlabel('Relative Easting (m)')
		ax.set_ylabel('Relative Northing (m)')
		ax.set_zlabel('Time (s)')
	else:
		ax = fig.add_subplot(111)
		ax.scatter(east, north, marker="+")
		# 42.337202, -71.090221
		# ax.scatter([tru_east], [tru_north], marker="x", color="r")
		# ax.plot(east, intercept+slope*east, '-', color='r')	
		ax.set_xlabel('Relative Easting (m)')
		ax.set_ylabel('Relative Northing (m)')
		# ax2 = fig.add_subplot(111)
		# ax2.scatter(time, y_err)
		# ax2.plot(time, y_err*0, '-', color='r')
		# ax2.set_xlabel('Time (s)')
		# ax2.set_ylabel('Northing Error (m)')

	# fig.savefig('a.png')
	plot.show()

