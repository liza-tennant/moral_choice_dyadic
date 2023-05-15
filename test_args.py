import argparse

parser = argparse.ArgumentParser(description='Process two player titles (3 letters) from user string input.')
parser.add_argument('--title1', type=str, required=True,
                    help='the title for player1')
parser.add_argument('--title2', type=str, required=True,
                    help='the title for player2')

args = parser.parse_args()
print(args.title1, args.title2)
#print(args.accumulate(args.integers))







########################################
#### try to measure RAM required for one expriment #####################
#### NB this requires all packages & functions from the main.py script ####
########################################



#from pympler import asizeof
#obj = [1, 2, (3, 4), 'text']
#asizeof.asizeof(run_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2))
#print(asizeof.asized(obj, detail=1).format())


from pympler import tracker
summary_tracker = tracker.SummaryTracker()
#summary_tracker.print_diff()

s0 = summary_tracker.create_summary()

#### QLS vs QLS, 1 episodes
master_seed = 1
num_iterations = 10000
num_runs = 100
destination_folder = 'results_QLS_QLS_4states_tightpayoffs_100runs'
title1 = 'QLS'
title2 = 'QLS'

run_and_save(master_seed, num_runs, num_iterations, destination_folder, title1, title2)

import os, psutil
#print how many MB my process takes
print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

s1 = summary_tracker.create_summary()

summary_tracker.print_diff(summary1=s0, summary2=s1)