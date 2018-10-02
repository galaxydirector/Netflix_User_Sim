# multiprocess
import numpy as np
import random
import time
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def get_sig_dic(hash_num,user_dic,prime):
	sig = np.empty((hash_num,len(user_dic)),dtype = int)
	a = [random.randint(0,prime-1) for i in range(hash_num)]
	b = [random.randint(0,prime-1) for i in range(hash_num)]
	for i in range(0,hash_num):
		for user in user_dic.keys():
			sig[i][user]=min(list(map(lambda x: (x*a[i]+b[i])%prime, user_dic[user])))
	return sig,(a,b)

def find_candidates(sig, r, prime):
		'''
		sig - (hash_num, user_num)
		r - the length of bands
		prime - a large prime number
		'''
		buckets = []
		bands = int(sig.shape[0]/ r)
		a = [random.randint(0,prime-1) for i in range(r)]
		b = [random.randint(0,prime-1) for i in range(r)]
		print(str(bands)+" bands to be processed.")
		for i in range(0,bands):
			bucket = {}
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
		start = time.time()
		candidates = set()
		count = 1
		for bucket in buckets:
			print("Looking for candidate pairs in bucket ",str(count))
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
			count = count + 1
		print(str(len(candidates))+" condidates found!")
		print("Time to go through for loops to find pairs: {} seconds".format(int(time.time()-start)))

		return candidates,buckets,(a,b)

class find_sim_dic():
	def __init__(self,sig,candidates,
				thre):
		self.sig = sig
		self.thre = thre
		self.queue = mp.Manager().Queue()
		self.candidates = list(candidates)
	def hard_cock(self, pair):
		count = sum(self.sig[:,pair[0]].reshape(-1)==self.sig[:,pair[1]].reshape(-1))
		if(float(count)/float(self.sig.shape[0])>=self.thre):
			#return (self.sorted_username[i],self.sorted_username[j]), (i,j)
			self.final_pairs_ind.append(pair)

	def soft_cock(self, data):
		for (i,j) in tqdm(data):
			count = sum(self.sig[:,i].reshape(-1)==self.sig[:,j].reshape(-1))
			if(float(count)/float(self.sig.shape[0])>=self.thre):
				self.queue.put((i,j))

	def findpairs_multiprocess(self):
		NUM_PROCESSES = 4 # number of cores you want to ultilize
		NUM_JOBS = NUM_PROCESSES

		split_from = int(len(self.candidates)/NUM_PROCESSES)
		splited_list = [self.candidates[i:i + split_from] for i in range(0, len(self.candidates), split_from)]
		print("Len of splited_list", len(splited_list))

		with Pool(processes=NUM_PROCESSES) as p:
			with tqdm(total=NUM_JOBS, desc='Parallel Processing') as pbar:
				for result_index in p.imap_unordered(self.soft_cock, splited_list):
					pbar.update()

		final_pairs_ind = []
		print("Dumping the queue into a list")
		while self.queue.empty() is False:
			final_pairs_ind.append(self.queue.get())

		print("Pairs found {}".format(len(final_pairs_ind)))	
		return final_pairs_ind

def jaccard_similarity(list_1, list_2):
	'''
	list_1/list_2: 2 integer lists
	return: jaccard_distance as a float
	'''
	arr1 = np.array(list_1).reshape(-1,)
	arr2 = np.array(list_2).reshape(-1,)

	return len(set(arr1).intersection(set(arr2)))/len(set(arr1).union(set(arr2)))

def pair_similarity(user_dic,final_pairs_ind):

	output = []
	for (i,j) in final_pairs_ind:
		jaccard_sim= jaccard_similarity(user_dic[i],user_dic[j])
		if jaccard_sim>=0.65:
			output.append((i,j))

	return output