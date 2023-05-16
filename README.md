# Modeling Moral Choice in Dyadic Social Dilemmas with Multi-Agent Reinforcement Learning

This repository contains implementation and analysis code for the following paper: 
Modeling Moral Choices in Social Dilemmas with Multi-Agent Reinforcement Learning, IJCAI'23. 

## Cite us
***

If you use this code, please cite the following paper:

```bibtex
@INPROCEEDINGS{TennantMoralRL2023,
    author={Tennant, Elizaveta and Hailes, Stephen and Musolesi, Mirco},
    booktitle={The 32nd International Joint Conference on Artificial Intelligence (IJCAI'23)}, 
    title={Modeling Moral Choices in Social Dilemmas with Multi-Agent Reinforcement Learning}, 
    year={2023},
    pages={...-...},
    venue={Macao, S.A.R.},
    doi={...}
}
```

You can contact the authors at: `l.karmannaya.16@ucl.ac.uk`

## The environment 

This code can be used to run a simulation of social dilemma games between two agents - a learning moral agent M and a learning opponent O. 

![Reinformcenet Learning by a Moral learning agent M and a learning opponent O](pics/diagram_V2.png "Reinformcenet Learning by a Moral learning agent M and a learning opponent O")

In particular, we use three social dilemma games (Iterated Prisoner's Dilemma - IPD, Iterated Volunteer's dilemma - IVD, Iterated Stag Hunt - ISH), with the following payoffs: 

```{=latex}

         \begin{table}[t]
        \caption{Payoff matrices for each step of the Iterated Prisoner's Dilemma (IPD), Iterated Volunteer's Dilemma (IVD) \& Iterated Stag Hunt (ISH) games, in which players are motivated to defect by either \textit{greed} (IVD), \textit{fear} (ISH), or both (IPD).}
        \label{tab:three_games}
        \begin{tabular}{l|cc}
        \textbf{IPD} & C    & D    \\ \hline
        C         & 3,3 & 1,4 \\ 
        D         & 4,1 & 2,2 %\\
        \end{tabular}
        \hfill
        \begin{tabular}{l|cc}
        \textbf{IVD} & C    & D    \\ \hline
        C         & 4,4 & 2,5 \\ 
        D         & 5,2 & 1,1 %\\
        \end{tabular}
        \hfill
        \begin{tabular}{l|cc}
        \textbf{ISH} & C    & D    \\ \hline
        C         & 5,5 & 1,4 \\ 
        D         & 4,1 & 2,2 %\\
        \end{tabular}
        \end{table}     
```
