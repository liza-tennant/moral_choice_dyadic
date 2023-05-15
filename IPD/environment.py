import numpy as np 

class Game_for_learning:
    '''This is the environment used by the two agents during learning 
    - the game that they play, Iterated Prisoners Dilemma. 
    It takes in states, allows each player to take an action (in the 'step' function) 
    and returns payoffs & next state'''
    
    def __init__(self, player1, player2, payoffmat, n_games):
        self.player1 = player1
        self.player2 = player2
        self.players = [ player1, player2 ]
        self.payoffmat = payoffmat
        self.history = list() #TO DO make this a circular array / queue instead 
        self.opponents = {player1:player2, player2:player1}
        self.state_index_converter = {(0,0):0, (0,1):1, (1,0):2, (1,1):3}
    
    def reset(self): 
        pass #TO DO if reset_learning_parameters is not enough... 


    #def run(self, game_iter=1): #game_iter=n_games
    #    #NOTE this function is not currently used
    #    # unpack the two players
    #    player1, player2 = self.players
    #    # each iteration, get new moves and append these to history
    #    for iteration in range(game_iter):
    #        #request move from player - use methods from the Player object
    #        newmoves = player1.make_fixed_move(self), player2.make_fixed_move(self) 
    #        self.history.append(newmoves) #append pair of moves to the history attritbute of this game 
    #    # prompt players to record the game played (i.e., 'self') - ???? 
    #    player1.record(self); player2.record(self) #use methods from the Player object
    

    def game_reward(self, m1, m2): #this is the EXTRINSIC REWARD from the game environment
        pay1, pay2 = self.payoffmat[m1][m2][0], self.payoffmat[m1][m2][1]
        #payoffs = (self.payoffmat[m1][m2]) 
        #pay1 = payoffs[0]
        #pay2 = payoffs[1]
        # return a mapping of each player index to its payoff
        return [pay1, pay2]
    
    
    def collective_reward(self, m1, m2): #this is a copy of the utilitarian reward         
        pay1, pay2 = self.payoffmat[m1][m2][0], self.payoffmat[m1][m2][1]
        pay_final = pay1 + pay2
        return pay_final

    def reward_ratio(self, m1, m2): #this is a copy of the virtue reward 
        pay1, pay2 = self.payoffmat[m1][m2][0], self.payoffmat[m1][m2][1]
        pay_final = (min(pay1, pay2) +1) / (max(pay1, pay2) +1)
        return pay_final
    
    def reward_gini(self, m1, m2):
        pay1, pay2 = self.payoffmat[m1][m2][0], self.payoffmat[m1][m2][1]
        pay_final = 1 - ((abs(pay1 - pay2)) / (pay1 + pay2))
        return pay_final

    def reward_min(self, m1, m2): 
        pay1, pay2 = self.payoffmat[m1][m2][0], self.payoffmat[m1][m2][1]
        pay_final = min(pay1, pay2)
        return pay_final
    
    
    def step(self, state_player1, state_player2, iteration, global_history, num_iter, RNG):
        '''function for the two learning agents to interact with the environment simultaneously (i.e. play the game).
        For each player, it takes a state as input and:
        - generates an action (based on exploration_policy),
        - computes reward (game (extrinsic), intrinsic (moral), total, collective)
        - computes a next state.
        
        The function returns the two axctions, two s', game, total and global rewards.
        Apart from returning these variables, it also updates the global_history object (defined outside this class) with more detailed results.'''

        #generate 2*4 random numbers, then use whichever is needed. Generate all of them to make sure we go through the RN list consistently 
        player1_RN_1 = RNG.player1_streams[0].uniform(0,1) #random move when Q-table is empty
        player2_RN_1 = RNG.player2_streams[0].uniform(0,1) #random move when Q-table is empty
        player1_RN_2 = RNG.player1_streams[1].uniform(0,1) #probability to compare against eps
        player2_RN_2 = RNG.player2_streams[1].uniform(0,1) #probability to compare against eps
        player1_RN_3 = RNG.player1_streams[2].uniform(0,1) #random move due to eps
        player2_RN_3 = RNG.player2_streams[2].uniform(0,1) #random move due to eps
        #there is also a 4th random number, used to generate move for a static agent with strategy==’random’, and a 5th random number -  used to generate the intial state within the main script

        state_index_player1 = self.state_index_converter[state_player1]
        state_index_player2 = self.state_index_converter[state_player2]

        action_player1, eps_player1, reason_player1, RNs_player1 = self.player1.make_exploratory_move(state_index = state_index_player1, iteration=iteration, num_iter=num_iter, RNs=np.array([player1_RN_1, player1_RN_2, player1_RN_3], dtype=object))
        action_player2, eps_player2, reason_player2, RNs_player2 = self.player2.make_exploratory_move(state_index = state_index_player2, iteration=iteration, num_iter=num_iter, RNs=np.array([player2_RN_1, player2_RN_2, player2_RN_3], dtype=object))

        #save the key information as next_state for each agent - of shape (action_opponent, action_own)
        next_state_player1 = (action_player2, action_player1)
        next_state_player2 = (action_player1, action_player2)


        #calculate reward - extrinsic (from the game scores), intrinsic (based on moral rule of the player), collective
        reward_game_player1 = self.game_reward(m1=action_player1, m2=action_player2)[0]
        reward_game_player2 = self.game_reward(m1=action_player2, m2=action_player1)[0]

        reward_intrinsic_player1 = self.player1.intrinsic_reward(self, m1=action_player1, m2=action_player2, state=state_player1)
        reward_intrinsic_player2 = self.player2.intrinsic_reward(self, m1=action_player2, m2=action_player1, state=state_player2)

        reward_collective = self.collective_reward(m1=action_player1, m2=action_player2)
        reward_ratio = self.reward_ratio(m1=action_player1, m2=action_player2) 
        reward_gini = self.reward_gini(m1=action_player1, m2=action_player2)
        reward_min = self.reward_min(m1=action_player1, m2=action_player2) 


        #append values to the history dataframe - used for plotting later 
        global_history.loc[iteration, ['state_player1', 'action_player1', 'state_player2', 'action_player2']] = [
            state_player1, action_player1, state_player2, action_player2]

        global_history.loc[iteration, ['reward_game_player1', 'next_state_player1', 'reward_game_player2', 'next_state_player2']] = [
            reward_game_player1, next_state_player1, reward_game_player2, next_state_player2]

        global_history.loc[iteration, ['reward_intrinsic_player1', 'reward_intrinsic_player2', 'reward_collective', 'reward_ratio', 'reward_gini', 'reward_min']] = [
            reward_intrinsic_player1, reward_intrinsic_player2, reward_collective, reward_ratio, reward_gini, reward_min]

        global_history.loc[iteration, ['eps_player1', 'eps_player2', 'reason_player1', 'reason_player2']] = [
            eps_player1, eps_player2, reason_player1, reason_player2]
        
        global_history.loc[iteration, ['RNs_player1', 'RNs_player2']] = [
            str(RNs_player1), str(RNs_player2)]

        #determine which reward the player will be learning from based on their moral type:
        reward_learning_player1 = 0 #initialise
        reward_learning_player2 = 0

        if self.player1.moral_type == None: 
            reward_learning_player1 = reward_game_player1
        else: #if moral_type=='Utilitarian' or 'Deontological' or 'VirtueEthics': 
            reward_learning_player1 = reward_intrinsic_player1
        
        if self.player2.moral_type == None: 
            reward_learning_player2 = reward_game_player2
        else: #if moral_type=='Utilitarian' or 'Deontological' or 'VirtueEthics': 
            reward_learning_player2 = reward_intrinsic_player2


        global_history.loc[iteration, ['reward_learning_player1', 'reward_learning_player2']] = [
            reward_learning_player1, reward_learning_player2] 

        #if need to debug - print action, next_state and rewards here        
        #print('One step done')
        
        return int(action_player1), int(action_player2), next_state_player1, next_state_player2, reward_learning_player1, reward_learning_player2


    def step_static(self, state_player1, state_player2, iteration, global_history, RNG):
        '''function for  two static agents to interact with the environment simultaneously (i.e. play the game).
        Here state = single last move of the opponent.'''
        #generate 2*4 random numbers, then use whichever is needed. Generate all of them to make sure we go through the RN list consistently 
        #RN_1 to RN_3 not used by player1 or player2 
        player1_RN_4 = RNG.player1_streams[3].uniform(0,1) #move for a static agent with strategy==’random’
        player2_RN_4 = RNG.player2_streams[3].uniform(0,1) #move for a static agent with strategy==’random’

        action_player1 = self.player1.make_fixed_move(state=state_player1, playerx_RN_4=player1_RN_4)
        action_player2 = self.player2.make_fixed_move(state=state_player2, playerx_RN_4=player2_RN_4)

        #save the key information as next_state for each agent #NOTE we record state with opponent's move first, then own movement
        next_state_player1 = (action_player2, action_player1)
        next_state_player2 = (action_player1, action_player2)

        #calculate reward - extrinsic (from the game scores), collective
        reward_game_player1 = self.game_reward(m1=action_player1, m2=action_player2)[0]
        reward_game_player2 = self.game_reward(m1=action_player2, m2=action_player1)[0]

        reward_collective = self.collective_reward(m1=action_player1, m2=action_player2)
        reward_ratio = self.reward_ratio(m1=action_player1, m2=action_player2) 
        reward_gini = self.reward_gini(m1=action_player1, m2=action_player2)
        reward_min = self.reward_min(m1=action_player1, m2=action_player2) 

        #append values to the history dataframe - used for plotting later 
        global_history.loc[iteration, ['state_player1', 'action_player1', 'state_player2', 'action_player2']] = [
            state_player1, action_player1, state_player2, action_player2]

        global_history.loc[iteration, ['reward_game_player1', 'next_state_player1', 'reward_game_player2', 'next_state_player2']] = [
            reward_game_player1, next_state_player1, reward_game_player2, next_state_player2]

        global_history.loc[iteration, ['reward_collective', 'reward_ratio', 'reward_gini', 'reward_min']] = [
            reward_collective, reward_ratio, reward_gini, reward_min]
      
        #if need to debug - print action, next_state and rewards here        
        #print('One step done')        
        return next_state_player1, next_state_player2 #reward_game_player1, reward_game_player2, reward_collective

    

    def step_mixed(self, state_player1, state_player2, iteration, global_history, num_iter, RNG): #myVars
        '''function for the two learning agents to interact with the environment simultaneously (i.e. play the game).
        For each player, it takes a state as input and:
        - generates an action (based on exploration_policy),
        - computes reward (game (extrinsic), intrinsic (moral - only for player1), total, collective)
        - computes a next state.
        
        The function returns the two actions, two s', game, total and global rewards.
        Apart from returning these variables, it also updates the global_history object (defined outside this class) with more detailed results.'''

        #generate 2*4 random numbers, then use whichever is needed. Generate all of them to make sure we go through the RN list consistently 
        #only using some of the RNs generated, since one of the players is static
        player1_RN_1 = RNG.player1_streams[0].uniform(0,1) #random move when Q-table is empty
        player1_RN_2 = RNG.player1_streams[1].uniform(0,1) #probability to compare against eps
        player1_RN_3 = RNG.player1_streams[2].uniform(0,1) #random move due to eps
        player2_RN_4 = RNG.player2_streams[3].uniform(0,1) #move for a static agent with strategy==’random’

        state_index_player1 = self.state_index_converter[state_player1]
        
        action_player1, eps_player1, reason_player1, RNs_player1 = self.player1.make_exploratory_move(state_index = state_index_player1, iteration=iteration, num_iter=num_iter, RNs=(player1_RN_1, player1_RN_2, player1_RN_3))
        action_player2 = self.player2.make_fixed_move(state=state_player2, playerx_RN_4=player2_RN_4)

        #save the key information as next_state for each agent #NOTE we record state with opponent's move first, then own movement
        next_state_player1 = (action_player2, action_player1)
        next_state_player2 = (action_player1, action_player2) #note this does not really get used as player2 is static 

        #calculate reward - extrinsic (from the game scores), intrinsic (based on moral rule of the player), collective
        reward_game_player1 = self.game_reward(m1=action_player1, m2=action_player2)[0]
        reward_game_player2 = self.game_reward(m1=action_player2, m2=action_player1)[0]

        reward_intrinsic_player1 = self.player1.intrinsic_reward(self, m1=action_player1, m2=action_player2, state=state_player1)

        reward_collective = self.collective_reward(m1=action_player1, m2=action_player2)
        reward_ratio = self.reward_ratio(m1=action_player1, m2=action_player2) 
        reward_gini = self.reward_gini(m1=action_player1, m2=action_player2)
        reward_min = self.reward_min(m1=action_player1, m2=action_player2) 

        #append values to the history dataframe - used for plotting later 
        global_history.loc[iteration, ['state_player1', 'action_player1', 'state_player2', 'action_player2']] = [
            state_player1, action_player1, state_player2, action_player2]

        global_history.loc[iteration, ['reward_game_player1', 'next_state_player1', 'reward_game_player2', 'next_state_player2']] = [
            reward_game_player1, next_state_player1, reward_game_player2, next_state_player2]

        global_history.loc[iteration, ['reward_intrinsic_player1', 'reward_collective', 'reward_ratio', 'reward_gini', 'reward_min']] = [
            reward_intrinsic_player1, reward_collective, reward_ratio, reward_gini, reward_min]

        global_history.loc[iteration, ['eps_player1', 'reason_player1', 'RNs_player1']] = [
            eps_player1, reason_player1, str(RNs_player1)]
            #NOTE if we do not use str() here, this throws and error about creating np arrray from ragged nested sequences - ignore for now

        #determine which reward the player will be learning from based on their moral type:
        reward_learning_player1 = 0 #initialise

        if self.player1.moral_type == None: 
            reward_learning_player1 = reward_game_player1
        else: #if moral_type=='Utilitarian' or 'Deontological' or 'VirtueEthics': 
            reward_learning_player1 = reward_intrinsic_player1
        #if need to debug - print action, next_state and rewards here        
        #print('One step done')

        global_history.loc[iteration, ['reward_learning_player1']] = [reward_learning_player1] 

        
        return int(action_player1), next_state_player1, next_state_player2, reward_learning_player1

