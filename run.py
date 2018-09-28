from preprocessing import *
from get_similarity import *
from thousand_jaccard import *
import time
import numpy as np


### seting all the parameters
hash_num = 160
prime_minhash = 4507
threshold = 0.65
length_per_band = 4
prime_bucket = 4523

### start processing 
final_rows_wo_movienames, movie_row = import_preprocess(path)
data_dict, user_dict, sorted_username = convert_into_dict(final_rows_wo_movienames, movie_row)
matrix_output = convert_dict_to_matrix(sorted_username, movie_row, data_dict)

# ############### Problem 2
# avg_dist, min_dist = output_avg_min_img(matrix_output)
# # print("avg_dist",avg_dist) # result: 0.98
# # print("min_dist",min_dist) # result: 0.5


### find signature matrix
s = time.time()
# sig = get_sig_dic(hash_num,len(sorted_username),user_dict,prime_minhash)
sig = get_sig_dic(hash_num,user_dict,prime_minhash)
print("Signature matrix completed. Time : "+ str(time.time()-s))

### find similar pairs
#sig = np.zeros((160,20000),dtype = int)
s = time.time()
pairs = find_sim_dic(sig,threshold,length_per_band,prime_bucket，sorted_username)
print(pairs)
print(str(len(pairs)) + " pairs found. Time: " + str(time.time()-s))

### for a queried user









# #######################
# sig_matrix = get_sig(1,matrix_output,4499)
# print("Signature matrix completed!")
# pairs = find_sim(sig_matrix,0.65,20,23)
# print("Similar pairs completed!")
# print(pairs)
# #print(time.time()-start_time)


