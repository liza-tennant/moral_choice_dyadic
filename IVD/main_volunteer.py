#!/cs/academic/phd3/lkarmann/my_env/bin/python3.8
# if running on a cluster
import pandas as pd
import numpy as np 
from matplotlib.pyplot import figure

#from test import Test #test out importing a module in this environment
#test_object = Test()
#test_object.test_function()

#import own modules that contain the player, environment and random nummber generator. 
from environment import Game_for_learning
from player import Player
from rn_generator import my_RN_generator
#from explorationpolicy import ExplorationPolicy

#import itertools 
#import matplotlib.pyplot as plt 
#import seaborn as sns 
#import pickle
#import random 
import os
import argparse

#state_index_converter = {(0,0):0, (0,1):1, (1,0):2, (1,1):3}

#os.chdir("~/Library/Mobile\ Documents/com~apple~CloudDocs/PhD_data")

PAYOFFMAT_IPD = [ [(3,3),(1,4)] , [(4,1),(2,2)] ] #IPD game 
PAYOFFMAT_VOLUNTEER = [ [(4,4),(2,5)] , [(5,2),(1,1)] ] #VOLUNTEER game 
PAYOFFMAT_STAGHUNT = [ [(5,5),(1,4)] , [(4,1),(2,2)] ] #STAGHUNT game 

my_game = 'VOLUNTEER' 

def reset_learning_parameters(counter, destination_folder, RNG): 
    #alpha0 = 0.5 #0.3 #0.01 # initial learning rate
    #decay = 0.0005 #0.005 # learning rate decay
    #gamma = 0.90 # discount factor
    #alpha0, decay, gamma now defined outside of this function!!    

    state_player1 = RNG.player1_streams[4].choice([(0,0), (0,1), (1,0), (1,1)], 1)
    state_player1 = tuple(state_player1[0])

    if 'TFT' in destination_folder: #specifically, if player2 is TFT
        state_player2 = (0,0) #hard-code as though TFT's opponent cooperated on the previous move, to force TFT to cooperate at first 
    else: 
        state_player2 = tuple(RNG.player2_streams[4].choice([(0,0), (0,1), (1,0), (1,1)], 1))
        state_player2 = tuple(state_player2[0])

    if counter == 1: #on the first iteration, save QL parameters to file for future reference
        with open(f'{destination_folder}/QL_parameters.txt', 'w') as fp:
            fp.write("run 0, Q-learning parameters: \n") # write each item on a new line
            fp.write("initial exploration rate eps0: %s \n" % str(eps0)) 
            fp.write("Is eps (exploration) decay to 0 present: %s \n" % str(epsdecay))
            fp.write("initial learning rate alpha0: %s \n" % str(alpha0)) 
            fp.write("learning rate decay: %s \n" % str(decay))
            fp.write("discount factor gamma: %s \n" % str(gamma))
            #fp.write("initial state_player1 at run0: %s \n" % str(state_player1))
            #fp.write("initial state_player2 at run0: %s \n" % str(state_player2))
            print('saved parameters for player1 & player2')

    return alpha0, decay, gamma, state_player1, state_player2

def create_pair_of_players(title1, title2, num_runs):
    strategy_mapping = {'AC':'AlwaysCooperate', 'AD':'AlwaysDefect', 'TFT':'TitForTat', 'Random':'random', 'QLS':'Q-Learning eps-greedy', 'QLUT':'Q-Learning eps-greedy', 'QLDE':'Q-Learning eps-greedy', 'QLVE_e':'Q-Learning eps-greedy', 'QLVE_k':'Q-Learning eps-greedy', 'QLVM':'Q-Learning eps-greedy'}
    moral_mapping = {'AC':None, 'AD':None, 'TFT':None, 'Random':None, 'QLS':None, 'QLUT':'Utilitarian', 'QLDE':'Deontological', 'QLVE_e':'VirtueEthics_equality', 'QLVE_k':'VirtueEthics_kindness', 'QLVM':'VirtueEthics_mixed'}

    pairs_of_players = [
        (Player(strategy=strategy_mapping[title1], moral_type=moral_mapping[title1], eps0=eps0, epsdecay=epsdecay, mixed_beta=mixed_beta), 
        Player(strategy=strategy_mapping[title2], moral_type=moral_mapping[title2], eps0=eps0, epsdecay=epsdecay, mixed_beta=mixed_beta)) 
        for i in range (num_runs)]
    
    return pairs_of_players

def store_raw_data(my_DF_list, my_range, destination_folder):
    '''This function takes in a DF_list resulting from n episodes & m iterations, 
    and stores each type of reward in its own dataframe for plotting. 
    It also stores the s,a,s' and eps values. '''
    #make sure folders 'player1' and 'player2' exist within each results folder before storing data

    if not os.path.isdir(str(destination_folder)+'/player1'):
        os.makedirs(str(destination_folder)+'/player1')

    if not os.path.isdir(str(destination_folder)+'/player2'):
        os.makedirs(str(destination_folder)+'/player2')

    #store game reward
    my_labels=['episode' for i in range(my_range)]

    df_reward_game_player1 = pd.concat([df['reward_game_player1'] for df in my_DF_list], axis=1)
    df_reward_game_player1.set_axis(my_labels, axis=1, inplace=True)
    df_reward_game_player1.to_csv(str(destination_folder+'/player1/df_reward_game.csv'))

    df_reward_game_player2 = pd.concat([df['reward_game_player2'] for df in my_DF_list], axis=1)
    df_reward_game_player2.set_axis(my_labels, axis=1, inplace=True)
    df_reward_game_player2.to_csv(str(destination_folder)+'/player2/df_reward_game.csv')

    #print('saved game reward')
    
    ##if we need different names for each column/episode:
    #my_labels = ['episode'+str(i+1) for i in range(30)]
    #df2 = df_reward_game_player1['episode'].set_axis(my_labels, axis=1, inplace=False)
    #df2.reset_index(inplace=True)

    #store intrinsic reward 
    df_reward_intrinsic_player1 = pd.concat([df['reward_intrinsic_player1'] for df in my_DF_list], axis=1)
    df_reward_intrinsic_player1.set_axis(my_labels, axis=1, inplace=True)
    df_reward_intrinsic_player1.to_csv(str(destination_folder)+'/player1/df_reward_intrinsic.csv')

    df_reward_intrinsic_player2 = pd.concat([df['reward_intrinsic_player2'] for df in my_DF_list], axis=1)
    df_reward_intrinsic_player2.set_axis(my_labels, axis=1, inplace=True)
    df_reward_intrinsic_player2.to_csv(str(destination_folder)+'/player2/df_reward_intrinsic.csv')
    #print('saved intrinsic reward')

    #store learning reward 
    df_reward_learning_player1 = pd.concat([df['reward_learning_player1'] for df in my_DF_list], axis=1)
    df_reward_learning_player1.set_axis(my_labels, axis=1, inplace=True)
    df_reward_learning_player1.to_csv(str(destination_folder)+'/player1/df_reward_learning.csv')

    df_reward_learning_player2 = pd.concat([df['reward_learning_player2'] for df in my_DF_list], axis=1)
    df_reward_learning_player2.set_axis(my_labels, axis=1, inplace=True)
    df_reward_learning_player2.to_csv(str(destination_folder)+'/player2/df_reward_learning.csv')
    #print('saved learning reward')

    #store cumulative_reward_game
    cumulative_reward_game_player1 = np.cumsum(df_reward_game_player1['episode'])
    cumulative_reward_game_player2 = np.cumsum(df_reward_game_player2['episode'])

    cumulative_reward_game_player1.to_csv(str(destination_folder)+'/player1/df_cumulative_reward_game.csv')
    cumulative_reward_game_player2.to_csv(str(destination_folder)+'/player2/df_cumulative_reward_game.csv')
    #print('saved cumulative game reward')

    #store cumulative_reward_intrinsic 
    cumulative_reward_intrinsic_player1 = np.cumsum(df_reward_intrinsic_player1['episode'])
    cumulative_reward_intrinsic_player2 = np.cumsum(df_reward_intrinsic_player2['episode'])

    cumulative_reward_intrinsic_player1.to_csv(str(destination_folder)+'/player1/df_cumulative_reward_intrinsic.csv')
    cumulative_reward_intrinsic_player2.to_csv(str(destination_folder)+'/player2/df_cumulative_reward_intrinsic.csv')
    #print('saved cumulative intrinsic reward')

    #store collective reward 
    df_reward_collective = pd.concat([df['reward_collective'] for df in my_DF_list], axis=1)
    df_reward_collective.set_axis(my_labels, axis=1, inplace=True)
    df_reward_collective.to_csv(str(destination_folder)+'/df_reward_collective.csv')
    #print('saved collective reward')

    #store cumulative_reward_collective
    cumulative_reward_collective = np.cumsum(df_reward_collective['episode'])
    cumulative_reward_collective.to_csv(str(destination_folder)+'/df_cumulative_reward_collective.csv')
    #print('saved cumulative collective reward')

    #store ratio reward 
    #df_reward_ratio = pd.concat([df['reward_ratio'] for df in my_DF_list], axis=1)
    #df_reward_ratio.set_axis(my_labels, axis=1, inplace=True)
    #df_reward_ratio.to_csv(str(destination_folder)+'/df_reward_ratio.csv')
    ##print('saved ratio reward')

    #store cumulative_reward_ratio
    #cumulative_reward_ratio = np.cumsum(df_reward_ratio['episode'])
    #cumulative_reward_ratio.to_csv(str(destination_folder)+'/df_cumulative_reward_ratio.csv')
    ##print('saved cumulative ratio reward')

    #store gini reward 
    df_reward_gini = pd.concat([df['reward_gini'] for df in my_DF_list], axis=1)
    df_reward_gini.set_axis(my_labels, axis=1, inplace=True)
    df_reward_gini.to_csv(str(destination_folder)+'/df_reward_gini.csv')
    #print('saved gini reward')

    #store cumulative_reward_gini
    cumulative_reward_gini = np.cumsum(df_reward_gini['episode'])
    cumulative_reward_gini.to_csv(str(destination_folder)+'/df_cumulative_reward_gini.csv')
    #print('saved cumulative gini reward')

    #store min reward 
    df_reward_min = pd.concat([df['reward_min'] for df in my_DF_list], axis=1)
    df_reward_min.set_axis(my_labels, axis=1, inplace=True)
    df_reward_min.to_csv(str(destination_folder)+'/df_reward_min.csv')
    #print('saved min reward')

    #store cumulative_reward_min
    cumulative_reward_min = np.cumsum(df_reward_min['episode'])
    cumulative_reward_min.to_csv(str(destination_folder)+'/df_cumulative_reward_min.csv')
    #print('saved cumulative min reward')


    #store state
    df_state_player1 = pd.concat([df['state_player1'] for df in my_DF_list], axis=1)
    df_state_player1.set_axis(my_labels, axis=1, inplace=True)
    df_state_player1.to_csv(str(destination_folder)+'/player1/state.csv')

    df_state_player2 = pd.concat([df['state_player2'] for df in my_DF_list], axis=1)
    df_state_player2.set_axis(my_labels, axis=1, inplace=True)
    df_state_player2.to_csv(str(destination_folder)+'/player2/state.csv')
    #print('saved state')

    #store action
    df_action_player1 = pd.concat([df['action_player1'] for df in my_DF_list], axis=1)
    df_action_player1.set_axis(my_labels, axis=1, inplace=True)
    df_action_player1.to_csv(str(destination_folder)+'/player1/action.csv')

    df_action_player2 = pd.concat([df['action_player2'] for df in my_DF_list], axis=1)
    df_action_player2.set_axis(my_labels, axis=1, inplace=True)
    df_action_player2.to_csv(str(destination_folder)+'/player2/action.csv')
    #print('saved action')

    #store next_state 
    #df_next_state_player1 = pd.concat([df['next_state_player1'] for df in my_DF_list], axis=1)
    #df_next_state_player1.set_axis(my_labels, axis=1, inplace=True)
    #df_next_state_player1.to_csv(str(destination_folder)+'/player1/next_state.csv')

    #df_next_state_player2 = pd.concat([df['next_state_player2'] for df in my_DF_list], axis=1)
    #df_next_state_player2.set_axis(my_labels, axis=1, inplace=True)
    #df_next_state_player2.to_csv(str(destination_folder)+'/player2/next_state.csv')
    ##print('saved next_state')

    #store eps 
    #df_eps_player1 = pd.concat([df['eps_player1'] for df in my_DF_list], axis=1)
    #df_eps_player1.set_axis(my_labels, axis=1, inplace=True)
    #if df_eps_player1.iloc[0,0] == df_eps_player1.iloc[1,0]:
    #    df_eps_player1.iloc[0].to_csv(str(destination_folder)+'/player1/eps.csv') #store only the first row, as eps does not decay
    #else: #store all eps as they decay 
    #    df_eps_player1.to_csv(str(destination_folder)+'/player1/eps.csv')

    #try: 
    #    df_eps_player2 = pd.concat([df['eps_player2'] for df in my_DF_list], axis=1)
    #    df_eps_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_eps_player2.to_csv(str(destination_folder)+'/player2/eps.csv')
    #    #print('saved eps')
    #except: 
    #    print('failed to save eps_player2')

    #store reason 
    #df_reason_player1 = pd.concat([df['reason_player1'] for df in my_DF_list], axis=1)
    #df_reason_player1.set_axis(my_labels, axis=1, inplace=True)
    #df_reason_player1.to_csv(str(destination_folder)+'/player1/reason.csv')

    #try: 
    #    df_reason_player2 = pd.concat([df['reason_player2'] for df in my_DF_list], axis=1)
    #    df_reason_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_reason_player2.to_csv(str(destination_folder)+'/player2/reason.csv')
    #    #print('saved reason')
    #except: 
    #    print('failed to save reason_player2')
    
    #store RN used here
    #df_RN_player1 = pd.concat([df['RNs_player1'] for df in my_DF_list], axis=1)
    #df_RN_player1.set_axis(my_labels, axis=1, inplace=True)
    #df_RN_player1.to_csv(str(destination_folder)+'/player1/randomnumbers.csv')
    ##print('saved RNs')

    #try: 
    #    df_RN_player2 = pd.concat([df['RNs_player2'] for df in my_DF_list], axis=1)
    #    df_RN_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_RN_player2.to_csv(str(destination_folder)+'/player2/randomnumbers.csv')
    #    #print('saved RNs')
    #except: 
    #    print('failed to save RNs_player2')

    print('done storing all raw data')

# TO DO maybe edit store_raw_data so it does not store intrinsic reward in cases where it is empty 


def store_raw_data_new(destination_folder, my_range):
    '''This function takes in a DF_list resulting from n episodes & m iterations, 
    and stores each type of reward in its own dataframe for plotting. 
    It also stores the s,a,s' and eps values. '''
    #make sure folders 'player1' and 'player2' exist within each results folder before storing data

    my_DF_list = [pd.read_csv(str(destination_folder)+f'/history/run{run_idx+1}.csv', index_col=0) for run_idx in range(my_range)] ## ?? is this the best way of doing this ??? 

    if not os.path.isdir(str(destination_folder)+'/player1'):
        os.makedirs(str(destination_folder)+'/player1')

    if not os.path.isdir(str(destination_folder)+'/player2'):
        os.makedirs(str(destination_folder)+'/player2')

    #store game reward
    my_labels=['episode' for i in range(my_range)]

    df_reward_game_player1 = pd.concat([df['reward_game_player1'] for df in my_DF_list], axis=1)
    df_reward_game_player1.set_axis(my_labels, axis=1, inplace=True)
    df_reward_game_player1.to_csv(str(destination_folder+'/player1/df_reward_game.csv'))

    df_reward_game_player2 = pd.concat([df['reward_game_player2'] for df in my_DF_list], axis=1)
    df_reward_game_player2.set_axis(my_labels, axis=1, inplace=True)
    df_reward_game_player2.to_csv(str(destination_folder)+'/player2/df_reward_game.csv')

    #print('saved game reward')
    
    ##if we need different names for each column/episode:
    #my_labels = ['episode'+str(i+1) for i in range(30)]
    #df2 = df_reward_game_player1['episode'].set_axis(my_labels, axis=1, inplace=False)
    #df2.reset_index(inplace=True)

    #store intrinsic reward 
    df_reward_intrinsic_player1 = pd.concat([df['reward_intrinsic_player1'] for df in my_DF_list], axis=1)
    df_reward_intrinsic_player1.set_axis(my_labels, axis=1, inplace=True)
    df_reward_intrinsic_player1.to_csv(str(destination_folder)+'/player1/df_reward_intrinsic.csv')

    df_reward_intrinsic_player2 = pd.concat([df['reward_intrinsic_player2'] for df in my_DF_list], axis=1)
    df_reward_intrinsic_player2.set_axis(my_labels, axis=1, inplace=True)
    df_reward_intrinsic_player2.to_csv(str(destination_folder)+'/player2/df_reward_intrinsic.csv')
    #print('saved intrinsic reward')

    #store learning reward 
    #try:
    #    df_reward_learning_player1 = pd.concat([df['reward_learning_player1'] for df in my_DF_list], axis=1)
    #    df_reward_learning_player1.set_axis(my_labels, axis=1, inplace=True)
    #    df_reward_learning_player1.to_csv(str(destination_folder)+'/player1/df_reward_learning.csv')
    #except: 
    #    print('failed to save reward_learning_player1')

    #try:
    #    df_reward_learning_player2 = pd.concat([df['reward_learning_player2'] for df in my_DF_list], axis=1)
    #    df_reward_learning_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_reward_learning_player2.to_csv(str(destination_folder)+'/player2/df_reward_learning.csv')
    #except: 
    #    print('failed to save reward_learning_player2')
    ##print('saved learning reward')

    #store cumulative_reward_game
    cumulative_reward_game_player1 = np.cumsum(df_reward_game_player1['episode'])
    cumulative_reward_game_player2 = np.cumsum(df_reward_game_player2['episode'])

    cumulative_reward_game_player1.to_csv(str(destination_folder)+'/player1/df_cumulative_reward_game.csv')
    cumulative_reward_game_player2.to_csv(str(destination_folder)+'/player2/df_cumulative_reward_game.csv')
    #print('saved cumulative game reward')

    #store cumulative_reward_intrinsic 
    cumulative_reward_intrinsic_player1 = np.cumsum(df_reward_intrinsic_player1['episode'])
    cumulative_reward_intrinsic_player2 = np.cumsum(df_reward_intrinsic_player2['episode'])

    cumulative_reward_intrinsic_player1.to_csv(str(destination_folder)+'/player1/df_cumulative_reward_intrinsic.csv')
    cumulative_reward_intrinsic_player2.to_csv(str(destination_folder)+'/player2/df_cumulative_reward_intrinsic.csv')
    #print('saved cumulative intrinsic reward')

    #store collective reward 
    df_reward_collective = pd.concat([df['reward_collective'] for df in my_DF_list], axis=1)
    df_reward_collective.set_axis(my_labels, axis=1, inplace=True)
    df_reward_collective.to_csv(str(destination_folder)+'/df_reward_collective.csv')
    #print('saved collective reward')

    #store cumulative_reward_collective
    cumulative_reward_collective = np.cumsum(df_reward_collective['episode'])
    cumulative_reward_collective.to_csv(str(destination_folder)+'/df_cumulative_reward_collective.csv')
    #print('saved cumulative collective reward')

    #store ratio reward 
    #df_reward_ratio = pd.concat([df['reward_ratio'] for df in my_DF_list], axis=1)
    #df_reward_ratio.set_axis(my_labels, axis=1, inplace=True)
    #df_reward_ratio.to_csv(str(destination_folder)+'/df_reward_ratio.csv')
    ##print('saved ratio reward')

    #store cumulative_reward_ratio
    #cumulative_reward_ratio = np.cumsum(df_reward_ratio['episode'])
    #cumulative_reward_ratio.to_csv(str(destination_folder)+'/df_cumulative_reward_ratio.csv')
    ##print('saved cumulative ratio reward')

    #store gini reward 
    df_reward_gini = pd.concat([df['reward_gini'] for df in my_DF_list], axis=1)
    df_reward_gini.set_axis(my_labels, axis=1, inplace=True)
    df_reward_gini.to_csv(str(destination_folder)+'/df_reward_gini.csv')
    #print('saved gini reward')

    #store cumulative_reward_gini
    cumulative_reward_gini = np.cumsum(df_reward_gini['episode'])
    cumulative_reward_gini.to_csv(str(destination_folder)+'/df_cumulative_reward_gini.csv')
    #print('saved cumulative gini reward')

    #store min reward 
    df_reward_min = pd.concat([df['reward_min'] for df in my_DF_list], axis=1)
    df_reward_min.set_axis(my_labels, axis=1, inplace=True)
    df_reward_min.to_csv(str(destination_folder)+'/df_reward_min.csv')
    #print('saved min reward')

    #store cumulative_reward_min
    cumulative_reward_min = np.cumsum(df_reward_min['episode'])
    cumulative_reward_min.to_csv(str(destination_folder)+'/df_cumulative_reward_min.csv')
    #print('saved cumulative min reward')


    #store state
    df_state_player1 = pd.concat([df['state_player1'] for df in my_DF_list], axis=1)
    df_state_player1.set_axis(my_labels, axis=1, inplace=True)
    df_state_player1.to_csv(str(destination_folder)+'/player1/state.csv')

    df_state_player2 = pd.concat([df['state_player2'] for df in my_DF_list], axis=1)
    df_state_player2.set_axis(my_labels, axis=1, inplace=True)
    df_state_player2.to_csv(str(destination_folder)+'/player2/state.csv')
    #print('saved state')

    #store action
    df_action_player1 = pd.concat([df['action_player1'] for df in my_DF_list], axis=1)
    df_action_player1.set_axis(my_labels, axis=1, inplace=True)
    df_action_player1.to_csv(str(destination_folder)+'/player1/action.csv')

    df_action_player2 = pd.concat([df['action_player2'] for df in my_DF_list], axis=1)
    df_action_player2.set_axis(my_labels, axis=1, inplace=True)
    df_action_player2.to_csv(str(destination_folder)+'/player2/action.csv')
    #print('saved action')

    #store next_state 
    #df_next_state_player1 = pd.concat([df['next_state_player1'] for df in my_DF_list], axis=1)
    #df_next_state_player1.set_axis(my_labels, axis=1, inplace=True)
    #df_next_state_player1.to_csv(str(destination_folder)+'/player1/next_state.csv')

    #df_next_state_player2 = pd.concat([df['next_state_player2'] for df in my_DF_list], axis=1)
    #df_next_state_player2.set_axis(my_labels, axis=1, inplace=True)
    #df_next_state_player2.to_csv(str(destination_folder)+'/player2/next_state.csv')
    ##print('saved next_state')

    #store eps 
    #try:
    #    df_eps_player1 = pd.concat([df['eps_player1'] for df in my_DF_list], axis=1)
    #    df_eps_player1.set_axis(my_labels, axis=1, inplace=True)
    #    if df_eps_player1.iloc[0,0] == df_eps_player1.iloc[1,0]:
    #        df_eps_player1.iloc[0].to_csv(str(destination_folder)+'/player1/eps.csv') #store only the first row, as eps does not decay
    #    else: #store all eps as they decay 
    #        df_eps_player1.to_csv(str(destination_folder)+'/player1/eps.csv')
    #except:
    #    print('failed to save eps_player1')

    #try: 
    #    df_eps_player2 = pd.concat([df['eps_player2'] for df in my_DF_list], axis=1)
    #    df_eps_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_eps_player2.to_csv(str(destination_folder)+'/player2/eps.csv')
    #    #print('saved eps')
    #except: 
    #    print('failed to save eps_player2')

    #store reason 
    #try:
    #    df_reason_player1 = pd.concat([df['reason_player1'] for df in my_DF_list], axis=1)
    #    df_reason_player1.set_axis(my_labels, axis=1, inplace=True)
    #    df_reason_player1.to_csv(str(destination_folder)+'/player1/reason.csv')
    #except: 
    #    print('failed to save reason_player1')

    #try: 
    #    df_reason_player2 = pd.concat([df['reason_player2'] for df in my_DF_list], axis=1)
    #    df_reason_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_reason_player2.to_csv(str(destination_folder)+'/player2/reason.csv')
    #    #print('saved reason')
    #except: 
    #    print('failed to save reason_player2')
    
    #store RN used here
    #try:
    #    df_RN_player1 = pd.concat([df['RNs_player1'] for df in my_DF_list], axis=1)
    #    df_RN_player1.set_axis(my_labels, axis=1, inplace=True)
    #    df_RN_player1.to_csv(str(destination_folder)+'/player1/randomnumbers.csv')
    #except:
    #    print('failed to save RNs_player1')
    ##print('saved RNs')

    #try: 
    #    df_RN_player2 = pd.concat([df['RNs_player2'] for df in my_DF_list], axis=1)
    #    df_RN_player2.set_axis(my_labels, axis=1, inplace=True)
    #    df_RN_player2.to_csv(str(destination_folder)+'/player2/randomnumbers.csv')
    #    #print('saved RNs')
    #except: 
    #    print('failed to save RNs_player2')

    print('done storing all raw data')


def store_learning_data(my_RESULTS_list, my_Q_VALUES_player1_list, my_Q_VALUES_player2_list, destination_folder):
    '''save results (= learnt optimal actions), Q_values_player1 and Q_values_player2, or just player1 if player2 was static.
    Save in two formats - npy for plotting and txt for visual inspection. '''
    #save RESULTS_list to numpy 
    np.save(str(destination_folder) + r'/RESULTS_list.npy', my_RESULTS_list, allow_pickle=True)

    #save RESULTS_list to txt
    with open(str(destination_folder) + r'/RESULTS_list.txt', 'w') as fp:
        for item in my_RESULTS_list:
            # write each item on a new line
            fp.write("%s\n" % str(item)) #as player2 is static (not learning), only save the learnt optiomal policies for player1 
        #print('done saving results (optimal policies)')
    
    #save Q_VALUES_list for player1 (learning over time) to npy file
    np.save(str(destination_folder) + r'/Q_VALUES_player1_list.npy', my_Q_VALUES_player1_list, allow_pickle=True)
    
    #save Q_VALUES_list for each player (learning over time) to txt file
    with open(str(destination_folder) + r'/Q_VALUES_player1_list.txt', 'w') as fp:
        for item in my_Q_VALUES_player1_list:
            fp.write("%s\n" % str(item))
        #print('done saving Q_values_player1')

    #save Q_VALUES_list for player2 if available - if player2 is a QL player
    if my_Q_VALUES_player2_list: 
        np.save(str(destination_folder) + r'/Q_VALUES_player2_list.npy', my_Q_VALUES_player2_list, allow_pickle=True)

        with open(str(destination_folder) + r'/Q_VALUES_player2_list.txt', 'w') as fp:
            for item in my_Q_VALUES_player2_list:
                fp.write("%s\n" % str(item))
            #print('done saving Q_values_player2')
    else: 
        print ('failed to save Q_values_player2')
        print('done storing all learning data')




def run_one_episode_mixed(counter, player1, player2, num_iter, RNG, destination_folder):
    '''this instantiates a game with 2 players 
    (player1 is a learning player (maybe with a fixed moral type) and player2 is a static player),
    and outputs:
    1) a dataframe with the game history that can be used for plotting
    2) a list of learnt optimal policies (to interpret the learning outcome)
    3) a history of all Q-values for visualisation '''

    #print(f'running 1 run, {num_iter} iterations each, storing in {destination_folder}')

    if my_game == 'IPD':
        PAYOFFMAT = PAYOFFMAT_IPD
    elif my_game == 'VOLUNTEER':
        PAYOFFMAT = PAYOFFMAT_VOLUNTEER
    elif my_game == 'STAGHUNT':
        PAYOFFMAT = PAYOFFMAT_STAGHUNT

    game = Game_for_learning(player1, player2, PAYOFFMAT, n_games=1)
    #game.run(1)

    global_history = pd.DataFrame.from_dict({'state_player1':[None], 'action_player1':[None], 
                                            'state_player2':[None], 'action_player2':[None] , 'reward_game_player1':[None], 'next_state_player1':[None],
                                            'reward_game_player2':[None], 'next_state_player2':[None], 
                                            'reward_intrinsic_player1':[None], 'reward_intrinsic_player2':[None], #NB reward_intrinsic_player2 will remian empty
                                            'reward_collective':[None], 'reward_ratio':[None], 'reward_gini':[None], 'reward_min':[None],
                                            'reward_learning_player1':[None], 'reward_learning_player2':[None],
                                            'eps_player1':[None], 'reason_player1':[None], 'RNs_player1':[None]}) 

    player1.Q_values = np.zeros((4, 2)) #np.zeros((2, 2))
    state_index_converter = game.state_index_converter
    
    #store myVars to allow the code to refer to a previously defined variable name - used to look up Q-value table for each agent
    #myVars = vars()

    alpha0, decay, gamma, state_player1, state_player2 = reset_learning_parameters(counter, destination_folder, RNG)
    history_Qvalues_player1 = []    

    for iteration in range(num_iter): #e.g. num_iter - e.g. encounters
        #print('iteration: ', iteration, '; state_player1: ', state_player1)
        history_Qvalues_player1.append(player1.Q_values.copy()) 

        #execute a step that interacts with the environment & updates global_history behind the scenes 
        action_player1, next_state_player1, next_state_player2, reward_learning_player1 = game.step_mixed(state_player1, state_player2, iteration, global_history, num_iter, RNG)
        
        #if need to debug - print the below 
        #print('state_player1 = ', state_player1, 'state_player2 = ', state_player2)

        state_index_player1 = state_index_converter[state_player1]
        #state_index_player2 = state_index_converter[state_player2]

        next_state_index_player1 = state_index_converter[next_state_player1] #NEW

        alpha = alpha0 / (1 + iteration * decay)

        next_value_player1 = np.max(player1.Q_values[next_state_index_player1]) # greedy policy at the next step
        #NOTE the above will choose C,C when all cells are 0 --> will need to wait until random exploration to try D instead of C... 
        player1.Q_values[state_index_player1, action_player1] *= 1 - alpha #TO DO change this to state_index 
        player1.Q_values[state_index_player1, action_player1] += alpha * (reward_learning_player1 + gamma * next_value_player1)
        state_player1 = next_state_player1
        
        state_player2 = next_state_player2
        

    history_Qvalues_player1 = np.array(history_Qvalues_player1) 

    result = np.zeros(4) #np.argmax(player1.Q_values, axis=1)
    for state in range(len(result)):
        if not np.any(player1.Q_values[state]): #if empty
            result[state] = None
        else:
            result[state] = np.argmax(player1.Q_values[state]) #, axis=1
    #print(f'in episode {counter}, {num_iter} iterations, the player learnt the following optimal policies: ', result)

    return global_history, result, history_Qvalues_player1

def run_one_episode(counter, player1, player2, num_iter, RNG, destination_folder): 
    '''this instantiates a game with 2 players (each player learning a strategy and potentially having a pre-defined moral type),
    and outputs three things:
    1) a dataframe with the game history that can be used for plotting
    2) a list of learnt optimal policies (to interpret the learning outcome)
    3) a pair of Q-value histories, also for plotting. '''

    if my_game == 'IPD':
        PAYOFFMAT = PAYOFFMAT_IPD
    elif my_game == 'VOLUNTEER':
        PAYOFFMAT = PAYOFFMAT_VOLUNTEER
    elif my_game == 'STAGHUNT':
        PAYOFFMAT = PAYOFFMAT_STAGHUNT

    game = Game_for_learning(player1, player2, PAYOFFMAT, n_games=1)
    #possible_actions = [[0, 1], [0, 1]] #shape = state C,D; action C,D

    global_history = pd.DataFrame.from_dict({'state_player1':[None], 'action_player1':[None], 
                                            'state_player2':[None], 'action_player2':[None] , 'reward_game_player1':[None], 'next_state_player1':[None],
                                            'reward_game_player2':[None], 'next_state_player2':[None], 
                                            'reward_intrinsic_player1':[None], 'reward_intrinsic_player2':[None], 
                                            'reward_collective':[None], 'reward_ratio':[None], 'reward_gini':[None], 'reward_min':[None],
                                            'reward_learning_player1':[None], 'reward_learning_player2':[None],
                                            'eps_player1':[None], 'eps_player2':[None], 'reason_player1':[None], 'reason_player2':[None],
                                            'RNs_player1':[None], 'RNs_player2':[None]})

    #Q-Learning:
    player1.Q_values = np.zeros((4, 2))#np.zeros((2, 2))
    player2.Q_values = np.zeros((4, 2))
    state_index_converter = game.state_index_converter

    alpha0, decay, gamma, state_player1, state_player2 = reset_learning_parameters(counter, destination_folder, RNG) #player1 & player2 will use the same learning parameters

    history_Qvalues_player1 = [] 
    history_Qvalues_player2 = [] 

    for iteration in range(num_iter): #default =10000 encounters of the game
        
        history_Qvalues_player1.append(player1.Q_values.copy()) 
        history_Qvalues_player2.append(player2.Q_values.copy()) 

        #execute a step that interacts with the environment & updates global_history behind the scenes 
        action_player1, action_player2, next_state_player1, next_state_player2, reward_learning_player1, reward_learning_player2 = game.step(state_player1, state_player2, iteration, global_history, num_iter, RNG)
        
        state_index_player1 = state_index_converter[state_player1]
        state_index_player2 = state_index_converter[state_player2]

        next_state_index_player1 = state_index_converter[next_state_player1] #NEW
        next_state_index_player2 = state_index_converter[next_state_player2] #NEW

        alpha = alpha0 / (1 + iteration * decay)

        #next_value_player1 = np.max(player1.Q_values[next_state_player1]) # greedy policy at the next step
        next_value_player1 = np.max(player1.Q_values[next_state_index_player1]) # NEW
        player1.Q_values[state_index_player1, action_player1] *= 1 - alpha 
        player1.Q_values[state_index_player1, action_player1] += alpha * (reward_learning_player1 + gamma * next_value_player1)
        state_player1 = next_state_player1
        
        #next_value_player2 = np.max(player2.Q_values[next_state_player2]) # greedy policy at the next step
        next_value_player2 = np.max(player2.Q_values[next_state_index_player2]) # NEW
        player2.Q_values[state_index_player2, action_player2] *= 1 - alpha 
        player2.Q_values[state_index_player2, action_player2] += alpha * (reward_learning_player2 + gamma * next_value_player2)
        state_player2 = next_state_player2

    history_Qvalues_player1 = np.array(history_Qvalues_player1) 
    history_Qvalues_player2 = np.array(history_Qvalues_player2) 

    #result = np.argmax(player1.Q_values, axis=1), np.argmax(player1.Q_values, axis=1)
    #print(f'in episode {counter}, {num_iter} iterations, the two players learnt the following optimal policies: ', result)

    result_player1 = np.zeros(4) #np.argmax(player1.Q_values, axis=1)
    for state in range(len(result_player1)):
        if not np.any(player1.Q_values[state]): #if empty
            result_player1[state] = None
        else:
            result_player1[state] = np.argmax(player1.Q_values[state]) #, axis=1

    result_player2 = np.zeros(4) #np.argmax(player1.Q_values, axis=1)
    for state in range(len(result_player2)):
        if not np.any(player2.Q_values[state]): #if empty
            result_player2[state] = None
        else:
            result_player2[state] = np.argmax(player2.Q_values[state]) #, axis=1
        
    result = (result_player1, result_player2)

    #print(f'in episode {counter}, {num_iter} iterations, the two players learnt the following optimal policies: ', result)

    return global_history, result, history_Qvalues_player1, history_Qvalues_player2

def run_one_episode_static(counter, player1, player2, num_iter, RNG): 
    '''this instantiates a game with 2 players (each with a fixe / static / pre-defined strategy and moral type),
    and outputs:
    1) a dataframe with the game history that can be used for plotting'''

    if my_game == 'IPD':
        PAYOFFMAT = PAYOFFMAT_IPD
    elif my_game == 'VOLUNTEER':
        PAYOFFMAT = PAYOFFMAT_VOLUNTEER
    elif my_game == 'STAGHUNT':
        PAYOFFMAT = PAYOFFMAT_STAGHUNT 

    game = Game_for_learning(player1, player2, PAYOFFMAT, n_games=1)
    #game.run(1)

    #possible_actions = [[0, 1], [0, 1]] #shape = C,D

    global_history = pd.DataFrame.from_dict({'state_player1':[None], 'action_player1':[None], 
                                            'state_player2':[None], 'action_player2':[None] , 'reward_game_player1':[None], 'next_state_player1':[None],
                                            'reward_game_player2':[None], 'next_state_player2':[None], 
                                            'reward_intrinsic_player1':[None], 'reward_intrinsic_player2':[None], 
                                            'reward_collective':[None], 'reward_ratio':[None], 'reward_gini':[None], 'reward_min':[None]})

    #state_player1 = 0 # initial state = as though opponent Cooperated in the previous move
    #state_player2 = 0
    state_player1 = RNG.player1_streams[4].choice([(0,0), (0,1), (1,0), (1,1)], 1)
    state_player1 = tuple(state_player1[0])
    if 'TFT' in destination_folder: #specifically, if player2 is TFT
        state_player2 = (0,0) #hard-code as though TFT's opponent cooperated on the previous move, to forcce TFT to cooperate at first 
    else: 
        state_player2 = tuple(RNG.player2_streams[4].choice([(0,0), (0,1), (1,0), (1,1)], 1))
        state_player2 = tuple(state_player2[0])
    #TO DO vary the initial state and see what changes 

    #print('from run_one_episode_static function, 1st iteration: state_player1 = ', state_player1)

    for iteration in range(num_iter):
        #execute a step that interacts with the environment & updates global_history behind the scenes 
        next_state_player1, next_state_player2 = game.step_static(state_player1=state_player1, state_player2=state_player2, iteration=iteration, global_history=global_history, RNG=RNG)

        state_player1 = next_state_player1
        state_player2 = next_state_player2

        #if need to debug - print the below 
        #print('state_player1 = ', state_player1, 'state_player2 = ', state_player2)
        #print('action_player1 = ', action_player1, 'action_player2 = ', action_player2)

    #print(f'one episode (episode {counter}), {num_iter} iterations complete')
    return global_history 


def save_history(history_df, run_idx, destination_folder):
    if not os.path.isdir(str(destination_folder)+'/history'):
        os.makedirs(str(destination_folder)+'/history')

    history_df.to_csv(str(destination_folder)+f'/history/run{run_idx}.csv')


def run_mixed_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2):
    '''funnction to run n_runs encounters between player1=QL, player2=static'''
    print(f'running {title1} vs {title2}, {num_runs} runs, {num_iterations} iterations each, storing in {destination_folder}')
    if 'QL' not in title1:
        return '!! this is not the right function for these player types !!'
    
    if not os.path.isdir('results/'+ str(destination_folder)):
        os.makedirs('results/'+ str(destination_folder))
    destination_folder = 'results/'+ str(destination_folder)

    pairs_of_players = create_pair_of_players(title1, title2, num_runs)

    #instantiate the RN_generator before I run my n runs - so that all n runs share a single set of RN streams (4, to be exact) and read from it sequentially
    my_RNG = my_RN_generator(master_seed) #4 #1862
    my_RNG.generate(destination_folder=destination_folder)

    DF_list = list()
    RESULTS_list = list()
    Q_VALUES_player1_list = []
    counter = 0
    for player1, player2 in pairs_of_players:
        counter += 1
        #print('player1: ', player1)
        global_history, result, history_Qvalues_player1 = run_one_episode_mixed(counter, player1, player2, num_iterations, my_RNG, destination_folder)
        save_history(history_df=global_history, run_idx=counter, destination_folder=destination_folder)
        RESULTS_list.append(result) #save the optimal policies
        Q_VALUES_player1_list.append(history_Qvalues_player1)
        print(f'finished run {counter}, {title1} vs {title2}')

    ## store raw data (DF_list) - all 100 data points for each type of reward: ##
    store_raw_data_new(destination_folder=destination_folder, my_range=num_runs)

    #store learnt optimal oplicies and learnt Q-values over time
    store_learning_data(my_RESULTS_list=RESULTS_list, my_Q_VALUES_player1_list=Q_VALUES_player1_list, my_Q_VALUES_player2_list=None, destination_folder=destination_folder)

def run_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2):
    '''function to run n_runs encounters between player1=QL, player2=QL'''
    print(f'running {title1} vs {title2}, {num_runs} runs, {num_iterations} iterations each, storing in {destination_folder}')
    #check that this is the right function for theese types of players: 
    if 'QL' not in title1:
        return '!! this is not the right function for these player types !!'
    if 'QL' not in title2:
        return '!! this is not the right function for these player types !!'

    if not os.path.isdir('results/'+ str(destination_folder)):
        os.makedirs('results/'+ str(destination_folder))
    destination_folder = 'results/'+ str(destination_folder)

    pairs_of_players = create_pair_of_players(title1, title2, num_runs)

    #instantiate the RN_generator before I run my n runs - so that all n runs share a single set of RN streams (4, to be exact) and read from it sequentially
    my_RNG = my_RN_generator(master_seed) #4 #1862
    my_RNG.generate(destination_folder=destination_folder)

    DF_list = list()
    RESULTS_list = list()
    Q_VALUES_player1_list = []
    Q_VALUES_player2_list = []
    counter = 0
    for player1, player2 in pairs_of_players:
        counter += 1
        #print('player1: ', player1)
        global_history, result, history_Qvalues_player1, history_Qvalues_player2 = run_one_episode(counter, player1, player2, num_iterations, my_RNG, destination_folder)
        RESULTS_list.append(result) #save the optimal policies
        Q_VALUES_player1_list.append(history_Qvalues_player1)
        Q_VALUES_player2_list.append(history_Qvalues_player2)
        save_history(history_df=global_history, run_idx=counter, destination_folder=destination_folder) 
        print(f'finished run {counter}, {title1} vs {title2}')

     ## store raw data (DF_list) - all 100 data points for each type of reward: ##
    store_raw_data_new(destination_folder=destination_folder, my_range=num_runs)

    #store learnt optimal oplicies and learnt Q-values over time
    store_learning_data(my_RESULTS_list=RESULTS_list, my_Q_VALUES_player1_list=Q_VALUES_player1_list, my_Q_VALUES_player2_list=Q_VALUES_player2_list, destination_folder=destination_folder)

def run_static(master_seed, num_runs, num_iterations, destination_folder, title1, title2):
    '''function to run n_runs encounters between player1=static, player2=static'''
    print(f'running {title1} vs {title2}, {num_runs} runs, {num_iterations} iterations each, storing in {destination_folder}')
    if 'QL' in title1:
        return '!! this is not the right function for these player types !!'
    if 'QL' in title2:
        return '!! this is not the right function for these player types !!'
    
    if not os.path.isdir('results/'+ str(destination_folder)):
        os.makedirs('results/'+ str(destination_folder))
    destination_folder = 'results/'+ str(destination_folder)

    pairs_of_players = create_pair_of_players(title1, title2, num_runs)

    #instantiate the RN_generator before I run my n runs - so that all n runs share a single set of RN streams (4, to be exact) and read from it sequentially
    my_RNG = my_RN_generator(master_seed) #4 #1862
    my_RNG.generate(destination_folder=destination_folder)

    #DF_list = list()
    counter = 0
    for player1, player2 in pairs_of_players:
        counter += 1
        #print('player1: ', player1)
        global_history = run_one_episode_static(counter, player1, player2, num_iterations, my_RNG)

        #### NEW ####
        save_history(history_df=global_history, run_idx=counter, destination_folder=destination_folder)
        #DF_list.append(global_history)
        print(f'finished run {counter}, {title1} vs {title2}')

    #store_raw_data(my_DF_list=DF_list, my_range=num_runs, destination_folder=destination_folder)
    store_raw_data_new(destination_folder=destination_folder, my_range=num_runs)


#read in two player titles from user input on the command line
parser = argparse.ArgumentParser(description='Process two player titles (short versions) from user string input.')
parser.add_argument('--title1', type=str, required=True, help='the title for player1 - required')
parser.add_argument('--title2', type=str, required=True, help='the title for player2 - required')

parser.add_argument('--master_seed', type=int, required=False, help='master seed to initialise random number generator - optional, default 1')
parser.add_argument('--num_iterations', type=int, required=False, help='number of iterations to be run in one run - optional, default 10000')
parser.add_argument('--num_runs', type=int, required=False, help='number of runs/replicas with different seeds to be created - optional, default 100')
parser.add_argument('--eps0', type=float, required=False, help='the initial exploration rate eps to be used when playing actions (will decay to 0) - optional, default 0.05. NOTE if you feed in eps0, it will assume that eps must decay to 0')
parser.add_argument('--epsdecay', type=bool, required=False, help='whether eps decay is present, default False')
parser.add_argument('--alpha0', type=float, required=False, help='the initial learning rate alpha to be used in Q-Learning, default 0.01')
parser.add_argument('--decay', type=float, required=False, help='the learning rate decay to be used in Q-Learning, default 0')
parser.add_argument('--gamma', type=float, required=False, help='the discount factor to be used in Q-Learning, default 0.9')
parser.add_argument('--beta', type=float, required=False, help='the beta to be used for relative weighting of two mixed virtue rewards, default 0.5')
parser.add_argument('--extra', type=str, required=False, help='extra detail to be added to the destination_folder name - optional')

args = parser.parse_args()
title1 = args.title1
title2 = args.title2
destination_folder = title1+'_'+title2

#try to read in the optional arguments
if args.master_seed:
    master_seed = args.master_seed
    destination_folder += f'_seed{master_seed}'
else: 
    master_seed = 1 

if args.num_iterations:
    num_iterations = args.num_iterations
    destination_folder += f'_iter{num_iterations}'
else: 
    num_iterations=10000 

if args.num_runs:
    num_runs = args.num_runs
    destination_folder += f'_runs{num_runs}'
else: 
    num_runs = 100

if args.extra:
    destination_folder += f'_{args.extra}'


if args.eps0:
    eps0 = args.eps0
    destination_folder += f'_eps0{eps0}'
else: 
    eps0 = 0.05

if args.epsdecay:
    epsdecay = True
    destination_folder += '_epsdecay'
else: 
    epsdecay = False

if args.alpha0:
    alpha0 = args.alpha0
    destination_folder += f'_alpha0{alpha0}'
else: 
    alpha0 = 0.01

if args.decay:
    decay = args.decay
    destination_folder += f'_decay{decay}'
else: 
    decay = 0 

if args.gamma:
    gamma = args.gamma
    destination_folder += f'_gamma{gamma}'
else: 
    gamma = 0.9 

if args.beta:
    mixed_beta = args.beta
    destination_folder += f'_beta{mixed_beta}'
else: 
    mixed_beta = 0.5
    

#run given number of episodes & iterations for this specific pair of players , after establishing which function to use for this pair of players: 
if 'QL' in title1: 
    if 'QL' in title2: 
        run_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2)
    else: #if player2 is static
        run_mixed_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2)
else: #if both players are static
    run_static(master_seed, num_runs, num_iterations, destination_folder, title1, title2)


#baseline QL parameters: seed=1, eps=5%, alpha=0.5 & decay=0.0005, num_iter=10000




#
#run_and_save(master_seed=1, num_runs=2, num_iterations=10000, destination_folder='QLS_QLS_test', title1='QLS', title2='QLS')
#num_runs=5
#destination_folder='Random_Random_runs5'
#my_DF_list = [pd.read_csv('results/'+ str(destination_folder)+f'/history/run{run_idx+1}.csv', index_col=0) for run_idx in range(num_runs)]
#store_raw_data_new(destination_folder='results/'+str(destination_folder), my_range=num_runs)


