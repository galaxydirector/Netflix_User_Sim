# problem 2:
# 1. randomly pick a thousand pairs at random
# 2. average jaccard distance of the paris
# 3. as well as lowest distance among them

import numpy as np
import random
import os
import matplotlib.pyplot as plt


def jaccard_distance(list_1, list_2):
	'''
	list_1/list_2: 2 integer lists
	return: jaccard_distance as a float
	'''
	return 1-(len(set(list_1).intersection(list_2)))/len(set(list_1+list_2))

def calculate_batch_distance(user_dic, n= 10000):
	distance_list = []
	# generate 10000 pairs
	for i in range(n):
		pair = random.sample(range(1, 231424), 2)
		list_1 = user_dic[pair[0]]
		list_2 = user_dic[pair[1]]
		dis = jaccard_distance(list_1, list_2)
		distance_list.append(dis)

	return distance_list

def output_avg_min_img(user_dic):
	distance_list = calculate_batch_distance(user_dic, n= 10000)
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



