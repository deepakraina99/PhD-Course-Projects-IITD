#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Deepak Raina - 2019MEZ8497 - PhD@IITD
# COL864 - Homework 1 

import numpy as np
import random
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm

# In[3]:

GridSize = int(sys.argv[1])
DoFiltering = eval(sys.argv[2]) if len(sys.argv) >= 3 else False
DoPrediction = eval(sys.argv[3]) if len(sys.argv) >= 4 else False
DoFilteringSingleObs = eval(sys.argv[4]) if len(sys.argv) >=5 else False
DoSmoothing = eval(sys.argv[5]) if len(sys.argv) >= 6 else False
DoMostLikelyPath = eval(sys.argv[6]) if len(sys.argv) >= 7 else False
#Grid
gridX,gridY = GridSize,GridSize
noS = gridX*gridY
state = np.arange(noS).reshape(gridX,gridY).T

# In[8]:

#Transition matrix
TM = np.zeros((noS,noS))
noA = 4
nrows,ncols = state.shape[0], state.shape[1]

def IsValidPos(x,y,m,n):
    if (x<m and x>=0) and (y<n and y>=0):
        return True
    else:
        return False
    
for x in range(nrows):
    for y in range(ncols):
        #MoveRight
        if IsValidPos(x,y+1,nrows,ncols):
            TM[state[x,y+1]][state[x,y]]=1
        #MoveLeft
        if IsValidPos(x,y-1,nrows,ncols):
            TM[state[x,y-1]][state[x,y]]=1
        #MoveUp
        if IsValidPos(x-1,y,nrows,ncols):
            TM[state[x-1,y]][state[x,y]]=1
        #MoveDown
        if IsValidPos(x+1,y,nrows,ncols):
            TM[state[x+1,y]][state[x,y]]=1
#Normalized Transition Matrix            
TM_normed = TM/TM.sum(axis=0)

#Initial-state
initial_state = np.ones((noS))*(1/noS)


# In[11]:


#functions for plotting
def plot_grid(ax,grid,colormap,plot_title=None,colorbar=False):
    grid = np.reshape(grid,(gridX,gridY))
    pd = ax.imshow(grid.T,cmap=colormap)
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, gridX, 1))
    ax.set_yticks(np.arange(-.5, gridY, 1))
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    if (colorbar):
        cbar = fig.colorbar(pd)
    if not plot_title is None:
        ax.set_title(plot_title,fontsize=10)

def plot_state(T,inferred_state,figtitle,figsavename,compare=False):
    # Plotting
    if (T<=5):
        fig, ax = plt.subplots(1,T,figsize=(15,6))
    elif (T>5 and (T%5==0)):
        fig, ax = plt.subplots(T//5,5,figsize=(15,6))
    else:
        fig, ax = plt.subplots(T//5+1,5,figsize=(15,6))
    fig.suptitle(figtitle,fontweight="bold",fontsize=16)
    plt.subplots_adjust(left=0.01, bottom=None, right=0.99, top=None, wspace=0.46, hspace=None)
    i,j=0,0
    if(compare): 
        cmap=cm.coolwarm 
    else: 
        cmap=cm.bone
    for t in range(T):
        if (T==1):
            plot_grid(ax,inferred_state[:,t],cmap,"t={}\n".format(t+1))
        elif (T<=5):
            plot_grid(ax[j],inferred_state[:,t],cmap,"t={}\n".format(t+1))
        else:
            plot_grid(ax[i,j],inferred_state[:,t],cmap, "t={}\n".format(t+1))
        j+=1    
        if (j%5) == 0:
            i+=1
            j=0
    plt.show()
    fig.savefig(figsavename)

#function for genrating random number from given distribution
def gen_random(dist):
    cs = np.cumsum(dist)
    cs = cs/cs[-1]
    r = np.random.uniform()
    comp = (cs<r)*1
    y = np.sum(comp)
    return y

# In[12]:


#Observation model
noObs=2
P_Sound,P_noSound=0.9,0.1
bumpObs = np.ones(noS)*P_noSound
rotorObs = np.ones(noS)*P_noSound
dist_type = 1
if dist_type == 0: #Given spatial distribution
    distrib1 = np.array([1,2,8,11,12,13,16,17,19,22])
    rotorObs[distrib1] = P_Sound
    distrib2 = np.array([0,1,5,6,9,10,12,14,17,19])
    bumpObs[distrib2] = P_Sound
    
elif dist_type ==1: # Random-distribution
    noR = int(0.4*noS)
    distrib1 = np.random.randint(noS,size=noR)
    rotorObs[distrib1] = P_Sound

    distrib2 = np.random.randint(noS,size=noR)
    bumpObs[distrib2] = P_Sound

#observations cases
obs_cases = noObs**2
OM = np.zeros((obs_cases,noS))
OM[0][:]=rotorObs*bumpObs
OM[1][:]=rotorObs*(1-bumpObs)
OM[2][:]=(1-rotorObs)*(bumpObs)
OM[3][:]=(1-rotorObs)*(1-bumpObs)

OBS_MAT = {0:(OM[0],rotorObs,bumpObs,'[Rotor, Bump]'),
            1:(OM[1],rotorObs,1-bumpObs,'[Rotor, NoBump]'),
            2:(OM[2],1-rotorObs,bumpObs,'[NoRotor, Bump]'),
            3:(OM[3],1-rotorObs,1-bumpObs,'[NoRotor, NoBump]')}

fig, ax = plt.subplots(obs_cases,noObs,figsize=(5,10))
fig.suptitle('{} states of observations'.format(obs_cases),fontweight="bold",fontsize=16)
for i in range(obs_cases):
    plot_grid(ax[i,0],OBS_MAT[i][1],cm.Blues_r,'Rotor Sound')
    plot_grid(ax[i,1],OBS_MAT[i][2],cm.Blues_r, 'Bump sound')
plt.show()
fig.savefig('obsall.pdf')


# In[13]:

#Simulation
T=10
print('SIMULATION of robot for {} time steps'.format(T))
#Choose random initial state
state_seq, obs_seq = np.zeros(T), np.zeros(T)
state_seq[0] = gen_random(initial_state)
obs_dist=[]
for keys in OBS_MAT.keys():
    obs_dist.append(OBS_MAT[keys][0][int(state_seq[0])])
obs_seq[0] = gen_random(obs_dist)

#Generate random sequence
for t in range(T-1):
    state_seq[t+1] = gen_random(TM_normed[:,int(state_seq[t])])
    obs_dist=[]
    for keys in OBS_MAT.keys():
        obs_dist.append(OBS_MAT[keys][0][int(state_seq[t+1])])
    obs_seq[t+1] = gen_random(obs_dist)

#Prefixed (for testing)
# state_seq = np.array([14,9,4,9,8,13,12,11,10,11])
# obs_seq = np.array([2,2,3,2,1,1,0,1,0,1])

print('True states: ',state_seq)
# print('Observations: ',obs_seq)

#True state and observation grid
true_state = np.zeros((noS,T))
obs_list=[]
for t in range(T):
    #true state
    true_state_idx = int(state_seq[t])
    true_state[true_state_idx,t]=1
    #sound observation
    obs_idx = obs_seq[t]
    obs_list.append(OBS_MAT[obs_idx][3])

print('Observations: ',obs_list)
plot_state(T,true_state,'Robot ground truth and observations','true_robot_state_obs.pdf',True)

# In[14]:

## Inference tasks
#Function to get filtered state
def filtering(Ot,st):
    temp = np.matmul(TM_normed,st)
    fst = np.matmul(np.diag(Ot),temp)
    return fst

#Function to get fpredicted state
def prediction(st):
    pst = np.matmul(TM_normed,st)
    return pst

#Function to get backward msg for smoothing
def backward(Ot,bst):
    temp = np.multiply(bst,Ot.T)
    bst_new = np.matmul(TM_normed,temp)
    return bst_new

#Function to get likelihood ans most-likely state
def get_likelihood(est_state,compare=False):
    log_likelihood= np.zeros((noS,T))
    likely_state = np.zeros((noS,T))
    for t in range(T):
        #finding log-likelihood
        log_likelihood[:,t] = np.log(est_state[:,t])
        #finding most likely locations
        most_likely_location = np.argwhere(log_likelihood[:,t]==np.max(log_likelihood[:,t]))
        if(compare):
            likely_state[most_likely_location,t] = 0.5
            likely_state[int(state_seq[t]),t]=1
        else:
            likely_state[most_likely_location,t] = 1

    return log_likelihood, likely_state

#1. Filtering
# Input: Initial, TM, Obs
if (DoFiltering):
    print('Filtering Inference task : START')
    filtered_state = np.zeros((noS,T))
    #Initialization
    Ot = OBS_MAT[obs_seq[0]][0]
    filtered_state[:,0] = np.matmul(np.diag(Ot),initial_state)
    current_state = filtered_state[:,0]
    for t in range(1,T):
        Ot = OBS_MAT[obs_seq[t]][0]
        filtered_state[:,t] = filtering(Ot,current_state)
        current_state = filtered_state[:,t]
    filtered_state = filtered_state/filtered_state.sum(axis=0)

    # finding log-likelihood and likely state
    log_likelihood, likely_state = get_likelihood(filtered_state,compare=True)

    # Plotting
    plot_state(T,log_likelihood,'Filtering','filtering.pdf')
    plot_state(T,likely_state,'Filtering - Most likely state Vs Ground truth','filtering_most_likely.pdf',compare=True)
    print('Filtering Inference task : END')

# In[15]:

#2. Prediction
if (DoPrediction):
    print('Prediction Inference task : START')
    noP = T
    predicted_state = np.zeros((noS,T))
    try: filtered_state
    except: filtered_state = None
    if filtered_state is None:
        current_state = initial_state
    else:
        current_state = filtered_state[:,T-1]
    for t in range(noP):
        predicted_state[:,t] = prediction(current_state)
        current_state = predicted_state[:,t]
    predicted_state = predicted_state/predicted_state.sum(axis=0)

    # finding log-likelihood and likely state
    log_likelihood, likely_state = get_likelihood(predicted_state)

    # Plotting
    plot_state(T,log_likelihood,'Prediction for {} time steps'.format(noP) ,'prediction.pdf')
    plot_state(T,likely_state,'Prediction - Most likely state','prediction_most_likely.pdf',True)
    print('Prediction Inference task : END')

# In[16]:


#2. Filtering with bump observation
if (DoFilteringSingleObs):
    print('Filtering Inference task (Single obs.) : START')
    filtered_state_single = np.zeros((noS,T))
    #Initialization
    Ot = OBS_MAT[obs_seq[0]][2]
    filtered_state_single[:,0] = np.matmul(np.diag(Ot),initial_state)
    current_state = filtered_state_single[:,0]
    for t in range(1,T):
        Ot = OBS_MAT[obs_seq[t]][2]
        filtered_state_single[:,t] = filtering(Ot,current_state)
        current_state = filtered_state_single[:,t]
    filtered_state_single = filtered_state_single/filtered_state_single.sum(axis=0)

    # finding log-likelihood and likely state
    log_likelihood, likely_state = get_likelihood(filtered_state_single,True)

    # Plotting
    plot_state(T,log_likelihood,'Filtering (Single observation)' ,'filtering_single_obs.pdf')
    plot_state(T,likely_state,'Filtering (Single observation) - Most likely state vs Ground truth','filtering_single_obs_most_likely.pdf',True)
    print('Filtering Inference task (Single obs.) : END')

# In[17]:


##Inference task
#3. Smoothing: forward-backward algorithim
if (DoSmoothing):
    print('Smoothing Inference task : START')
    #backward
    bkwd = np.zeros((noS,T))
    bkwd[:,T-1] = np.ones(noS)
    bwdprev = bkwd[:,T-1]
    for t in range(T-1,0,-1):
        Ot = OBS_MAT[obs_seq[t]][0]
        bkwd[:,t-1] = backward(Ot,bwdprev)
        bwdprev = bkwd[:,t-1]
    bkwd = bkwd/bkwd.sum(axis=0)

    #forward
    frwd = np.zeros((noS,T))
    #Initialization
    Ot = OBS_MAT[obs_seq[0]][0]
    frwd[:,0] = np.matmul(np.diag(Ot),initial_state)
    frwdprev = frwd[:,0]
    for t in range(1,T):
        Ot = OBS_MAT[obs_seq[t]][0]
        frwd[:,t] = filtering(Ot,frwdprev)
        frwdprev = frwd[:,t]
    frwd = frwd/frwd.sum(axis=0)

    #smoothing
    smoothed_state = np.zeros((noS,T))
    smoothed_state = np.multiply(frwd,bkwd)
    smoothed_state = smoothed_state/smoothed_state.sum(axis=0)

    # finding log-likelihood and likely state
    log_likelihood, likely_state = get_likelihood(smoothed_state,True)

    plot_state(T,log_likelihood,'Smoothing' ,'smoothing.pdf')
    plot_state(T,likely_state,'Smoothing - Most likely state Vs Ground tuth','smoothing_most_likely.pdf',True)
    print('Smoothing Inference task : END')

# In[19]:


## Inference task
#4. Most likely path - Viterbi Algorithm
if (DoMostLikelyPath):
    print('Most likely path finding task : START')
    most_likely_path = []
    mu = np.zeros((noS,T))
    mu[:,T-1]=np.ones((noS))*(1/noS)
    for t in range(T-1,0,-1):
        Ot = OBS_MAT[obs_seq[t]][0]
        temp1 = np.matmul(np.diag(Ot),mu[:,t])
        temp2 = np.array([temp1,]*noS).T
        temp3 = np.multiply(temp2,TM_normed)
        temp4 = np.max(temp3,axis=0)
        mu[:,t-1] = temp4/np.sum(temp4)

    # Backtrack
    t=0
    Ot = OBS_MAT[obs_seq[t]][0]
    temp1 = np.squeeze(np.matmul(np.diag(Ot),initial_state))
    temp2 = np.multiply(temp1,mu[:,t])
    most_likely_val,most_likely_state = np.max(temp2),np.argmax(temp2)
    most_likely_path.append(most_likely_state)

    for t in range(1,T):
        Ot = OBS_MAT[obs_seq[t]][0]
        Tm = TM_normed[:,most_likely_path[t-1]]
        temp1 = np.multiply(Ot,Tm)
        temp2 = np.multiply(temp1,mu[:,t])
        most_likely_val,most_likely_state = np.max(temp2),np.argmax(temp2)
        most_likely_path.append(most_likely_state)
    print('Most likely path:',most_likely_path)
    manhattan_dist = np.sum(abs(most_likely_path-state_seq))
    print('Error (Manhattan distance metric): {} units'.format(manhattan_dist))

    max_state = np.zeros((noS,T))
    for t in range(T):
        max_state[most_likely_path[t],t] = 0.5
        max_state[int(state_seq[t]),t]=1

    plot_state(T,max_state,'Most likely path Vs Ground truth','most_likely_path.pdf',True)
    print('Most likely path finding task : END')
