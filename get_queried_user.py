def get_queried_user(user_dic, sorted_username, queried_user_list):
	'''
	user_dic: previously generated dictionary, key:value = user_index:movie_list
	sorted_username: a sorted user_id list, use this to look up the real user_id via user_index
	queried_user_list: a favorate movie list for the queried user
	'''
	nearest = []
	for i in range(len(user_dic)):
		curr_dis = 1-(len(set(queried_user_list).intersection(set(user_dic[i]))))/len(set(queried_user_list+user_dic[i]))
		if(curr_dis<0.35):
			nearest.append(sorted_username[i])
	return nearest
