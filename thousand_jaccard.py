# problem 2:
# 1. randomly pick a thousand pairs at random
# 2. average jaccard distance of the paris
# 3. as well as lowest distance among them

import numpy as np
import random
import os
import matplotlib.pyplot as plt


def jaccard_distance(col_1, col_2):
	"""input as two lists, output jaccard_distance as a float"""
	# sanity
	arr1 = np.array(col_1).reshape(-1,)
	arr2 = np.array(col_2).reshape(-1,)

	intersection = 0
	union = 0
	for i in range(len(arr1)):

		if arr1[i] == 1 and arr2[i] ==1:
			intersection +=1
			union +=1
		elif arr1[i] != arr2[i]:
			union +=1

	jaccard_sim = intersection/union

	return 1 - jaccard_sim

def calculate_batch_distance(data_matrix, n= 10000):
	# data_matrix = np.zeros((5,231424))
	distance_list = []
	# generate 1000 pairs
	for i in range(n):
		pair = random.sample(range(1, 231424), 2)
		col_1 = data_matrix[:,pair[0]]
		col_2 = data_matrix[:,pair[1]]
		dis = jaccard_distance(col_1, col_2)
		distance_list.append(dis)

	return distance_list

def output_avg_min_img(data_matrix):
	distance_list = calculate_batch_distance(data_matrix, n= 10000)
	print("average distance",sum(distance_list)/len(distance_list))
	print("smallest distance",min(distance_list))

	figure = plt.hist(x=distance_list, bins=10, color='#0504aa')

	plt.xlabel('No. pairs')
	plt.ylabel('Frequency')
	plt.title('Histogram of random 10,000 pairs distance')
	plt.savefig(os.path.expanduser('histogram.png'))

	return sum(distance_list)/len(distance_list),min(distance_list)



if __name__ == '__main__':
	
	# test function 
	arr1 = [1,0,0,1,0,1,0]
	arr2 = [1,1,0,1,1,1,1]

	print("distance is ",jaccard_distance(arr1, arr2))



