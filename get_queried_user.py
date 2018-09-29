def get_queried_user(user_dic, sorted_username, queried_user_id):
	user_index = sorted_username.index(queried_user_id)
	min_dis = 1
	curr_nearest = -1
	for i in range(len(user_dic)):
		if(i != user_index):
			curr_dis = 1-(len(set(user_dic[user_index]).intersection(set(user_dic[i]))))/len(set(user_dic[user_index]+user_dic[i]))
			if(curr_dis<min_dis):
				min_dis = curr_dis
				curr_nearest = i
	return sorted_username[i]
