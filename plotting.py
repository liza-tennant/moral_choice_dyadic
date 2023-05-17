#plotting rewards (mean and cumulative mean with SD); actions (C or D) and actions types (in response to state) 
import numpy as np
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt 
import seaborn as sns 
from matplotlib.pyplot import figure
import dataframe_image as dfi
import os 
#import scipy.stats as st

#TO DO 
# edit plot_last_20_actions & plot_firt_20_actions to have more readable titles and conssitent colors for certsin action-state pairs

# - add CI instead of SD to the collective outcome plots - CHECK
# - ensure QLS_TFT and QLS_Random are being plotted on collective outcomes plots 
# make colors more consistent 
# make cumulative plots y-axis all the same scale, for ease of comparison 


#PAYOFFMAT_IPD = [ [(3,3),(1,4)] , [(4,1),(2,2)] ] #IPD game 
#PAYOFFMAT_VOLUNTEER = [ [(4,4),(2,5)] , [(5,2),(1,1)] ] #VOLUNTEER game 
#PAYOFFMAT_STAGHUNT = [ [(5,5),(1,4)] , [(4,1),(2,2)] ] #STAGHUNT game 

#os.getcwd()
#os.chdir('~/Library/Mobile\ Documents/com~apple~CloudDocs/PhD_data') 

########################
#### pairwise plots ####
########################
def plot_results(destination_folder, player1_title, player2_title, n_runs, game_title):
    '''plot reward over time - cumulative and non-cumulative; game reward and intrinsic and others'''
    if not os.path.isdir(str(destination_folder)+'/plots'):
        os.makedirs(str(destination_folder)+'/plots')

    if not os.path.isdir(str(destination_folder)+'/plots/outcome_plots'):
        os.makedirs(str(destination_folder)+'/plots/outcome_plots')

    ##################################
    #### cumulative - game reward ####
    ##################################
    my_df_player1 = pd.read_csv(f'{destination_folder}/player1/df_cumulative_reward_game.csv', index_col=0)
    means_player1 = my_df_player1.mean(axis=1)
    sds_player1 = my_df_player1.std(axis=1)
    #ci = st.t.interval(alpha=0.95, df=len(data)-1, loc=np.mean(data), scale=st.sem(data)) 
    ci_player1 = 1.96 * sds_player1/np.sqrt(n_runs)

    my_df_player2 = pd.read_csv(f'{destination_folder}/player2/df_cumulative_reward_game.csv', index_col=0)
    means_player2 = my_df_player2.mean(axis=1)
    sds_player2 = my_df_player2.std(axis=1)
    ci_player2 = 1.96 * sds_player2/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6) 
    plt.plot(my_df_player1.index[:], means_player1[:], label=f'player1 - {player1_title}', color='blue')
    plt.plot(my_df_player2.index[:], means_player2[:], label=f'player2 - {player2_title}', color='orange')
    #plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
    #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
    plt.fill_between(my_df_player1.index[:], means_player1-ci_player1, means_player1+ci_player1, facecolor='#95d0fc', alpha=0.7)
    plt.fill_between(my_df_player2.index[:], means_player2-ci_player2, means_player2+ci_player2, facecolor='#fed8b1', alpha=0.7)
    
    plt.title('Cumulative Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title+' vs '+player2_title)
    #plt.title('Cumulative Game Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    plt.ylabel('Cumulative Game reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/reward_cumulative_Game.png', bbox_inches='tight')


    ######################################
    #### non-cumulative - game reward ####
    ######################################
    my_df_player1 = pd.read_csv(f'{destination_folder}/player1/df_reward_game.csv', index_col=0)
    means_player1 = my_df_player1.mean(axis=1)
    sds_player1 = my_df_player1.std(axis=1)
    ci_player1 = 1.96 * sds_player1/np.sqrt(n_runs)

    my_df_player2 = pd.read_csv(f'{destination_folder}/player2/df_reward_game.csv', index_col=0)
    means_player2 = my_df_player2.mean(axis=1)
    sds_player2 = my_df_player2.std(axis=1)
    ci_player2 = 1.96 * sds_player2/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6) 
    plt.plot(my_df_player1.index[:], means_player1[:], lw=0.5, label=f'player1 - {player1_title}', color='blue')
    plt.plot(my_df_player2.index[:], means_player2[:], lw=0.5, label=f'player2 - {player2_title}', color='orange')
    #plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
    #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
    plt.fill_between(my_df_player1.index[:], means_player1-ci_player1, means_player1+ci_player1, facecolor='#95d0fc', alpha=0.7)
    plt.fill_between(my_df_player2.index[:], means_player2-ci_player2, means_player2+ci_player2, facecolor='#fed8b1', alpha=0.7)
    plt.title('Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title+' vs '+player2_title)
    #plt.title(r'Game Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    #plt.gca().set_ylim([1, 4]) #[0,5]
    if game_title=='IPD':
        plt.gca().set_ylim([1, 4])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([1, 5])
    elif game_title=='STAGHUNT':  
       plt.gca().set_ylim([1, 5])  
    plt.ylabel('Game reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/reward_Game.png', bbox_inches='tight')

    if False: #do not plot at the moment
        plt.figure(figsize=(10, 6), dpi=80)
        plt.plot(my_df_player1.index[:], means_player1[:], lw=0.5, label=f'player1 - {player1_title}', color='blue')
        plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
        plt.title('Game Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+player1_title)
        plt.gca().set_ylim([0, 5])
        plt.ylabel('Game reward')
        plt.xlabel('Iteration')
        plt.legend(loc='upper left')
        plt.savefig(f'{destination_folder}/plots/reward_Game_player1.png')


        plt.figure(figsize=(10, 6), dpi=80)
        plt.plot(my_df_player2.index[:], means_player2[:], lw=0.5, label=f'player2 - {player2_title}', color='orange')
        plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
        plt.title(r'Game Reward (Mean over '+str(n_runs)+r' runs $\pm$ SD), '+player2_title)
        plt.gca().set_ylim([0, 5])
        plt.ylabel('Game reward')
        plt.xlabel('Iteration')
        plt.legend(loc='upper left')
        plt.savefig(f'{destination_folder}/plots/reward_Game_player2.png')




    ##################################
    #### cumulative - intrinsic reward ###
    ##################################
    my_df_player1 = pd.read_csv(f'{destination_folder}/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    means_player1 = my_df_player1.mean(axis=1)
    sds_player1 = my_df_player1.std(axis=1)

    my_df_player2 = pd.read_csv(f'{destination_folder}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    means_player2 = my_df_player2.mean(axis=1)
    sds_player2 = my_df_player2.std(axis=1)

    #plot player1 and player2 separately
    #only plot player1 intrinsic reward if they are a QL player 
    if 'QL' in player1_title:
        if 'Selfish' not in player1_title: 
            plt.figure(dpi=80) #figsize=(10, 6)
            plt.plot(my_df_player1.index[:], means_player1[:], label=f'player1 - {player1_title}', color='blue')
            #plt.plot(my_df_player2.index[:], means_player2[:], label=f'player2 - {player2_title}', color='orange')
            plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
            #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
            #plt.title(r'Cumulative Intrinsic Reward (Mean over '+str(n_runs)+r' runs $\pm$ SD), '+player1_title+' vs '+player2_title)
            plt.title('Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title)
            #plt.title(r'Cumulative Intrinsic Reward (Mean over '+str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title)
            plt.ylabel('Cumulative Intrinsic reward')
            plt.xlabel('Iteration')
            leg = plt.legend() # get the legend object
            for line in leg.get_lines(): # change the line width for the legend
                line.set_linewidth(4.0)
            plt.savefig(f'{destination_folder}/plots/reward_cumulative_Intrinsic_player1.png', bbox_inches='tight')

    #only plot player2 intrinsic reward if they are a QL player 
    if 'QL' in player2_title:
        if 'Selfish' not in player2_title: 
            plt.figure(dpi=80) #figsize=(10, 6)
            plt.plot(my_df_player2.index[:], means_player2[:], label=f'player2 - {player2_title}', color='orange')
            plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
            plt.title('Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player2_title)
            #plt.title(r'Cumulative Intrinsic Reward (Mean over '+str(n_runs)+r' runs $\pm$ SD), '+'\n'+player2_title)
            plt.ylabel('Cumulative Intrinsic reward')
            plt.xlabel('Iteration')
            leg = plt.legend() # get the legend object
            for line in leg.get_lines(): # change the line width for the legend
                line.set_linewidth(4.0)
            plt.savefig(f'{destination_folder}/plots/reward_cumulative_Intrinsic_player2.png', bbox_inches='tight')


    ######################################
    #### non-cumulative - intrinsic reward ###
    ######################################
    #only plot player1 intrinsic reward if they are a QL player 
    if 'QL' in player1_title:
        if 'Selfish' not in player1_title: 
            my_df_player1 = pd.read_csv(f'{destination_folder}/player1/df_reward_intrinsic.csv', index_col=0)
            means_player1 = my_df_player1.mean(axis=1)
            sds_player1 = my_df_player1.std(axis=1)

            plt.figure(dpi=80) #figsize=(10, 6)
            plt.plot(my_df_player1.index[:], means_player1[:], lw=0.5, label=f'player1 - {player1_title}', color='blue')
            #plt.plot(my_df_player2.index[:], means_player2[:], lw=0.5, label=f'player2 - {player2_title}', color='orange')
            plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
            #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
            plt.title('Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title)
            #plt.title(r'Intrinsic Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title)
            if game_title=='IPD':
                plt.gca().set_ylim([-5, 6])
            elif game_title=='VOLUNTEER':
                plt.gca().set_ylim([-5, 8])
            elif game_title=='STAGHUNT':  
                plt.gca().set_ylim([-5, 10])  
            plt.ylabel('Intrinsic reward')
            plt.xlabel('Iteration')
            leg = plt.legend() # get the legend object
            for line in leg.get_lines(): # change the line width for the legend
                line.set_linewidth(4.0)
            plt.savefig(f'{destination_folder}/plots/reward_Intrinsic_player1.png', bbox_inches='tight')

    if 'QL' in player2_title:
        if 'Selfish' not in player2_title: 
            my_df_player2 = pd.read_csv(f'{destination_folder}/player2/df_reward_intrinsic.csv', index_col=0)
            means_player2 = my_df_player2.mean(axis=1)
            sds_player2 = my_df_player2.std(axis=1)

            plt.figure(dpi=80) #figsize=(10, 6)
            plt.plot(my_df_player2.index[:], means_player2[:], lw=0.5, label=f'player2 - {player2_title}', color='orange')
            plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
            plt.title('Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player2_title)
            #plt.title(r'Intrinsic Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player2_title)
            if game_title=='IPD':
                plt.gca().set_ylim([-5, 6])
            elif game_title=='VOLUNTEER':
                plt.gca().set_ylim([-5, 8])
            elif game_title=='STAGHUNT':  
                plt.gca().set_ylim([-5, 10])
            plt.ylabel('Intrinsic reward')
            plt.xlabel('Iteration')
            leg = plt.legend() # get the legend object
            for line in leg.get_lines(): # change the line width for the legend
                line.set_linewidth(4.0)
            plt.savefig(f'{destination_folder}/plots/reward_Intrinsic_player2.png', bbox_inches='tight')

    
    ##################################
    #### cumulative - collective game reward ####
    ##################################
    my_df = pd.read_csv(f'{destination_folder}/df_cumulative_reward_collective.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)


    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
#    plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    plt.title('Cumulative Collective Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title+' vs '+player2_title)
    #plt.title(r'Cumulative Collective Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    plt.ylabel('Cumulative Collective reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_cumulative_Collective.png', bbox_inches='tight')

    ######################################
    #### non-cumulative - collective game reward ####
    ######################################
    #TO DO 
    my_df = pd.read_csv(f'{destination_folder}/df_reward_collective.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
#    plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    plt.title('Collective Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+player1_title+' vs '+player2_title)
    #plt.title(r'Collective Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    if game_title=='IPD':
        plt.gca().set_ylim([4, 6])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([2, 8])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([4, 10])
    plt.ylabel('Collective reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_Collective.png', bbox_inches='tight')


    ##################################
    #### cumulative - gini game reward ####
    ##################################
    my_df = pd.read_csv(f'{destination_folder}/df_cumulative_reward_gini.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    #plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    #plt.title('Cumulative Gini Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+'runs), '+'\n'+player1_title+' vs '+player2_title)
    plt.title(r'Cumulative Gini Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    plt.ylabel('Cumulative Gini reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_cumulative_Gini.png', bbox_inches='tight')

    ######################################
    #### non-cumulative - gini game reward ####
    ######################################
    #TO DO 
    my_df = pd.read_csv(f'{destination_folder}/df_reward_gini.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    #plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    #plt.title('Gini Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+'runs), '+'\n'+player1_title+' vs '+player2_title)
    plt.title(r'Gini Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    plt.gca().set_ylim([0, 1])
    plt.ylabel('Gini reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_Gini.png', bbox_inches='tight')




    ##################################
    #### cumulative - min game reward ####
    ##################################
    my_df = pd.read_csv(f'{destination_folder}/df_cumulative_reward_min.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    #plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    #plt.title('Cumulative Min Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+'runs), '+'\n'+player1_title+' vs '+player2_title)
    plt.title(r'Cumulative Min Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    plt.ylabel('Cumulative Min reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_cumulative_Min.png', bbox_inches='tight')

    ######################################
    #### non-cumulative - min game reward ####
    ######################################
    #TO DO 
    my_df = pd.read_csv(f'{destination_folder}/df_reward_min.csv', index_col=0)
    means = my_df.mean(axis=1)
    sds = my_df.std(axis=1)
    ci = 1.96 * sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
    plt.fill_between(my_df.index[:], means-ci, means+ci, facecolor='#bf92e4', alpha=0.7)
    #plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    #plt.title('Min Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+'runs), '+'\n'+player1_title+' vs '+player2_title)
    plt.title(r'Min Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    if game_title=='IPD':
        plt.gca().set_ylim([1, 3])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([1, 4])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([1, 5]) 
    plt.ylabel('Min reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/outcome_plots/reward_Min.png', bbox_inches='tight')


def plot_actions(destination_folder, player1_title, player2_title, n_runs):
    '''explore the actions taken by players at every step out of 10000 (or num_iter) - what percentage are cooperating? '''

    actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)
    #actions_player1.iloc[9999].value_counts()

    #calculate % of 100 agents (runs) that cooperate at every step  out of the 10000
    actions_player1['%_defect'] = actions_player1[actions_player1[:]==1].count(axis='columns')
    actions_player1['%_cooperate'] = n_runs-actions_player1['%_defect']

    #convert to %
    actions_player1['%_defect'] = (actions_player1['%_defect']/n_runs)*100
    actions_player1['%_cooperate'] = (actions_player1['%_cooperate']/n_runs)*100

    #plot results 
    plt.figure(dpi=80) #figsize=(10, 6), 
    plt.plot(actions_player1.index[:], actions_player1['%_cooperate'], label=f'player1 - {player1_title}', color='blue')
    #plt.plot(my_df_player2.index[:], means_player2[:], label=f'player2 - {player2_title}', color='orange')
    #plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
    #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
    plt.title('The actions of Player 1 at every step of the episode \n (percentage cooperated over '+str(n_runs)+r' runs)')
    plt.gca().set_ylim([0, 100])
    plt.ylabel('Percentage cooperating')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/actions_player1.png', bbox_inches='tight')



    #repeat for player2
    actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)
    #actions_player2.iloc[9999].value_counts()

    actions_player2['%_defect'] = actions_player2[actions_player2[:]==1].count(axis='columns')
    actions_player2['%_cooperate'] = n_runs-actions_player2['%_defect']

    #convert to %
    actions_player2['%_defect'] = (actions_player2['%_defect']/n_runs)*100
    actions_player2['%_cooperate'] = (actions_player2['%_cooperate']/n_runs)*100

    plt.figure(dpi=80) #figsize=(10, 6), 
    plt.plot(actions_player2.index[:], actions_player2['%_cooperate'], label=f'player2 - {player2_title}', color='orange')
    #plt.plot(my_df_player2.index[:], means_player2[:], label=f'player2 - {player2_title}', color='orange')
    #plt.fill_between(my_df_player1.index[:], means_player1-sds_player1, means_player1+sds_player1, facecolor='#95d0fc', alpha=0.7)
    #plt.fill_between(my_df_player2.index[:], means_player2-sds_player2, means_player2+sds_player2, facecolor='#fed8b1', alpha=0.7)
    plt.title('The actions of Player 2 at every step of the episode \n (percentage cooperated over '+str(n_runs)+r' runs)')
    plt.gca().set_ylim([0, 100])
    plt.ylabel('Percentage cooperating')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'{destination_folder}/plots/actions_player2.png', bbox_inches='tight')


def plot_action_types_area(destination_folder, player1_title, player2_title, n_runs):
    '''visualise action types that each individual player takes against their opponent's last move 
    --> what strategies are being learnt at all steps of the run? 
    - consider the whole run'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    ##############################################
    ### Plot from the perspective of player1 first ####

    actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)
    state_player1 = pd.read_csv(f'{destination_folder}/player1/state.csv', index_col=0)
    #rename columns 
    colnames = ['run'+str(i) for i in range(n_runs)]
    actions_player1.columns = colnames
    state_player1.columns = colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player1[colname].astype(str) + ' | ' + state_player1[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    #results.to_csv(str(destination_folder+'/player1/action_types_full.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    results_counts.dropna(axis=1, how='all', inplace=True)

    #plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.area(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | (C,C)':'lightblue', 'C | (C,D)':'deepskyblue', 'C | (D,C)':'cyan', 'C | (D,D)':'royalblue', 'D | (C,C)':'orange', 'D | (C,D)':'yellow', 'D | (D,C)':'peru', 'D | (D,D)':'dimgrey'}, 
        title='Types of actions over time: \n '+player1_title+' agent (player1) against '+player2_title+' agent')
    plt.savefig(f'{destination_folder}/plots/action_types_area_player1.png', bbox_inches='tight')


    ##############################################
    ### Plot from the perspective of player2 ####

    actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)
    state_player2 = pd.read_csv(f'{destination_folder}/player2/state.csv', index_col=0)
    #rename columns - use colnames form above
    actions_player2.columns = colnames
    state_player2.columns = colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player2[colname].astype(str) + ' | ' + state_player2[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    #results.to_csv(str(destination_folder+'/player2/action_types_full.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:]
    results_counts.dropna(axis=1, how='all', inplace=True)

    #plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.area(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | C':'lightblue', 'C | D':'yellow', 'D | C':'brown', 'D | D':'orange'},
        #color={'C | (C,C)':'lightblue', 'C | (C,D)':'yellow', 'D | (D,C)':'brown', 'D | (D,D)':'orange',
        #        'D | (C,C)':'darkblue', 'D | (C,D)':'mustard', 'C | (D,C)':'grey', 'C | (D,D)':'red'}, 
        title='Types of actions over time: \n '+player2_title+' agent (player2) against '+player1_title+' agent')
    plt.savefig(f'{destination_folder}/plots/action_types_area_player2.png', bbox_inches='tight')


def plot_last_20_actions(destination_folder, player1_title, player2_title, n_runs):
    '''deep-dive into the strategy learnt by the end - interpert the last 20 moves
    NOTE this also generates the csv last_20_actions.csv that we can use to visualise a matrix later'''
    ##############################################
    ### Plot from the perspective of player1 first ####

    actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)[-20:]
    state_player1 = pd.read_csv(f'{destination_folder}/player1/state.csv', index_col=0)[-20:]
    #rename columns 
    colnames = ['run'+str(i) for i in range(n_runs)]
    actions_player1.columns = colnames
    state_player1.columns = colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player1[colname].astype(str) + ' | ' + state_player1[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    results.to_csv(str(destination_folder+'/player1/last_20_actions.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    results_counts.dropna(axis=1, how='all', inplace=True)

    plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.bar(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | C':'lightblue', 'C | D':'yellow', 'D | C':'brown', 'D | D':'orange'}, 
        title='Last 20 action types: \n '+player1_title+' agent (player1) against '+player2_title+' agent')
    plt.savefig(f'{destination_folder}/plots/last_20_actions_player1.png', bbox_inches='tight')


    ##############################################
    ### Plot from the perspective of player2 ####

    actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)[-20:]
    state_player2 = pd.read_csv(f'{destination_folder}/player2/state.csv', index_col=0)[-20:]
    #rename columns - use colnames form above
    actions_player2.columns=colnames
    state_player2.columns=colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player2[colname].astype(str) + ' | ' + state_player2[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    results.to_csv(str(destination_folder+'/player2/last_20_actions.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:]
    results_counts.dropna(axis=1, how='all', inplace=True)

    plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.bar(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | C':'lightblue', 'C | D':'yellow', 'D | C':'brown', 'D | D':'orange'}, 
        title='Last 20 action types: \n '+player2_title+' agent (player2) against '+player1_title+' agent')
    plt.savefig(f'{destination_folder}/plots/last_20_actions_player2.png', bbox_inches='tight')

## NB keep this!!! 
def C_condition(v):
        if v == 'C | (C, C)':
            color = "#28641E"
        elif v =='C | (C, D)':
            color = "#63A336"
        elif v =='C | (D, C)':
            color = "#B0DC82"
        elif v =='C | (D, D)':
            color = "#EBF6DC"
        elif v =='D | (C, C)':
            color = "#FBE6F1"
        elif v =='D | (C, D)':
            color = "#EEAED4"
        elif v =='D | (D, C)':
            color = "#CE4591"
        elif v == 'D | (D, D)':
            color = "#8E0B52"
        return 'background-color: %s' % color
        
reference = pd.DataFrame(['C | (C, C)', 'C | (C, D)', 'C | (D, C)', 'C | (D, D)', 'D | (C, C)', 'D | (C, D)', 'D | (D, C)', 'D | (D, D)'])
reference = reference.style.applymap(C_condition).set_caption(f"Colour map for action types")
#dfi.export(reference,"reference_color_map_for_action_types.png")


def visualise_last_20_actions_matrix(destination_folder):
    '''explore individual strategies learnt by individual players (not a collection of 100 players) 
    - look at 20 last moves as a vector
    NOTE plot_last_20_actions needs to be run first, to create the last_20_actions csv'''

    results_player1 = pd.read_csv(str(destination_folder+'/player1/last_20_actions.csv'), index_col=0).transpose()
    results_player2 = pd.read_csv(str(destination_folder+'/player2/last_20_actions.csv'), index_col=0).transpose()

    caption = destination_folder.replace('results/', '')
    caption = caption.replace('QL', '')
    results_player1 = results_player1.style.applymap(C_condition).set_caption(f"Player1 from {caption}")
    dfi.export(results_player1,f"{destination_folder}/plots/table_export_player1_last20.pdf")

    results_player2 = results_player2.style.applymap(C_condition).set_caption(f"Player2 from {caption}")
    dfi.export(results_player2,f"{destination_folder}/plots/table_export_player2_last20.pdf")

def plot_first_20_actions(destination_folder, player1_title, player2_title, n_runs):
    '''deep-dive into the strategy learnt by the end - interpert the last 20 moves
    NOTE this also generates the csv last_20_actions.csv that we can use to visualise a matrix later'''
    ##############################################
    ### Plot from the perspective of player1 first ####

    actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)[0:20]
    state_player1 = pd.read_csv(f'{destination_folder}/player1/state.csv', index_col=0)[0:20]
    #rename columns 
    colnames = ['run'+str(i) for i in range(n_runs)]
    actions_player1.columns = colnames
    state_player1.columns = colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player1[colname].astype(str) + ' | ' + state_player1[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    results.to_csv(str(destination_folder+'/player1/first_20_actions.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    results_counts.dropna(axis=1, how='all', inplace=True)

    plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.bar(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | C':'lightblue', 'C | D':'yellow', 'D | C':'brown', 'D | D':'orange'}, 
        title='First 20 action types: \n '+player1_title+' agent (player1) against '+player2_title+' agent')
    plt.savefig(f'{destination_folder}/plots/first_20_actions_player1.png', bbox_inches='tight')


    ##############################################
    ### Plot from the perspective of player2 ####

    actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)[0:20]
    state_player2 = pd.read_csv(f'{destination_folder}/player2/state.csv', index_col=0)[0:20]
    #rename columns - use colnames form above
    actions_player2.columns=colnames
    state_player2.columns=colnames
    results = pd.DataFrame(columns=colnames)

    for colname in colnames: 
        str_value = actions_player2[colname].astype(str) + ' | ' + state_player2[colname].astype(str)
        str_value = str_value.str.replace('1', 'D')
        str_value = str_value.str.replace('0', 'C')
        results[colname] = str_value

    results.to_csv(str(destination_folder+'/player2/first_20_actions.csv'))
    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:]
    results_counts.dropna(axis=1, how='all', inplace=True)

    plt.figure(figsize=(20, 15), dpi=100)
    results_counts.plot.bar(stacked=True, ylabel = '# agents taking this type of action \n (across '+str(n_runs)+' runs)', rot=45,
        xlabel='Iteration', colormap='PiYG_r',
        #color={'C | C':'lightblue', 'C | D':'yellow', 'D | C':'brown', 'D | D':'orange'}, 
        title='First 20 action types: \n '+player2_title+' agent (player2) against '+player1_title+' agent')
    plt.savefig(f'{destination_folder}/plots/first_20_actions_player2.png', bbox_inches='tight')

def visualise_first_20_actions_matrix(destination_folder):
    '''explore individual strategies learnt by individual players (not a collection of 100 players) 
    - look at 20 first moves as a vector
    NOTE plot_first_20_actions needs to be run first, to create the first_20_actions csv'''

    results_player1 = pd.read_csv(str(destination_folder+'/player1/first_20_actions.csv'), index_col=0).transpose()
    results_player2 = pd.read_csv(str(destination_folder+'/player2/first_20_actions.csv'), index_col=0).transpose()

    caption = destination_folder.replace('results/', '')
    caption = caption.replace('QL', '')
    results_player1 = results_player1.style.applymap(C_condition).set_caption(f"Player1 from {caption}")
    dfi.export(results_player1,f"{destination_folder}/plots/table_export_player1_first20.png")

    results_player2 = results_player2.style.applymap(C_condition).set_caption(f"Player2 from {caption}")
    dfi.export(results_player2,f"{destination_folder}/plots/table_export_player2_first20.png")

def visualise_first_20_actions_matrix_randomorder(destination_folder):
    '''for debugging - explore individual strategies learnt by individual players (not a collection of 100 players) 
    - look at 20 first moves as a vector
    NOTE plot_first_20_actions needs to be run first, to create the first_20_actions csv'''

    results_player1 = pd.read_csv(str(destination_folder+'/player1/first_20_actions.csv'), index_col=0).transpose()
    results_player2 = pd.read_csv(str(destination_folder+'/player2/first_20_actions.csv'), index_col=0).transpose()

    #shuffle the rows to output a matrix in a different order - for checking our clustering problem 
    results_player1 = results_player1.sample(frac=1)
    results_player2 = results_player2.sample(frac=1)

    caption = destination_folder.replace('results_', '')
    caption = caption.replace('QL', '')
    results_player1 = results_player1.style.applymap(C_condition).set_caption(f"Player1 from {caption}; randomly shuffled rows")
    dfi.export(results_player1,f"{destination_folder}/plots/table_export_player1_first20_randomorder.png")
    results_player2 = results_player2.style.applymap(C_condition).set_caption(f"Player2 from {caption}; randomly shuffled rows")
    dfi.export(results_player2,f"{destination_folder}/plots/table_export_player2_first20_randomorder.png")

def plot_one_run_Q_values(Q_values_list, run_idx):
    '''plot pregression of Q-value updates over the 10000 iterations for one example run - separately for each state.
    We plot both actions (C and D) on one plot to copare which action ends up being optimal in every state.'''
    rXs0a0_list = [iteration[0,0] for iteration in Q_values_list[run_idx]] #run x, state0, action1
    rXs0a1_list = [iteration[0,1] for iteration in Q_values_list[run_idx]]
    rXs1a0_list = [iteration[1,0] for iteration in Q_values_list[run_idx]]
    rXs1a1_list = [iteration[1,1] for iteration in Q_values_list[run_idx]]
    rXs2a0_list = [iteration[2,0] for iteration in Q_values_list[run_idx]]
    rXs2a1_list = [iteration[2,1] for iteration in Q_values_list[run_idx]]
    rXs3a0_list = [iteration[3,0] for iteration in Q_values_list[run_idx]]
    rXs3a1_list = [iteration[3,1] for iteration in Q_values_list[run_idx]]

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20, 4), sharey=True)
    fig.suptitle(f'Q-values for all state-action pairs, run{run_idx}')
    ax1.plot(range(len(rXs0a0_list)), rXs0a0_list[:], label=f'Action=C', color='darkgreen')
    ax1.plot(range(len(rXs0a1_list)), rXs0a1_list[:], label=f'Action=D', color='purple')
    ax1.set_title('State=(C,C)')
    ax2.plot(range(len(rXs1a0_list)), rXs1a0_list[:], label=f'Action=C', color='darkgreen')
    ax2.plot(range(len(rXs1a1_list)), rXs1a1_list[:], label=f'Action=D', color='purple')
    ax2.set_title('State=(C,D)')
    ax3.plot(range(len(rXs2a0_list)), rXs2a0_list[:], label=f'Action=C', color='darkgreen')
    ax3.plot(range(len(rXs2a1_list)), rXs2a1_list[:], label=f'Action=D', color='purple')
    ax3.set_title('State=(D,C)')
    ax4.plot(range(len(rXs3a0_list)), rXs3a0_list[:], label=f'Action=C', color='darkgreen')
    ax4.plot(range(len(rXs3a1_list)), rXs3a1_list[:], label=f'Action=D', color='purple')
    ax4.set_title('State=(D,D)')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    ax1.set(ylabel='Q-value')
    #max_Q_value = max(max(rXs0a0_list), max(rXs0a1_list), max(rXs1a0_list), max(rXs1a1_list)) #max q-value on this run
    #plt.ylim(0, int(max_Q_value+5))
    #set y axis limit based on the claculation of a max possible return in this game and the discount factor: r=4, gamma=0.9, max return = r*(1/1-gamma)
    if game_title == 'IPD': 
        plt.ylim(0, 40+5) 
    elif game_title == 'VOLUNTEER':
        plt.ylim(0, 50+5)
    elif game_title == 'STAGHUNT':
        plt.ylim(0, 50+5)
    #then export the interactive outupt / single plot as pdf/html to store the results compactly 


title_mapping = {'AC':'AlwaysCooperate', 'AD':'AlwaysDefect', 'TFT':'TitForTat', 'Random':'random', 'QLS':'Selfish', 'QLUT':'Utilitarian', 'QLDE':'Deontological', 'QLVE_e':'VirtueEthics_equality', 'QLVE_k':'VirtueEthics_kindness', 'QLVM':'VirtueEthics_mixed'}

def plot_action_pairs(destination_folder, player1_title, player2_title, n_runs, option=None):
    '''visualise action types that each individual player takes against their opponent's last move 
    --> what strategies are being learnt at all steps of the run? 
    - consider the whole run'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    if os.path.exists(str(destination_folder+'/action_pairs.csv')):
        results = pd.read_csv(str(destination_folder+'/action_pairs.csv'), index_col=0)

    else: #if action_pairs.csv does not yet exist 
        actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)
        actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)

        #rename columns 
        colnames = ['run'+str(i) for i in range(n_runs)]
        actions_player1.columns = colnames
        actions_player2.columns = colnames

        results = pd.DataFrame(columns=colnames)

        for colname in colnames: #loop over every run
            str_value = actions_player1[colname].astype(str) + ', ' + actions_player2[colname].astype(str)
            str_value = str_value.str.replace('1', 'D')
            str_value = str_value.str.replace('0', 'C')
            results[colname] = str_value

        results.to_csv(str(destination_folder+'/action_pairs.csv'))

    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    results_counts.dropna(axis=1, how='all', inplace=True)

    #plt.figure(figsize=(20, 15), dpi=100)
    plt.figure(dpi=80, figsize=(5, 4))
    plt.rcParams.update({'font.size':20})
    results_counts.plot.area(stacked=True, ylabel = '# action pairs observed', #rot=45,
        xlabel='Iteration', #colormap='PiYG_r',
        color={'C, C':'#28641E', 'C, D':'#B0DC82', 'D, C':'#EEAED4', 'D, D':'#8E0B52'}, linewidth=0.05, alpha=0.9,
        #color={'C, C':'royalblue', 'C, D':'lightblue', 'D, C':'yellow', 'D, D':'orange'},
        title=str(player1_title.replace('Ethics','').replace('_','-') +' vs '+player2_title.replace('Ethics','').replace('_','-'))) #Pairs of simultaneous actions over time: \n '+

    #plt.savefig(f'{destination_folder}/plots/action_pairs.png', bbox_inches='tight')
    if not os.path.isdir('results/outcome_plots/actions'):
            os.makedirs('results/outcome_plots/actions')

    if not option: #if plotting main results
        pair = destination_folder.split('/')[1]

    else: #if plotting extra parameter search for beta in QLVM 
        pair = destination_folder
        #pair += str(option)
    
    plt.savefig(f'results/outcome_plots/actions/pairs_{pair}.pdf', bbox_inches='tight')

	
	
def plot_action_pairs_20K(destination_folder, player1_title, player2_title, n_runs, option=None):
    '''visualise action types that each individual player takes against their opponent's last move 
    --> what strategies are being learnt at all steps of the run? 
    - consider the whole run'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    if os.path.exists(str(destination_folder+'/action_pairs.csv')):
        results = pd.read_csv(str(destination_folder+'/action_pairs.csv'), index_col=0)

    else: #if action_pairs.csv does not yet exist 
        actions_player1 = pd.read_csv(f'{destination_folder}/player1/action.csv', index_col=0)
        actions_player2 = pd.read_csv(f'{destination_folder}/player2/action.csv', index_col=0)

        #rename columns 
        colnames = ['run'+str(i) for i in range(n_runs)]
        actions_player1.columns = colnames
        actions_player2.columns = colnames

        results = pd.DataFrame(columns=colnames)

        for colname in colnames: #loop over every run
            str_value = actions_player1[colname].astype(str) + ', ' + actions_player2[colname].astype(str)
            str_value = str_value.str.replace('1', 'D')
            str_value = str_value.str.replace('0', 'C')
            results[colname] = str_value

        results.to_csv(str(destination_folder+'/action_pairs.csv'))

    results_counts = results.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    results_counts.dropna(axis=1, how='all', inplace=True)

    #plt.figure(figsize=(20, 15), dpi=100)
    plt.figure(dpi=80, figsize=(10, 4))
    plt.rcParams.update({'font.size':20})
    results_counts.plot.area(stacked=True, ylabel = '# action pairs observed', #rot=45,
        xlabel='Iteration', #colormap='PiYG_r',
        color={'C, C':'#28641E', 'C, D':'#B0DC82', 'D, C':'#EEAED4', 'D, D':'#8E0B52'}, linewidth=0.05, alpha=0.9,
        #color={'C, C':'royalblue', 'C, D':'lightblue', 'D, C':'yellow', 'D, D':'orange'},
        title=str(player1_title.replace('Ethics','').replace('_','-') +' vs '+player2_title.replace('Ethics','').replace('_','-') + f'\n (longer training)')) #Pairs of simultaneous actions over time: \n '+

    #plt.savefig(f'{destination_folder}/plots/action_pairs.png', bbox_inches='tight')
    if not os.path.isdir('results/outcome_plots/actions'):
            os.makedirs('results/outcome_plots/actions')

    if not option: #if plotting main results
        pair = destination_folder.split('/')[1]

    else: #if plotting extra parameter search for beta in QLVM 
        pair = destination_folder
        #pair += str(option)
    
    #save in the parent directory for simplicity 
    plt.savefig(f'{pair}.pdf', bbox_inches='tight')




########################
#### group plots ####
########################



def plot_relative_reward(player1_title, n_runs):
    '''plot game reward - relatie cumulative (bar & over time) & per iteration
    - how well off did the players end up relative to each other on the game?'''
    ##################################
    #### bar chart game cumulative reward for player1_tytle vs others  ####
    ##################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLS_means = against_QLS.mean()
    against_QLS_sds = against_QLS.std()
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLUT_means = against_QLUT.mean()
    against_QLUT_sds = against_QLUT.std()
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLDE_means = against_QLDE.mean()
    against_QLDE_sds = against_QLDE.std()
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLVE_e_means = against_QLVE_e.mean()
    against_QLVE_e_sds = against_QLVE_e.std()
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLVE_k_means = against_QLVE_k.mean()
    against_QLVE_k_sds = against_QLVE_k.std()
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_QLVM_means = against_QLVM.mean()
    against_QLVM_sds = against_QLVM.std()
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)


    #import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(3, 3), dpi=80)
    plt.rcParams.update({'font.size':20})
    ax = fig.add_axes([0,0,1,1])
    #labels = ['vs_S', 'vs_UT', 'vs_DE', 'vs_'+r'$VE_e$', 'vs_'+r'$VE_k$'] 
    labels = ['S', 'UT', 'DE', 'VE'+r'$_e$', 'VE'+r'$_k$'] 
    means = [against_QLS_means,against_QLUT_means,against_QLDE_means,against_QLVE_e_means,against_QLVE_k_means]
    cis = [against_QLS_ci,against_QLUT_ci,against_QLDE_ci,against_QLVE_e_ci, against_QLVE_k_ci]
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']  
    #add QLVM mixed agent 
    labels.append('VE'+r'$_m$')
    means.append(against_QLVM_means)
    cis.append(against_QLVM_ci)
    colors.append('pink')
    ax.bar(labels, means, yerr=cis, color=colors, width = 0.8) #capsize=7, 
    #plt.xticks(rotation=45)
    ax.set_ylabel(r'Cumulative $R_{extr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    #(f'R^{extr}_{i=QLUT}'# for {player1_title}')
    long_title = title_mapping[player1_title].replace('Ethics','').replace('_', '-')
    ax.set_title(long_title +' vs other \n') #'Cumulative Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    ax.set_xlabel('Opponent type')
    if game_title=='IPD': #NOTE game_title is set outside this function - in the overall environment - see code below 
        plt.gca().set_ylim([0, 40000])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([0, 50000])  
    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/bar_cumulative_game_reward_{player1_title}.pdf', bbox_inches='tight')
    
    ##################################
    #### cumulative - game reward for player1_tytle vs others  ####
    ##################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_game.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_game.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_game.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_game.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_game.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_game.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLS', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLUT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLDE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVE_e', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVE_k', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVM', color='pink')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)
    

    #long_title = title_mapping[player1_title]
    plt.title(long_title +' vs other \n') #r'Cumulative game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        plt.gca().set_ylim([0, 40000])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([0, 50000])  
    plt.ylabel(r'Cumulative $R_{extr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/cumulative_game_reward_{player1_title}.pdf', bbox_inches='tight')


    ##################################
    #### non-cumulative - game reward for player1_tytle vs others  ####
    ##################################
    figsize=(5, 4)

    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_reward_game.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_reward_game.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_reward_game.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_reward_game.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_reward_game.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_reward_game.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_reward_game.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_reward_game.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_reward_game.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_reward_game.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_reward_game.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLS', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLUT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLDE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVE_e', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVE_k', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVM', color='palevioletred')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)
    

    #long_title = title_mapping[player1_title]
    plt.title(long_title +' vs other \n') #r'Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        plt.gca().set_ylim([1, 4])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([1, 5])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([1, 5])
    plt.ylabel(r'$R_{extr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/game_reward_{player1_title}.pdf', bbox_inches='tight')

def plot_relative_moral_reward(player1_title, n_runs):
    '''plot moral reward - relatie cumulative (over time & bar plot) & per iteration
    - how well off did the players end up relative to each other in terms of moral reward?'''
    
    ##################################
    #### moral cumulative reward for player1_tytle vs others  ####
    ##################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLS_means = against_QLS.mean()
    against_QLS_sds = against_QLS.std()
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLUT_means = against_QLUT.mean()
    against_QLUT_sds = against_QLUT.std()
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLDE_means = against_QLDE.mean()
    against_QLDE_sds = against_QLDE.std()
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLVE_e_means = against_QLVE_e.mean()
    against_QLVE_e_sds = against_QLVE_e.std()
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLVE_k_means = against_QLVE_k.mean()
    against_QLVE_k_sds = against_QLVE_k.std()
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)


    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_QLVM_means = against_QLVM.mean()
    against_QLVM_sds = against_QLVM.std()
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    fig = plt.figure(figsize=(3, 3), dpi=80)
    plt.rcParams.update({'font.size':20})
    ax = fig.add_axes([0,0,1,1])
    #labels = ['vs_S', 'vs_UT', 'vs_DE', 'vs_'+r'$VE_e$', 'vs_'+r'$VE_k$'] 
    labels = ['S', 'UT', 'DE', 'VE'+r'$_e$', 'VE'+r'$_k$'] 
    means = [against_QLS_means,against_QLUT_means,against_QLDE_means,against_QLVE_e_means,against_QLVE_k_means]
    cis = [against_QLS_ci,against_QLUT_ci,against_QLDE_ci,against_QLVE_e_ci,against_QLVE_k_ci]
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']  
    #add QLVM
    labels.append('VE'+r'$_m$')
    means.append(against_QLVM_means)
    cis.append(against_QLVM_ci)
    colors.append('pink')
    ax.bar(labels, means, yerr=cis, color=colors, width = 0.8) #capsize=7, 
    #plt.xticks(rotation=45)
    ax.set_ylabel(r'Cumulative $R_{intr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    #(f'R^{extr}_{i=QLUT}'# for {player1_title}')
    long_title = title_mapping[player1_title].replace('Ethics','').replace('_','-')
    ax.set_title(long_title +' vs other \n') #'Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    ax.set_xlabel('Opponent type')
    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 60000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 80000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 100000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    plt.savefig(f'results/outcome_plots/reward/bar_cumulative_intrinsic_reward_{player1_title}.pdf', bbox_inches='tight')
    
    ##################################
    #### cumulative - game reward for player1_tytle vs others  ####
    ##################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)


    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLS', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLUT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLDE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVE_e', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVE_k', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_QLVM', color='pink')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)
    
    plt.title(long_title +' vs other \n') #r'Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 60000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 80000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 100000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    plt.ylabel(r'Cumulative $R_{intr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/cumulative_intrinsic_reward_{player1_title}.pdf', bbox_inches='tight')


    ##################################
    #### non-cumulative - game reward for player1_tytle vs others  ####
    ##################################
    figsize=(5, 4)

    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_reward_intrinsic.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_reward_intrinsic.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_reward_intrinsic.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_reward_intrinsic.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_reward_intrinsic.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_reward_intrinsic.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_reward_intrinsic.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_reward_intrinsic.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_reward_intrinsic.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)


    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLS', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLUT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLDE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVE_e', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVE_k', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_QLVM', color='palevioletred')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)
        
    plt.title(long_title +' vs other \n') #r'Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 

    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 6])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([2, 8])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 10])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])

    plt.ylabel(r'$R_{intr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/intrinsic_reward_{player1_title}.pdf', bbox_inches='tight')


def plot_relative_action_pairs(player1_title, n_runs):
    '''visualise % mutual cooperation
    - consider the whole run'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    figsize=(5, 4)

    action_pairs_against_QLS = pd.read_csv(f'results/{player1_title}_QLS/action_pairs.csv', index_col=0)
    try:
        action_pairs_against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/action_pairs.csv', index_col=0)
        order_QLUT = ''
    except:
        action_pairs_against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/action_pairs.csv', index_col=0)
        order_QLUT = 'QLUT_first'
    try:
        action_pairs_against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/action_pairs.csv', index_col=0)
        order_QLDE = ''
    except:
        action_pairs_against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/action_pairs.csv', index_col=0)
        order_QLDE = 'QLDE_first'
    try:
        action_pairs_against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/action_pairs.csv', index_col=0)
        order_QLVE_e = ''
    except:
        action_pairs_against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/action_pairs.csv', index_col=0)
        order_QLVE_e = 'QLVE_e_first'
    try:
        action_pairs_against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/action_pairs.csv', index_col=0)
        order_QLVE_k = ''
    except:
        action_pairs_against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/action_pairs.csv', index_col=0)
        order_QLVE_k = 'QLVE_k_first'
    if player1_title == 'QLVM':
        try:
            action_pairs_against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/action_pairs.csv', index_col=0)
            order_QLVM = ''
        except:
            action_pairs_against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/action_pairs.csv', index_col=0)
            order_QLVM = 'QLVM_first'


    ################################
    #### plot mutual cooperation ####
    ################################
    action_pairs_against_QLS['%_CC'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='C, C'].count(axis='columns') / n_runs)*100
    action_pairs_against_QLUT['%_CC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, C'].count(axis='columns') / n_runs)*100
    action_pairs_against_QLDE['%_CC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, C'].count(axis='columns') / n_runs)*100
    action_pairs_against_QLVE_e['%_CC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, C'].count(axis='columns') / n_runs)*100
    action_pairs_against_QLVE_k['%_CC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, C'].count(axis='columns') / n_runs)*100
    if player1_title == 'QLVM':
        action_pairs_against_QLVM['%_CC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, C'].count(axis='columns') / n_runs)*100


    #plot results 
    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']
    plt.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])
    plt.plot(action_pairs_against_QLUT.index[:], action_pairs_against_QLUT['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLUT', color=colors[1])
    plt.plot(action_pairs_against_QLDE.index[:], action_pairs_against_QLDE['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLDE', color=colors[2])
    plt.plot(action_pairs_against_QLVE_e.index[:], action_pairs_against_QLVE_e['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_e', color=colors[3])
    plt.plot(action_pairs_against_QLVE_k.index[:], action_pairs_against_QLVE_k['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_k', color=colors[4])
    if player1_title == 'QLVM':
        plt.plot(action_pairs_against_QLVM.index[:], action_pairs_against_QLVM['%_CC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVM', color='pink')
    plt.title('Mutual C - '+ player1_title.replace('QL','') +' vs other \n') # among the two agents (% over ' +str(n_runs)+' runs), '+'\n'+ 
    plt.gca().set_ylim([0, 100])
    plt.ylabel('% C,C (over 100 runs)')
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    if player1_title != 'QLVM':
        leg = plt.legend(fontsize=14, labels=['vs S', 'vs UT', 'vs DE', r'vs VE$_e$', r'vs VE$_k$']) # get the legend object
    else: 
        leg = plt.legend(fontsize=14, labels=['vs S', 'vs UT', 'vs DE', r'vs VE$_e$', r'vs VE$_k$', 'vs VM']) # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(8)
    if not os.path.isdir('results/outcome_plots/cooperation'):
        os.makedirs('results/outcome_plots/cooperation')
    plt.savefig(f'results/outcome_plots/cooperation/mutual_cooperation_{player1_title}.png', bbox_inches='tight')


    ################################
    #### plot mutual defection ####
    ################################
    action_pairs_against_QLS['%_DD'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='D, D'].count(axis='columns')/ n_runs)*100
    action_pairs_against_QLUT['%_DD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, D'].count(axis='columns')/ n_runs)*100
    action_pairs_against_QLDE['%_DD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, D'].count(axis='columns')/ n_runs)*100
    action_pairs_against_QLVE_e['%_DD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, D'].count(axis='columns')/ n_runs)*100
    action_pairs_against_QLVE_k['%_DD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, D'].count(axis='columns')/ n_runs)*100
    if player1_title == 'QLVM':
        action_pairs_against_QLVM['%_DD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, D'].count(axis='columns') / n_runs)*100

    #plot results 
    plt.figure(dpi=80, figsize=figsize) 
    plt.rcParams.update({'font.size':20})
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']
    plt.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])
    plt.plot(action_pairs_against_QLUT.index[:], action_pairs_against_QLUT['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLUT', color=colors[1])
    plt.plot(action_pairs_against_QLDE.index[:], action_pairs_against_QLDE['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLDE', color=colors[2])
    plt.plot(action_pairs_against_QLVE_e.index[:], action_pairs_against_QLVE_e['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_e', color=colors[3])
    plt.plot(action_pairs_against_QLVE_k.index[:], action_pairs_against_QLVE_k['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_k',color=colors[4])
    if player1_title == 'QLVM':
        plt.plot(action_pairs_against_QLVM.index[:], action_pairs_against_QLVM['%_DD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVM', color=colors[4])
    plt.title('Mutual D - '+ player1_title.replace('QL','') +' vs other \n') #'Mutual Defection among the two agents (% over ' +str(n_runs)+' runs), '+'\n'+
    plt.gca().set_ylim([0, 100])
    plt.ylabel('% D,D (over 100 runs)')
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/cooperation/mutual_defection_{player1_title}.png', bbox_inches='tight')


    ################################
    #### plot player1 eploits player2 ####
    ################################
    action_pairs_against_QLS['%_DC'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='D, C'].count(axis='columns')/ n_runs)*100
    if order_QLUT=='QLUT_first':
        action_pairs_against_QLUT['%_DC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, D'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLUT['%_DC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, C'].count(axis='columns')/ n_runs)*100
    if order_QLDE=='QLDE_first':
        action_pairs_against_QLDE['%_DC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, D'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLDE['%_DC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, C'].count(axis='columns')/ n_runs)*100
    if order_QLVE_e=='QLVE_e_first':
        action_pairs_against_QLVE_e['%_DC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, D'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLVE_e['%_DC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, C'].count(axis='columns')/ n_runs)*100
    if order_QLVE_k=='QLVE_k_first':
        action_pairs_against_QLVE_k['%_DC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, D'].count(axis='columns')/ n_runs)*100
    else:
        action_pairs_against_QLVE_k['%_DC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, C'].count(axis='columns')/ n_runs)*100
    if player1_title == 'QLVM':
        if order_QLVM=='QLVM_first':
            action_pairs_against_QLVM['%_DC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, D'].count(axis='columns')/ n_runs)*100
        else:
            action_pairs_against_QLVM['%_DC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, C'].count(axis='columns')/ n_runs)*100
    

    #plot results 
    plt.figure(dpi=80, figsize=figsize) 
    plt.rcParams.update({'font.size':20})
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']
    plt.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])
    plt.plot(action_pairs_against_QLUT.index[:], action_pairs_against_QLUT['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLUT', color=colors[1])
    plt.plot(action_pairs_against_QLDE.index[:], action_pairs_against_QLDE['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLDE', color=colors[2])
    plt.plot(action_pairs_against_QLVE_e.index[:], action_pairs_against_QLVE_e['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_e', color=colors[3])
    plt.plot(action_pairs_against_QLVE_k.index[:], action_pairs_against_QLVE_k['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_k', color=colors[4])
    if player1_title == 'QLVM':
        plt.plot(action_pairs_against_QLVM.index[:], action_pairs_against_QLVM['%_DC'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVM', color=colors[4])
    plt.title(player1_title.replace('QL','') +' exploits other \n') #'Exploitation among the two agents (% over ' +str(n_runs)+' runs), '+'\n'+ 
    plt.gca().set_ylim([0, 100])
    plt.ylabel('% D,C (over 100 runs)') #\n player i exploits other
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/cooperation/exploitation_{player1_title}.png', bbox_inches='tight')


    ################################
    #### plot player1 gets exploited by player2 ####
    ################################
    action_pairs_against_QLS['%_CD'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='C, D'].count(axis='columns')/ n_runs)*100
    if order_QLUT=='QLUT_first':
        action_pairs_against_QLUT['%_CD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, C'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLUT['%_CD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, D'].count(axis='columns')/ n_runs)*100
    if order_QLDE=='QLDE_first':
        action_pairs_against_QLDE['%_CD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, C'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLDE['%_CD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, D'].count(axis='columns')/ n_runs)*100
    if order_QLVE_e=='QLVE_e_first':
        action_pairs_against_QLVE_e['%_CD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, C'].count(axis='columns')/ n_runs)*100
    else: 
        action_pairs_against_QLVE_e['%_CD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, D'].count(axis='columns')/ n_runs)*100
    if order_QLVE_k=='QLVE_k_first':
        action_pairs_against_QLVE_k['%_CD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, C'].count(axis='columns')/ n_runs)*100
    else:
        action_pairs_against_QLVE_k['%_CD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, D'].count(axis='columns')/ n_runs)*100
    if player1_title == 'QLVM':
        if order_QLVM=='QLVM_first':
            action_pairs_against_QLVM['%_CD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, C'].count(axis='columns')/ n_runs)*100
        else:
            action_pairs_against_QLVM['%_CD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, D'].count(axis='columns')/ n_runs)*100
    
    #plot results 
    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']
    plt.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])
    plt.plot(action_pairs_against_QLUT.index[:], action_pairs_against_QLUT['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLUT', color=colors[1])
    plt.plot(action_pairs_against_QLDE.index[:], action_pairs_against_QLDE['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLDE', color=colors[2])
    plt.plot(action_pairs_against_QLVE_e.index[:], action_pairs_against_QLVE_e['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_e', color=colors[3])
    plt.plot(action_pairs_against_QLVE_k.index[:], action_pairs_against_QLVE_k['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_k', color=colors[4])
    if player1_title == 'QLVM':
        plt.plot(action_pairs_against_QLVM.index[:], action_pairs_against_QLVM['%_CD'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVM', color=colors[4])
    plt.title(player1_title.replace('QL','') +' gets exploited \n') #Exploitation among the two agents (% over ' +str(n_runs)+' runs), '+'\n'+ 
    plt.gca().set_ylim([0, 100])
    plt.ylabel('% C,D (over 100 runs)') #\n player i gets exploited by other
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/cooperation/gets_exploited_{player1_title}.png', bbox_inches='tight')


def plot_relative_outcomes(type, player1_title, n_runs, game_title):
    '''plot different types of social outcoes - collective / gini / min (game) reward for different pairs'''    
    ##################################
    #### cumulative - {type} game reward for player1_tytle vs others  ####
    ##################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/df_cumulative_reward_{type}.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/df_cumulative_reward_{type}.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/df_cumulative_reward_{type}.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/df_cumulative_reward_{type}.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/df_cumulative_reward_{type}.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    plt.figure(dpi=80, figsize=(5,4)) 
    plt.rcParams.update({'font.size':20})
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_S', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_UT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_DE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_'+r'$VE_e$', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_'+r'$VE_k$', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_'+r'$VE_m$', color='palevioletred')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)
    long_title = title_mapping[player1_title].replace('Ethics','').replace('_','-')
    plt.title(long_title +' vs other \n') #r'Cumulative '+type+' Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        if type=='collective':
            plt.gca().set_ylim([0, 60000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 30000])
    elif game_title=='VOLUNTEER':
        if type=='collective': 
            plt.gca().set_ylim([0, 80000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 40000])
    elif game_title=='STAGHUNT': 
        if type=='collective': 
            plt.gca().set_ylim([0, 100000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 40000])  
    plt.ylabel(f'$G_{{{type}}}$') #Cumulative
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/group_outcomes'):
        os.makedirs('results/outcome_plots/group_outcomes')

    #plt.savefig(f'results/outcome_plots/group_outcomes/cumulative_{type}_reward_{player1_title}.png', bbox_inches='tight')

    

    

    ######################################
    #### cumulative bar plot - {type} game reward ####
    ######################################
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLS_means = against_QLS.mean()
    against_QLS_sds = against_QLS.std()
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLUT_means = against_QLUT.mean()
    against_QLUT_sds = against_QLUT.std()
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLDE_means = against_QLDE.mean()
    against_QLDE_sds = against_QLDE.std()
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLVE_e_means = against_QLVE_e.mean()
    against_QLVE_e_sds = against_QLVE_e.std()
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLVE_k_means = against_QLVE_k.mean()
    against_QLVE_k_sds = against_QLVE_k.std()
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
    against_QLVM_means = against_QLVM.mean()
    against_QLVM_sds = against_QLVM.std()
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)


    #import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(3, 3), dpi=80)
    plt.rcParams.update({'font.size':20})
    ax = fig.add_axes([0,0,1,1])
    #labels = ['vs_S', 'vs_UT', 'vs_DE', 'vs_'+r'$VE_e$', 'vs_'+r'$VE_k$']
    labels = ['S', 'UT', 'DE', 'VE'+r'$_e$', 'VE'+r'$_k$', 'VE'+r'$_m$']
    means = [against_QLS_means,against_QLUT_means,against_QLDE_means,against_QLVE_e_means,against_QLVE_k_means,against_QLVM_means]
    cis = [against_QLS_ci,against_QLUT_ci,against_QLDE_ci,against_QLVE_e_ci,against_QLVE_k_ci,against_QLVM_ci]
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple', 'pink']
    ax.bar(labels, means, yerr=cis, capsize=7, color=colors)
    ax.set_title(long_title +' vs other \n') #r'Cumulative '+type+' Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        if type=='collective':
            plt.gca().set_ylim([0, 60000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 30000])
    elif game_title=='VOLUNTEER':
        if type=='collective': 
            plt.gca().set_ylim([0, 80000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 40000])
    elif game_title=='STAGHUNT': 
        if type=='collective': 
            plt.gca().set_ylim([0, 100000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 40000])  
    ax.set_ylabel(f'$G_{{{type}}}$') #Cumulative
    ax.set_xlabel('Opponent type')
    #plt.xticks(rotation=45)
    plt.savefig(f'results/outcome_plots/group_outcomes/bar_cumulative_{type}_reward_{player1_title}.pdf', bbox_inches='tight')



    ######################################
    #### non-cumulative - {type} game reward ####
    ######################################
    #my_df = pd.read_csv(f'{destination_folder}/df_reward_collective.csv', index_col=0)
    #means = my_df.mean(axis=1)
    #sds = my_df.std(axis=1)

    #plt.figure(dpi=80) #figsize=(10, 6)
    #plt.plot(my_df.index[:], means[:], lw=0.5, label=f'both players', color='purple')
    #plt.fill_between(my_df.index[:], means-sds, means+sds, facecolor='#bf92e4', alpha=0.7)
    #plt.title(r'Collective Reward (Mean over ' +str(n_runs)+r' runs $\pm$ SD), '+'\n'+player1_title+' vs '+player2_title)
    #plt.ylabel('Collective reward')
    #plt.xlabel('Iteration')
    #plt.legend() #loc='upper left'
    #plt.savefig(f'{destination_folder}/plots/Collective_reward.png', bbox_inches='tight') 
    against_QLS = pd.read_csv(f'results/{player1_title}_QLS/df_reward_{type}.csv', index_col=0)
    against_QLS_means = against_QLS.mean(axis=1)
    against_QLS_sds = against_QLS.std(axis=1)
    against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

    try:
        against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/df_reward_{type}.csv', index_col=0)
    except:
        against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/df_reward_{type}.csv', index_col=0)
    against_QLUT_means = against_QLUT.mean(axis=1)
    against_QLUT_sds = against_QLUT.std(axis=1)
    against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

    try:
        against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/df_reward_{type}.csv', index_col=0)
    except:
        against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/df_reward_{type}.csv', index_col=0)
    against_QLDE_means = against_QLDE.mean(axis=1)
    against_QLDE_sds = against_QLDE.std(axis=1)
    against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

    try:
        against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/df_reward_{type}.csv', index_col=0)
    except:
        against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/df_reward_{type}.csv', index_col=0)
    against_QLVE_e_means = against_QLVE_e.mean(axis=1)
    against_QLVE_e_sds = against_QLVE_e.std(axis=1)
    against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

    try:
        against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/df_reward_{type}.csv', index_col=0)
    except:
        against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/df_reward_{type}.csv', index_col=0)
    against_QLVE_k_means = against_QLVE_k.mean(axis=1)
    against_QLVE_k_sds = against_QLVE_k.std(axis=1)
    against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

    try:
        against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/df_reward_{type}.csv', index_col=0)
    except:
        against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/df_reward_{type}.csv', index_col=0)
    against_QLVM_means = against_QLVM.mean(axis=1)
    against_QLVM_sds = against_QLVM.std(axis=1)
    against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

    plt.figure(dpi=80, figsize=(5,4))
    plt.rcParams.update({'font.size':20})
    plt.plot(against_QLS.index[:], against_QLS_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_S', color='red')
    plt.fill_between(against_QLS.index[:], against_QLS_means-against_QLS_ci, against_QLS_means+against_QLS_ci, facecolor='#ff9999', alpha=0.5)
    plt.plot(against_QLUT.index[:], against_QLUT_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_UT', color='#556b2f')
    plt.fill_between(against_QLUT.index[:], against_QLUT_means-against_QLUT_ci, against_QLUT_means+against_QLUT_ci, facecolor='#ccff99', alpha=0.5)
    plt.plot(against_QLDE.index[:], against_QLDE_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_DE', color='#00cccc')
    plt.fill_between(against_QLDE.index[:], against_QLDE_means-against_QLDE_ci, against_QLDE_means+against_QLDE_ci, facecolor='#99ffff', alpha=0.5)
    plt.plot(against_QLVE_e.index[:], against_QLVE_e_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_'+'VE'+r'$_e$', color='orange')
    plt.fill_between(against_QLVE_e.index[:], against_QLVE_e_means-against_QLVE_e_ci, against_QLVE_e_means+against_QLVE_e_ci, facecolor='#ffcc99', alpha=0.5)
    plt.plot(against_QLVE_k.index[:], against_QLVE_k_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_'+'VE'+r'$_k$', color='purple')
    plt.fill_between(against_QLVE_k.index[:], against_QLVE_k_means-against_QLVE_k_ci, against_QLVE_k_means+against_QLVE_k_ci, facecolor='#CBC3E3', alpha=0.5)
    plt.plot(against_QLVM.index[:], against_QLVM_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_'+'VE'+r'$_m$', color='palevioletred')
    plt.fill_between(against_QLVM.index[:], against_QLVM_means-against_QLVM_ci, against_QLVM_means+against_QLVM_ci, facecolor='pink', alpha=0.5)

    plt.title(long_title +' vs other \n') #type+r' Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if type=='gini':
        plt.gca().set_ylim([0, 1])

    if game_title=='IPD':
        if type=='collective':
            plt.gca().set_ylim([4, 6])
        elif type=='min':
            plt.gca().set_ylim([1, 3])
    elif game_title=='VOLUNTEER':
        if type=='collective': 
            plt.gca().set_ylim([2, 8])
        elif type=='min':
            plt.gca().set_ylim([1, 4])
    elif game_title=='STAGHUNT': 
        if type=='collective': 
            plt.gca().set_ylim([4, 10])
        elif type=='min':
            plt.gca().set_ylim([1, 5])
    plt.ylabel(f'$G_{{{type}}}$')
    plt.xlabel('Iteration')
    #leg = plt.legend(fontsize=14, labels=['vs QLS', 'vs QLUT', 'vs QLDE', r'vs QLVE$_e$', r'vs QLVE$_k$']) # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(8)
    #plt.savefig(f'results/outcome_plots/group_outcomes/{type}_reward_{player1_title}.png', bbox_inches='tight')



def create_legend():
    player1_title = 'QLUT'
    action_pairs_against_QLS = pd.read_csv(f'results/{player1_title}_QLS/action_pairs.csv', index_col=0)
    try:
        action_pairs_against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/action_pairs.csv', index_col=0)
        order_QLUT = ''
    except:
        action_pairs_against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/action_pairs.csv', index_col=0)
        order_QLUT = 'QLUT_first'
    try:
        action_pairs_against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/action_pairs.csv', index_col=0)
        order_QLDE = ''
    except:
        action_pairs_against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/action_pairs.csv', index_col=0)
        order_QLDE = 'QLDE_first'
    try:
        action_pairs_against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/action_pairs.csv', index_col=0)
        order_QLVE_e = ''
    except:
        action_pairs_against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/action_pairs.csv', index_col=0)
        order_QLVE_e = 'QLVE_e_first'
    try:
        action_pairs_against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/action_pairs.csv', index_col=0)
        order_QLVE_k = ''
    except:
        action_pairs_against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/action_pairs.csv', index_col=0)
        order_QLVE_k = 'QLVE_k_first'
    try:
        action_pairs_against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/action_pairs.csv', index_col=0)
        order_QLVEM = ''
    except:
        action_pairs_against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/action_pairs.csv', index_col=0)
        order_QLVM = 'QLVM_first'


    ################################
    #### plot mutual cooperation ####
    ################################
    action_pairs_against_QLS['%_CC'] = action_pairs_against_QLS[action_pairs_against_QLS[:]=='C, C'].count(axis='columns')
    action_pairs_against_QLUT['%_CC'] = action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, C'].count(axis='columns')
    action_pairs_against_QLDE['%_CC'] = action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, C'].count(axis='columns')
    action_pairs_against_QLVE_e['%_CC'] = action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, C'].count(axis='columns')
    action_pairs_against_QLVE_k['%_CC'] = action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, C'].count(axis='columns')
    action_pairs_against_QLVM['%_CC'] = action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, C'].count(axis='columns')

    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple', 'palevioletred']

    #plot results - these will be ignored and not stored, just to make the plot 
    plt.figure(dpi=80) #figsize=(10, 6), 
    plt.rcParams.update({'font.size':20})
    plt.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_CC'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])

    fig = plt.figure("Line plot")
    legendFig = plt.figure("Legend plot", figsize=(2.5, 2.5))
    ax = fig.add_subplot(111)
    line1, = ax.plot(action_pairs_against_QLS.index[:], action_pairs_against_QLS['%_CC'], c=colors[0], lw=6)
    line2, = ax.plot(action_pairs_against_QLUT.index[:], action_pairs_against_QLUT['%_CC'], c=colors[1], lw=6)
    line3, = ax.plot(action_pairs_against_QLDE.index[:], action_pairs_against_QLDE['%_CC'], c=colors[2], lw=6)
    line4, = ax.plot(action_pairs_against_QLVE_e.index[:], action_pairs_against_QLVE_e['%_CC'], c=colors[3], lw=6)
    line5, = ax.plot(action_pairs_against_QLVE_k.index[:], action_pairs_against_QLVE_k['%_CC'], c=colors[4], lw=6)
    line6, = ax.plot(action_pairs_against_QLVM.index[:], action_pairs_against_QLVM['%_CC'], c=colors[5], lw=6)

    legendFig.legend([line1, line2, line3, line4, line5, line6], ['vs Selfish', 'vs UT', 'vs DE', r'vs VE$_e$', r'vs VE$_k$', r'vs VE$_m$'], loc='center')
    legendFig.savefig('results/outcome_plots/legend.pdf', bbox='tight', transparent=True)

#create_legend()




def plot_relative_cooperation(player1_title, n_runs): 
    actions_against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/action.csv', index_col=0)
    #calculate % of 100 agents (runs) that cooperate at every step  out of the 10000
    actions_against_QLS['%_defect'] = actions_against_QLS[actions_against_QLS[:]==1].count(axis='columns')
    actions_against_QLS['%_cooperate'] = n_runs-actions_against_QLS['%_defect']
    actions_against_QLS['%_defect'] = (actions_against_QLS['%_defect']/n_runs)*100
    actions_against_QLS['%_cooperate'] = (actions_against_QLS['%_cooperate']/n_runs)*100

    try:
        actions_against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/action.csv', index_col=0)
    except:
        actions_against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/action.csv', index_col=0)
    actions_against_QLUT['%_defect'] = actions_against_QLUT[actions_against_QLUT[:]==1].count(axis='columns')
    actions_against_QLUT['%_cooperate'] = n_runs-actions_against_QLUT['%_defect']
    actions_against_QLUT['%_defect'] = (actions_against_QLUT['%_defect']/n_runs)*100
    actions_against_QLUT['%_cooperate'] = (actions_against_QLUT['%_cooperate']/n_runs)*100

    try:
        actions_against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/action.csv', index_col=0)
    except:
        actions_against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/action.csv', index_col=0)
    actions_against_QLDE['%_defect'] = actions_against_QLDE[actions_against_QLDE[:]==1].count(axis='columns')
    actions_against_QLDE['%_cooperate'] = n_runs-actions_against_QLDE['%_defect']
    actions_against_QLDE['%_defect'] = (actions_against_QLDE['%_defect']/n_runs)*100
    actions_against_QLDE['%_cooperate'] = (actions_against_QLDE['%_cooperate']/n_runs)*100

    try:
        actions_against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/action.csv', index_col=0)
    except:
        actions_against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/action.csv', index_col=0)
    actions_against_QLVE_e['%_defect'] = actions_against_QLVE_e[actions_against_QLVE_e[:]==1].count(axis='columns')
    actions_against_QLVE_e['%_cooperate'] = n_runs-actions_against_QLVE_e['%_defect']
    actions_against_QLVE_e['%_defect'] = (actions_against_QLVE_e['%_defect']/n_runs)*100
    actions_against_QLVE_e['%_cooperate'] = (actions_against_QLVE_e['%_cooperate']/n_runs)*100

    try:
        actions_against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/action.csv', index_col=0)
    except:
        actions_against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/action.csv', index_col=0)
    actions_against_QLVE_k['%_defect'] = actions_against_QLVE_k[actions_against_QLVE_k[:]==1].count(axis='columns')
    actions_against_QLVE_k['%_cooperate'] = n_runs-actions_against_QLVE_k['%_defect']
    actions_against_QLVE_k['%_defect'] = (actions_against_QLVE_k['%_defect']/n_runs)*100
    actions_against_QLVE_k['%_cooperate'] = (actions_against_QLVE_k['%_cooperate']/n_runs)*100

    #plot results 
    plt.figure(dpi=80) #figsize=(10, 6), 
    colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple']
    plt.plot(actions_against_QLS.index[:], actions_against_QLS['%_cooperate'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLS', color=colors[0])
    plt.plot(actions_against_QLUT.index[:], actions_against_QLUT['%_cooperate'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLUT', color=colors[1])
    plt.plot(actions_against_QLDE.index[:], actions_against_QLDE['%_cooperate'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLDE', color=colors[2])
    plt.plot(actions_against_QLVE_e.index[:], actions_against_QLVE_e['%_cooperate'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_e', color=colors[3])
    plt.plot(actions_against_QLVE_k.index[:], actions_against_QLVE_k['%_cooperate'], lw=0.1, alpha=0.5, label=f'{player1_title} vs. QLVE_k', color=colors[4])
    long_title = title_mapping[player1_title]
    plt.title(long_title +' vs other') #Probability of Cooperation,'+'\n'+ 
    plt.gca().set_ylim([0, 100])
    plt.ylabel('% '+r'$a_M=C$'+' (over ' +str(n_runs)+' runs)')
    plt.xlabel('Iteration')
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/cooperation'):
        os.makedirs('results/outcome_plots/cooperation')
    plt.savefig(f'results/outcome_plots/cooperation/cooperation_{player1_title}.png', bbox_inches='tight')

def C_pairs_condition(v):
        if v == 'C, C':
            color = "#28641E"
        elif v =='C, D':
            color = "#B0DC82"
        elif v =='D, C':
            color = "#EEAED4"
        elif v == 'D, D':
            color = "#8E0B52"
        return 'background-color: %s' % color
        
reference = pd.DataFrame(['C, C', 'C, D', 'D, C', 'D, D'])
reference = reference.style.applymap(C_pairs_condition).set_caption(f"Colour map for action pairs")
#dfi.export(reference,"reference_color_map_for_action_pairs.png")




def plot_matrix_action_pairs(n_runs):
    '''visualise % mutual cooperation
    - consider only the final pair to see where the pair ended up'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    figsize=(8, 6.5)
    types = ['S','UT','DE','Ve','Vk','Vm']

    matrix_CC = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_DD = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_DC = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_CD = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)


    for player1_title in ['QLS','QLUT','QLDE','QLVE_e','QLVE_k','QLVM']:
        action_pairs_against_QLS = pd.read_csv(f'results/{player1_title}_QLS/action_pairs.csv', index_col=0).iloc[9999]
        try:
            action_pairs_against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/action_pairs.csv', index_col=0).iloc[9999]
            order_QLUT = ''
        except:
            action_pairs_against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/action_pairs.csv', index_col=0).iloc[9999]
            order_QLUT = 'QLUT_first'
        try:
            action_pairs_against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/action_pairs.csv', index_col=0).iloc[9999]
            order_QLDE = ''
        except:
            action_pairs_against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/action_pairs.csv', index_col=0).iloc[9999]
            order_QLDE = 'QLDE_first'
        try:
            action_pairs_against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVE_e = ''
        except:
            action_pairs_against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVE_e = 'QLVE_e_first'
        try:
            action_pairs_against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVE_k = ''
        except:
            action_pairs_against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVE_k = 'QLVE_k_first'
        try:
            action_pairs_against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVM = ''
        except:
            action_pairs_against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/action_pairs.csv', index_col=0).iloc[9999]
            order_QLVM = 'QLVM_first'

    
        action_pairs_against_QLS['%_CC'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_QLUT['%_CC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_QLDE['%_CC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_QLVE_e['%_CC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_QLVE_k['%_CC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_QLVM['%_CC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, C'].count() / n_runs)*100

        short_title = player1_title.replace('QL','').replace('VE_e','Ve').replace('VE_k','Vk').replace('VM','Vm')
        matrix_CC.loc[short_title] = [action_pairs_against_QLS['%_CC'],action_pairs_against_QLUT['%_CC'],action_pairs_against_QLDE['%_CC'],action_pairs_against_QLVE_e['%_CC'],action_pairs_against_QLVE_k['%_CC'],action_pairs_against_QLVM['%_CC']]
        


        action_pairs_against_QLS['%_DD'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='D, D'].count()/ n_runs)*100
        action_pairs_against_QLUT['%_DD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, D'].count()/ n_runs)*100
        action_pairs_against_QLDE['%_DD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, D'].count()/ n_runs)*100
        action_pairs_against_QLVE_e['%_DD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, D'].count()/ n_runs)*100
        action_pairs_against_QLVE_k['%_DD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, D'].count()/ n_runs)*100
        action_pairs_against_QLVM['%_DD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, D'].count() / n_runs)*100

        matrix_DD.loc[short_title] = [action_pairs_against_QLS['%_DD'],action_pairs_against_QLUT['%_DD'],action_pairs_against_QLDE['%_DD'],action_pairs_against_QLVE_e['%_DD'],action_pairs_against_QLVE_k['%_DD'],action_pairs_against_QLVM['%_DD']]



        action_pairs_against_QLS['%_DC'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='D, C'].count()/ n_runs)*100
        if order_QLUT=='QLUT_first':
            action_pairs_against_QLUT['%_DC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, D'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLUT['%_DC'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, C'].count()/ n_runs)*100
        if order_QLDE=='QLDE_first':
            action_pairs_against_QLDE['%_DC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, D'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLDE['%_DC'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, C'].count()/ n_runs)*100
        if order_QLVE_e=='QLVE_e_first':
            action_pairs_against_QLVE_e['%_DC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, D'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLVE_e['%_DC'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, C'].count()/ n_runs)*100
        if order_QLVE_k=='QLVE_k_first':
            action_pairs_against_QLVE_k['%_DC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, D'].count()/ n_runs)*100
        else:
            action_pairs_against_QLVE_k['%_DC'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, C'].count()/ n_runs)*100
        if order_QLVM=='QLVM_first':
            action_pairs_against_QLVM['%_DC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, D'].count()/ n_runs)*100
        else:
            action_pairs_against_QLVM['%_DC'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, C'].count()/ n_runs)*100
        
        matrix_DC.loc[short_title] = [action_pairs_against_QLS['%_DC'],action_pairs_against_QLUT['%_DC'],action_pairs_against_QLDE['%_DC'],action_pairs_against_QLVE_e['%_DC'],action_pairs_against_QLVE_k['%_DC'],action_pairs_against_QLVM['%_DC']]




        action_pairs_against_QLS['%_CD'] = (action_pairs_against_QLS[action_pairs_against_QLS[:]=='C, D'].count()/ n_runs)*100
        if order_QLUT=='QLUT_first':
            action_pairs_against_QLUT['%_CD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='D, C'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLUT['%_CD'] = (action_pairs_against_QLUT[action_pairs_against_QLUT[:]=='C, D'].count()/ n_runs)*100
        if order_QLDE=='QLDE_first':
            action_pairs_against_QLDE['%_CD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='D, C'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLDE['%_CD'] = (action_pairs_against_QLDE[action_pairs_against_QLDE[:]=='C, D'].count()/ n_runs)*100
        if order_QLVE_e=='QLVE_e_first':
            action_pairs_against_QLVE_e['%_CD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='D, C'].count()/ n_runs)*100
        else: 
            action_pairs_against_QLVE_e['%_CD'] = (action_pairs_against_QLVE_e[action_pairs_against_QLVE_e[:]=='C, D'].count()/ n_runs)*100
        if order_QLVE_k=='QLVE_k_first':
            action_pairs_against_QLVE_k['%_CD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='D, C'].count()/ n_runs)*100
        else:
            action_pairs_against_QLVE_k['%_CD'] = (action_pairs_against_QLVE_k[action_pairs_against_QLVE_k[:]=='C, D'].count()/ n_runs)*100
        if order_QLVM=='QLVM_first':
            action_pairs_against_QLVM['%_CD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='D, C'].count()/ n_runs)*100
        else:
            action_pairs_against_QLVM['%_CD'] = (action_pairs_against_QLVM[action_pairs_against_QLVM[:]=='C, D'].count()/ n_runs)*100

        matrix_CD.loc[short_title] = [action_pairs_against_QLS['%_CD'],action_pairs_against_QLUT['%_CD'],action_pairs_against_QLDE['%_CD'],action_pairs_against_QLVE_e['%_CD'],action_pairs_against_QLVE_k['%_CD'],action_pairs_against_QLVM['%_CD']]



        #matrix_DCCD.loc[short_title] = action_pairs_against_QLS['%_DC'],action_pairs_against_QLUT['%_DC'],action_pairs_against_QLDE['%_DC'],action_pairs_against_QLVE_e['%_DC'],action_pairs_against_QLVE_k['%_DC']


    for label in types:
        for matrix in [matrix_CC, matrix_DD, matrix_DC, matrix_CD]:
            matrix[label] = matrix[label].astype(float)


    types_long = ['Selfish','Utilitarian','Deontolog.','Virtue-eq.','Virtue-kind.','Virtue-mix.']

    if not os.path.isdir('results/outcome_plots/actions_matrix'):
        os.makedirs('results/outcome_plots/actions_matrix')
        
    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_CC, cmap='YlGn', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='Mutual Cooperation \n')
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/CC.pdf', bbox_inches='tight')
    matrix_CC.to_csv('results/outcome_plots/actions_matrix/matrix_CC.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_DD, cmap='PuRd', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='Mutual Defection \n')
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/DD.pdf', bbox_inches='tight')
    matrix_DD.to_csv('results/outcome_plots/actions_matrix/matrix_DD.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_DC, cmap='Oranges', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='M Defects, O Cooperates\n ') #M exploits O
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/DC.pdf', bbox_inches='tight')
    matrix_DC.to_csv('results/outcome_plots/actions_matrix/matrix_DC.csv')

    plt.figure(figsize=figsize)
    s = sns.heatmap(matrix_CD, cmap='Blues', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    sns.set(font_scale=4)
    s.set(xlabel='Opponent O', ylabel='Player M', title='M Cooperates, O Defects\n') #M Getting Exploited
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/CD.pdf', bbox_inches='tight')
    matrix_CD.to_csv('results/outcome_plots/actions_matrix/matrix_CD.csv')


def plot_baseline_matrix_action_pairs(n_runs):
    '''visualise % mutual cooperation
    - consider only the final pair to see where the pair ended up'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    figsize=(8, 6.5)
    types = ['S','UT','DE','Ve','Vk','Vm']
    static_strategies = ['AC','AD','TFT','Random']

    matrix_CC = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_DD = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_DC = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_CD = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)


    for player1_title in ['QLS','QLUT','QLDE','QLVE_e','QLVE_k','QLVM']:
        action_pairs_against_AC = pd.read_csv(f'results/{player1_title}_AC/action_pairs.csv', index_col=0).iloc[9999]
        action_pairs_against_AD = pd.read_csv(f'results/{player1_title}_AD/action_pairs.csv', index_col=0).iloc[9999]
        action_pairs_against_TFT = pd.read_csv(f'results/{player1_title}_TFT/action_pairs.csv', index_col=0).iloc[9999]
        action_pairs_against_Random = pd.read_csv(f'results/{player1_title}_Random/action_pairs.csv', index_col=0).iloc[9999]


        action_pairs_against_AC['%_CC'] = (action_pairs_against_AC[action_pairs_against_AC[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_AD['%_CC'] = (action_pairs_against_AD[action_pairs_against_AD[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_TFT['%_CC'] = (action_pairs_against_TFT[action_pairs_against_TFT[:]=='C, C'].count() / n_runs)*100
        action_pairs_against_Random['%_CC'] = (action_pairs_against_Random[action_pairs_against_Random[:]=='C, C'].count() / n_runs)*100


        short_title = player1_title.replace('QL','').replace('VE_e','Ve').replace('VE_k','Vk').replace('VM','Vm')
        matrix_CC.loc[short_title] = [action_pairs_against_AC['%_CC'],action_pairs_against_AD['%_CC'],action_pairs_against_TFT['%_CC'],action_pairs_against_Random['%_CC']]
        

        action_pairs_against_AC['%_DD'] = (action_pairs_against_AC[action_pairs_against_AC[:]=='D, D'].count() / n_runs)*100
        action_pairs_against_AD['%_DD'] = (action_pairs_against_AD[action_pairs_against_AD[:]=='D, D'].count() / n_runs)*100
        action_pairs_against_TFT['%_DD'] = (action_pairs_against_TFT[action_pairs_against_TFT[:]=='D, D'].count() / n_runs)*100
        action_pairs_against_Random['%_DD'] = (action_pairs_against_Random[action_pairs_against_Random[:]=='D, D'].count() / n_runs)*100

        matrix_DD.loc[short_title] = [action_pairs_against_AC['%_DD'],action_pairs_against_AD['%_DD'],action_pairs_against_TFT['%_DD'],action_pairs_against_Random['%_DD']]


        action_pairs_against_AC['%_DC'] = (action_pairs_against_AC[action_pairs_against_AC[:]=='D, C'].count() / n_runs)*100
        action_pairs_against_AD['%_DC'] = (action_pairs_against_AD[action_pairs_against_AD[:]=='D, C'].count() / n_runs)*100
        action_pairs_against_TFT['%_DC'] = (action_pairs_against_TFT[action_pairs_against_TFT[:]=='D, C'].count() / n_runs)*100
        action_pairs_against_Random['%_DC'] = (action_pairs_against_Random[action_pairs_against_Random[:]=='D, C'].count() / n_runs)*100
        
        matrix_DC.loc[short_title] = [action_pairs_against_AC['%_DC'],action_pairs_against_AD['%_DC'],action_pairs_against_TFT['%_DC'],action_pairs_against_Random['%_DC']]


        action_pairs_against_AC['%_CD'] = (action_pairs_against_AC[action_pairs_against_AC[:]=='C, D'].count() / n_runs)*100
        action_pairs_against_AD['%_CD'] = (action_pairs_against_AD[action_pairs_against_AD[:]=='C, D'].count() / n_runs)*100
        action_pairs_against_TFT['%_CD'] = (action_pairs_against_TFT[action_pairs_against_TFT[:]=='C, D'].count() / n_runs)*100
        action_pairs_against_Random['%_CD'] = (action_pairs_against_Random[action_pairs_against_Random[:]=='C, D'].count() / n_runs)*100
        
        matrix_CD.loc[short_title] = [action_pairs_against_AC['%_CD'],action_pairs_against_AD['%_CD'],action_pairs_against_TFT['%_CD'],action_pairs_against_Random['%_CD']]

        #matrix_DCCD.loc[short_title] = action_pairs_against_QLS['%_DC'],action_pairs_against_QLUT['%_DC'],action_pairs_against_QLDE['%_DC'],action_pairs_against_QLVE_e['%_DC'],action_pairs_against_QLVE_k['%_DC']


    for label in static_strategies:
        for matrix in [matrix_CC, matrix_DD, matrix_DC, matrix_CD]:
            matrix[label] = matrix[label].astype(float)


    types_long = ['Selfish','Utilitarian','Deontolog.','Virtue-eq.','Virtue-kind.','Virtue-mix.']
    static_strategies_long = ['Always Coop.','Always Defect','Tit for Tat','Random']

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_CC, cmap='YlGn', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='Mutual Cooperation \n')
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/baseline_CC.pdf', bbox_inches='tight')
    matrix_CC.to_csv('results/outcome_plots/actions_matrix/baseline_matrix_CC.csv')


    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_DD, cmap='PuRd', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='Mutual Defection \n')
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/baseline_DD.pdf', bbox_inches='tight')
    matrix_DD.to_csv('results/outcome_plots/actions_matrix/baseline_matrix_DD.csv')


    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_DC, cmap='Oranges', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    s.set(xlabel='Opponent O', ylabel='Player M',title='M Defects, O Cooperates\n ') #M exploits O
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/baseline_DC.pdf', bbox_inches='tight')
    matrix_DC.to_csv('results/outcome_plots/actions_matrix/baseline_matrix_DC.csv')


    plt.figure(figsize=figsize)
    s = sns.heatmap(matrix_CD, cmap='Blues', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = 0, vmax = 100)
    sns.set(font_scale=4)
    s.set(xlabel='Opponent O', ylabel='Player M', title='M Cooperates, O Defects \n') #M Getting Exploited
    #plt.show()
    plt.savefig('results/outcome_plots/actions_matrix/baseline_CD.pdf', bbox_inches='tight')
    matrix_CD.to_csv('results/outcome_plots/actions_matrix/baseline_matrix_CD.csv')




def plot_matrix_social_outcomes(n_runs):
    '''visualise % mutual cooperation
    - consider only the final pair to see where the pair ended up'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    figsize=(8, 6.5)
    types = ['S','UT','DE','Ve','Vk','Vm']
    types_long = ['Selfish','Utilitarian','Deontolog.','Virtue-eq.','Virtue-kind.','Virtue-mix.']

    matrix_collective = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_gini = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_min = pd.DataFrame(columns=types, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)

    ylabs = {}
    ylims = {}

    if not os.path.isdir('results/outcome_plots/outcomes_matrix'):
        os.makedirs('results/outcome_plots/outcomes_matrix')

    for player1_title in ['QLS','QLUT','QLDE','QLVE_e','QLVE_k','QLVM']:
        short_title = player1_title.replace('QL','').replace('VE_e','Ve').replace('VE_k','Vk').replace('VM','Vm')
        
        for type in ['collective', 'gini', 'min']:
            against_QLS = pd.read_csv(f'results/{player1_title}_QLS/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLS_mean = against_QLS.mean()
            against_QLS_sds = against_QLS.std()
            against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

            try:
                against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            except:
                against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLUT_mean = against_QLUT.mean()
            against_QLUT_sds = against_QLUT.std()
            against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

            try:
                against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            except:
                against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLDE_mean = against_QLDE.mean()
            against_QLDE_sds = against_QLDE.std()
            against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

            try:
                against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            except:
                against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLVE_e_mean = against_QLVE_e.mean()
            against_QLVE_e_sds = against_QLVE_e.std()
            against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

            try:
                against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            except:
                against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLVE_k_mean = against_QLVE_k.mean()
            against_QLVE_k_sds = against_QLVE_k.std()
            against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

            try:
                against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            except:
                against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_QLVM_mean = against_QLVM.mean()
            against_QLVM_sds = against_QLVM.std()
            against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)
        
            ylabs[f'{type}'] = (f'$G_{{{type}}}$')

            if game_title=='IPD':
                if type=='collective':
                    ylims[f'{type}'] = [40000, 60000]
                elif type=='gini':
                    ylims[f'{type}'] = [5000, 10000] #5714.285714285714 min vale for G_gini
                elif type=='min':
                    ylims[f'{type}'] = [10000, 30000]
            elif game_title=='VOLUNTEER':
                if type=='collective': 
                    ylims[f'{type}'] = [20000, 80000]
                elif type=='gini':
                    ylims[f'{type}'] = [4000, 10000]
                elif type=='min':
                    ylims[f'{type}'] = [10000, 40000]
            elif game_title=='STAGHUNT': 
                if type=='collective': 
                    ylims[f'{type}'] = [40000, 100000]
                elif type=='gini':
                    ylims[f'{type}'] = [4000, 10000]
                elif type=='min':
                    ylims[f'{type}'] = [10000, 40000]
            


            if type == 'collective': 
                matrix_collective.loc[short_title] = [against_QLS_mean,against_QLUT_mean,against_QLDE_mean, against_QLVE_e_mean, against_QLVE_k_mean, against_QLVM_mean]
                for label in types:
                    matrix_collective[label] = matrix_collective[label].astype(float)

            elif type == 'gini':
                matrix_gini.loc[short_title] = [against_QLS_mean,against_QLUT_mean,against_QLDE_mean, against_QLVE_e_mean, against_QLVE_k_mean, against_QLVM_mean]
                for label in types:
                    matrix_gini[label] = matrix_gini[label].astype(float)
            
            elif type == 'min':
                matrix_min.loc[short_title] = [against_QLS_mean,against_QLUT_mean,against_QLDE_mean, against_QLVE_e_mean, against_QLVE_k_mean, against_QLVM_mean]
                for label in types:
                    matrix_min[label] = matrix_min[label].astype(float)

                
    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_collective, cmap='BrBG', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['collective'][0], vmax = ylims['collective'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Collective Return '+ylabs['collective']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/collective.pdf', bbox_inches='tight')
    matrix_collective.to_csv('results/outcome_plots/outcomes_matrix/matrix_collective.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_gini, cmap='BrBG', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['gini'][0], vmax = ylims['gini'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Gini Return '+ylabs['gini']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/gini.pdf', bbox_inches='tight')
    matrix_gini.to_csv('results/outcome_plots/outcomes_matrix/matrix_gini.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_min, cmap='BrBG', xticklabels=types_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['min'][0], vmax = ylims['min'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Minimum Return '+ylabs['min']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/min.pdf', bbox_inches='tight')
    matrix_min.to_csv('results/outcome_plots/outcomes_matrix/matrix_min.csv')
        

def plot_baseline_matrix_social_outcomes(n_runs):
    '''visualise % mutual cooperation
    - consider only the final pair to see where the pair ended up'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    figsize=(8, 6.5)
    types = ['S','UT','DE','Ve','Vk','Vm']
    static_strategies = ['AC','AD','TFT','Random']
    types_long = ['Selfish','Utilitarian','Deontolog.','Virtue-eq.','Virtue-kind.','Virtue-mix.']
    static_strategies_long = ['Always Coop.','Always Defect','Tit for Tat','Random']

    matrix_collective = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_gini = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)
    matrix_min = pd.DataFrame(columns=static_strategies, index=types) #shape = vs S,UT,DE,Ve,Vk(,VEm)

    ylabs = {}
    ylims = {}

    if not os.path.isdir('results/outcome_plots/outcomes_matrix'):
        os.makedirs('results/outcome_plots/outcomes_matrix')

    for player1_title in ['QLS','QLUT','QLDE','QLVE_e','QLVE_k','QLVM']:
        short_title = player1_title.replace('QL','').replace('VE_e','Ve').replace('VE_k','Vk').replace('VM','Vm')
        
        for type in ['collective', 'gini', 'min']:
            against_AC = pd.read_csv(f'results/{player1_title}_AC/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_AC_mean = against_AC.mean()
            against_AC_sds = against_AC.std()
            against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

            against_AD = pd.read_csv(f'results/{player1_title}_AD/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_AD_mean = against_AD.mean()
            against_AD_sds = against_AD.std()
            against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

            against_TFT = pd.read_csv(f'results/{player1_title}_TFT/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_TFT_mean = against_TFT.mean()
            against_TFT_sds = against_TFT.std()
            against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

            against_Random = pd.read_csv(f'results/{player1_title}_Random/df_cumulative_reward_{type}.csv', index_col=0).iloc[-1]
            against_Random_mean = against_Random.mean()
            against_Random_sds = against_Random.std()
            against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

        
            ylabs[f'{type}'] = (f'$G_{{{type}}}$')

            if game_title=='IPD':
                if type=='collective':
                    ylims[f'{type}'] = [40000, 60000]
                elif type=='gini':
                    ylims[f'{type}'] = [5000, 10000] #5714.285714285714 min vale for Gmin
                elif type=='min':
                    ylims[f'{type}'] = [10000, 30000]
            elif game_title=='VOLUNTEER':
                if type=='collective': 
                    ylims[f'{type}'] = [20000, 80000]
                elif type=='gini':
                    ylims[f'{type}'] = [4000, 10000]
                elif type=='min':
                    ylims[f'{type}'] = [10000, 40000]
            elif game_title=='STAGHUNT': 
                if type=='collective': 
                    ylims[f'{type}'] = [40000, 100000]
                elif type=='gini':
                    ylims[f'{type}'] = [4000, 10000]
                elif type=='min':
                    ylims[f'{type}'] = [10000, 40000]
            

            if type == 'collective': 
                matrix_collective.loc[short_title] = [against_AC_mean, against_AD_mean, against_TFT_mean, against_Random_mean]
                for label in static_strategies:
                    matrix_collective[label] = matrix_collective[label].astype(float)

            elif type == 'gini':
                matrix_gini.loc[short_title] = [against_AC_mean, against_AD_mean, against_TFT_mean, against_Random_mean]
                for label in static_strategies:
                    matrix_gini[label] = matrix_gini[label].astype(float)
            
            elif type == 'min':
                matrix_min.loc[short_title] = [against_AC_mean, against_AD_mean, against_TFT_mean, against_Random_mean]
                for label in static_strategies:
                    matrix_min[label] = matrix_min[label].astype(float)

                
    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_collective, cmap='BrBG', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['collective'][0], vmax = ylims['collective'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Collective Return '+ylabs['collective']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/baseline_collective.pdf', bbox_inches='tight')
    matrix_collective.to_csv('results/outcome_plots/outcomes_matrix/baseline_matrix_collective.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_gini, cmap='BrBG', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['gini'][0], vmax = ylims['gini'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Gini Return '+ylabs['gini']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/baseline_gini.pdf', bbox_inches='tight')
    matrix_gini.to_csv('results/outcome_plots/outcomes_matrix/baseline_matrix_gini.csv')

    plt.figure(figsize=figsize)
    sns.set(font_scale=4)
    s = sns.heatmap(matrix_min, cmap='BrBG', xticklabels=static_strategies_long, yticklabels=types_long, annot=False, linecolor='black', linewidths=0, square=False, vmin = ylims['min'][0], vmax = ylims['min'][1])
    s.set(xlabel='Opponent O', ylabel='Player M',title='Minimum Return '+ylabs['min']+' \n')
    plt.savefig('results/outcome_plots/outcomes_matrix/baseline_min.pdf', bbox_inches='tight')
    matrix_min.to_csv('results/outcome_plots/outcomes_matrix/baseline_matrix_min.csv')
            



def plot_stacked_relative_reward(n_runs):
    '''plot game reward - relatie cumulative (bar & over time) & per iteration
    - how well off did the players end up relative to each other on the game?'''

    data = dict() #keys=['QLS', 'QLUT', 'QLDE', 'QLVE_e', 'QLVE_k', 'QLVM'], values=[]

    for player1_title in ['QLS', 'QLUT', 'QLDE', 'QLVE_e', 'QLVE_k', 'QLVM']: 
        ##################################
        #### bar chart game cumulative reward for player1_tytle vs others  ####
        ##################################
        against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLS_means = against_QLS.mean()
        against_QLS_sds = against_QLS.std()
        against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

        try:
            against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        except:
            against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLUT_means = against_QLUT.mean()
        against_QLUT_sds = against_QLUT.std()
        against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

        try:
            against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        except:
            against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLDE_means = against_QLDE.mean()
        against_QLDE_sds = against_QLDE.std()
        against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

        try:
            against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        except:
            against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLVE_e_means = against_QLVE_e.mean()
        against_QLVE_e_sds = against_QLVE_e.std()
        against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

        try:
            against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        except:
            against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLVE_k_means = against_QLVE_k.mean()
        against_QLVE_k_sds = against_QLVE_k.std()
        against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

        try:
            against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        except:
            against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
        against_QLVM_means = against_QLVM.mean()
        against_QLVM_sds = against_QLVM.std()
        against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

        data[str('means_'+player1_title)] = [against_QLS_means, against_QLUT_means, against_QLDE_means, against_QLVE_e_means, against_QLVE_k_means, against_QLVM_means]
        data[str('CIs_'+player1_title)] = [against_QLS_ci, against_QLUT_ci, against_QLDE_ci, against_QLVE_e_ci, against_QLVE_k_ci, against_QLVM_ci]



    labels = ['S', 'UT', 'DE', 'V'+r'$_e$', 'V'+r'$_k$', 'V'+r'$_m$'] 
    #colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple', 'pink'] 
    colors = ['#984464', '#e6a176', '#556b2f', '#5eccab', '#537eff', '#c0affb']
    #colors = ['#e1562c', 'orange', '#556b2f', 'lightblue', '#00678a', 'pink']
    #plt.rcParams.update({'font.size':20})
    font = {'size'   : 15}
    matplotlib.rc('font', **font)

    fig, axes = plt.subplots(1, 6, figsize=(11, 3.5), sharey=True) #constrained_layout=False, tight_layout=False, 
    ax1, ax2, ax3, ax4, ax5, ax6 = axes

    ax1.bar(labels, data['means_QLS'], yerr=data['CIs_QLS'], color=colors) #, width = 0.8
    ax1.set_title('Selfish') #vs others
    ax1.set_ylabel('Cumulative \n' + 'Game Reward') #r'$R_{extr}$'
    #ax1.set_ylim()
    if game_title=='IPD': #NOTE game_title is set outside this function - in the overall environment - see code below 
        plt.gca().set_ylim([0, 40000])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([0, 50000])  
    #ax1.set_xticklabels(ax1.get_xticklabels(), rotation = 45)
    #ax1.set_xticklabels(labels, rotation=90, ha='right')
    #ax1.yaxis.set_label(r'Cumulative Game Reward $R_{extr}$')
 
    
    ax2.bar(labels, data['means_QLUT'], yerr=data['CIs_QLUT'], color=colors) #, width = 0.8
    ax2.set_title('Utilitarian')

    ax3.bar(labels, data['means_QLDE'], yerr=data['CIs_QLDE'], color=colors) #, width = 0.8
    ax3.set_title('Deontolog.')

    ax4.bar(labels, data['means_QLVE_e'], yerr=data['CIs_QLVE_e'], color=colors) #, width = 0.8
    ax4.set_title(' Virtue-equal.')

    ax5.bar(labels, data['means_QLVE_k'], yerr=data['CIs_QLVE_k'], color=colors) #, width = 0.8
    ax5.set_title(' Virtue-kind.')

    ax6.bar(labels, data['means_QLVM'], yerr=data['CIs_QLVM'], color=colors) #, width = 0.8
    ax6.set_title(' Virtue-mixed')

    fig.suptitle('Game Reward for player type M vs all others \n')
    
    #ax1.yaxis.set_label(r'Cumulative Game Reward $R_{extr}$')
    fig.autofmt_xdate(rotation=90, bottom=0.2, ha='center')
    #plt.xticks(rotation=45)
    fig.supxlabel('\n'+'Opponent type') #NOTE this requires matplotlib>3.4 
    plt.tight_layout(pad=0.001, w_pad=0.8)
    fig.show()


    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/new_cumulative_game_reward.png', bbox_inches='tight')
    

def set_ylims(game_title, player1_title): 
    '''this function sets ylims for the plots of cumulative moral reward across all 3 games & 6 player types'''
    ylims = [] 
    if game_title=='IPD':
        if player1_title == 'QLUT':
            ylims[0:1] = [0, 60000]
        elif player1_title == 'QLDE':
            ylims[0:1] = [-50000, 0]
        elif player1_title == 'QLVE_e':
            ylims[0:1] = [0, 10000]
        elif player1_title == 'QLVE_k':
            ylims[0:1] = [0, 50000]
        elif player1_title == 'QLVM':
            ylims[0:1] = [0, 10000]
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            ylims[0:1] = [0, 80000]
        elif player1_title == 'QLDE':
            ylims[0:1] = [-50000, 0]
        elif player1_title == 'QLVE_e':
            ylims[0:1] = [0, 10000]
        elif player1_title == 'QLVE_k':
            ylims[0:1] = [0, 50000]
        elif player1_title == 'QLVM':
            ylims[0:1] = [0, 10000]
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            ylims[0:2] = [0, 100000]
        elif player1_title == 'QLDE':
            ylims[0:2] = [-50000, 0]
        elif player1_title == 'QLVE_e':
            ylims[0:2] = [0, 10000]
        elif player1_title == 'QLVE_k':
            ylims[0:2] = [0, 50000]
        elif player1_title == 'QLVM':
            ylims[0:2] = [0, 10000]
    return ylims[0], ylims[1]

def plot_stacked_relative_moral_reward(n_runs):
    '''plot game reward - relatie cumulative (bar & over time) & per iteration
    - how well off did the players end up relative to each other on the game?'''

    data = dict() #keys=['QLS', 'QLUT', 'QLDE', 'QLVE_e', 'QLVE_k', 'QLVM'], values=[]

    for player1_title in ['QLS', 'QLUT', 'QLDE', 'QLVE_e', 'QLVE_k', 'QLVM']: 
        ##################################
        #### bar chart game cumulative reward for player1_tytle vs others  ####
        ##################################
        against_QLS = pd.read_csv(f'results/{player1_title}_QLS/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLS_means = against_QLS.mean()
        against_QLS_sds = against_QLS.std()
        against_QLS_ci = 1.96 * against_QLS_sds/np.sqrt(n_runs)

        try:
            against_QLUT = pd.read_csv(f'results/{player1_title}_QLUT/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        except:
            against_QLUT = pd.read_csv(f'results/QLUT_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLUT_means = against_QLUT.mean()
        against_QLUT_sds = against_QLUT.std()
        against_QLUT_ci = 1.96 * against_QLUT_sds/np.sqrt(n_runs)

        try:
            against_QLDE = pd.read_csv(f'results/{player1_title}_QLDE/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        except:
            against_QLDE = pd.read_csv(f'results/QLDE_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLDE_means = against_QLDE.mean()
        against_QLDE_sds = against_QLDE.std()
        against_QLDE_ci = 1.96 * against_QLDE_sds/np.sqrt(n_runs)

        try:
            against_QLVE_e = pd.read_csv(f'results/{player1_title}_QLVE_e/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        except:
            against_QLVE_e = pd.read_csv(f'results/QLVE_e_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLVE_e_means = against_QLVE_e.mean()
        against_QLVE_e_sds = against_QLVE_e.std()
        against_QLVE_e_ci = 1.96 * against_QLVE_e_sds/np.sqrt(n_runs)

        try:
            against_QLVE_k = pd.read_csv(f'results/{player1_title}_QLVE_k/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        except:
            against_QLVE_k = pd.read_csv(f'results/QLVE_k_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLVE_k_means = against_QLVE_k.mean()
        against_QLVE_k_sds = against_QLVE_k.std()
        against_QLVE_k_ci = 1.96 * against_QLVE_k_sds/np.sqrt(n_runs)

        try:
            against_QLVM = pd.read_csv(f'results/{player1_title}_QLVM/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        except:
            against_QLVM = pd.read_csv(f'results/QLVM_{player1_title}/player2/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
        against_QLVM_means = against_QLVM.mean()
        against_QLVM_sds = against_QLVM.std()
        against_QLVM_ci = 1.96 * against_QLVM_sds/np.sqrt(n_runs)

        data[str('means_'+player1_title)] = [against_QLS_means, against_QLUT_means, against_QLDE_means, against_QLVE_e_means, against_QLVE_k_means, against_QLVM_means]
        data[str('CIs_'+player1_title)] = [against_QLS_ci, against_QLUT_ci, against_QLDE_ci, against_QLVE_e_ci, against_QLVE_k_ci, against_QLVM_ci]



    labels = ['S', 'UT', 'DE', 'V'+r'$_e$', 'V'+r'$_k$', 'V'+r'$_m$'] 
    #colors = ['red', '#556b2f', '#00cccc', 'orange', 'purple', 'pink'] 
    colors = ['#984464', '#e6a176', '#556b2f', '#5eccab', '#537eff', '#c0affb']
    #colors = ['#e1562c', 'orange', '#556b2f', 'lightblue', '#00678a', 'pink']
    #plt.rcParams.update({'font.size':20})
    font = {'size'   : 15}
    matplotlib.rc('font', **font)

    fig, axes = plt.subplots(1, 5, figsize=(11, 3.5), sharey=False) #constrained_layout=False, tight_layout=False, 
    ax2, ax3, ax4, ax5, ax6 = axes

    #ax1.bar(labels, data['means_QLS'], yerr=data['CIs_QLS'], color=colors) #, width = 0.8
    #ax1.set_title('Selfish') #vs others
    #ax1.set_ylabel('Cumulative \n' + 'Moral Reward') #r'$R_{extr}$' 
    
    ax2.bar(labels, data['means_QLUT'], yerr=data['CIs_QLUT'], color=colors) #, width = 0.8
    ax2.set_title('Utilitarian')
    ylims = set_ylims(game_title, 'QLUT')
    ax2.set_ylim(ylims)

    ax3.bar(labels, data['means_QLDE'], yerr=data['CIs_QLDE'], color=colors) #, width = 0.8
    ax3.set_title('Deontolog.')
    ylims = set_ylims(game_title, 'QLDE')
    ax3.set_ylim(ylims)

    ax4.bar(labels, data['means_QLVE_e'], yerr=data['CIs_QLVE_e'], color=colors) #, width = 0.8
    ax4.set_title(' Virtue-equal.')
    ylims = set_ylims(game_title, 'QLVE_e')
    ax4.set_ylim(ylims)

    ax5.bar(labels, data['means_QLVE_k'], yerr=data['CIs_QLVE_k'], color=colors) #, width = 0.8
    ax5.set_title(' Virtue-kind.')
    ylims = set_ylims(game_title, 'QLVE_k')
    ax5.set_ylim(ylims)

    ax6.bar(labels, data['means_QLVM'], yerr=data['CIs_QLVM'], color=colors) #, width = 0.8
    ax6.set_title(' Virtue-mixed')
    ylims = set_ylims(game_title, 'QLVM')
    ax6.set_ylim(ylims)

    for ax in axes:
        for label in ax.get_yticklabels():
	        label.set_fontsize(11)

    fig.suptitle('Moral Reward for player type M vs all others \n')
    
    ax2.set_ylabel('Cumulative \n Moral Reward')
    fig.autofmt_xdate(rotation=90, bottom=0.2, ha='center')
    #plt.xticks(rotation=45)
    fig.supxlabel('\n'+'Opponent type') #NOTE this requires matplotlib>3.4 
    plt.tight_layout(pad=0.001, w_pad=0.1)
    fig.show()


    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/new_cumulative_intrinsic_reward.png', bbox_inches='tight')
    





########################
#### baseline group plots (learning vs. static opponent), or fuly static opponent ####
########################
#TO DO UPDATE THESE
def plot_basleline_relative_moral_reward(player1_title, n_runs):
    ##################################
    #### cumulative - game reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_intrinsic.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99', 
    
    plt.title(r'Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 60000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-1300, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 80000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-1300, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 80000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-1300, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
    plt.ylabel(f'Cumulative Intrinsoc reward for {player1_title}')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/baseline_cumulative_intrinsic_reward_{player1_title}.png', bbox_inches='tight')


    ##################################
    #### non-cumulative - game reward for player1_title vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_reward_intrinsic.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_reward_intrinsic.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_reward_intrinsic.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_reward_intrinsic.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99', 
    
    plt.title(r'Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')

    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 6])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([2, 8])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 10])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])

    plt.ylabel(f'Intrinsic reward for {player1_title}')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/group_outcomes/baseline_intrinsic_reward_{player1_title}.png', bbox_inches='tight')

def plot_baseline_cumulative_reward(player1_title, n_runs):
    #plot game and moral cumulative rewards as  barplots - how well off did the players end up relative to each other on the game / in terms of moral reward? 

    ##################################
    #### game cumulative reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_AC_means = against_AC.mean()
    against_AC_sds = against_AC.std()
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_AD_means = against_AD.mean()
    against_AD_sds = against_AD.std()
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_TFT_means = against_TFT.mean()
    against_TFT_sds = against_TFT.std()
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_Random_means = against_Random.mean()
    against_Random_sds = against_Random.std()
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

   
    #import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.rcParams.update({'font.size':14})
    ax = fig.add_axes([0,0,1,1])
    labels = ['vs_AC', 'vs_AD', 'vs_TFT', 'vs_Random']
    means = [against_AC_means,against_AD_means,against_TFT_means,against_Random_means]
    cis = [against_AC_ci,against_AD_ci,against_TFT_ci,against_Random_ci]
    colors = ['cornflowerblue', 'orange', 'lightgreen', 'lightcoral']
    ax.bar(labels, means, yerr=cis, color=colors)
    ax.set_ylabel(f'Cumulative Game reward for {player1_title}')
    ax.set_title('Cumulative Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player')
    ax.set_xlabel('Opponent type')
    plt.savefig(f'results/outcome_plots/reward/bar_baseline_cumulative_game_reward_{player1_title}.png', bbox_inches='tight')


    ##################################
    #### moral cumulative reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_AC_means = against_AC.mean()
    against_AC_sds = against_AC.std()
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_AD_means = against_AD.mean()
    against_AD_sds = against_AD.std()
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_TFT_means = against_TFT.mean()
    against_TFT_sds = against_TFT.std()
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_Random_means = against_Random.mean()
    against_Random_sds = against_Random.std()
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

   
    #import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.rcParams.update({'font.size':14})
    ax = fig.add_axes([0,0,1,1])
    labels = ['vs_AC', 'vs_AD', 'vs_TFT', 'vs_Random']
    means = [against_AC_means,against_AD_means,against_TFT_means,against_Random_means]
    cis = [against_AC_ci,against_AD_ci,against_TFT_ci,against_Random_ci]
    colors = ['cornflowerblue', 'orange', 'lightgreen', 'lightcoral']
    ax.bar(labels, means, yerr=cis, color=colors)
    ax.set_ylabel(f'Cumulative Intrinsic reward for {player1_title}')
    ax.set_title('Cumulative Intrinsic Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player')
    ax.set_xlabel('Opponent type')
    plt.savefig(f'results/outcome_plots/reward/bar_baseline_cumulative_intrinsic_reward_{player1_title}.png', bbox_inches='tight')

def plot_basleline_relative_cooperation(player1_title, n_runs): 
    actions_against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/action.csv', index_col=0)
    #calculate % of 100 agents (runs) that cooperate at every step  out of the 10000
    actions_against_AC['%_defect'] = actions_against_AC[actions_against_AC[:]==1].count(axis='columns')
    actions_against_AC['%_cooperate'] = n_runs-actions_against_AC['%_defect']
    actions_against_AC['%_defect'] = (actions_against_AC['%_defect']/n_runs)*100
    actions_against_AC['%_cooperate'] = (actions_against_AC['%_cooperate']/n_runs)*100

    actions_against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/action.csv', index_col=0)
    actions_against_AD['%_defect'] = actions_against_AD[actions_against_AD[:]==1].count(axis='columns')
    actions_against_AD['%_cooperate'] = n_runs-actions_against_AD['%_defect']
    actions_against_AD['%_defect'] = (actions_against_AD['%_defect']/n_runs)*100
    actions_against_AD['%_cooperate'] = (actions_against_AD['%_cooperate']/n_runs)*100

    actions_against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/action.csv', index_col=0)
    actions_against_TFT['%_defect'] = actions_against_TFT[actions_against_TFT[:]==1].count(axis='columns')
    actions_against_TFT['%_cooperate'] = n_runs-actions_against_TFT['%_defect']
    actions_against_TFT['%_defect'] = (actions_against_TFT['%_defect']/n_runs)*100
    actions_against_TFT['%_cooperate'] = (actions_against_TFT['%_cooperate']/n_runs)*100

    actions_against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/action.csv', index_col=0)
    actions_against_Random['%_defect'] = actions_against_Random[actions_against_Random[:]==1].count(axis='columns')
    actions_against_Random['%_cooperate'] = n_runs-actions_against_Random['%_defect']
    actions_against_Random['%_defect'] = (actions_against_Random['%_defect']/n_runs)*100
    actions_against_Random['%_cooperate'] = (actions_against_Random['%_cooperate']/n_runs)*100

    #plot results 
    plt.figure(dpi=80) #figsize=(10, 6), 
    plt.plot(actions_against_AC.index[:], actions_against_AC['%_cooperate'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. AC')#, color='blue')
    plt.plot(actions_against_AD.index[:], actions_against_AD['%_cooperate'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. AD')#, color='blue')
    plt.plot(actions_against_TFT.index[:], actions_against_TFT['%_cooperate'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. TFT')#, color='blue')
    plt.plot(actions_against_Random.index[:], actions_against_Random['%_cooperate'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. Random')#, color='blue')
    
    plt.title('Probability of Cooperation (% over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    plt.gca().set_ylim([0, 100])
    plt.ylabel('Percentage cooperating')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/cooperation'):
        os.makedirs('results/outcome_plots/cooperation')
    plt.savefig(f'results/outcome_plots/cooperation/baseline_cooperation_{player1_title}.png', bbox_inches='tight')

def plot_relative_baseline_action_pairs(player1_title, n_runs):
    '''visualise action types that each individual player takes against their opponent's last move 
    --> what strategies are being learnt at all steps of the run? 
    - consider the whole run'''
    #NOTE this will only work for 10000 iterations right now, not fewer!!!
    #NOTE we plot after iteration 0 as then the agent is reacting to a default initial state, not a move from the opponent

    action_pairs_against_AC = pd.read_csv(f'results/{player1_title}_AC/action_pairs.csv', index_col=0)
    action_pairs_against_AD = pd.read_csv(f'results/{player1_title}_AD/action_pairs.csv', index_col=0)
    ction_pairs_against_TFT = pd.read_csv(f'results/{player1_title}_TFT/action_pairs.csv', index_col=0)
    action_pairs_against_Random = pd.read_csv(f'results/{player1_title}_Random/action_pairs.csv', index_col=0)

    #results_counts = action_pairs_against_QLS.transpose().apply(pd.value_counts).transpose()[1:] 
    #plot after first episode, as in the first apisode they are reacting to default state=0
    #results_counts.dropna(axis=1, how='all', inplace=True)

    action_pairs_against_AC['%_CC'] = action_pairs_against_AC[action_pairs_against_AC[:]=='C, C'].count(axis='columns')
    action_pairs_against_AD['%_CC'] = action_pairs_against_AD[action_pairs_against_AD[:]=='C, C'].count(axis='columns')
    ction_pairs_against_TFT['%_CC'] = ction_pairs_against_TFT[ction_pairs_against_TFT[:]=='C, C'].count(axis='columns')
    action_pairs_against_Random['%_CC'] = action_pairs_against_Random[action_pairs_against_Random[:]=='C, C'].count(axis='columns')


    #plt.figure(figsize=(20, 15), dpi=100)
    #results_counts.plot.area(stacked=True, ylabel = '# agent pairs taking this pair of actions \n (across '+str(n_runs)+' runs)', rot=45,
    #    xlabel='Iteration', #colormap='PiYG_r',
    #    color={'C, C':'#28641E', 'C, D':'#B0DC82', 'D, C':'#EEAED4', 'D, D':'#8E0B52'}, 
    #    title='Pairs of simultaneous actions over time: \n '+player1_title+' agent vs '+player2_title+' agent')
    #plt.savefig(f'{destination_folder}/plots/relative_action_pairs.png', bbox_inches='tight')

    #plot results 
    plt.figure(dpi=80) #figsize=(10, 6), 
    plt.plot(action_pairs_against_AC.index[:], action_pairs_against_AC['%_CC'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. AC')#, color='blue')
    plt.plot(action_pairs_against_AD.index[:], action_pairs_against_AD['%_CC'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. AD')#, color='blue')
    plt.plot(ction_pairs_against_TFT.index[:], ction_pairs_against_TFT['%_CC'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. TFT')#, color='blue')
    plt.plot(action_pairs_against_Random.index[:], action_pairs_against_Random['%_CC'], lw=0.5, alpha=0.5, label=f'{player1_title} vs. Random')#, color='blue')

    plt.title('Mutual Cooperation among the two agents (% over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    plt.gca().set_ylim([0, 100])
    plt.ylabel('Percentage mutually cooperating')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/cooperation'):
        os.makedirs('results/outcome_plots/cooperation')
    plt.savefig(f'results/outcome_plots/cooperation/baseline_mutual_cooperation_{player1_title}.png', bbox_inches='tight')

def plot_baseline_relative_outcomes(type, player1_title, n_runs, game_title):
    ##################################
    #### cumulative - {type} game reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/df_cumulative_reward_{type}.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/df_cumulative_reward_{type}.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/df_cumulative_reward_{type}.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/df_cumulative_reward_{type}.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99', 
    
    plt.title(r'Cumulative '+type+' Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    if game_title=='IPD':
        if type=='collective':
            plt.gca().set_ylim([0, 60000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 30000])
    elif game_title=='VOLUNTEER':
        if type=='collective': 
            plt.gca().set_ylim([0, 80000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 40000])
    elif game_title=='STAGHUNT': 
        if type=='collective': 
            plt.gca().set_ylim([0, 100000])
        elif type=='gini':
            plt.gca().set_ylim([0, 10000])
        elif type=='min':
            plt.gca().set_ylim([0, 50000])    
    plt.ylabel(f'Cumulative {type} reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/group_outcomes'):
        os.makedirs('results/outcome_plots/group_outcomes')
    plt.savefig(f'results/outcome_plots/group_outcomes/baseline_cumulative_{type}_reward_{player1_title}.png', bbox_inches='tight')


    ######################################
    #### non-cumulative - {type} game reward ####
    ######################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/df_reward_{type}.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/df_reward_{type}.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/df_reward_{type}.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/df_reward_{type}.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.5, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99',
    
    plt.title(type+' Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    if type=='gini':
        plt.gca().set_ylim([0, 1])
    if game_title=='IPD':
        if type=='collective':
            plt.gca().set_ylim([4, 6])
        elif type=='min':
            plt.gca().set_ylim([1, 3])
    elif game_title=='VOLUNTEER':
        if type=='collective': 
            plt.gca().set_ylim([2, 8])
        elif type=='min':
            plt.gca().set_ylim([1, 4])
    elif game_title=='STAGHUNT': 
        if type=='collective': 
            plt.gca().set_ylim([4, 10])
        elif type=='min':
            plt.gca().set_ylim([1, 5])    
    plt.ylabel(f'{type} reward')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/group_outcomes/baseline_{type}_reward_{player1_title}.png', bbox_inches='tight')

def old_plot_basleline_relative_reward(player1_title, n_runs):
    ##################################
    #### cumulative - game reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_game.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_game.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_game.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_game.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99', 
    
    plt.title(r'Cumulative game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')
    if game_title=='IPD':
        plt.gca().set_ylim([0, 40000])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([0, 50000])  
    plt.ylabel(f'Cumulative game reward for {player1_title}')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/baseline_cumulative_game_reward_{player1_title}.png', bbox_inches='tight')


    ##################################
    #### non-cumulative - game reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_reward_game.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_reward_game.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_reward_game.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_reward_game.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    plt.figure(dpi=80) #figsize=(10, 6)
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AC')#, color='red')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, alpha=0.5) #facecolor='#ff9999', 
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_AD')#, color='#556b2f')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, alpha=0.5) #facecolor='#ccff99', 
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_TFT')#, color='#00cccc')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, alpha=0.5) #facecolor='#99ffff', 
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.8, alpha=0.5, label=f'{player1_title}_Random')#, color='orange')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, alpha=0.5) #facecolor='#ffcc99', 
    
    plt.title(r'Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ player1_title +' vs static player (baseline)')

    if game_title=='IPD':
        plt.gca().set_ylim([1, 4])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([1, 5])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([1, 5])
    plt.ylabel(f'Game reward for {player1_title}')
    plt.xlabel('Iteration')
    leg = plt.legend() # get the legend object
    for line in leg.get_lines(): # change the line width for the legend
        line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/baseline_game_reward_{player1_title}.png', bbox_inches='tight')


def plot_baseline_relative_reward(player1_title, n_runs):
    '''plot game reward - relatie cumulative (bar & over time) & per iteration
    - how well off did the players end up relative to each other on the game?'''
    ##################################
    #### bar chart game cumulative reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_AC_means = against_AC.mean()
    against_AC_sds = against_AC.std()
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_AD_means = against_AD.mean()
    against_AD_sds = against_AD.std()
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_TFT_means = against_TFT.mean()
    against_TFT_sds = against_TFT.std()
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_game.csv', index_col=0).iloc[-1]
    against_Random_means = against_Random.mean()
    against_Random_sds = against_Random.std()
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)


    #import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(3, 3), dpi=80)
    plt.rcParams.update({'font.size':20})
    ax = fig.add_axes([0,0,1,1])
    labels = ['AC', 'AD', 'TFT', 'Rand.'] 
    means = [against_AC_means,against_AD_means,against_TFT_means,against_Random_means]
    cis = [against_AC_ci,against_AD_ci,against_TFT_ci,against_Random_ci]
    colors = ['lightgreen', 'crimson', 'gold', 'slategrey']  
    #add QLVM mixed agent 
    ax.bar(labels, means, yerr=cis, color=colors, width = 0.8) #capsize=7, 
    #plt.xticks(rotation=45)
    ax.set_ylabel(r'Cumulative $R_{extr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    #(f'R^{extr}_{i=QLUT}'# for {player1_title}')
    long_title = title_mapping[player1_title].replace('Ethics','').replace('_', '-')
    ax.set_title(long_title +' vs other \n') #'Cumulative Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    ax.set_xlabel('Opponent type')
    if game_title=='IPD': #NOTE game_title is set outside this function - in the overall environment - see code below 
        plt.gca().set_ylim([0, 40000])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([0, 50000])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([0, 50000])  
    if not os.path.isdir('results/outcome_plots/reward'):
        os.makedirs('results/outcome_plots/reward')
    plt.savefig(f'results/outcome_plots/reward/baseline_bar_cumulative_game_reward_{player1_title}.pdf', bbox_inches='tight')
    


    ##################################
    #### non-cumulative - game reward for player1_tytle vs others  ####
    ##################################
    figsize=(5, 4)

    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_reward_game.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_reward_game.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_reward_game.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_reward_game.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

   

    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_AC', color='lightgreen')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, facecolor='lightgreen', alpha=0.5)
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_AD', color='crimson')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, facecolor='crimson', alpha=0.5)
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_TFT', color='yellow')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, facecolor='yellow', alpha=0.5)
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_Random', color='darkgrey')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, facecolor='darkgrey', alpha=0.5)


    #long_title = title_mapping[player1_title]
    plt.title(long_title +' vs other \n') #r'Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        plt.gca().set_ylim([1, 4])
    elif game_title=='VOLUNTEER':
        plt.gca().set_ylim([1, 5])
    elif game_title=='STAGHUNT': 
        plt.gca().set_ylim([1, 5])
    plt.ylabel(r'$R_{extr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/baseline_game_reward_{player1_title}.pdf', bbox_inches='tight')

def plot_baseline_relative_moral_reward(player1_title, n_runs):
    '''plot moral reward - relatie cumulative (over time & bar plot) & per iteration
    - how well off did the players end up relative to each other in terms of moral reward?'''
    
    ##################################
    #### bar chart moral cumulative reward for player1_tytle vs others  ####
    ##################################
    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_AC_means = against_AC.mean()
    against_AC_sds = against_AC.std()
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_AD_means = against_AD.mean()
    against_AD_sds = against_AD.std()
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_TFT_means = against_TFT.mean()
    against_TFT_sds = against_TFT.std()
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_cumulative_reward_intrinsic.csv', index_col=0).iloc[-1]
    against_Random_means = against_Random.mean()
    against_Random_sds = against_Random.std()
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

    #import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(3, 3), dpi=80)
    plt.rcParams.update({'font.size':20})
    ax = fig.add_axes([0,0,1,1])
    labels = ['AC', 'AD', 'TFT', 'Rand.'] 
    means = [against_AC_means,against_AD_means,against_TFT_means,against_Random_means]
    cis = [against_AC_ci,against_AD_ci,against_TFT_ci,against_Random_ci]
    colors = ['lightgreen', 'crimson', 'gold', 'slategrey']  
    #add QLVM mixed agent 
    ax.bar(labels, means, yerr=cis, color=colors, width = 0.8) #capsize=7, 
    #plt.xticks(rotation=45)
    ax.set_ylabel(r'Cumulative $R_{intr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    #(f'R^{extr}_{i=QLUT}'# for {player1_title}')
    long_title = title_mapping[player1_title].replace('Ethics','').replace('_', '-')
    ax.set_title(long_title +' vs other \n') #'Cumulative Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    ax.set_xlabel('Opponent type')
    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 60000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 80000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([0, 100000])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-50000, 0]) #[-1300, 0]
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 10000])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 50000])
        elif player1_title == 'QLVM':
            plt.gca().set_ylim([0, 10000])
    plt.savefig(f'results/outcome_plots/reward/baseline_bar_cumulative_intrinsic_reward_{player1_title}.pdf', bbox_inches='tight')
    
    
    ##################################
    #### non-cumulative - game reward for player1_tytle vs others  ####
    ##################################
    figsize=(5, 4)

    against_AC = pd.read_csv(f'results/{player1_title}_AC/player1/df_reward_intrinsic.csv', index_col=0)
    against_AC_means = against_AC.mean(axis=1)
    against_AC_sds = against_AC.std(axis=1)
    against_AC_ci = 1.96 * against_AC_sds/np.sqrt(n_runs)

    against_AD = pd.read_csv(f'results/{player1_title}_AD/player1/df_reward_intrinsic.csv', index_col=0)
    against_AD_means = against_AD.mean(axis=1)
    against_AD_sds = against_AD.std(axis=1)
    against_AD_ci = 1.96 * against_AD_sds/np.sqrt(n_runs)

    against_TFT = pd.read_csv(f'results/{player1_title}_TFT/player1/df_reward_intrinsic.csv', index_col=0)
    against_TFT_means = against_TFT.mean(axis=1)
    against_TFT_sds = against_TFT.std(axis=1)
    against_TFT_ci = 1.96 * against_TFT_sds/np.sqrt(n_runs)

    against_Random = pd.read_csv(f'results/{player1_title}_Random/player1/df_reward_intrinsic.csv', index_col=0)
    against_Random_means = against_Random.mean(axis=1)
    against_Random_sds = against_Random.std(axis=1)
    against_Random_ci = 1.96 * against_Random_sds/np.sqrt(n_runs)

   

    plt.figure(dpi=80, figsize=figsize)
    plt.rcParams.update({'font.size':20})
    plt.plot(against_AC.index[:], against_AC_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_AC', color='lightgreen')
    plt.fill_between(against_AC.index[:], against_AC_means-against_AC_ci, against_AC_means+against_AC_ci, facecolor='lightgreen', alpha=0.5)
    plt.plot(against_AD.index[:], against_AD_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_AD', color='crimson')
    plt.fill_between(against_AD.index[:], against_AD_means-against_AD_ci, against_AD_means+against_AD_ci, facecolor='crimson', alpha=0.5)
    plt.plot(against_TFT.index[:], against_TFT_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_TFT', color='yellow')
    plt.fill_between(against_TFT.index[:], against_TFT_means-against_TFT_ci, against_TFT_means+against_TFT_ci, facecolor='yellow', alpha=0.5)
    plt.plot(against_Random.index[:], against_Random_means[:], lw=0.1, alpha=0.5, label=f'{player1_title}_Random', color='darkgrey')
    plt.fill_between(against_Random.index[:], against_Random_means-against_Random_ci, against_Random_means+against_Random_ci, facecolor='darkgrey', alpha=0.5)


    #long_title = title_mapping[player1_title]
    plt.title(long_title +' vs other \n') #r'Game Reward (Mean '+r'$\pm$ 95% CI over ' +str(n_runs)+' runs), '+'\n'+ 
    if game_title=='IPD':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 6])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='VOLUNTEER':
        if player1_title == 'QLUT':
            plt.gca().set_ylim([2, 8])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    elif game_title=='STAGHUNT': 
        if player1_title == 'QLUT':
            plt.gca().set_ylim([4, 10])
        elif player1_title == 'QLDE':
            plt.gca().set_ylim([-5, 0]) 
        elif player1_title == 'QLVE_e':
            plt.gca().set_ylim([0, 1])
        elif player1_title == 'QLVE_k':
            plt.gca().set_ylim([0, 5])
    plt.ylabel(r'$R_{intr}$ for '+str(player1_title).replace('QL','').replace('_e', r'$_e$').replace('_k', r'$_k$').replace('M', 'E'+r'$_m$'))
    plt.xlabel('Iteration')
    #plt.xticks(rotation=45)
    #leg = plt.legend() # get the legend object
    #for line in leg.get_lines(): # change the line width for the legend
    #    line.set_linewidth(4.0)
    plt.savefig(f'results/outcome_plots/reward/baseline_intrinsic_reward_{player1_title}.pdf', bbox_inches='tight')





############################################
#### set the right working directory for this game  ####
############################################
#os.getcwd()
os.chdir('..')
#'/Users/lizakarmannaya/RL/IPD'
#'/Users/lizakarmannaya/Documents/PhD_data/IPD'


#set directory according to the game 
game_title = 'IPD'

if game_title == 'IPD':
    #os.chdir('~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/PhD_data/IPD')
    os.chdir('IPD')
elif game_title == 'VOLUNTEER':
    #os.chdir('~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/PhD_data/VOLUNTEER')    
    os.chdir('VOLUNTEER')  
elif game_title == 'STAGHUNT':
    #os.chdir('~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents/PhD_data/STAGHUNT')    
    os.chdir('STAGHUNT')
print(os.getcwd())


############################################################################################
#### rename directories for each ecxperiment to get rid of 'eps' and 'epsdecay\ details ####
############################################################################################

for dirname in os.listdir('results'):
    if '_eps01.0_epsdecay' in dirname: 
        #get rid of formatting that reflects our parameter shoice 
        os.rename('results/'+dirname, 'results/'+dirname.replace('_eps01.0_epsdecay',''))



############################################
#### template for plotting all results for one pair of players ####
############################################

#plot reward & actions over time - manually put in destination_folder OR use loop below
#destination_folder = 'results/QLS_QLS'
destination_folder = 'results/QLVE_e_QLUT'

n_runs = 100
if 'QLVE' not in destination_folder.split('/')[1]:
    short_titles = destination_folder.split('/')[1].split('_')[0:2]
else: #manually split the 'QLVE_' types
    short_titles = destination_folder.split('/')[1][0:6], destination_folder.split('/')[1][7:]
long_titles = [title_mapping[title] for title in short_titles]

plot_results(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, game_title=game_title) 
#plot_actions(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
plot_action_pairs(destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
plot_action_types_area(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
plot_first_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
visualise_first_20_actions_matrix(destination_folder = destination_folder)
plot_last_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
visualise_last_20_actions_matrix(destination_folder = destination_folder)




############################################
#### plotting all results for pair of players in a loop ####
############################################

#plotting ony the pairs of actions - NB the 'plots' folder must already exist 
QLS_list = ['QLS_QLS', 'QLUT_QLS', 'QLDE_QLS', 'QLVE_e_QLS', 'QLVE_k_QLS']
QLmoral_QLmoral_list_1 = ['QLUT_QLUT', 'QLDE_QLUT', 'QLDE_QLDE', 'QLVE_e_QLUT']
QLmoral_QLmoral_list_2 =['QLVE_e_QLDE', 'QLVE_e_QLVE_e', 'QLVE_k_QLUT', 'QLVE_k_QLDE', 'QLVE_k_QLVE_e', 'QLVE_k_QLVE_k']
static_list = ['QLS_AC', 'QLS_AD', 'QLS_TFT', 'QLS_Random', 'QLUT_AC', 'QLUT_AD', 'QLUT_TFT', 'QLUT_Random', 'QLDE_AC', 'QLDE_AD', 'QLDE_TFT', 'QLDE_Random', 'QLVE_e_AC', 'QLVE_e_AD', 'QLVE_e_TFT', 'QLVE_e_Random', 'QLVE_k_AC', 'QLVE_k_AD', 'QLVE_k_TFT', 'QLVE_k_Random']

QLS_list = ['results/'+i for i in QLS_list]
QLmoral_QLmoral_list_1 = ['results/'+i for i in QLmoral_QLmoral_list_1]
QLmoral_QLmoral_list_2 = ['results/'+i for i in QLmoral_QLmoral_list_2]
static_list = ['results/'+i for i in static_list]


n_runs = 100
for destination_folder in static_list: #paste all 4 lists here one by one
    if 'QLVE' not in destination_folder.split('/')[1]:
        short_titles = destination_folder.split('/')[1].split('_')[0:2]
    else: #manually split the 'QLVE_' types
        short_titles = destination_folder.split('/')[1][0:6], destination_folder.split('/')[1][7:]
    long_titles = [title_mapping[title] for title in short_titles]
    print('plotting results for: ', long_titles)
    plot_action_pairs(destination_folder=destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
    
    plot_results(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, game_title=game_title) 
    plot_actions(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
    plot_action_types_area(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    plot_first_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    visualise_first_20_actions_matrix(destination_folder = destination_folder)
    plot_last_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    visualise_last_20_actions_matrix(destination_folder = destination_folder)



############################################
#### plotting all individual results for mixed moral player (QLVM) ####
############################################

#testing
#destination_folder = 'results/QLVM_QLS'
#n_runs = 100
#short_titles = ['QLVM', 'QLS']
#long_titles = [title_mapping[title] for title in short_titles]
#plot_results(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, game_title=game_title) 

QLVM_list = ['QLVM_QLS', 'QLVM_QLUT', 'QLVM_QLDE', 'QLVM_QLVE_e', 'QLVM_QLVE_k', 'QLVM_QLVM']
QLVM_static_list = ['QLVM_AC', 'QLVM_AD', 'QLVM_TFT', 'QLVM_Random']

QLVM_list = ['results/'+i for i in QLVM_list]
QLVM_static_list = ['results/'+i for i in QLVM_static_list]

for destination_folder in QLVM_static_list:
    if 'QLVE' not in destination_folder.split('/')[1]:
        short_titles = destination_folder.split('/')[1].split('_')[0:2]
    else: #manually split the 'QLVE_' types
        short_titles = destination_folder.split('/')[1][0:4], destination_folder.split('/')[1][5:] #NOTE indices here are different to those in the loop plotting main results! 
    long_titles = [title_mapping[title] for title in short_titles]

    plot_action_pairs(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
    
    plot_results(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, game_title=game_title) 
    plot_actions(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs)
    plot_action_types_area(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    plot_first_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    visualise_first_20_actions_matrix(destination_folder = destination_folder)
    plot_last_20_actions(destination_folder = destination_folder, player1_title = short_titles[0], player2_title = short_titles[1], n_runs=n_runs)
    visualise_last_20_actions_matrix(destination_folder = destination_folder)





############################################
#### template for plotting learning progress (Q-Values) for one pair of players, given n_runs (100 too many to plot) ####
############################################
#use destnation_folder etc. from above
Q_VALUES_player1 = np.load(f'{destination_folder}/Q_VALUES_player1_list.npy', allow_pickle=True)
for run_idx in range(1):
    plot_one_run_Q_values(Q_values_list = Q_VALUES_player1, run_idx = run_idx)


Q_VALUES_player2 = np.load(f'{destination_folder}/Q_VALUES_player2_list.npy', allow_pickle=True)
for run_idx in range(1):
    plot_one_run_Q_values(Q_values_list = Q_VALUES_player2, run_idx = run_idx)





############################################
#### template for plotting relative outcomes for one player type vs. other learning players ####
############################################

player1_title = 'QLVM'
n_runs = 100

#plot cumulative reward for various pairs in one graph
plot_relative_reward(player1_title=player1_title, n_runs=n_runs)
plot_relative_moral_reward(player1_title=player1_title, n_runs=n_runs) 
#plot_cumulative_reward(player1_title=player1_title, n_runs=n_runs)

#plot types of nmutual actions between this player & other oppponent types 
plot_relative_action_pairs(player1_title, n_runs) #NOT USED IN THE PAPER 

#plot % cooperating in every pair - NOTE not used in paper
plot_relative_cooperation(player1_title=player1_title, n_runs=n_runs) 

#### plot collective reward for various pairs one one graph, to compare relative outcomes
plot_relative_outcomes(type='collective', player1_title=player1_title, n_runs=n_runs, game_title=game_title) 
plot_relative_outcomes(type='gini', player1_title=player1_title, n_runs=n_runs, game_title=game_title)
plot_relative_outcomes(type='min', player1_title=player1_title, n_runs=n_runs, game_title=game_title)







############################################
#### template for plotting baseline relative outcomes for one player type vs. other static players ####
############################################
#NOTE this was not done!!! (NEED TO UPDATE FUNCTIONS BEFORE RUNNING) 

plot_baseline_relative_outcomes(type='collective', player1_title=player1_title, n_runs=n_runs, game_title=game_title) 
plot_baseline_relative_outcomes(type='gini', player1_title=player1_title, n_runs=n_runs, game_title=game_title)
plot_baseline_relative_outcomes(type='min', player1_title=player1_title, n_runs=n_runs, game_title=game_title)

plot_baseline_relative_reward(player1_title=player1_title, n_runs=n_runs)
plot_baseline_relative_moral_reward(player1_title=player1_title, n_runs=n_runs)




plot_baseline_cumulative_reward(player1_title=player1_title, n_runs=n_runs)

plot_basleline_relative_cooperation(player1_title=player1_title, n_runs=n_runs)

plot_relative_baseline_action_pairs(player1_title, n_runs)


plot_stacked_relative_reward(n_runs)
plot_stacked_relative_moral_reward(n_runs)


############################################
#### do last! plotting simultaneous action pairs ####
############################################

n_runs = 100

plot_matrix_action_pairs(n_runs)
plot_baseline_matrix_action_pairs(n_runs)

plot_matrix_social_outcomes(n_runs)
plot_baseline_matrix_social_outcomes(n_runs)




########################################################################################
#### extra - analysis of the effect of beta in the QLVM (CVirtue-mixed) agent ####
########################################################################################

#set directory according to the game 
game_title = 'STAGHUNT'
#os.chdir('PhD_data')
#os.chdir('../..')
if game_title == 'IPD':
    os.chdir('EXTRA_results_QLVM_diffbeta/IPD')
elif game_title == 'VOLUNTEER':
    os.chdir('EXTRA_results_QLVM_diffbeta/VOLUNTEER')  
elif game_title == 'STAGHUNT':
    os.chdir('EXTRA_results_QLVM_diffbeta/STAGHUNT')
print(os.getcwd())



#define lists of players:

#extra_list = ['QLVM_AD_eps01.0_epsdecay', 'QLVM_AD_eps01.0_epsdecay_beta0.2', 'QLVM_AD_eps01.0_epsdecay_beta0.4', 'QLVM_AD_eps01.0_epsdecay_beta0.6', 'QLVM_AD_eps01.0_epsdecay_beta0.8', 'QLVM_AD_eps01.0_epsdecay_beta1.0']
extra_list = ['QLVM_QLS_eps01.0_epsdecay', 'QLVM_QLS_eps01.0_epsdecay_beta0.2', 'QLVM_QLS_eps01.0_epsdecay_beta0.4', 'QLVM_QLS_eps01.0_epsdecay_beta0.6', 'QLVM_QLS_eps01.0_epsdecay_beta0.8', 'QLVM_QLS_eps01.0_epsdecay_beta1.0']

n_runs = 100
for destination_folder in extra_list: #paste all 4 lists here one by one
    #short_titles = 'QLVM', 'AD'
    short_titles = 'QLVM', 'QLS'
    long_titles = [title_mapping[title] for title in short_titles]
    try:
        option = destination_folder.split('_')[4]
    except: 
        option = '_beta0'
    print('plotting results for: ', long_titles, option)
    plot_action_pairs(destination_folder=destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, option=option)


########################################################################################
#### extra - analysis of the effect os smaller eps and no decay on the learning of agents ####
########################################################################################

os.chdir('EXTRA_results_IPD_eps0.05')
os.getcwd()
n_runs = 100
folders = ['QLS_QLS', 'QLUT_QLUT', 'QLDE_QLDE', 'QLVE_e_QLVE_e', 'QLVE_k_QLVE_k']
for destination_folder in folders: 
    if 'QLVE' not in destination_folder:
        short_titles = destination_folder.split('_')[0:2]
    else: #manually split the 'QLVE_' types
        short_titles = destination_folder[0:6], destination_folder[7:]
    long_titles = [title_mapping[title] for title in short_titles]
    print('plotting results for: ', long_titles)

    plot_action_pairs(destination_folder=destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, option='eps0.05')






########################################################################################
#### extra - analysis of the effect of longer training on Virtue-equality's learning ####
########################################################################################


n_runs = 100

destination_folder = 'results/QLVE_e_QLUT_iter20000_eps01.0_epsdecay'
destination_folder = 'results/QLVE_e_QLDE_iter20000_eps01.0_epsdecay'
destination_folder = 'results/QLVE_e_QLVE_e_iter20000_eps01.0_epsdecay'
destination_folder = 'results/QLVE_e_QLVE_k_iter20000_eps01.0_epsdecay'
destination_folder = 'results/QLVE_e_QLVE_m_iter20000_eps01.0_epsdecay'

#manually split the 'QLVE_' types
short_titles = destination_folder.split('/')[1][0:6], destination_folder.split('/')[1][7:11]
long_titles = [title_mapping[title] for title in short_titles]
print('plotting results for: ', long_titles)

plot_action_pairs_20K(destination_folder=destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, option='eps0.05')
#save plot manually in this case 











#### TESTING new indexing in Q-value updates ####
#run these lines in the shell 
#python3 main.py --title1 QLS --title2 QLS --num_runs 10 --extra old_code
#python3 main.py --title1 QLS --title2 QLS --num_runs 10 --extra new_code_indexing
#python3 main.py --title1 QLS --title2 QLS --num_runs 100 --extra new_code_indexing

destination_folder = 'results/QLS_QLS_runs10_old_code'
destination_folder = 'results/QLS_QLS_runs10_new_code_indexing'
destination_folder = 'results/QLS_QLS_runs100_new_code_indexing'

game_title='IPD'
n_runs = 100
short_titles = destination_folder.split('/')[1].split('_')[0:2]
long_titles = [title_mapping[title] for title in short_titles]
plot_results(destination_folder = destination_folder, player1_title=long_titles[0], player2_title=long_titles[1], n_runs=n_runs, game_title=game_title) 
