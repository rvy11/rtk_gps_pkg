#!/usr/bin/python3
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
from scipy import stats

if __name__ == "__main__":
	time = []
	utm_north = []
	utm_east = []
	fix = []
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
			fix.append(row['field.fix'])

	north = np.array(list(map(float, utm_north)))
	east = np.array(list(map(float, utm_east)))
	time = np.array(list(map(float, time))) / 1_000_000_000


	rel_north = north - np.min(north)
	rel_east = east - np.min(east)
	rel_time = time - np.min(time)

	# # North
	# rel_north_outlier_rm = []
	# time_rel_north_outlier_rm = []

	# for i in range(len(rel_north)):
	# 	if rel_north[i] < 500.0:
	# 		rel_north_outlier_rm.append(rel_north[i])
	# 		time_rel_north_outlier_rm.append(rel_time[i])

	# fig1 = plt.figure(1);
	# plt.scatter(time_rel_north_outlier_rm, rel_north_outlier_rm)

	# print("mean: %.4f"%(np.mean(rel_north_outlier_rm)))

	# f3 = plt.figure(3)

	# plt.hist(rel_north_outlier_rm-np.mean(rel_north_outlier_rm), bins="auto")
	# plt.title("Error in Relative Northing, RTK Fixed")
	# plt.xlabel("Error (m)")
	# plt.ylabel("Samples")

	# # East
	# rel_east_outlier_rm = []
	# time_rel_east_outlier_rm = []

	# for i in range(len(rel_east)):
	# 	if rel_east[i] < 500.0:
	# 		rel_east_outlier_rm.append(rel_east[i])
	# 		time_rel_east_outlier_rm.append(rel_time[i])

	# fig1 = plt.figure(4);
	# plt.scatter(time_rel_east_outlier_rm, rel_east_outlier_rm)

	# print("mean: %.4f"%(np.mean(rel_east_outlier_rm)))

	# f3 = plt.figure(5)

	# plt.hist(rel_east_outlier_rm-np.mean(rel_east_outlier_rm), bins="auto")
	# plt.title("Error in Relative Easting, RTK Fixed")
	# plt.xlabel("Error (m)")
	# plt.ylabel("Samples")
	

	# north (moving)
	rel_north_moving = []
	time_rel_north_moving = []

	for i in range(len(rel_time)):
		if rel_time[i] > 5.0 and rel_time[i] < 15.0:
			rel_north_moving.append(rel_north[i])
			time_rel_north_moving.append(rel_time[i])

	fig1 = plt.figure(4);
	plt.scatter(time_rel_north_moving, rel_north_moving)

	slope, intercept, r_value, p_value, std_err = stats.linregress(time_rel_north_moving, rel_north_moving)
	print("linear regression: slope = %.4f, intercept = %.4f, r_value = %.4f, p_value = %.4f, std_err = %.4f" % (slope, intercept, r_value, p_value, std_err))

	fit_line = intercept+(slope*np.array(time_rel_north_moving))
	rel_north_error = rel_north_moving - fit_line
	print("min %.4f, max %.4f"%(min(rel_north_error), max(rel_north_error)))

	f3 = plt.figure(5)

	plt.hist(rel_north_error, bins="auto")
	plt.title("Error in Relative Northing")
	plt.xlabel("Error (m)")
	plt.ylabel("Samples")

	# east (moving)
	rel_east_moving = []
	time_rel_east_moving = []

	for i in range(len(rel_time)):
		if rel_time[i] > 5.0 and rel_time[i] < 20.0:
			rel_east_moving.append(rel_north[i])
			time_rel_east_moving.append(rel_time[i])

	fig1 = plt.figure(1);
	plt.scatter(time_rel_east_moving, rel_east_moving)

	slope, intercept, r_value, p_value, std_err = stats.linregress(time_rel_east_moving, rel_east_moving)
	print("linear regression: slope = %.4f, intercept = %.4f, r_value = %.4f, p_value = %.4f, std_err = %.4f" % (slope, intercept, r_value, p_value, std_err))

	fit_line = intercept+(slope*np.array(time_rel_east_moving))
	rel_east_error = rel_east_moving - fit_line
	print("min %.4f, max %.4f"%(min(rel_east_error), max(rel_east_error)))

	f3 = plt.figure(3)

	plt.hist(rel_east_error, bins="auto")
	plt.title("Error in Relative Easting")
	plt.xlabel("Error (m)")
	plt.ylabel("Samples")

	dim = int(args.d)
	fig = plt.figure(2)
	if dim == 3:
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(rel_east, rel_north, rel_time)
		# ax.plot(rel_east, intercept+slope*rel_east, '-')
		ax.set_xlabel('Relative Easting (m)')
		ax.set_ylabel('Relative Northing (m)')
		ax.set_zlabel('Time (s)')
		ax.set_title('Relative Easting vs. Northing')
	else:
		ax = fig.add_subplot(221)
		ax.scatter(rel_east, rel_north, marker="+")
		ax.set_xlabel('Relative Easting (m)')
		ax.set_ylabel('Relative Northing (m)')
		ax.set_title('Relative Easting vs. Northing')
		ax.grid(True)

		ax2 = fig.add_subplot(222)
		ax2.scatter(rel_time, rel_east, marker=".", color='c')
		ax2.set_xlabel('Time (seconds)')
		ax2.set_ylabel('Relative Easting (m)')
		ax2.set_title('Relative Easting vs. Time')
		ax2.grid(True)

		ax3 = fig.add_subplot(223)
		ax3.scatter(rel_time, rel_north, marker=".", color='m')
		ax3.set_xlabel('Time (seconds)')
		ax3.set_ylabel('Relative Northing (m)')
		ax3.set_title('Relative Northing vs. Time')
		ax3.grid(True)

		ax4 = fig.add_subplot(224)
		ax4.plot(rel_time, fix, color='r')
		ax4.grid(True)
		ax4.set_xlabel('Time (seconds)')
		ax4.set_ylabel('Fix Quality')
		ax4.set_title('Fix Quality vs. Time')

		# ax4 = fig.add_subplot(224)
		# ax4.hist(rel_north, bins='auto')

	# fig.savefig('a.png')
	plt.show()

