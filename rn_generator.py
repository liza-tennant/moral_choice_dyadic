from numpy.random import SeedSequence, default_rng
import os 

class my_RN_generator: 
    '''this class takes in a single master_seed (defined before each set of runs) and creates:
    - 2 streams of numbers for players 1&2, 
    - then, for each player, 5 streams of numbers to be used in the experiments'''

    def __init__(self, master_seed):
        self.master_seed = master_seed
        self.player1_streams = None 
        self.player2_streams = None 


    def generate(self, destination_folder):
        ss = SeedSequence(self.master_seed)

        # Spawn off 2 child SeedSequences (2 players) to pass to grandchild/child processes.
        child_seeds = ss.spawn(2) 

        #save child seeds to file for future reference
        if not os.path.isdir(str(destination_folder)):
            os.makedirs(str(destination_folder))

        with open(f'{destination_folder}/child_seeds.txt', 'w') as fp:
            for item in child_seeds:
                fp.write("%s\n" % str(item)) # write each item on a new line
            print('saved child_seeds for players 1 and 2')

        #generate four streams of numbers for each of the two players
        grandchildren_player1 = child_seeds[0].spawn(5)
        player1_streams = [default_rng(s) for s in grandchildren_player1]
        self.player1_streams = player1_streams

        grandchildren_player2 = child_seeds[1].spawn(5)
        player2_streams = [default_rng(s) for s in grandchildren_player2]
        self.player2_streams = player2_streams



