# multiprocess
import numpy as np
import random
import time
import multiprocessing as mp
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

def get_sig_dic(hash_num,user_dic,prime):
	sig = np.empty((hash_num,len(user_dic)),dtype = int)

	for i in range(0,hash_num):
		a = random.randint(0,prime-1)
		b = random.randint(0,prime-1)
		for user in user_dic.keys():
			sig[i][user]=min(list(map(lambda x: (x*a+b)%prime, user_dic[user])))
	return sig

class find_sim_dic():
	def __init__(self,sig,
				thre,
				r,
				prime,
				sorted_username):
		self.sig = sig
		self.thre = thre
		self.r = r
		self.prime = prime
		self.sorted_username = sorted_username
		self.final_pairs_ind = []
		self.queue = mp.Manager().Queue()

	def find_candidates(self):
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
		bands = int(self.sig.shape[0]/self.r)
		print(str(bands)+" bands to be processed.")
		for i in range(0,bands):
			bucket = {}

			a = [random.randint(0,self.prime) for i in range(self.r)]
			b = [random.randint(0,self.prime) for i in range(self.r)]
			for j in range(0,self.sig.shape[1]):
				s = time.time()
				tempHash = 0;
				for k in range(self.r):
					tempHash += (self.sig[i*self.r:(i+1)*self.r,j]*a[k]+b[k])%self.prime

				#print("time line 1: "+ str(time.time()-s))
				tempHash = tuple(tempHash)
				s = time.time()
				bucket.setdefault(tempHash,[]).append(j)
				#print("time line 2: "+ str(time.time()-s))
			buckets.append(bucket)
			print("band {} completed.".format(str(i+1)))

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
		print("time to go through for loops to find pairs: {}".format(time.time()-start))

		return candidates

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

		candidates = list(self.find_candidates())
		split_from = int(len(candidates)/NUM_PROCESSES)
		splited_list = [candidates[i:i + split_from] for i in range(0, len(candidates), split_from)]
		print("len of splited_list", len(splited_list))

		with Pool(processes=NUM_PROCESSES) as p:
			with tqdm(total=NUM_JOBS, desc='Parallel Processing') as pbar:
				for result_index in p.imap_unordered(self.soft_cock, splited_list):
					pbar.update()

		final_pairs_ind = []
		print("dump the queue into a list")
		while self.queue.empty() is False:
			final_pairs_ind.append(self.queue.get())

		print("pairs found {}".format(len(final_pairs_ind)))	
		return final_pairs_ind
