# problem 2:
# 1. randomly pick a thousand pairs at random
# 2. average jaccard distance of the paris
# 3. as well as lowest distance among them

def jaccard_distance(col_1, col_2):
	"""input as two lists, output jaccard_distance as a float"""
	# sanity
	arr1 = np.array(col_1)
	arr2 = np.array(col_1)

	intersection = 0
	union = 0
	for i in range(len(arr1)):
		if arr1[i] == 1 and arr2[i] ==1:
			intersection +=1
			union +=1
		if arr1[i] == 1 and arr2[i] ==0:
			union +=1
		if arr1[i] == 0 and arr2[i] ==1:
			union +=1

	jaccard_sim = intersection/union

	return 1 - jaccard_sim

