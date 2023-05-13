# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 14:21:37 2022

@author: Ahmad Al Musawi
Main 3
"""
import networkx as nx
from itertools import combinations
import numpy as np
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #visualisation
from random import sample
import random, math
import LP 
import Graph_Reading as GR
import growing as grow
import statistics as stt

Models = {'High Degree': 'HD',
 'High Betweeness': 'HB',
 'High Closeness': 'HClo',
 'High Clustering': 'HClu',
 'PA': 'PA',
 'PA Betweeness': 'PAB',
 'PA Closeness': 'PAClo',
 'PA Clustering': 'PAClu',
 'LP CAR': 'CAR',
 'LP CH2_L2': 'Ch2_L2',
 'LP Ch2_L3': 'Ch2_L3'}

centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
PP = "D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/"
selected = ['Dolphins',
'Polbooks',
'Word adjacencies',
'Karate',
'Circuits1',
'bn-macaque-rhesus_brain_2',
'soc-tribes',
'bn-cat-mixed-species_brain_1',
'ca-sandi_auths',
'soc-firm-hi-tech',
'CAG_mat72',
'ENZYMES123',
'ENZYMES8']

work_path = f'{PP}/Plots/'
DS = GR.DS

NodesAttacks = ['DNA', 'BNA', 'CNA', 'CcNA']
M1 = ['HD', 'HB', 'HC','HCc']
MPA = ['PA', 'BPA', 'CPA','CcPA']
LPM = ['CAR', 'CH2_L2', 'CH2_L3']#, 'PA', 'CN', 'AA', 'RA', 'JA', 'SO','SA', 'HDI']

attacksM = ['Rn_DNA', 'Re_DNA', 'Rn_BNA', 'Re_BNA', 'Rn_CNA', 'Re_CNA', 'Rn_CcNA', 'Re_CcNA']
attacks = {centr[i]: NodesAttacks[i] for i in range(4)}
C = {centr[i]: i for i in range(4)}
            
def task1():
    '''Attacking networks and save them as gml'''
    df = DataFrame()
    for net in selected:
        g = nx.read_gml(f'{PP}Networks/{net}.gml')
        RN = [net, Rn(g)]
        RE = [Re(g)]
        for cent in centr:
            g2 = attack0(g, 0.2, C[cent])
            RN.append(Rn(g2))
            RE.append(Re(g2))
            nx.write_gml(g2, f'{PP}Results/Attacked Networks/{cent} {net}.gml')
        df.append(RN+RE)
    return df


def task2():
    '''Testing Rn, Re'''
    inPath = f'{PP}Results/Attacked Networks/'
    total = []
    for net in selected:
        g = GR.read_graph(net)
        st1 = [net] + [Rn(g), Re(g)]
        st2 = []
        for cent in centr:
            g2 = nx.read_gml(f'{inPath}{cent} {net}.gml')
            st2 = st2 + [Rn(g2) , Re(g2)]
        total.append(st1 + st2)
        ddf = DataFrame(total, columns=['Network', 'Rn', 'Re', 'RnD','ReD', 'RnB','ReB', 'RnC','ReC', 'RnCLS','ReCLS' ])
        print (f'{ddf}')
    df = DataFrame(total, columns=['Network', 'Rn', 'Re', 'RnD','ReD', 'RnB','ReB', 'RnC','ReC', 'RnCLS','ReCLS' ])
    df.to_csv(f'{inPath}Results.csv')

    
def task3_1():
    '''For each network in the attacked networks, 
    grow the network by adding the lost nodes and edges,
    distribute the edges based on the different growing models
    Using 'HD', 'HB', 'HClo','HClu'
    '''
    inPath = f'{PP}Results/Attacked Networks/'
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/Attacked Networks/grown networks/'
    for cen in centr:
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml')
            # print(gn)
            # _=input(list(original_g.nodes()))
            # _=input(list(attacked_g.nodes()))
            V = [node for node in original_g if node not in attacked_g]
            # _=input(V)
            E = len(original_g.edges())-len(attacked_g.edges())
            for m in M1:
                grown_g = nx.Graph()
                grown_g = grow.grow(attacked_g, V, E, m)
                # _=input(f'{list(grown_g.nodes())}............................................................................')
                nx.write_gml(grown_g, f'{outPath} {cen} {m} {gn}.gml')
            
def common_tasks(inP, outP):
    '''showing the effect of attacks on the selected networks
    measure Rn Re of grown networks'''
    df = DataFrame([], columns=['Network','Rn','Re']+attacksM)
    df.to_csv(f'{outP}/Results.csv', index = False)
    from csv import writer
    with open(f'{outP}/Results.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            Rn1, Re1 = Rn(original_g) , Re(original_g)
            R2 = []
            for cen in centr:
                attacked_g = nx.read_gml(f'{inP}/{cen} {gn}.gml')
                R2 = R2 + [Rn(attacked_g ) , Re(attacked_g ) ]
            writer_object.writerow([gn, Rn1, Re1]+R2)
    f_object.close()
    cPath = outP
    A = pd.read_csv(f'{cPath}/Results.csv')
    total_Rn = {m: A[m]/A['Rn'] for m in ['Rn_DNA', 'Rn_BNA', 'Rn_CNA', 'Rn_CcNA']}
    total_Re = {m: A[m]/A['Re'] for m in ['Re_DNA', 'Re_BNA', 'Re_CNA', 'Re_CcNA']}
    plot_df(DataFrame(total_Rn), 'Node Robustness', 'Rn', f'{cPath}/{attacks[cen]} Rn', 'Attacking Criteria', 'Rn, STD', True)
    plot_df(DataFrame(total_Re), 'Edge Robustness', 'Re', f'{cPath}/{attacks[cen]} Re', 'Attacking Criteria', 'Re, STD', True)


def task3_2():
    '''measure Rn Re of grown networks'''
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/Attacked Networks/grown networks/'
    M1 = ['HD', 'HB', 'HClo','HClu']
    df = DataFrame([], columns=['Network','Rn','Re','Attacking Model','Rn_attacked','Re_attacked','Rn_HD', 'Re_HD', 'Rn_HB', 'Re_HB', 'Rn_HClo', 'Re_HClo', 'Rn_HClu', 'Re_HClu'])
    from csv import writer
    with open(f'{outPath}\Results.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            Rn1, Re1 = Rn(original_g) , Re(original_g)
            for cen in centr:
                attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml')
                Rn2, Re2 = Rn(attacked_g ) , Re(attacked_g ) 
                print (gn, Rn1, Re1, cen, Rn2, Re2)
                R3 = []
                for m in M1:
                    grown_g = nx.read_gml(f'{outPath} {cen} {m} {gn}.gml')
                    R3.append(Rn(grown_g))
                    R3.append(Re(grown_g))
                writer_object.writerow([gn, Rn1, Re1, cen, Rn2, Re2]+R3)
    f_object.close()

def task3_3():
    '''plotting fig 4, 5 of paper, using task3'''
    cPath = f'{PP}Results/Attacked Networks/grown networks'
    A = pd.read_csv(f'{cPath}/First Results.csv')
    for cen in centr:
        newA = A[A['Attacking Model']== cen]
        total_Rn = {m: newA[m]/newA['Rn'] for m in ['Rn_HD', 'Rn_HB', 'Rn_HClo','Rn_HClu']}
        total_Re = {m: newA[m]/newA['Re'] for m in ['Re_HD', 'Re_HB', 'Re_HClo','Re_HClu']}
        plot_df(DataFrame(total_Rn), f'Rn of grown {attacks[cen]} networks', 'Rn', f'{cPath}/{attacks[cen]} Rn', 'Growing Criteria', 'Rn, STD', False)
        plot_df(DataFrame(total_Re), f'Re of grown {attacks[cen]} networks', 'Re', f'{cPath}/{attacks[cen]} Re', 'Growing Criteria', 'Re, STD', False)

def task5():
    '''for each network in the attacked networks, 
    grow the network by adding the lost nodes and edges,
    then, distribute the edges based on the centrality based preferrential attachment'''
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/Attacked Networks/grown networks/'
    for cen in centr:
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml')
            V = [node for node in original_g if node not in attacked_g]
            E = len(original_g.edges())-len(attacked_g.edges())
            random_edges = [(V[i], sample(list(attacked_g.nodes()),1)[0]) for i in range(len(V))]
            newG = nx.Graph()
            newG.add_edges_from(random_edges)
            newG.add_edges_from(list(attacked_g.edges()))

            M1 = ['PAD', 'PAB', 'PAClo','PAClu']
            for m in M1:
                C = get_centralities(newG, M1.index(m)+1)
                
                grown_g = nx.Graph()
                grown_g = grow.grow(attacked_g, V, E, m)
                # _=input(f'{list(grown_g.nodes())}............................................................................')
                nx.write_gml(grown_g, f'{outPath} {cen} {m} {gn}.gml')
def task6():
    '''STANDALONE SIMULATION\n
    showing attacking affect on networks'''
    cc = []
    for d in [10,20,30,40,50]:
        for net in selected:
            g = nx.read_gml(f'{PP}Networks/{net}.gml')
            RN = [net, Rn(g), d/100]
            for cent in centr:
                results = [Rn(attack0(g, d/100, cent)) for _ in range(20)]
                RN.append(stt.mean(results))
            cc.append(RN)
            print(RN)
    df = DataFrame(cc, columns=['Network', 'Rn', 'd', 'Rn_D', 'Rn_B', 'Rn_Clo', 'Rn_Clu'])
    df.to_csv(f'{PP}Node robustness.csv')

def task6_1():
    '''averaging results of task6'''
    A = pd.read_csv(f'{PP}Node robustness.csv')
    total = {m: A[m]/A['Rn'] for m in ['Rn_D', 'Rn_B', 'Rn_Clo','Rn_Clu']}
    plot_df(DataFrame(total), 'Node Robustness', 'Rn', f'{PP}Node robustness')



def task7():
    '''Major Mission: implementing centrality-based PA models\n        '''
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/PA Grown Networks/'
    for gn in selected:
        original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
        for cen in centr:
            attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml') 
            V = [node for node in original_g if node not in attacked_g]
            E = len(original_g.edges())-len(attacked_g.edges())
            for m in MPA:
                print(f'working on .. {gn}.. {cen} .. {m} ..')
                grown_g = nx.Graph()
                grown_g = grow.grow(attacked_g, V, E, m)
                nx.write_gml(grown_g, f'{outPath} {cen} {m} {gn}.gml')

def task7_2():
    '''measure Rn Re of grown networks'''
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/PA Grown Networks/'
    from csv import writer
    df = DataFrame([], columns=['Network','Rn','Re','Attacking Model','Rn_attacked','Re_attacked','Rn_HD', 'Re_HD', 'Rn_HB', 'Re_HB', 'Rn_HClo', 'Re_HClo', 'Rn_HClu', 'Re_HClu'])
    df.to_csv(f'{outPath}Results.csv', index=False)
    with open(f'{outPath}\Results.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            Rn1, Re1 = Rn(original_g) , Re(original_g)
            for cen in centr:
                attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml')
                Rn2, Re2 = Rn(attacked_g ) , Re(attacked_g ) 
                print (gn, Rn1, Re1, cen, Rn2, Re2)
                R3 = []
                for m in MPA:
                    grown_g = nx.read_gml(f'{outPath} {cen} {m} {gn}.gml')
                    R3.append(Rn(grown_g))
                    R3.append(Re(grown_g))
                writer_object.writerow([gn, Rn1, Re1, cen, Rn2, Re2]+R3)
    f_object.close()
            


    
def LP_task_1():
    '''For each network in the attacked networks, 
    grow the network by adding the lost nodes and edges,
    distribute the edges based on the different growing models
    Using CAR, L2 and L3 LP models
    '''
    inPath = f'{PP}Results/Attacked Networks'
    outPath= f'{PP}Results/LP Grown Networks'
    for cen in centr:
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            attacked_g = nx.read_gml(f'{inPath}/{cen} {gn}.gml')
            V = [node for node in original_g if node not in attacked_g]

            E = len(original_g.edges())-len(attacked_g.edges())
            for m in LPM:
                print(f'Working on ... Network: {gn}\t attacked: {cen}\t Grown Criteria: {m}')
                grown_g = nx.Graph()
                grown_g = grow.grow(attacked_g, V, E, m)
                nx.write_gml(grown_g, f'{outPath}/{cen} {m} {gn}.gml')
                print(f'{cen} {m} {gn}.gml is done...')


def LP_task_2():
    '''measure Rn Re of grown networks'''
    inPath = f'{PP}Results/Attacked Networks/'
    outPath= f'{PP}Results/LP Grown Networks/'
    from csv import writer
    df = DataFrame([], columns=['Network','Rn','Re','Attacking Model','Rn_attacked','Re_attacked','Rn_CAR', 'Re_CAR', 'Rn_L2', 'Re_L2', 'Rn_L3', 'Re_L3'])
    df.to_csv(f'{outPath}Results.csv', index=False)
    with open(f'{outPath}\Results.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            Rn1, Re1 = Rn(original_g) , Re(original_g)
            for cen in centr:
                attacked_g = nx.read_gml(f'{inPath}{cen} {gn}.gml')
                Rn2, Re2 = Rn(attacked_g ) , Re(attacked_g ) 
                print (gn, Rn1, Re1, cen, Rn2, Re2)
                R3 = []
                for m in LPM:
                    grown_g = nx.read_gml(f'{outPath}{cen} {m} {gn}.gml')
                    R3.append(Rn(grown_g))
                    R3.append(Re(grown_g))
                writer_object.writerow([gn, Rn1, Re1, cen, Rn2, Re2]+R3)
    f_object.close()
def LP_task_3():
    '''plotting fig 4, 5 of paper, using task3'''
    cPath = f'{PP}Results/LP Grown Networks'
    A = pd.read_csv(f'{cPath}/Results.csv')
    for cen in centr:
        newA = A[A['Attacking Model']== cen]
        total_Rn = {m: newA[m]/newA['Rn'] for m in ['Rn_CAR', 'Rn_L2', 'Rn_L3']}
        total_Re = {m: newA[m]/newA['Re'] for m in ['Re_CAR', 'Re_L2', 'Re_L3']}
        plot_df(DataFrame(total_Rn), f'Rn of grown {attacks[cen]} networks', 'Rn', f'{cPath}/{attacks[cen]} Rn', 'Growing Criteria', 'Rn, STD', False)
        plot_df(DataFrame(total_Re), f'Re of grown {attacks[cen]} networks', 'Re', f'{cPath}/{attacks[cen]} Re', 'Growing Criteria', 'Re, STD', False)

def task7_3():
    '''plotting all results in one plot...'''
    cPath = f'{PP}Results/Final'
    HC = pd.read_csv(f'{cPath}/HC Results.csv')
    LL = pd.read_csv(f'{cPath}/LP Results.csv')
    PA = pd.read_csv(f'{cPath}/PA Results.csv')
    
    A = HC
    for cen in centr:
        A = HC
        newA = A[A['Attacking Model']== cen]
        HC_Rn = {m: newA[m]/newA['Rn'] for m in ['Rn_HD', 'Rn_HB', 'Rn_HC','Rn_HCc']}
        HC_Re = {m: newA[m]/newA['Re'] for m in ['Re_HD', 'Re_HB', 'Re_HC','Re_HCc']}
        A = LL
        newA = A[A['Attacking Model']==cen]
        LP_Rn = {m: newA[m]/newA['Rn'] for m in ['Rn_CAR', 'Rn_L2', 'Rn_L3']}
        LP_Re = {m: newA[m]/newA['Re'] for m in ['Re_CAR', 'Re_L2', 'Re_L3']}
        A = PA
        newA = A[A['Attacking Model']==cen]
        PA_Rn = {m: newA[m]/newA['Rn'] for m in ['Rn_PA', 'Rn_BPA', 'Rn_CPA','Rn_CcPA']}
        PA_Re = {m: newA[m]/newA['Re'] for m in ['Re_PA', 'Re_BPA', 'Re_CPA','Re_CcPA']}
    
        Rn = Merge(PA_Rn, LP_Rn)  
        Rn = Merge(Rn, HC_Rn)
        
        Re = Merge(PA_Re, LP_Re)  
        Re = Merge(Re, HC_Re)
        
        plot_df(DataFrame(Rn), f'Rn of grown {attacks[cen]} networks', 'Rn', f'{cPath}/Rn {attacks[cen]}', 'Growing Criteria', 'Rn, SEM', False)
        plot_df(DataFrame(Re), f'Re of grown {attacks[cen]} networks', 'Re', f'{cPath}/Re {attacks[cen]}', 'Growing Criteria', 'Re, SEM', False)
    
    
def task_RND1():
    '''read all graphs and generate 100 networks attacked RND ly'''
    for net in selected:
        g = nx.read_gml(f'{PP}Networks/{net}.gml')
        for i in range(100):
            g2 = attack0(g, 0.2, 'RND')
            nx.write_gml(g2, f'{PP}Results/Attacked Networks/RND/{net} {i}.gml')


def task_RND2():
    '''read all 100 networks attacked RND ly
    for each network, grow using given methods and save...'''
    inPath = f'{PP}Results/Attacked Networks/RND'
    outPath= f'{PP}Results/Attacked Networks/RND/Grown'
    for gn in [ 'ENZYMES123', 'ENZYMES8']:
        for i in range(10):
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            attacked_g = nx.read_gml(f'{inPath}/{gn} {i}.gml')
            V = [node for node in original_g if node not in attacked_g]
            E = len(original_g.edges())-len(attacked_g.edges())
            for m in M1 + MPA + LPM:
                print(f'Working on ... Network: {gn} {i}\t Grown Criteria: {m}')
                grown_g = nx.Graph()
                grown_g = grow.grow(attacked_g, V, E, m)
                nx.write_gml(grown_g, f'{outPath}/{m} {gn} {i}.gml')
                print(f'{m} {gn} {i}.gml is done...')
def task_RND3():
    '''measure Rn Re of grown networks'''
    inPath = f'{PP}Results/Attacked Networks/RND'
    outPath= f'{inPath}/Grown'
    from csv import writer
    df = DataFrame([], columns=['Network','Rn','Rn_attacked', 'Rn_HD', 'Rn_HB', 'Rn_HC', 'Rn_HCc', 'Rn_PA', 'Rn_BPA', 'Rn_CPA', 'Rn_CcPA', 'Rn_CAR', 'Rn_CH2_L2', 'Rn_CH2_L3'])
    df.to_csv(f'{outPath}/Results.csv', index=False)
    
    from os import listdir
    from os.path import isfile, join
    myFiles = [f for f in listdir(inPath) if isfile(join(inPath, f)) and f.endswith('.gml')]
    with open(f'{outPath}\Results.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for gn in selected:
            original_g = nx.read_gml(f'{PP}Networks/{gn}.gml')
            Rn1 = Rn(original_g) 
            for i in range(100):
                attacked_g = nx.read_gml(f'{inPath}/{gn} {i}.gml')
                Rn2 = Rn(attacked_g ) 
                print (gn, Rn1, Rn2)
                R3 = [Rn(nx.read_gml(f'{outPath}/{m} {gn} {i}.gml')) for m in M1 + MPA + LPM]
                writer_object.writerow([gn, Rn1, Rn2]+R3)
    f_object.close()
    
def task_RND4():
    '''Plotting rnd'''
    A = pd.read_csv(f'{PP}Results/Attacked Networks/RND/Grown/Results.csv')
    tt = [f'Rn_{i}' for i in M1 + MPA + LPM]
    ALL = {m: A[m]/A['Rn'] for m in tt}    
    plot_df(DataFrame(ALL), f'Rn of grown randomly attacked networks', 'Rn', f'{PP}Results/Attacked Networks/RND/Grown/RND', 'Growing Criteria', 'Rn, SEM', False)
    

def plotting():
    import matplotlib.pyplot as mp    
    df1 = pd.read_csv(f'{PP}Results/Attacked Networks/Results.csv')
    df2 = pd.read_csv(f'{PP}Results/Attacked Networks/RND/Grown/Results.csv')
    A = {m: df1[m]/df1['Rn'] for m in [f'Rn_{i}' for i in NodesAttacks]}
    B = {'RND': df2['Rn_attacked']/df2['Rn']}
    plot_df(DataFrame(Merge(A, B)), 'Node Robustness after attack', 'attacking', f'{PP}Results/Attacked Networks/Results', 'Attacking Criteria', 'Rn, SEM') 
    

def get_centralities(G, cen):
    if cen==1:
        C = nx.degree(G)
        N = {}
        for v,d in C:
            N[v] = d
    elif cen==2:
        N = nx.betweenness_centrality(G)    
    elif cen==3:
        N = nx.closeness_centrality(G)
    elif cen==4:
        N = nx.clustering(G)
    return N


    
    
def attack0(G, perc, cen):
    '''G: network, 
    perc: percentage of nodes to be deleted
    cen: selected centrality
    return Gd after removing selected nodes!'''
    p = round(len(G.nodes())*perc)
    # _ = input(f'{perc}.. {p} .. out of .. {len(G.nodes())}')
    N = []
    G2 = nx.Graph()
    G2.add_nodes_from(list(G.nodes()))
    G2.add_edges_from(list(G.edges()))
    if p==0:
        p=1
    if cen =='RND':
        N = random.sample(list(G.nodes()), p)
        G2.remove_nodes_from([x for x in N])
        return G2
    elif C[cen]==0:
        #degree
        N = sorted(G.degree, key=lambda x: x[1], reverse=True)
        G2.remove_nodes_from([x for x,_ in N[:p]])
        return G2
    elif C[cen]==1:
        #betweenness
        N = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)
        G2.remove_nodes_from([x for x,_ in N[:p]])
        return G2
    elif C[cen]==2:
        #closeness
        N = sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)
        G2.remove_nodes_from([x for x,_ in N[:p]])
        return G2
    elif C[cen]==3:
        #clustering
        N = sorted(nx.clustering(G).items(), key=lambda x: x[1], reverse=True)        
        G2.remove_nodes_from([x for x,_ in N[:p]])
        return G2


def attack_edges(G, perc, cen):
    '''G: network, 
    perc: percentage of nodes to be deleted
    cen: selected centrality
    return Gd after removing selected nodes!'''
    p = round(len(G.edges())*perc)
    if p==0:
        p=1
    if cen==1:
        #degree
        N = sorted(G.degree, key=lambda x: x[1], reverse=True)
    elif cen==2:
        #betweenness
        N = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)
    elif cen==3:
        #closeness
        N = sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)
    elif cen==4:
        #clustering
        N = sorted(nx.clustering(G).items(), key=lambda x: x[1], reverse=True)    
        
    D = {i: d for i,d in N}
    for (x,y) in G.edges():
        G[x][y]['weight'] = D[x]*D[y]
    edges=sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1), reverse=True)
    # _=input(edges)
    # _=input([(x, y) for x,y,_ in edges[:p]])
    G2 = nx.Graph()
    G2 = G.copy()
    G2.remove_edges_from([(x, y) for x,y,_ in edges[:p]])
    return G2

    

def Rn(G):
    N = len(G.nodes())
    t = []
    G2 = nx.Graph()
    G2 = G.copy()
    if N!= 0:
        for q in range(1,N):
            d = (q/N) * len(G2.nodes())
            D = sample(G2.nodes(), int(d))
            G2.remove_nodes_from(D)
            t.append(len(LCC(G2).nodes()))
        return sum(t)/N
    else:
        return 0

def Re(G):
    E = len(G.edges())
    t = []
    G2 = nx.Graph()
    G2 = G.copy()
    if E!=0:
        for q in range(1,E):
            d = (q/E) * len(G2.edges())
            D = sample(G2.edges(), int(d))
            G2.remove_edges_from(D)
            t.append(len(LCC(G2).edges()))
        return sum(t)/E
    else:
        return 0


def LCC(G):
    Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
    if len(Gcc)>0:
        return G.subgraph(Gcc[0])
    else:
        return nx.Graph()


def plot_df(df, title, method, path='', xlabel='', ylabel = '', asc = True):
    # _ = input(df.columns)
    # df.columns = ['Degree', 'Betweenness', 'Closeness','Clustering']
    df.columns = ['PA', 'BPA', 'CPA', 'CcPA', 'CAR', 'L2', 'L3','HD', 'HB', 'HC', 'HCc']
    # df.rename(columns = {}, inplace = True)
    # df.columns = ['DNA','BNA','CNA','CcNA','RND']
    df.mean().sort_values()
    df = df.reindex(df.mean().sort_values(ascending = asc,).index, axis=1)
    df.mean().sort_values()
    diff =  [i for i in df]
    aver  = [df[i].mean() for i in df]
    stdev = [df[i].sem() for i in df]
    #---------------------------------
    """Colored plotting"""
    # Create lists for the plot
    x_pos = np.arange(len(diff))
    fig, ax = plt.subplots()
    ax.bar(x_pos, aver, yerr=stdev, align='center', alpha=0.5, ecolor='black', capsize=5, width=0.5)

    max_y_lim = max(aver) + max(stdev)/2 +0.1
    min_y_lim = min(aver) - max(stdev)/2 -0.1
    plt.ylim(min_y_lim, max_y_lim)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(diff, fontsize=8)
    ax.set_title(title)
    ax.yaxis.grid(True)
    
    xlocs, xlabs = plt.xticks()
    plt.xticks(rotation=90)

    # Save the figure and show
    plt.tight_layout()
    print(path+title+'.png')
    plt.savefig(path+'.png', dpi = 450)
    plt.show()
    
    
def Merge(dict1, dict2):
    for i in dict2.keys():
        dict1[i]=dict2[i]
    return dict1 
    
    
    
