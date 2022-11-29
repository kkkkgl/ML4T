""""""  		  	   		  	  		  		  		    	 		 		   		 		  
"""Assess a betting strategy.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  	  		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  	  		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  	  		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  	  		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  	  		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  	  		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  	  		  		  		    	 		 		   		 		  
or edited.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  	  		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  	  		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  	  		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
Student Name: Dang Kangni(replace with your name)  		  	   		  	  		  		  		    	 		 		   		 		  
GT User ID: kdang49 (replace with your User ID)  		  	   		  	  		  		  		    	 		 		   		 		  
GT ID: 903825229 (replace with your GT ID)  		  	   		  	  		  		  		    	 		 		   		 		  
"""  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
import numpy as np  	
import matplotlib.pyplot as plt	  	   		  	  		  		  		    	 		 		   		 		  
import pandas as pd

#image_dir = '/home/connie/Documents/gatech/CS7464-ml4t/ml4t_2022fall/martingale/images/' 	  		  		  		    	 		 		   		 		  
def author():  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  	  		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    return "kdang49"  # replace tb34 with your Georgia Tech username.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
def gtid():  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		  	  		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    return 903825229   # replace with your GT ID number  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
  
###############################################################################		  	   		  	  		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  	  		  		  		    	 		 		   		 		  
  		  	   		  	  		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		  	  		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		  	  		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		  	  		  		  		    	 		 		   		 		  
    :rtype: bool  		  	   		  	  		  		  		    	 		 		   		 		  
    """  
    result = False  		  	   		  	  		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		  	  		  		  		    	 		 		   		 		  
        result = True  		  	   		  	  		  		  		    	 		 		   		 		  
    return result  
		  	   		  	  		  		  		    	 		 		   		 		  


def simulate_episode(n,win_prob):
    
    i = 0      
    episode_array = np.zeros((n,1001), dtype=int)
    while i < n:
        time = 1
        episode_winnings = 0
        while episode_winnings < 80:
            won = False
            bet_amount = 1
            while not won:
                won = get_spin_result(win_prob)
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount * 2
                episode_array[i, time] = episode_winnings
                time += 1
                if time > 1000:
                    break
            if time > 1000:
                break
    
        while time <= 1000 and episode_winnings >= 80:
            episode_array[i, time] = episode_winnings 
            time += 1
        i += 1
    return episode_array


def plot_figure_1():
    
    column_name = []
    index_name = []
    for i in range(0,1001):
        column_name.append("Spin_" + str(i))
    for i in range(0,10):
        index_name.append("Episode_" + str(i))
        
    figure_1_data = simulate_episode(10,9/19)
    figure_1_data = pd.DataFrame(figure_1_data,columns=column_name,index=index_name)
    trans_figure_1_data = figure_1_data.T
    figure_1 = trans_figure_1_data.plot()
    figure_1.set_xlim([0,300])
    figure_1.set_ylim([-256,100])
    figure_1.set_title('figure_1')
    plt.savefig( 'figure_1')
    plt.close()

def plot_figure_2():
        
    figure_2_data = simulate_episode(1000,9/19)
    figure_2_data = pd.DataFrame(figure_2_data)
    each_spin_round_mean = figure_2_data.mean()
    each_spin_round_mean = each_spin_round_mean.T
    ax = each_spin_round_mean.plot()
    ax.set_xlim([0,300])
    ax.set_ylim([-256,100])
    ax.set_title('figure_2')
    plt.savefig('figure_2')
           		
def plot_figure_3():
    
    figure_2_data = simulate_episode(1000,9/19)
    figure_2_data = pd.DataFrame(figure_2_data)
    each_spin_round_med = figure_2_data.median() 
    std = figure_2_data.std()   
    upper_band = each_spin_round_med + std
    lower_band = each_spin_round_med - std      
    for i in [each_spin_round_med,upper_band,lower_band]:
        i = pd.DataFrame(i)
    df = pd.DataFrame({'median':each_spin_round_med, 'upper_band': upper_band, 'lower_band': lower_band}) 
    ax = df.plot(title = 'figure_3')
    ax.set_xlim([0,300])
    ax.set_ylim([-256,100])
    plt.savefig('figure_3')

   
def simulate_episode_256_bankroll():
    i = 0   
    episode_array = np.zeros((1000,1001), dtype=int)
    while i < 1000: #n episode
        time = 1
        episode_winnings = 0
        while episode_winnings < 80:
            won = False
            bet_amount = 1
            while not won:
                won = get_spin_result(9/19)#win_prob
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    #print('episode_winnings:  ',episode_winnings)
                else:
                    episode_winnings = episode_winnings - bet_amount
                    #print('episode_winnings:  ',episode_winnings)
                    bet_amount = bet_amount * 2
                    worst_case = episode_winnings - bet_amount
                    #print('worst_case: ', worst_case)
                    if worst_case < -256:
                        bet_amount = episode_winnings + 256 
                        #print('updated bet amount: ', bet_amount)
                episode_array[i, time] = episode_winnings
                time += 1
                if episode_winnings <= -256 or bet_amount <= 0:
                    break
                if time > 1000:
                    break
            if episode_winnings <= -256 or bet_amount <= 0:
                break
            if time > 1000:
                break
    
        while time <= 1000 and (episode_winnings >= 80 or episode_winnings <= 256):
            episode_array[i, time] = episode_winnings 
            time += 1
        i += 1
    return episode_array


    
def plot_figure_4():

    figure_4_data = simulate_episode_256_bankroll()
    figure_4_data = pd.DataFrame(figure_4_data)	
    trans_figure_4_data = figure_4_data.T
    each_spin_round_mean = figure_4_data.mean()
    std = figure_4_data.std()   
    upper_band = each_spin_round_mean + std
    lower_band = each_spin_round_mean - std  
    df = pd.DataFrame({'mean':each_spin_round_mean, 'upper_band': upper_band, 'lower_band': lower_band}) 
    ax = df.plot()   
    ax.set_title('figure_4')
    ax.set_xlim([0,300])
    ax.set_ylim([-256,100])
    plt.savefig('figure_4')
    
def plot_figure_5():
    
    figure_5_data = simulate_episode_256_bankroll()
    figure_5_data = pd.DataFrame(figure_5_data)	
    each_spin_round_med = figure_5_data.median()
    std = figure_5_data.std()   
    upper_band = each_spin_round_med + std
    lower_band = each_spin_round_med - std  
    df = pd.DataFrame({'median':each_spin_round_med, 'upper_band': upper_band, 'lower_band': lower_band}) 
    ax = df.plot()   
    ax.set_title('figure_5')
    ax.set_xlim([0,300])
    ax.set_ylim([-256,100])
    plt.savefig('figure_5')

 		   		 		  
def test_code():  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		  	  		  		  		    	 		 		   		 		  
    """  		  	   		  	  		  		  		    	 		 		   		 		  
    win_prob = 9/19  # set appropriately to the probability of a win  		  	   		  	  		  		  		    	 		 		   		 		  
    np.random.seed(gtid())  # do this only once  		  	   		  	  		  		  		    	 		 		   		 		  
    print(get_spin_result(win_prob))  # test the roulette spin  		  	   		  	  		  		  		    	 		 		   		 		  
    # add your code here to implement the experiments  		  	   		  	  		  		  		    	 		 		   		 		  
    plot_figure_1()
    plot_figure_2()
    plot_figure_3()
    plot_figure_4()	   
    plot_figure_5()		  	  		  		  		    	 		 		   		 		  
  		  	   		
  	  		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		  	  		  		  		    	 		 		   		 		  
    test_code() 	  		  		  		    	 		 		   		 		  
