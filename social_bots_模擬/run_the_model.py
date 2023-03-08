# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 11:47:10 2023

@author: Emile
"""

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import numpy as np
import math
from social_bots import social_bot_small_world


def decorate(**options):
    """Decorate the current axes.

    Call decorate with keyword arguments like

    decorate(title='Title',
             xlabel='x',
             ylabel='y')

    The keyword arguments can be any of the axis properties

    https://matplotlib.org/api/axes_api.html

    In addition, you can use `legend=False` to suppress the legend.

    And you can use `loc` to indicate the location of the legend
    (the default value is 'best')
    """
    loc = options.pop("loc", "best")
    if options.pop("legend", True):
        legend(loc=loc)

    plt.gca().set(**options)
    plt.tight_layout()


def legend(**options):
    """Draws a legend only if there is at least one labeled item.

    options are passed to plt.legend()
    https://matplotlib.org/api/_as_gen/matplotlib.pyplot.legend.html

    """
    underride(options, loc="best", frameon=False)

    ax = plt.gca()
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, **options)


def set_palette(*args, **kwds):
    """Set the matplotlib color cycler.

    args, kwds: same as for sns.color_palette

    Also takes a boolean kwd, `reverse`, to indicate
    whether the order of the palette should be reversed.

    returns: list of colors
    """
    reverse = kwds.pop('reverse', False)
    palette = sns.color_palette(*args, **kwds)

    palette = list(palette)
    if reverse:
        palette.reverse()

    cycler = plt.cycler(color=palette)
    plt.gca().set_prop_cycle(cycler)
    return palette
def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    d: dictionary
    options: keyword args to add to d
    """
    for key, val in options.items():
        d.setdefault(key, val)

    return d
def simulate_repaetly(bots_ratio,k,n):
    '''
    n:repeat_times
    k:the number of k
    bots_ration:the list of bots ratio
    '''
    prob_dominant_each_bots=[]
    
    t=0  #Set k to trace the process
    
    for bots in bots_ratio:
        prob_dominant=[]

        for i in range(0,n):
            ws=social_bot_small_world(n=1000,k=k,p=0.5,robot_ratio=bots)
            ws.constant()
            prob_dominant.append(ws.dominant_or_not())
            t+=1
            print(t)
        prob_dominant_each_bots.append(np.mean(prob_dominant))
    return prob_dominant_each_bots
def simulate_repaetly_by_prob(reconnect_prob,k,n):
    '''
    n:repeart_times
    k:the number of k
    reconnect_prob:the probaility of rewire in small world model
    '''
    prob_dominant_each_prob=[]
    clusters=[]
    t=0
    for probs in reconnect_prob:
        prob_dominant=[]
        for i in range(0,n):
            ws=social_bot_small_world(n=1000,k=k,p=probs,robot_ratio=0.05)
            ws.constant()
            prob_dominant.append(ws.dominant_or_not())
                
            t+=1                  
            print(t)
        cluster=nx.average_clustering(ws.network)
        clusters.append(cluster)
        prob_dominant_each_prob.append(np.mean(prob_dominant))
    return  prob_dominant_each_prob,clusters
    
#figure1
bots_ratio=np.arange(0.01,0.11,0.01)
# each k simulate 1000 times
k_6_prob_dominant_each_bots=simulate_repaetly(bots_ratio,6,1000)
k_8_prob_dominant_each_bots=simulate_repaetly(bots_ratio,8,1000)
k_10_prob_dominant_each_bots=simulate_repaetly(bots_ratio,10,1000)

# node colors for drawing networks
colors = sns.color_palette('pastel', 6)
sns.set_palette(colors) 
plt.plot(bots_ratio, k_6_prob_dominant_each_bots, 's-', linewidth=1, label='k=6')   
plt.plot(bots_ratio, k_8_prob_dominant_each_bots, 's-', linewidth=1, label='k=8')
plt.plot(bots_ratio, k_10_prob_dominant_each_bots, 's-', linewidth=1, label='k=10')
decorate(xlabel='Bots ratio',
         title='Probaility of robots dominating the public opinion',
         xlim=[0, 0.1], ylim=[0, 1.01])
plt.savefig('robots_dominatin_per_botsratio.png')



#figure2
reconnect_prob=np.arange(0,1.1,0.1)
k_6_prob_dominant_each_prob,k_6_cluster= simulate_repaetly_by_prob(reconnect_prob,6,1000)
k_8_prob_dominant_each_prob,k_8_cluster= simulate_repaetly_by_prob(reconnect_prob,8,1000)
k_10_prob_dominant_each_prob,k_10_cluster= simulate_repaetly_by_prob(reconnect_prob,10,1000)


plt.plot(reconnect_prob, k_6_prob_dominant_each_prob, 's-', linewidth=1, label='k=6')
plt.plot(reconnect_prob, k_6_cluster,linestyle="--" ,linewidth=1, label='k=6')
plt.plot(reconnect_prob, k_8_prob_dominant_each_prob, 's-', linewidth=1, label='k=8')
plt.plot(reconnect_prob, k_8_cluster,linestyle="--", linewidth=1, label='k=8')
plt.plot(reconnect_prob, k_10_prob_dominant_each_prob, 's-', linewidth=1, label='k=10')
plt.plot(reconnect_prob, k_10_cluster,linestyle="--", linewidth=1, label='k=10')

decorate(xlabel='reconnection of probaility(pr)',
         title='Probaility of robots dominating the public opinion/cluster coefficient',
         xlim=[0, 1], ylim=[0, 1.01])
plt.savefig('robots_dominatin_per_prob.png')