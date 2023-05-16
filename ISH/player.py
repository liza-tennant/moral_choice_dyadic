from explorationpolicy import ExplorationPolicy
import random 
import numpy as np 
from datetime import datetime

class Player:
    def __init__(self, strategy, eps0, epsdecay, moral_type = None, mixed_beta = None): 
        self.initial_move = False #cooperate on the first move if strategy == TitforTat or Q-Learning        
        self.reset() #defined below
        self.strategy = strategy
        self.moral_type = moral_type
        self.Q_values = None
        self.eps0 = eps0
        self.epsdecay = epsdecay
        self.mixed_beta = mixed_beta #will only be used for QLVM agent 
        
    def reset(self): 
        ''' assign empty lists to the player's games_played and players_played attributes. These attributes can 
        provide a player with “memory”, which can be augmented each time the player's record method is called.'''
        self.games_played = list()   #empty list
        self.players_played = list()  #empty list
    
    def get_last_move(self, game, global_history): #NOT NEEDED
        ''' get opponent and learn their last move ''' #NOTE not used as we feed this to the function explicitly as 'state' 
        opponent = game.opponents[self]
        opponent_idx = game.players.index(opponent)
        last_move = global_history[f'action_player{opponent_idx}'][-1] 
        #will return None if there is no move
        print('last_move: ', last_move)
        return last_move

    def make_exploratory_move(self, state_index, iteration, num_iter, RNs): #myVars
        '''this function is used in the online learning setting - when the player is making a move according to an ExplorationPolicy'''
        my_expl_policy = ExplorationPolicy(state_index=state_index, policy_type='eps_greedy', QV=self.Q_values, RNs=RNs) #myVars=myVars, 
        move, eps, reason = my_expl_policy.use_policy(iteration=iteration, total_iterations=num_iter, eps0=self.eps0, epsdecay=self.epsdecay)
        #NOTE set total_episodes here according to each experiment - manually for now
        return int(bool(move)), eps, reason, RNs
    
    def make_own_move(self, state, playerx_RN_4):
        '''this function can be used to play a fixed strategy - not exploring'''
        'TO DO finish fixing this - rename Q_values !!! '
        if self.strategy == 'random':
            return int(playerx_RN_4 < 0.5)
        
        else:  
            if self.strategy == 'TitForTat': 
                '''respond to opponent's last move using a reactive strategy based on 1 last move of the opponent'''
                #react to last move - NOTE currently we assume a state will always be given 
                #if state is None: #if this is the initial move
                #    return int(self.initial_move) #TO DO check that we are not duplicating initial_move in other functions 
                #else:
                return int(bool(state[0])) #take the first element of the state, i.e. the opponent's previous move
        
            elif self.strategy == 'AlwaysCooperate':
                return int(False)
            
            elif self.strategy == 'AlwaysDefect':
                return int(True)
        
            #elif self.strategy == 'Q-Learning greedy': #NOTE this is not currently used #NOTE TO DO re-write using player1.Q_values
            #    if state is None: #if this is the initial move
            #        return int(self.initial_move)
            #    else:
            #        myStr = f'Q_values_player{player_index}'
            #        #myVars = vars() #this will be defined outside the objects & functions instead 
            #        Q_values_variable = myVars[myStr] #NOTE this will currently not work 
            #        
            #        #move optimally based on current Q-value estimates 
            #        optimal_policy = list(np.argmax(Q_values_variable, axis=1)) 
            #        return int(bool(optimal_policy[state]))    
            
    def record(self, game):
        self.games_played.append(game) #NOT USED
        opponent = game.opponents[self]
        self.players_played.append(opponent) #NOT USED
        
    def intrinsic_reward(self, game, m1, m2, state):
        #create the baseline individual payoffs, as defined in the IPD game
        payoffs = (game.payoffmat[m1][m2]) 

        # transpose to get a payoff sequence for each player
        #pay1, pay2 = transpose(payoffs) # ????
        
        #extract integers from the tuple with payoffs
        pay1 = payoffs[0]
        pay2 = payoffs[1]

        k = 5 #the constant that defines het reward & punishment values for norm-based agents 
        
        #then add to or subtract from this payoff to follow the moral rule 
        if self.moral_type == 'Utilitarian':
            pay1_intrinsic = pay1 + pay2 #add Utilitarian element (externally)
            
        elif self.moral_type == 'Deontological':
            #check if I followed the norm conditional cooperation
            #TO DO make this extrinsic reward instead 
            if state[0] == 0: 
                if m1 == 1: #if I (player1) defected against a cooperator (based on 1 previous move of the opponent) 
                    pay1_intrinsic = -k
                else: 
                    pay1_intrinsic = 0
            else: 
                pay1_intrinsic = 0

            
            #check if player followed the external norm reciprocity - give what you receive
            #if yes - reward = +5, otherwise reward = -5 
            #if m1 == state: #if I reciprocated/copied my opponent's previous move
            #    pay1_intrinsic = 5
            #else:
            #    pay1_intrinsic=-5
            #TO DO - see Nicolas's 2nd paper; see Ernst Fehr (norms) 
        
        elif self.moral_type == 'VirtueEthics_equality':
            #pay1_intrinsic = (min(pay1, pay2) +1) / (max(pay1, pay2) +1)
            pay1_intrinsic = 1 - ((abs(pay1 - pay2)) / (pay1 + pay2)) #a simplification of the Gini coefficient for 2 players


        elif self.moral_type == 'VirtueEthics_kindness':
            if m1 == False: #if this agent cooperated
                pay1_intrinsic = k
            else: 
                pay1_intrinsic = 0

        elif self.moral_type == 'VirtueEthics_mixed':
            mixed_beta = int(self.mixed_beta)
            k_normalised = k/k
            if m1 == False: #if this agent cooperated
                pay1_intrinsic = mixed_beta * (1 - ((abs(pay1 - pay2)) / (pay1 + pay2))) + (1-mixed_beta) * k_normalised 
            else: 
                pay1_intrinsic = mixed_beta * (1 - ((abs(pay1 - pay2)) / (pay1 + pay2))) 

# TO DO - Rescale rewards to all be on the same scale 

        elif self.moral_type == None: 
            pay1_intrinsic = 0
#           pay2_intrinsic = 0
        #NOTE currently if the agent is selfish we record reward_intrinsic as = reward_game. Perhaps these should be kept separate?
        #TO DO separate this from intrinsic reward and rewrite the learning to be from one of the two rewards, not always intrinsic
            
        # return a mapping of each player index to its payoff
#       return [pay1_intrinsic, pay2_intrinsic]
        return pay1_intrinsic

        
    def total_reward(self, game, m1, m2):
        return 0 #TO DO - implement set of weights alpha & beta on entrinsic vs intrinsic reward 

