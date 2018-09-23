import numpy as np
import pandas as pd
import os
import time
import threading
# from tqdm import tqdm

path = '/home/aitrading/Desktop/google_drive/Course_Work/ESE545/Projects/Project_1_Netflix_data.txt/Netflix_data.txt' 

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

	print("import_preprocess completed")
	return final_rows_wo_movienames, movie_row

def convert_into_dict(final_rows_wo_movienames, movie_row):
	####################### 4. put into a dict, and 
	# save into a dict, key is movie, value is list of users
	data_dict={}
	for movie, [lowerbound, upperbound] in enumerate(zip(list(movie_row['user'].index),list(movie_row['user'].index)[1:]+[len(final_rows_wo_movienames)+1])):
		value = final_rows_wo_movienames.loc[(final_rows_wo_movienames.index<upperbound) &\
											 (final_rows_wo_movienames.index>lowerbound)]
		user_list = list(value['user'])
		data_dict[movie] = user_list
	print("convert_into_dict completed")
	return data_dict

def convert_dict_to_matrix(final_rows_wo_movienames, movie_row, data_dict):
	# matrix saves as a form of np.array

	####################### 4. put into a dict, and store into a matrix
	# sort user number
	sorted_username = sorted(list(final_rows_wo_movienames.groupby('user').count().index))
	user_num = len(sorted_username)
	matrix_shape = (len(movie_row),user_num)
	print("matrix shape: ",matrix_shape)

	matrix_output = np.zeros(shape=matrix_shape)
	for movie in range(len(movie_row)):

		# given a list of users, find the index in sorted_username
		users = data_dict[movie]
		index_list = [sorted_username.index(i) for i in sorted(users)]
		
		# have the row to be 1 at index, else to be 0
		row_arr = matrix_output[movie]
		for ind in index_list:
			row_arr[ind]=1

		if movie % 20 == 0:
			print("processing movie No. {}".format(movie))

	export_path = os.path.join(path,'converted_data.csv')
	np.savetxt(os.path.expanduser(export_path), np.array(matrix_output), delimiter=',')

	return matrix_output



# def start_threads(n_threads=4):
# 	threads =[]
# 	for _ in range(n_threads):
# 		thread = threading.Thread(target=convert_dict_to_matrix, args=(final_rows_wo_movienames, movie_row, data_dict,))
# 		thread.daemon = True  # Thread will close when parent quits.
# 		thread.start()
# 		threads.append(thread)


start_time = time.time()
final_rows_wo_movienames, movie_row = import_preprocess(path)
print(time.time()-start_time)
data_dict = convert_into_dict(final_rows_wo_movienames, movie_row)
print(time.time()-start_time)
start_threads(n_threads=4)
# matrix_output = parellel_convert_to_matrix(final_rows_wo_movienames, movie_row, data_dict)
# matrix_output = convert_dict_to_matrix(final_rows_wo_movienames, movie_row, data_dict)
print(time.time()-start_time)