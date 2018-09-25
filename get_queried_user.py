def get_queried_user(pairs, queried_user_id, sorted_user_name):
	user_index = sorted_username.index(queried_user_id)
	ret = []
	for pair in pairs:
		if user_index in pair:
			if pair[0]==user_index:
				partner = pair[1]
			else:
				partner = pair[0]
				ret.append(sorted_username[partner])
	return ret
