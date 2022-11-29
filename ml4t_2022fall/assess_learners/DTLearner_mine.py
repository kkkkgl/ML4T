#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 17:14:46 2022

@author: connie
"""


import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		   		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
class DTLearner(object):  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    This is a Linear Decision Tree Learner. It is implemented correctly.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  	  		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1, verbose=False):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  	  		  		  		    	 		 		   		 		  
        """  	
        self.leaf_size = leaf_size
        self.verbose = verbose 
        self.tree = np.empty((0,4),dtype = float) 		  	  		  		  		    	 		 		   		 		  
        pass  # move along, these aren't the drones you're looking for  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    def author(self):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        :return: The GT username of the student  		  	   		  	  		  		  		    	 		 		   		 		  
        :rtype: str  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        return "kdang49"  # replace tb34 with your Georgia Tech username  
    
    def all_y_same(self, data) :
        y = data[:, -1]
        return np.max(y) == np.min(y) #This return a bool 
    
    def max_corr_col(self,data,cols_ignore):
        max_idx = -1 
        max_corr = -2000
        for col in range(data.shape[1]-1):
            if np.var(data[:,col]) == 0:
                correlation = 0
            else:
                corr = np.corrcoef(data[:,col],y=data[:,-1])
                correlation = abs(corr[0][1])
            if correlation > max_corr and col not in cols_ignore:
                max_corr = correlation 
                max_idx = col 
        return int(max_idx)
                     
    def can_not_split(self, data,splitval,col_index):
        #this happens when the x column has same values 
        leftshape = (data[data[:,col_index]<=splitval]).shape[0]
        rightshape = (data[data[:,col_index]>splitval]).shape[0]
        return leftshape == 0 or rightshape == 0
            
           
    def build_tree(self,data):
        
        #print("data.shape[0]:", data.shape[0])
        #print("data.shape[1]:", data.shape[1])        
        
        if data.shape[0] <= self.leaf_size:
            return np.array([[np.NAN,int(data[0][-1]),np.NAN,np.NAN]])
        
        if self.all_y_same(data):
            return np.array([[np.NAN,int(data[0][-1]),np.NAN,np.NAN]])
  
        if data.shape[0] <= self.leaf_size:
            y = np.mean(data[:,-1])
            return np.array([[np.NAN, y, np.NAN, np.NAN]])
          
        else:
            cols_ignore = [] 
            max_corr_col_index = self.max_corr_col(data, cols_ignore)
            splitval = np.median(data[:,max_corr_col_index])
            
            while self.can_not_split(data,splitval,max_corr_col_index) and (data.shape[1] - len(cols_ignore)) > 1:
                cols_ignore.append(max_corr_col_index)
                max_corr_col_index = self.max_corr_col(data,cols_ignore)  
                splitval = np.median(data[:, max_corr_col_index])

            if (data.shape[1] - len(cols_ignore)) == 1:
                y = np.mean(data[:, -1])
                return np.array([[np.NAN, y, np.NAN, np.NAN]])

            lefttree = self.build_tree(data[data[:,max_corr_col_index]<=splitval])
            righttree = self.build_tree(data[data[:,max_corr_col_index]>splitval])
            root = np.array([[int(max_corr_col_index),int(splitval),int(1),int(lefttree.shape[0]+1)]])
            return np.vstack((root,lefttree,righttree))	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		 
 		  		    	 		 		   		 		  
    def add_evidence(self, data_x, data_y):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        :param data_x: A set of feature values used to train the learner  		  	   		  	  		  		  		    	 		 		   		 		  
        :type data_x: numpy.ndarray  		  	   		  	  		  		  		    	 		 		   		 		  
        :param data_y: The value we are attempting to predict given the X data  		  	   		  	  		  		  		    	 		 		   		 		  
        :type data_y: numpy.ndarray  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  		  	   		  	  		  		  		    	 		 		   		 		  
        new_data = np.column_stack((data_x,data_y)) 		  	   		  	  		  		  		    	 		 		   		 		  
        self.tree = self.build_tree(new_data)	  	   		  	  		  		  		    	 		 		   		 		  
        	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    def query(self, x):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Estimate a set of test points given the model we built.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		  	  		  		  		    	 		 		   		 		  
        :type points: numpy.ndarray  		  	   		  	  		  		  		    	 		 		   		 		  
        :return: The predicted result of the input data according to the trained model  		  	   		  	  		  		  		    	 		 		   		 		  
        :rtype: numpy.ndarray  		  	   		  	  		  		  		    	 		 		   		 		  
        """  
        result = np.empty((0,1))	
        for row in x:
            y = self.predict_with_tree(row)
            result = np.vstack([result,y])	
        return result
        		
  	
          		  	
    def predict_with_tree(self,row):
        
        total_tree_rows = self.tree.shape[0]
        idx = 0 
        node = self.tree[idx,:]
        while idx <= (total_tree_rows-1) :
            
            if np.isnan(node[0]):
                return node[1]
            
            #print("node: ",node, row)
            if row[int(node[0])] > node[1]:
                idx = idx + int(self.tree[idx][-1])
                #print("idx right: ", idx)
                node = self.tree[idx,:]
            else:
                idx = idx + 1
                #print("idx left: ", idx)
                node = self.tree[idx,:]
            
            
        	    	 		 		   		 		  
        		  	  		  		  		    	 		 		   		 		  
if __name__ == "__main__": 
    
    self = DTLearner(1, object)
    path = "/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/assess_learners/Data/"	
    path_test = "/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/assess_learners/Data/winequality-white.csv"
    import pandas as pd 
    data_train = pd.read_csv(path+"Istanbul.csv")  
    data_test = pd.read_csv(path+"winequality-white.csv",header = None)  
    data_test = data_test.iloc[:,1:]
    data_train = data_train.iloc[:,1:]
    data_arr = data_train.values	  
    data_test = data_test.values 
    self.tree = self.build_tree(data_arr)	
    query_result = self.query(data_test) 
  	 		 		   		 		  
    print("the secret clue is 'zzyzx'")  