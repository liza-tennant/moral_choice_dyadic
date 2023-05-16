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
![Payoffs](pics/payoffs.png "Payoffs")

