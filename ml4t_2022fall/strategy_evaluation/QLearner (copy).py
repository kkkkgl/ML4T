 		  	   		  	  		  		  		    	 		 		   		 		  
import random as rand  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
class QLearner(object):  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    This is a Q learner object.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    :param num_states: The number of states to consider.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type num_states: int  		  	   		  	  		  		  		    	 		 		   		 		  
    :param num_actions: The number of actions available..  		  	   		  	  		  		  		    	 		 		   		 		  
    :type num_actions: int  		  	   		  	  		  		  		    	 		 		   		 		  
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type alpha: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type gamma: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type rar: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type radr: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type dyna: int  		  	   		  	  		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  	  		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    def __init__(  		  	   		  	  		  		  		    	 		 		   		 		  
        self,  		  	   		  	  		  		  		    	 		 		   		 		  
        num_states=100,  		  	   		  	  		  		  		    	 		 		   		 		  
        num_actions=4,  		  	   		  	  		  		  		    	 		 		   		 		  
        alpha=0.2,  		  	   		  	  		  		  		    	 		 		   		 		  
        gamma=0.9,  		  	   		  	  		  		  		    	 		 		   		 		  
        rar=0.5,  		  	   		  	  		  		  		    	 		 		   		 		  
        radr=0.99,  		  	   		  	  		  		  		    	 		 		   		 		  
        dyna=0,  		  	   		  	  		  		  		    	 		 		   		 		  
        verbose=False,  
        		  	   		  	  		  		  		    	 		 		   		 		  
    ):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		  	  		  		  		    	 		 		   		 		  
        self.num_actions = num_actions  
        self.num_states = num_states	
        self.alpha = alpha
        self.gamma = gamma 
        self.rar = rar 
        self.radr = radr         	   		  	  		  		  		    	 		 		   		 		  
        self.s = 0  		  	   		  	  		  		  		    	 		 		   		 		  
        self.a = 0
        self.dyna = dyna
        self.experience = []
        
        self.q_table = np.zeros((num_states, num_actions)) 	
        self.t_count = np.full((num_states, num_actions, num_states), 0.00001)
        self.r_table = np.zeros((num_states, num_actions))
	   		  	  		  		  		    	 		 		   		 		  
    def author(self): 
        return 'kdang49'
 	    	 		 		   		 		  
    def querysetstate(self, s):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Update the state without updating the Q-table  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
        :param s: The new state  		  	   		  	  		  		  		    	 		 		   		 		  
        :type s: int  		  	   		  	  		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  	  		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		         	
        random_n = np.random.randint(0,1)
        # if random less than rar, we explore rather than exploit, else we exploit 
        random = rand.random()
        if random > self.rar:
            action = np.argmax(self.q_table[s,:])
        else:
            action = rand.randint(0, self.num_actions-1)
        
        self.s = s
        self.a = action      		  		    	 		 		   		 		  		  	   		  	  		  		  		    	 		 		   		 		  
        return action  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    def query(self, s_prime, r):  		  	   		  	  		  		  		    	 		 		   		 		  
        """  		  	   		  	  		  		  		    	 		 		   		 		  
        Update the Q table and return an action  		  	   		  	  		  		  		    	 		 		   		 		   	   		  	  		  		  		    	 		 		   		 		  
        :param s_prime: The new state  		  	   		  	  		  		  		    	 		 		   		 		  
        :type s_prime: int  		  	   		  	  		  		  		    	 		 		   		 		  
        :param r: The immediate reward  		  	   		  	  		  		  		    	 		 		   		 		  
        :type r: float  		  	   		  	  		  		  		    	 		 		   		 		  
        :return: The selected action  		  	   		  	  		  		  		    	 		 		   		 		  
        :rtype: int  		  	   		  	  		  		  		    	 		 		   		 		  
        """           
        #update the q table 
        self.update_qtable(self.s, self.a, s_prime, r)
        
        #update experience 
        self.experience.append((self.s, self.a, s_prime, r))
        exp_len = len(self.experience)
        
        #update t_counts and r_table 
        self.t_count[self.s, self.a, s_prime] += 1
        self.r_table[self.s,self.a] = (1-self.alpha)*self.r_table[self.s,self.a] + self.alpha*r 

        #use dyna  
        if self.dyna == 0:
            pass 
        
        else:
                     
            for i in range(self.dyna):
                
                exp_len = len(self.experience)
                random_pick = np.random.randint(exp_len, size=self.dyna)
                
                state = self.experience[random_pick[i]][0]
                action = self.experience[random_pick[i]][1]
                state_prime = self.experience[random_pick[i]][2]
                reward = self.experience[random_pick[i]][3]
                
                self.update_qtable(state, action, state_prime, reward)
         
        
        #update my action 
        random = rand.random()
        
        if random > self.rar:
            action = np.argmax(self.q_table[s_prime,:])
        else:
            action = rand.randint(0, self.num_actions-1)
            
        self.s = s_prime
        self.a = action  
        self.rar *= self.radr
        	  	 		  	  		  		  		    	 		 		   		 		      	  	   		  	  		  		  		    	 		 		   		 		  
        return action 

 		  	   		  	  		  		  		    	 		 		   		 		  
    def update_qtable(self, s, a, s_prime, r):
        
      	self.q_table[s, a] = (1-self.alpha)*self.q_table[s,a] +\
                        self.alpha *(r + self.gamma * np.max(self.q_table[s_prime,:]) )   		  	  		 		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  	  		  		  		    	 		 		   		 		  
    print("Remember Q from Star Trek? Well, this isn't him")  		  	   		  	  		  		  		    	 		 		   		 		  
