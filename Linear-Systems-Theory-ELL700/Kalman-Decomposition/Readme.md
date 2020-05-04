
#  Kalman Decomposition - MATLAB Code
The Kalman decomposition provides a mathematical means to convert the representation of any Linear Time-Invariant (LTI) system to a form in which the system can be decomposed into 
* Controllable and unobservable states
* Controllable but observable states
* Uncontrollable and unobservable states
* Uncontrollable but observable states

For more info, please refer this [report](https://github.com/deepakraina99/PhD-Course-Projects-IITD/blob/master/Linear-Systems-Theory-ELL700/Kalman-Decomposition/Report.pdf)

> This work has been done as part of Linear Systems Theory
> course at IIT Delhi.

#### System Specs:
- MATLAB R2019b with System Control Toolbox

# How to run the code?
```sh
[Abar,Bbar,Cbar,T] = getKalmanDec(A,B,C)
```
