# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:11:57 2022

@author: Ahmad Al Musawi

READING A GRAPH FROM COMPLEX NETWORKS

"""
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import matthews_corrcoef
import networkx as nx
import math
from random import sample
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
# from assort22 import gen
from itertools import combinations
from sklearn.model_selection import train_test_split
import random
import time

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 20:21:57 2021

@author: Ahmad Al Musawi
"""
import statistics
import pandas as pd
import os

current_path = "D:/Documents/Research Projects/Complex Networks Researches/Link Prediction in dynamic networks/Python/"
arr = os.listdir(current_path + '/networks set')

standard_networks = ["Dolphins", 
         "Polbooks", 
         "Word adjacencies", 
         "Arenas email", 
         "Karate", 
         "Erdos Renyi",
         "USAir97", 
         "Circuits1", 
         "Circuits2", 
         "Circuits3",
         "E. Coli",
         "Barabasi_albert_graph",
         "facebook0",
         "facebook107",
         "facebook348",
         "facebook414",
         "facebook686",
         "facebook1684",
         "bio-celegans",
         "bn-macaque-rhesus_brain_2",
         'soc-tribes',
         'fb-pages-food',
         'bn-cat-mixed-species_brain_1',
         'ca-sandi_auths',
         'soc-firm-hi-tech',
         'aves-weaver-social',
         'bio-SC-TS',
         'CAG_mat72',
         'ENZYMES123',
         'ENZYMES8',
         'reptilia-tortoise-network-bsv',
         'reptilia-tortoise-network-cs',
         'reptilia-tortoise-network-fi',
         'reptilia-tortoise-network-lm',
         'reptilia-tortoise-network-mc',
         'reptilia-tortoise-network-pv',
         'reptilia-tortoise-network-sg']
datasets = ["\dolphins\dolphins.gml",
            "\polbooks\out2.txt",
            "\\word_adjacencies.gml\out2.txt",
            "\\arenas-email\out2.txt",
            "Karate",
            "Erdos Renyi",
            "\\USAir97\\USAir97.mtx", 
            "\\circuits\s208_st.txt",
            "\\circuits\s420_st.txt",
            "\\circuits\s838_st.txt",
            "\\E. Coli\E. Coli.txt",
            "Barabasi_albert_graph",
            "\\facebook\\0.edges",
            "\\facebook\\107.edges",
            "\\facebook\\348.edges",
            "\\facebook\\414.edges",
            "\\facebook\\686.edges",
            "\\facebook\\1684.edges",
            "\\bio-celegans\\bio-celegans.mtx",
            "\\bn-macaque-rhesus_brain_2\\bn-macaque-rhesus_brain_2.txt",
            '\\soc-tribes\\soc-tribes.txt',
            '\\fb-pages-food\\fb-pages-food.txt',
            '\\bn-cat-mixed-species_brain_1\\bn-cat-mixed-species_brain_1.txt',
            '\\ca-sandi_auths\\ca-sandi_auths.mtx',
            '\\soc-firm-hi-tech\\soc-firm-hi-tech.txt',
            '\\aves-weaver-social\\aves-weaver-social.edges',
            '\\bio-SC-TS\\bio-SC-TS.edges',
            '\\CAG_mat72\\CAG_mat72.mtx',
            '\\ENZYMES123\\ENZYMES123.edges',
            '\\ENZYMES8\\ENZYMES8.edges',
            '\\reptilia-tortoise-network-bsv\\reptilia-tortoise-network-bsv.edges',
            '\\reptilia-tortoise-network-cs\\reptilia-tortoise-network-cs.edges',
            '\\reptilia-tortoise-network-fi\\reptilia-tortoise-network-fi.edges',
            '\\reptilia-tortoise-network-lm\\reptilia-tortoise-network-lm.edges',
            '\\reptilia-tortoise-network-mc\\reptilia-tortoise-network-mc.edges',
            '\\reptilia-tortoise-network-pv\\reptilia-tortoise-network-pv.edges',
            '\\reptilia-tortoise-network-sg\\reptilia-tortoise-network-sg.edges']
D = {'Dolphins': -1,
 'Polbooks': -1,
 'Word adjacencies': -1,
 'Arenas email': -1,
 'Karate': -1,
 'Erdos Renyi': -1,
 'USAir97': -1,
 'Circuits1': -1,
 'Circuits2': -1,
 'Circuits3': -1,
 'E. Coli': -1,
 'Barabasi_albert_graph': -1,
 'facebook0': 1,
 'facebook107': 1,
 'facebook348': 1,
 'facebook414': 1,
 'facebook686': 1,
 'facebook1684': 1,
 'bio-celegans': -1,
 'bn-macaque-rhesus_brain_2': -1,
 'soc-tribes': -1,
 'fb-pages-food': -1,
 'bn-cat-mixed-species_brain_1': -1,
 'ca-sandi_auths': 1,
 'soc-firm-hi-tech': -1,
 'aves-weaver-social': 1,
 'bio-SC-TS': 1,
 'CAG_mat72': 1,
 'ENZYMES123': 1,
 'ENZYMES8': 1,
 'reptilia-tortoise-network-bsv': 1,
 'reptilia-tortoise-network-cs': 1,
 'reptilia-tortoise-network-fi': 1,
 'reptilia-tortoise-network-lm': 1,
 'reptilia-tortoise-network-mc': 1,
 'reptilia-tortoise-network-pv': 1,
 'reptilia-tortoise-network-sg': 1}

Disassortative = [i for i in D if D[i]==-1] 
Assortative = [i for i in D if D[i]==1] 
DS = {standard_networks[i]: datasets[i] for i in range(37)}

def read_graph(g):
    '''Passing the name of the graph'''
    spath = current_path + "standard networks dataset"
    if g=='Karate':
        G = nx.karate_club_graph()
    elif g=='Erdos Renyi':
        G = nx.gnm_random_graph(500, 1500)
    elif g=='Barabasi_albert_graph':
        G = nx.barabasi_albert_graph(500, 3)
    elif DS[g].endswith('gml'):
        G = nx.read_gml(spath + DS[g])
    elif DS[g].endswith('txt'):
        G = nx.read_adjlist(spath + DS[g], create_using = nx.Graph(), nodetype = int)
    elif DS[g].endswith('edges') or DS[g].endswith('mtx'):
        file = open(spath + DS[g])
        lines=  file.readlines()
        G = nx.Graph()
        for line in lines:
            N = line.split(" ")
            G.add_edge(N[0], N[1])
    return G
