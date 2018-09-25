from preprocessing import *
from get_similarity import *
from thousand_jaccard import *
import time


### seting all the parameters
hash_num = 160
prime_minhash = 163
threshold = 0.65
lenth_band = 8
prime_bucket = 541

### start processing 
final_rows_wo_movienames, movie_row = import_preprocess(path)
user_dict,user_num = convert_into_dict(final_rows_wo_movienames, movie_row)

### find signature matrix
s = time.time()
sig = get_sig_dic(hash_num,user_num,user_dict,prime_minhash)
print("Signature matrix completed. Time: "+ str(time.time()-s))

### find similar pairs
s = time.time()
pairs = find_sim(sig,threshold,lenth_band,prime_bucket)
print(pairs)
print(time.time()-s)









# #######################
# sig_matrix = get_sig(1,matrix_output,4499)
# print("Signature matrix completed!")
# pairs = find_sim(sig_matrix,0.65,20,23)
# print("Similar pairs completed!")
# print(pairs)
# #print(time.time()-start_time)


###############problem 2
#avg_dist, min_dist = output_avg_min_img(matrix_output)
# print("avg_dist",avg_dist)
# print("min_dist",min_dist)