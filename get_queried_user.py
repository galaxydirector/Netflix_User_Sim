import numpy as np
def get_queried_user(sorted_username,user_dic, queried_user_list, sig_hash_parameters, prime_minhash, band_hash_parameters, prime_bucket, buckets):
	'''
	user_dic: previously generated dictionary, key:value = user_index:movie_list
	sorted_username: a sorted user_id list, use this to look up the real user_id via user_index
	queried_user_list: a favorate movie list for the queried user
	sig_hash_parameters: length = m, hash functions used to generate previous signature matrix
	band_hash_parameters: length = r, hash functions used to hash vectors
	buckets: length = m / r, bucket list for all bands
	'''
	m = len(sig_hash_parameters[0])
	r = len(band_hash_parameters[0])
	a = sig_hash_parameters[0]
	b = sig_hash_parameters[1]
	prime = prime_minhash

	sig_user = np.empty(m,dtype = int)
	for i in range(0,m):
		sig_user[i] = min(list(map(lambda x: (x*a[i]+b[i])%prime, queried_user_list)))
	a = band_hash_parameters[0]
	b = band_hash_parameters[1]
	prime = prime_bucket
	buckets_user = []
	bands = int(m / r)
	for i in range(0,bands):
		tempHash = 0;
		for k in range(r):
			tempHash += (sig_user[i*r:(i+1)*r]*a[k]+b[k])%prime
		tempHash = tuple(tempHash)
		buckets_user.append(tempHash)

	candi_groups = set()
	for i in range(bands):
		if buckets_user[i] in buckets[i]:
			candi_groups.update(buckets[i][buckets_user[i]])
	min_dis = 1;
	curr_nn = -1;
	for candi_nn in candi_groups:
		curr_dis = 1-len(set(user_dic[candi_nn]).intersection(queried_user_list))/len(set(user_dic[candi_nn]+queried_user_list))
		if curr_dis<min_dis:
			min_dis = curr_dis
			curr_nn = candi_nn

	# nearest_ind = nearests[np.argmin(distance)]
	# nearest = sorted_username[nearest_ind]
	# print("the nearest user id is {}", nearest)
	return (curr_nn,sorted_username[curr_nn],min_dis)
