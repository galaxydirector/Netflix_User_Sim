import numpy as np
import pandas as pd
import os
import time

# path = os.path.expanduser('./Netflix_data.txt')
path = os.path.expanduser('/home/aitrading/Desktop/google_drive/Course_Work/ESE545/Projects/Project_1_Netflix_data.txt/Netflix_data.txt')

def import_preprocess(path):
	####################### 1. read txt
	file_path = os.path.expanduser(path)
	x = pd.read_table(file_path, sep=',|\t',engine='python', names=('user', 'rate', 'date'))

	####################### 2. df[df['rate']>3] =1
	# find index of the row containing ':'
	movie_row = x[x['user'].str.contains(":")]
	print("Sanity check: no NA other than movie title row is {}".format(len(x[pd.isna(x['date']) == True]) == \
																		len(x.iloc[list(movie_row.index)])))

	data_wo_movie_row = x.drop(list(movie_row.index))
	data_wo_movie_row.loc[data_wo_movie_row['rate']<3, 'rate'] = 0 
	data_wo_movie_row.loc[data_wo_movie_row['rate']>=3, 'rate'] =1
	binary_wo_movie_row = data_wo_movie_row

	####################### 3. remove by groupby(df['user']) more than or equal to 20
	# groupby_filtered make sure only keeps users that the sum of rate is between 1 and 20
	groupby_filtered = binary_wo_movie_row.groupby("user").sum().apply(lambda x: x <=20) \
	& binary_wo_movie_row.groupby("user").sum().apply(lambda x: x >= 1)

	# find out which users are smaller than 0
	selected_user_rows = list(groupby_filtered[groupby_filtered['rate'] == True].index)
	rows_wo_movienames = binary_wo_movie_row[binary_wo_movie_row['user'].isin(selected_user_rows)]
	# eliminate rate = 0
	final_rows_wo_movienames = rows_wo_movienames[rows_wo_movienames['rate'] != 0]

	# no. user = 231,424
	# no. movie = 4499
	return final_rows_wo_movienames, movie_row


def convert_into_dict(final_rows_wo_movienames, movie_row):
	"""
	####################### 4. put into a dict, and 
	save data into two dicts: 
	1. key is movie, value is list of users
	2. key as user, value is list of movies
	"""

	sorted_username = sorted(list(final_rows_wo_movienames.groupby('user').count().index))
	user_IDs = dict(zip(sorted_username, list(range(0,len(sorted_username)))))

	data_dict={} 
	for movie, [lowerbound, upperbound] in enumerate(zip(list(movie_row['user'].index),list(movie_row['user'].index)[1:]+[len(final_rows_wo_movienames)+1])):
		value = final_rows_wo_movienames.loc[(final_rows_wo_movienames.index<upperbound) &\
											 (final_rows_wo_movienames.index>lowerbound)]
		users = list(value['user'])
		index_list = [user_IDs[i] for i in users] # map user to the full user map
		data_dict[movie] = index_list
	
	user_dic={}
	for movie in data_dict.keys():
		for user in data_dict[movie]:
			user_dic.setdefault(user,[]).append(movie)
	return data_dict, user_dic,sorted_username


def convert_dict_to_matrix(sorted_username, movie_row, data_dict):
	# matrix saves as a form of np.array

	user_num = len(sorted_username)
	matrix_shape = (len(movie_row),user_num)
	print("matrix shape: ",matrix_shape)

	matrix_output = np.zeros(shape=matrix_shape,dtype=int)
	for movie in range(len(movie_row)):

		users_index = data_dict[movie]

		# have the row to be 1 at index, else to be 0
		row_arr = matrix_output[movie]
		for ind in users_index:
			row_arr[ind]=1

		if movie % 100 == 0:
			print("processing movie No. {}".format(movie))

	return matrix_output