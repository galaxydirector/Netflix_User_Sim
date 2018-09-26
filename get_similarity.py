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

def get_sig_dic(hash_num,user_num,user_dic,prime):
	sig = np.empty((hash_num,user_num),dtype = int)
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
	r - the length of bands
	prime - a large prime number
	'''
	buckets = []
	bands = int(sig.shape[0]/r)
	print(str(bands)+" bands to be processed.")
	for i in range(0,bands):
		bucket = {}
		a = random.randint(0,prime)
		b = random.randint(0,prime)
		for j in range(0,sig.shape[1]):
		#for j in range(0,1):
			s = time.time()
			tempHash1 = tuple((sig[i*r:(i+1)*r,j]*a+b)%prime)
			#print("time line 1: "+ str(time.time()-s))
			s = time.time()
			bucket.setdefault(tempHash1,[]).append(j)
			#print("time line 2: "+ str(time.time()-s))
		buckets.append(bucket)
		print(str(i+1)+" bands completed.")
	candidates = set()
	a = 1
	for bucket in buckets:
		print("Looking for candidate pairs in bucket "+str(a))
		#print("Total groups: "+ str(len(bucket)))
		for l in bucket.values():
			size = len(l)
			#print("Current Group size" + str(len(l)))
			if size==1:
				continue;
			for i in range(size):
				for j in range(i+1,size):
					#if (i,j) not in candiates:
					candidates.add((i,j))
		a = a + 1
	print(str(len(candidates))+" condidates found!")
	final_pairs = []
	for (i,j) in candidates:
		count = sum(sig[:,i].reshape(-1)==sig[:,j].reshape(-1))
		if(float(count)/float(sig.shape[0])>=thre):
			final_pairs.append((sorted_username[i],sorted_username[j]))
	return final_pairs

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



