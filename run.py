from preprocessing import *
from get_sim_multiprocess import *
from thousand_jaccard import *
from get_queried_user import *
import time
import numpy as np
import csv

### seting all the parameters
hash_num = 161
prime_minhash = 4507
threshold = 0.65
length_per_band = 7
prime_bucket = 4523
path = os.path.expanduser('./Netflix_data.txt')
#path = os.path.expanduser('/home/aitrading/Desktop/google_drive/Course_Work/ESE545/Projects/Project_1_Netflix_data.txt/Netflix_data.txt')

start = time.time()
# ############### Problem 1
s = time.time()
final_rows_wo_movienames, movie_row = import_preprocess(path)
print("Import preprocess completed. Time: " + str(int(time.time()-s))+" seconds")
s = time.time()
data_dict, user_dict, sorted_username = convert_into_dict(final_rows_wo_movienames, movie_row)
#matrix_output = convert_dict_to_matrix(sorted_username, movie_row, data_dict)
print("Conversion to dictionary completed. Time: " + str(int(time.time()-s))+" seconds") 

# ############### Problem 2
avg_dist, min_dist = output_avg_min_img(user_dict)
print("avg_dist",avg_dist) # result: 0.98
print("min_dist",min_dist) # result: 0.5

################ Problem  3 & 4
### find similar pairs
s = time.time()
sig,sig_hash_parameters = get_sig_dic(hash_num,user_dict,prime_minhash)
print("Signature matrix completed. Time : "+ str(int(time.time()-s))+" seconds") 

### find similar pairs
s = time.time()
candidates, buckets, band_hash_parameters = find_candidates(sig,length_per_band,prime_bucket)
sim_class = find_sim_dic(sig,candidates,threshold)
final_pairs_ind = sim_class.findpairs_multiprocess()
print(str(len(final_pairs_ind)) + " pairs found. Time: " + str(int(time.time()-s))+" seconds")

### comparing the original user_dict
s = time.time()
output = pair_similarity(user_dict,final_pairs_ind)
print(str(len(output)) + " pairs found after comparing the original data.Time: " + str(int(time.time()-s))+" seconds")

# write the output pairs to csv
with open('similarPairs.csv','w') as writeFile:
  similarWriter = csv.writer(writeFile, delimiter=',')
  for i in range(len(output)):
    similarWriter.writerow([output[i][0], output[i][1]])

############### Problem 5
s = time.time()
print()
nearest_neighbor = get_queried_user(sorted_username,user_dict, user_dict[4], sig_hash_parameters, prime_minhash, band_hash_parameters, prime_bucket, buckets)
print("Nearest neighbor is "+str(nearest_neighbor[0])+"(original ID: "+str(nearest_neighbor[1])+")"+ "with distance "+str(nearest_neighbor[2])+"takes Time: " + str(int(time.time()-s))+"seconds") # less than 1s

print("Total time for this application: " +str(int((time.time()-start)/60))+" mins")


