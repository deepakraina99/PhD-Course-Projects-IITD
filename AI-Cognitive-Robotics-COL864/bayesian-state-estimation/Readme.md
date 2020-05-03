
# Bayesian State Estimation of an underwater robot (agent) using observations

This problem concerns tracking an agent (an underwater robot) exploring a lake. The robot is submerged at a particular depth and not visible on the surface. Our goal is to estimate the agent’s movement via an immersed acoustic receiver in the lake.

For more info, please refer this [assignment](https://github.com/deepakraina99/bayesian-state-estimation-robotics/blob/master/Homework-I.pdf), [report](https://github.com/deepakraina99/bayesian-state-estimation-robotics/blob/master/report.pdf)

> This work has been done as part of AI for Cognitive Robot Intelligence course at IIT Delhi

# How to run the code?
#### Syntax:

 ```sh
python run_prob_inf.py int grid size bool DoFiltering bool DoPrediction bool DoFilteringSingleObs bool DoSmoothing bool DoMostLikelyPath 
```
*For example*, to run all the inference tasks on 5 × 5 grid, use the following syntax:
```sh
python run prob inf.py 5 1 1 1 1 1
```
