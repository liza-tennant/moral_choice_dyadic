#### NB using python version 3.7.4 on laptop (on the shell, I installed 3.8.0)

#### UPLOAD FILES TO SERVER - does not work####
#rsync -azv --stats --progress -e 'ssh -A -J lkarmann@tails.cs.ucl.ac.uk' /RL/IPD lkarmann@engima.cs.ucl.ac.uk:/remote/experiment_data/IPD
#rsync -azv --stats --progress -e 'ssh -A -J lkarmann@tails.cs.ucl.ac.uk' ~/RL/IPD lkarmann@tails.cs.ucl.ac.uk:/my_env/experiment_data/IPD
#### DOWNLOAD FILES TO LAPTOP - not tried ####
#rsync -azv --stats --progress -e 'ssh -A -J lkarmann@tails.cs.ucl.ac.uk' lkarmann@enigma.cs.ucl.ac.uk:/remote/experiment_data/IPD/resuls /RL/IPD/results


#### RUN ON COMMAND LINE, before launching the bash script ####
ssh -t lkarmann@tails.cs.ucl.ac.uk ssh -t geogcpu3.cs.ucl.ac.uk 
htop 
tmux new -s phase1
#### TO RETURN TO PREVIOUS TMUX SESSION ####
tmux attach –t phase1
#### TO KILL SESSION ####
tmux kill-session -t phase1 

ssh -t lkarmann@tails.cs.ucl.ac.uk ssh -t pb-214172.cs.ucl.ac.uk  


bash

#### CREATE VENV ####
#python3.8 -m venv my_env

#### ACTIVATE VENV ####
cd my_env
source bin/activate.csh
#deactivate

#working from the home directory on the my_env; make sure I have lates version of pip installed 
pip install -r experiment_data/requirements.txt

cd experiment_data
cd IPD 
#OR cd VOLUNTEER
#OR cd STAGHUNT


#echo 'alias python3.8="/home/lkarmann/bin/python3.8"' >> ~/.bashrc


#### if runninig locally ####
#os.chdir('~/Library/Mobile\ Documents/com~apple~CloudDocs/PhD_data') 
#OR
#cd Documents/PhD_data


################################################
#### INITAL CHECKS & PARAMETER OPTIMISATION ####
################################################

#testing: 
python3 main.py --title1 QLS --title2 QLS --num_runs 1


#extra checks  - 
python3 main.py --title1 QLUT --title2 AC --extra alpha0=0.3,decay=0.005 #DONE

python3 main.py --title1 QLS --title2 QLS --num_iterations 100000 & 
python3 main.py --title1 QLUT --title2 QLS --num_iterations 100000 & 
python3 main.py --title1 QLVE_e --title2 QLS --num_iterations 100000 #DONE

python3 main.py --title1 Random --title2 AC &
python3 main.py --title1 Random --title2 Random


python3 main.py --title1 QLUT --title2 AC --extra eps=0.5 #DONE - had to manually change & re-upload exploration_policy

python3 main.py --title1 QLUT --title2 AC --extra eps=1 #DONE - had to manually change & re-upload exploration_policy

#NB here I added alpha0, decay and agmma to the argparse arguments - DONE
python3 main.py --title1 QLUT --title2 AC --alpha0=0.8 & 
python3 main.py --title1 QLVE_e --title2 AC --alpha0=0.8 & 
python3 main.py --title1 QLS --title2 QLS --alpha0=0.8 



#cd version_noLRdecay - DONE
python3 main_noLRdecay.py --title1 QLS --title2 QLS &
python3 main_noLRdecay.py --title1 QLUT --title2 AC & 
python3 main_noLRdecay.py --title1 QLVE_e --title2 AC 

python3 main_noLRdecay.py --title1 QLVE_e --title2 AC --num_iterations 50000 


#cd version_epsdecay20 - DONE
python3 main.py --title1 QLS --title2 QLS &
python3 main.py --title1 QLUT --title2 AC & 
python3 main.py --title1 QLUT --title2 QLS & 
python3 main.py --title1 QLVE_e --title2 AC &
python3 main.py --title1 QLDE --title2 AD & 
python3 main.py --title1 QLDE --title2 QLS 

python3 main.py --title1 QLS --title2 QLS &
python3 main.py --title1 QLUT --title2 QLS &
python3 main.py --title1 QLVE_e --title2 QLS &
python3 main.py --title1 QLUT --title2 QLUT &
python3 main.py --title1 QLVE_e --title2 QLVE_e &
python3 main.py --title1 QLVE_k --title2 QLUT &
python3 main.py --title1 QLVE_k --title2 QLVE_e 



#cd version_epsdecay35 - DONE
python3 main.py --title1 QLS --title2 QLS 
python3 main.py --title1 QLUT --title2 QLS & 
python3 main.py --title1 QLVE_e --title2 QLS & 
python3 main.py --title1 QLUT --title2 QLUT & 
python3 main.py --title1 QLVE_e --title2 QLVE_e & 
python3 main.py --title1 QLVE_k --title2 QLUT & 
python3 main.py --title1 QLVE_k --title2 QLVE_e 


#cd version_epsdecay50 - DONE
python3 main.py --title1 QLS --title2 QLS & 
python3 main.py --title1 QLUT --title2 QLS & 
python3 main.py --title1 QLVE_e --title2 QLS & 
python3 main.py --title1 QLUT --title2 QLUT & 
python3 main.py --title1 QLVE_e --title2 QLVE_e & 
python3 main.py --title1 QLVE_k --title2 QLUT & 
python3 main.py --title1 QLVE_k --title2 QLVE_e


#try new version without LR decay
python3 main.py --title1 QLS --title2 QLS --decay 0.9 --num_runs 2
#NOTE it will not parse in decay of 0! 

python3 main.py --title1 QLS --title2 QLS --epsdecay True --num_runs 3


python3 main.py --title1 QLS --title2 QLS --alpha0 0.5 &
python3 main.py --title1 QLS --title2 QLS --alpha0 0.3 &
python3 main.py --title1 QLS --title2 QLS --alpha0 0.1 & #DONE
python3 main.py --title1 QLS --title2 QLS --num_iterations 50000

& python3 main.py --title1 QLS --title2 QLS --alpha0 0.7 &
python3 main.py --title1 QLS --title2 QLS --alpha0 0.9 #DONE

python3 main.py --title1 QLS --title2 QLS --eps0 0.20 &
python3 main.py --title1 QLS --title2 QLS --eps0 0.50 &
python3 main.py --title1 QLS --title2 QLS --eps0 1



python3 main.py --title1 QLS --title2 QLS --num_runs 10 --eps0 0.20 &
python3 main.py --title1 QLS --title2 QLS --num_runs 10 --eps0 0.50 &
python3 main.py --title1 QLS --title2 QLS --num_runs 10 --eps0 1 #DONE

python3 main.py --title1 QLS --title2 QLS --num_runs 10 --eps0 0.20 --epsdecay True #DONE

python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True & 
python3 main.py --title1 QLUT --title2 QLS --eps0 1.0 --epsdecay True #DONE

#NOTE changed eps decay to end at 0.1
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True 

#TO DO decide whether we decay to 0.1 or 0 (if the latter, change)


#given the final chosen eps and decay, and no LR decay, choose optimal parameter alpha - DONE
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.01 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.1 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.3 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.5 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.7 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.9 & 
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True --alpha0 0.99 

#now set default alpha0 to 0.99

python3 main.py --title1 QLVM --title2 AC --num_runs 1 #test mixed agent works


#extra check - each moral agent against itself with eps=5%, no eps decayand no LR decay - DONE
python3 main.py --title1 QLS --title2 QLS --eps0 0.05 &
python3 main.py --title1 QLUT --title2 QLUT --eps0 0.05 &
python3 main.py --title1 QLDE --title2 QLDE --eps0 0.05 &
python3 main.py --title1 QLVE_e --title2 QLVE_e --eps0 0.05 &
python3 main.py --title1 QLVE_k --title2 QLVE_k --eps0 0.05



################################
#### MAIN BASH SCRIPT - IPD ####
################################

python3 main.py --title1 QLVE_e --title2 QLUT --eps0 0.5 --epsdecay True
python3 main.py --title1 QLVE_e --title2 QLUT --eps0 1.0 --epsdecay True --num_iterations 20000


#!/bin/bash

#run part 1 - QLS vs all other learners, some moral vs moral - DONE ON 3
python3 main.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 QLVE_e --eps0 1.0 --epsdecay True


#run part 2 - remainder of moral vs moral; moral mixed vs. all others - DONE ON 3
python3 main.py --title1 QLVE_k --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 QLVM --eps0 1.0 --epsdecay True



#run part 3 - all vs static - DONE on 3
python3 main.py --title1 QLS --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLS --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLS --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLS --title2 Random --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLUT --title2 Random --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLDE --title2 Random --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_e --title2 Random --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVE_k --title2 Random --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 AC --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 TFT --eps0 1.0 --epsdecay True &
python3 main.py --title1 QLVM --title2 Random --eps0 1.0 --epsdecay True 










#################################
#### BASH SCRIPT - VOLUNTEER ####
#################################


#run part 1 - QLS vs all other learners, some moral vs moral - DONE
python3 main_volunteer.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 QLVE_e --eps0 1.0 --epsdecay True


#run part 2 - remainder of moral vs moral; moral mixed vs. all others - DONE
python3 main_volunteer.py --title1 QLVE_k --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 QLVM --eps0 1.0 --epsdecay True



#run part 3 - all vs static - DONE
python3 main_volunteer.py --title1 QLS --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLS --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLS --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLS --title2 Random --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLUT --title2 Random --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLDE --title2 Random --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_e --title2 Random --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVE_k --title2 Random --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 AC --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_volunteer.py --title1 QLVM --title2 Random --eps0 1.0 --epsdecay True 





################################
#### BASH SCRIPT - STAGHUNT ####
################################


#run part 1 - QLS vs all other learners, some moral vs moral - DONE
python3 main_staghunt.py --title1 QLS --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 QLVE_e --eps0 1.0 --epsdecay True


#run part 2 - remainder of moral vs moral; moral mixed vs. all others - DONE
python3 main_staghunt.py --title1 QLVE_k --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLUT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLDE --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLVE_e --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLVE_k --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 QLVM --eps0 1.0 --epsdecay True



#run part 3 - all vs static - DONE
python3 main_staghunt.py --title1 QLS --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLS --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLS --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLS --title2 Random --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLUT --title2 Random --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLDE --title2 Random --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_e --title2 Random --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVE_k --title2 Random --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 AC --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 TFT --eps0 1.0 --epsdecay True &
python3 main_staghunt.py --title1 QLVM --title2 Random --eps0 1.0 --epsdecay True 





################################
#### CHECK MIXED AGENT RELATIVE VALUES ####
################################

python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0 &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 1.0

python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0 &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main_volunteer.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 1.0

python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0 &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main_staghunt.py --title1 QLVM --title2 AD --eps0 1.0 --epsdecay True --beta 1.0



python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0 &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 1.0

python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0 &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main_volunteer.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 1.0

python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0 &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.2 &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.4 &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.6 &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 0.8 &
python3 main_staghunt.py --title1 QLVM --title2 QLS --eps0 1.0 --epsdecay True --beta 1.0