# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 02:17:09 2023

@author: Emile
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
class social_bot_small_world:
    def __init__(self,n,k,p,robot_ratio):
        
        self.network=nx.watts_strogatz_graph(n=n,k=k,p=p)
        #decides each agent is human or robot 1 is human 2 is robot
        self.species=np.full((n,),1)
        robots_loc=np.random.choice(range(0,n),round(n*robot_ratio),replace=False)
        self.species[robots_loc]=2
        # 1=positive 0=negative
        self.opinions=np.random.choice([1,0],n)
        #if the agent is robot, turn it to negative
        self.opinions[self.species==2]=0
        # set the will to express
        self.will=np.random.random(n) 
        # if the agent is robot, will=1
        self.will[self.species==2]=1
        #set the threshold
        self.threshold=np.random.random(n)
        #if the agent is robot, threshold=0
        self.threshold[self.species==2]=0
        #set action or not
        self.state=np.random.random(n)
        self.state[self.will>=self.threshold]=1
        self.state[self.will<self.threshold]=0
    
    def opinion_climate(self):
        #caculate the opinion_climate
        opinions=self.opinions
        ws=self.network
        state=self.state
        opinion_climate_list=[]
        for agent in ws.nodes:
            #find the neighbor
            neighbors=np.array(ws[agent])
            # choose the neighbors that will express their opinions
            neighbors=neighbors[state[neighbors]==1]
            #check its opinion then caculate the supoorttive and opposive neighbors
            if opinions[agent]==1:
                # ns= number of supportive neighbor
                ns=sum(opinions[neighbors])
                # no= number of opposive neighbor
                no=len(neighbors)-ns
            elif opinions[agent]==0:
                no=sum(opinions[neighbors]) 
                ns=len(neighbors)-no
            if ns+no:
                opinion_climate=(ns-no)/(ns+no)
            else:
                opinion_climate=0
            opinion_climate_list.append(opinion_climate)
        return np.array(opinion_climate_list)
    def impact_of_opinion_climate(self):
        opinion_climate=self.opinion_climate()
        
        return np.array(list(map(lambda x: 2*(((1+math.exp(-5*x))**(-1))-(1/2)),opinion_climate)))
    def step(self):
        impact=self.impact_of_opinion_climate()
        will=self.will
        opinions=self.opinions
        species=self.species
        threshold=self.threshold
        state=self.state

        # if impact>=0
        will[impact>=0]=will[impact>=0]+((1-will[impact>=0])*impact[impact>=0])
        # if impact<0
        will[impact<0]=will[impact<0]+(will[impact<0]*impact[impact<0])
        # if the agent is robot, transfer its will to 1
        will[species==2]=1

        # update the cureent state
        state[will>=threshold]=1
        state[will<threshold]=0
        return sum(state)
    def dominant_or_not(self):
        """Determine whether the opinions are dominated """
        opinions=self.opinions
        state=self.state
        if  sum(opinions[state==1])<len(opinions[state==1])*1/3:
            return 1
        else:
            return 0
    def loop(self, iters=1):
        """Runs the given number of steps."""
        for i in range(iters):
            self.step()
    def constant(self):
        """ Run untilf the state become constant even run 10 stpes"""
        step_list=[]
        k=0
        t=0
        a2=0
        while k!=10:
            t+=1
            step_list.append(self.step())
            if len(step_list)>1:
                if step_list[t-2]==step_list[t-1]:
                    k+=1

                else:
                    k=0
        return t