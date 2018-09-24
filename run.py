from preprocessing import *
from get_similarity import *
from thousand_jaccard import *
import time

start_time = time.time()
final_rows_wo_movienames, movie_row = import_preprocess(path)
#print(time.time()-start_time)
data_dict = convert_into_dict(final_rows_wo_movienames, movie_row)
#print(time.time()-start_time)
matrix_output = convert_dict_to_matrix(final_rows_wo_movienames, movie_row, data_dict)
print("Matirx completed!")


# #######################
# sig_matrix = get_sig(1,matrix_output,4499)
# print("Signature matrix completed!")
# pairs = find_sim(sig_matrix,0.65,20,23)
# print("Similar pairs completed!")
# print(pairs)
# #print(time.time()-start_time)


###############problem 2
avg_dist, min_dist = output_avg_min_img(matrix_output)
print("avg_dist",avg_dist)
print("min_dist",min_dist)