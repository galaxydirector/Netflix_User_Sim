import numpy as np
import pandas as pd
import os
import time
from multiprocessing import Pool
import threading
from tqdm import tqdm

def mother():
    aa = np.zeros(shape=(5,8))
    row_list = range(3)
    
    def fucker(i):
        row = aa[i]
        row[3] = 10

    NUM_PROCESSES = 2
    NUM_JOBS = len(row_list)

    

    print("multiprocessing activated")
    for i in row_list:
        fucker(i)
    print("multiprocessing finished") 
    print(aa)


def start_threads(n_threads=2):
    threads = []
    for _ in range(n_threads):
        thread = threading.Thread(target=mother, args=())
        thread.daemon = True  # Thread will close when parent quits.
        thread.start()
        threads.append(thread)

    # return self.threads

if __name__ == '__main__':
    start_threads()