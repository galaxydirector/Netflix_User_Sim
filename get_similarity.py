import numpy as np
import random
import time


def find_prime(n):
	prime_list =[4493,4507,4513,4517,4519,4523]

	for i in prime_list:
		if i >= n:
			return i

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

def get_sig_dic_old(hash_num,user_num,user_dic,prime):
	############# Yanci's Question: Is len(user_dic)==user_num? #############
	############# if so, we could reduce a input ############################

	sig = np.empty((hash_num,user_num),dtype = int)
	for i in range(0,hash_num):
		a = random.randint(0,prime-1)
		b = random.randint(0,prime-1)
		for user in user_dic.keys():
			sig[i][user]=min(list(map(lambda x: (x*a+b)%prime, user_dic[user])))
	return sig

def get_sig_dic(hash_num,user_dic,prime):
	sig = np.empty((hash_num,len(user_dic)),dtype = int)

	for i in range(0,hash_num):
		a = random.randint(0,prime-1)
		b = random.randint(0,prime-1)
		for user in user_dic.keys():
			sig[i][user]=min(list(map(lambda x: (x*a+b)%prime, user_dic[user])))
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
	start = time.time()
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
	print("time to go through 4 for loops to find pairs: {}".format(time.time()-start))
	##################################################################

	final_pairs = []
	final_pairs_ind = []
	for (i,j) in candidates:
		count = sum(sig[:,i].reshape(-1)==sig[:,j].reshape(-1))
		if(float(count)/float(sig.shape[0])>=thre):
			final_pairs.append((sorted_username[i],sorted_username[j]))
			final_pairs_ind.append((i,j))






	# ##################### attempt to multithread it 
	# final_pairs = []
	# final_pairs_ind = []
	# for (i,j) in candidates:
	# 	count = sum(sig[:,i].reshape(-1)==sig[:,j].reshape(-1))
	# 	if(float(count)/float(sig.shape[0])>=thre):
	# 		final_pairs.append((sorted_username[i],sorted_username[j]))
	# 		final_pairs_ind.append((i,j))

	# def start_threads(n_threads=4):
	# 	threads =[]
	# 	for _ in range(n_threads):
	# 		thread = threading.Thread(target=find_sim_dic, args=(sig,threshold,length_per_band,prime_bucket,sorted_username,))
	# 		thread.daemon = True  # Thread will close when parent quits.
	# 		thread.start()
	# 		threads.append(thread)

	# 	return threads

	np.savetxt('final_pairs.txt',final_pairs,delimiter=',')
	np.savetxt('final_pairs_ind.txt',final_pairs_ind,delimiter=',')
	return final_pairs, final_pairs_ind

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

def pair_distance(user_dic,final_pairs_ind):
	output = []
	for (i,j) in final_pairs_ind:
		output.append(jaccard_distance(user_dic[i],user_dic[j]))

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



