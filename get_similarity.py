import numpy as np
import random
import time
# import threading
# from queue import Queue
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from tqdm import tqdm


def find_prime(n):
	prime_list =[4493,4507,4513,4517,4519,4523]

	for i in prime_list:
		if i >= n:
			return i

#################################### Dumb version#############################
def get_sig(num,data,r):
	sig = np.empty((num,data.shape[1]),dtype = int)
	for i in range(0,num):
		a = random.randint(0,r-1)
		b = random.randint(0,r-1)
		for col in range(0,data.shape[1]):
			tempMin = data.shape[0]
			for row in range(0, data.shape[0]):
				if data[row][col]==1:
					tempHash = (a*row+b) % r
					tempMin = min(tempMin,tempHash)
			sig[i][col] = tempMin
	return sig

def find_sim(sig,thre,r,prime):
	'''
	r - the length of bands
	prime - a large prime number
	'''
	pairs = []
	bands = int(sig.shape[0]/r)
	print(str(bands)+" bands to be processed.")
	for i in range(0,bands):
		bucket = {}
		a = random.randint(0,prime)
		b = random.randint(0,prime)
		for j in range(0,sig.shape[1]):
			tempHash1 = (sig[i*r:(i+1)*r,j]*a+b)%prime
			for k in range(j+1,sig.shape[1]):
				if((j,k) in pairs):
					continue
				tempHash2 = (sig[i*r:(i+1)*r,k]*a+b)%prime
				if((tempHash1==tempHash2).all()):
					pairs.append((j,k))
		print(str(i)+" bands completed.")

	final_pairs = []
	for (i,j) in pairs:
		count = 0
		for l in range(0, sig.shape[0]):
			if(sig[l][i]==sig[l][j]):
				count += 1
		if(float(count)/float(sig.shape[0])>=thre):
			final_pairs.append((i,j))
	return final_pairs
#################################### Dumb version#############################

####################################fast version below#############################
def get_sig_dic(hash_num,user_dic,prime):
	sig = np.empty((hash_num,len(user_dic)),dtype = int)

	for i in range(0,hash_num):
		a = random.randint(0,prime-1)
		b = random.randint(0,prime-1)
		for user in user_dic.keys():
			sig[i][user]=min(list(map(lambda x: (x*a+b)%prime, user_dic[user])))
	return sig


def find_sim_dic(sig,thre,r,prime,sorted_username):
	'''
	sig - (hash_num, user_num)
	r - the length of bands
	prime - a large prime number
	'''

	"""
	Question:
	1. tempHash1, do you have to more than one hash here????
	2. counter candidates.add((l[i],l[j])) user index instead of range(size)?
	"""
	buckets = []
	bands = int(sig.shape[0]/r)
	print(str(bands)+" bands to be processed.")
	for i in range(0,bands):
		bucket = {}

		a = [random.randint(0,prime) for i in range(r)]
		b = [random.randint(0,prime) for i in range(r)]
		for j in range(0,sig.shape[1]):
			s = time.time()
			tempHash = 0;
			for k in range(r):
				tempHash += (sig[i*r:(i+1)*r,j]*a[k]+b[k])%prime

			#print("time line 1: "+ str(time.time()-s))
			tempHash = tuple(tempHash)
			s = time.time()
			bucket.setdefault(tempHash,[]).append(j)
			#print("time line 2: "+ str(time.time()-s))
		buckets.append(bucket)
		print("band {} completed.".format(str(i+1)))

	##################################################################
	# this is a counter?
	start_counter = time.time()
	candidates = set()
	a = 1
	for bucket in buckets:
		print("Looking for candidate pairs in bucket ",str(a))
		for l in bucket.values():
			size = len(l)
			#print("Current Group size" + str(len(l)))
			if size==1:
				continue;
			# set up comparison paris for each two elements
			for i in range(size): 
				for j in range(i+1,size):
					candidates.add((l[i],l[j]))
					# do you actually want to write:
					# candidates.add((l[i],l[j])) where l[i] is the index of users
		a = a + 1
	print(str(len(candidates))+" condidates found!")
	print("time to go through for loops to find pairs: {}".format(time.time()-start_counter))
	##################################################################

	start = time.time()
	final_pairs = []
	final_pairs_ind = []
	for (i,j) in candidates:
		count = sum(sig[:,i].reshape(-1)==sig[:,j].reshape(-1))
		if(float(count)/float(sig.shape[0])>=thre):
			final_pairs.append((sorted_username[i],sorted_username[j]))
			final_pairs_ind.append((i,j))

	# print("final pairs takes {} seconds".format(time.time()-start) )
	
	return final_pairs, final_pairs_ind

def jaccard_similarity(list_1, list_2):
	"""input as two lists, output jaccard_distance as a float"""
	# sanity
	arr1 = np.array(list_1).reshape(-1,)
	arr2 = np.array(list_2).reshape(-1,)

	union = set()
	union = union.add(arr1)
	union = union.add(arr2)

	intersection = set(arr1).intersection(set(arr2))
	jaccard_similarity = len(intersection)/len(union)

	return jaccard_similarity

def pair_similarity(user_dic,final_pairs_ind):
	output = []
	for (i,j) in final_pairs_ind:
		jaccard_sim= jaccard_similarity(user_dic[i],user_dic[j])
		output.append(jaccard_sim)

	return output


# syn_data
# 1, 0, 0
# 0, 1, 1
# 1, 0, 1
#syn_data = np.array([(1,0,0),(0,1,1),(1,0,1)])
#sig = get_sig(10000,syn_data,3)
#print(sig)
#pairs = find_sim(sig,0.5)
#pairs = find_sim(sig,0.65,20,23)
#print(pairs)



# ##################### attempt to multithread it 
# 	q1 = Queue()
# 	q2 = Queue()
# 	def hard_cock():
# 		for (i,j) in candidates:
# 			count = sum(sig[:,i].reshape(-1)==sig[:,j].reshape(-1))
# 			if(float(count)/float(sig.shape[0])>=thre):
# 				q1.put((sorted_username[i],sorted_username[j]))
# 				q2.put((i,j))
# 				# final_pairs.append((sorted_username[i],sorted_username[j]))
# 				# final_pairs_ind.append((i,j))

# 	# def start_threads(n_threads=4):
# 	threads =[]
# 	for _ in range(4):
# 		print("multithread activate")
# 		thread = threading.Thread(target=hard_cock)
# 		thread.daemon = True  # Thread will close when parent quits.
# 		thread.start()
# 		threads.append(thread)

# 	final_pairs = list(q1.queue)
# 	final_pairs_ind = list(q2.queue)

# 	[i.join() for i in threads]
# 	print("multithread finished")