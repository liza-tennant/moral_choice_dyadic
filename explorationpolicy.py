import numpy as np 

class ExplorationPolicy:   
    def __init__(self, state_index, policy_type, QV, RNs): 
        self.state_index = state_index
        self.policy_type = policy_type
        self.RNs = RNs
        self.QV = QV

    def use_policy(self, iteration, total_iterations, eps0, epsdecay):

        if self.policy_type == 'eps_greedy': 
            '''eps-greedy exploration policy - to be used in taking actions during learning'''
            prob = self.RNs[1]
            if not epsdecay: 
                eps = eps0 #try 0.05 #0.01 #0.001 
            else: # if I need to implement eps_decay and eps0 has been pre-defined
                eps_initial = eps0
                eps_final = 0
                r = max((int(total_iterations)-int(iteration))/int(total_iterations), 0)
                eps = (eps_initial - eps_final)*r + eps_final

            if prob <= eps: 
                #make a random move with probability eps 
                reason = 'random, due to eps'
                return int(self.RNs[2] < 0.5), eps, reason
            else:             
                #move optimally based on current Q-value estimates, if they are not empty 
                if not np.any(self.QV[self.state_index]): #if Q-values for this state are empty
                    reason = 'random, due to empty Q-values'
                    return int(self.RNs[0] < 0.5), eps, reason #make a random move
                else: 
                    optimal_policy = np.argmax(self.QV, axis=1) #list(np.argmax(self.QV, axis=1))
                    reason = 'greedy, according to learnt Q-values'
                    return int(bool(optimal_policy[self.state_index])), eps, reason

        #'''random exploration policy '''
        #if self.policy_type == 'random':
                #return np.random.choice(possible_actions[state])



