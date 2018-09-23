import numpy as np
import random

def get_sig(num,data,r):
  sig = np.empty((num,data.shape[1]))
  for i in range(0,num):
    a = random.randint(0,r)
    b = random.randint(0,r)
    for col in range(0,data.shape[1]):
      tempMin = data.shape[0]
      for row in range(0, data.shape[0]):
        if(data[row][col]==1):
          tempHash = (a*row+b) % r;
          tempMin = min(tempMin,tempHash)
      sig[i][col] = tempMin
  return sig

def find_sim(sig,thre,r,p):
  pairs = []
  bands = int(sig.shape[0]/r)
  for i in range(0,bands):
    a = random.randint(0,p)
    b = random.randint(0,p)
    for j in range(0,sig.shape[1]):
      tempHash1 = (sig[i*r:(i+1)*r,j]*a+b)/p
      for k in range(j+1,sig.shape[1]):
        if((j,k) in pairs):
          continue
        tempHash2 = (sig[i*r:(i+1)*r,k]*a+b)/p
        if((tempHash1==tempHash2).all()):
          pairs.append((j,k))
  final_pairs = []
  for (i,j) in pairs:
    count = 0
    for l in range(0, sig.shape[0]):
      if(sig[l][i]==sig[l][j]):
        count += 1
    if(float(count)/float(sig.shape[0])>=thre):
      final_pairs.append((i,j))
  return final_pairs

# syn_data
# 1, 0, 0
# 0, 1, 1
# 1, 0, 1
#syn_data = np.array([(1,0,0),(0,1,1),(1,0,1)])
#sig = get_sig(10000,syn_data,3)
#print(sig)
#pairs = find_sim(sig,0.5)
#pairs = find_sim(sig,0.65,20,23)
#print(pairs)



