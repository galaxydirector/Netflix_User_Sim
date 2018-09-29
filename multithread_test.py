# multithread test

# import threading
# from queue import Queue
import numpy as np
import time
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

data = list(range(10000000))
def fucker(data):
	output = []
	q = Queue()
	def hard_cock():
		for i in data:
			output.append(i^2)

	threads =[]
	for _ in range(4):
		thread = threading.Thread(target=hard_cock)
		thread.daemon = True  # Thread will close when parent quits.
		thread.start()
		threads.append(thread)
	
	[i.join() for i in threads]

	print("task completed")

	return output

def easy_process(data):
	i = data[0]
	j = data[1]
	if i != j:
		return (i, j^2)

def multiprocess():
	candidates = set([(i,j) for (i,j) in zip(range(100),range(100,200))])


	def easy_process(data):
		i = data[0]
		j = data[1]
		if i != j:
			return (i, j^2)
	# for (i,j) in candidates:
	# 	print((i,j))
	final_pairs = []
	final_pairs_ind = []

	NUM_JOBS = len(candidates)
	NUM_PROCESSES = 3 # number of cores you want to ultilize
	with Pool(processes=NUM_PROCESSES) as p:
		with tqdm(total=NUM_JOBS, desc='Parallel Processing') as pbar:
			for result in p.imap_unordered(easy_process, candidates):
				final_pairs.append(result[0])
				final_pairs_ind.append(result[1])
				pbar.update()
	print(final_pairs_ind)
	return final_pairs, final_pairs_ind

# fucker(data)

if __name__ == '__main__':
	multiprocess()
	# print(output)
