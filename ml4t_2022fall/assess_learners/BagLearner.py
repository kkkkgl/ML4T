#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 15:38:01 2022

@author: connie
"""
import pandas as pd
import numpy as np
#import DTLearner as dtl

class BagLearner:
    def __init__(self, learner, kwargs, bags=20, boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.bag_list = []  # list that will be filled with bags in add_evidence

    def author(self):
        return 'kdang49'

    # in this case I'm expecting n_prime to be equal to n
    # ASSUMPTION: n_prime are the rows of my data so .shape[0]
    def randomly_sample(self, data, n_prime):
        # build an array of n_prime number of elements filled with random rows from data
        idx = np.random.randint(n_prime, size=n_prime)
        new_data = data[idx, :]
        x = new_data[:, :-1]  # all columns except the last
        y = new_data[:, -1]  # last column
        return x, y

    # generates several instances of the learner given with randomly sampled data
    # helper functions - randomly sample
    def add_evidence(self, x, y):
        # converting this to the form used in lecture to build the tree
        data = np.column_stack((x, y))
        n_prime = data.shape[0]  # we are told to assume n = n_prime
        for i in range(self.bags):
            x_sample, y_sample = self.randomly_sample(data, n_prime)
            y_sample = np.atleast_2d(y_sample).T
            # pass unpacked kwargs to the learner
            L = self.learner(**self.kwargs)
            L.add_evidence(x_sample, y_sample)
            self.bag_list.append(L)

    # helper function solely for my debugging, not needed for assignment
    def print_arr(self, string, arr):
        print(" ")
        print("Shape of " + string + " is " + str(arr.shape))
        print(" Head of dataframe")
        print(pd.DataFrame(arr).head())

    # find y values associated with instances of x feature data
    def query(self, x):
        y = None
        # build an array of output y's
        for i in range(len(self.bag_list)):
            L = self.bag_list[i]
            y_i = L.query(x)
            # necessary to match the grader's comparison
            y_i = np.atleast_2d(y_i).T
            if y is None:
                y = y_i
            else:
                y = np.column_stack((y, y_i))
        # since this is regression we use mean
        out = np.mean(y, axis=1)
        return out
        		  	
        	  		    	 		 		   	
if __name__ == "__main__": 
    import pandas as pd
    path = "/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/assess_learners/Data/"	
    path_test = "/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/assess_learners/Data/winequality-white.csv"
    
    data_train = pd.read_csv(path+"Istanbul.csv")  
    data_test = pd.read_csv(path+"winequality-white.csv",header = None)  
    data_test = data_test.iloc[:,1:]
    data_train = data_train.iloc[:,1:]
    data_arr = data_train.values	  
    data_test = data_test.values
    
    self = BagLearner(
                    learner=dtl.DTLearner,
                    kwargs={"leaf_size": 1},
                    bags=20,
                    boost=False,
                    verbose=False,
                )
    self.add_evidence(data_arr[:,:-1], data_arr[:,-1])
 
    
    query_result = self.query(data_test) 
  	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  