# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 15:23:03 2022

@author: Ahmad Al Musawi

These are constructing (growing) models given G.
N: nodes to be added
E: number of edges to be added
m: model of growing
"""
from random import sample
import random
import networkx as nx
import LP
import itertools

M1 = ['HD', 'HB', 'HC','HCc']
MPA = ['PA', 'BPA', 'CPA','CcPA']
LPM = ['CAR', 'CH2_L2', 'CH2_L3']
def grow(G, V, E, m):
    if m in M1:
        return high_centrality(G, V, E, M1.index(m))
    elif m in MPA:
        return PAModels(G, V, E, MPA.index(m))
    elif m in LPM:
        return LPModels(G, V, E, m)
    
def get_centrality(G, m):
    if m==0:
        #degree
        N = sorted(G.degree, key=lambda x: x[1], reverse=True)
    elif m==1:
        #betweenness
        N = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)
    elif m==2:
        #closeness
        N = sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)
    elif m==3:
        #clustering
        N = sorted(nx.clustering(G).items(), key=lambda x: x[1], reverse=True)        
    return N



def high_centrality(G, V, E, m):
    '''adding V to G based on sorted (Kx * Ky) for E times'''
    newG = nx.Graph()
    N = get_centrality(G, m)
    random_edges = [(V[i], sample(list(G.nodes()),1)[0]) for i in range(len(V))]
    # print(random_edges)
    newG.add_edges_from(random_edges)
    newG.add_edges_from(list(G.edges()))
    
    R = []
    for i in range(len(N)-1):
        for j in range(i+1, len(N)):
            u,v = N[i][0], N[j][0]
            if (u,v) not in G.edges():
                du = N[i][1]
                dv = N[j][1]
                R.append((u,v,du*dv))
    newR = sorted(R, key=lambda x: x[2],reverse=True)
    newG.add_edges_from([(newR[i][0], newR[i][1]) for i in range(E-len(V))])

    return newG

def LPModels(G, N, E, m):
    '''G: network to construct,
    N: nodes to be added, 
    E: number of links to be distributed,
    m: LP in use'''
    import operator

    G2 = nx.Graph()
    G2 = G.copy()

    Nodes = list(G.nodes()) + N
    for v in Nodes:
        if v not in list(G2.nodes()):
            G2.add_node(v)


    for v in N:
        G2.add_edge(v, random.choice(list(G2.nodes())))
    # _ = input(f'Neighbors: {[list(G2.neighbors(v)) for v in Nodes]}')

    E = E - len(N)


    L = list(itertools.combinations(Nodes, 2))
    # _ = input(f'all possible combination = {L}')


    E2 = [e for e in L if e not in list(G2.edges())]
    # _ = input(f'selected edges = {E2[:10]}')

    S = {}
    if m=='CAR':
        S = {e:LP.CAR(G2, G2.neighbors(e[0]), G2.neighbors(e[1])) for e in E2}
    elif m=='CH2_L2':
        S = {e:LP.CH2_L2(G2, G2.neighbors(e[0]), G2.neighbors(e[1]), e[0], e[1]) for e in E2}
    elif m=='CH2_L3':
        S = {e:LP.CH2_L3(G2, G2.neighbors(e[0]), G2.neighbors(e[1]), e[0], e[1]) for e in E2}
    
    S1 = [e for e in S if S[e]>0]
    if len(S1)>E:
        G2.add_edges_from(S1[:E])
    else:
        G2.add_edges_from(S1)
        S2 = [i for i in S.keys() if i not in S1]
        # print(S2)
        G2.add_edges_from([random.choice(S2) for _ in range(E-len(S1))])

    return G2.copy()    




def PAModels(G, N, E, m):
    '''G: network to construct,
    N: nodes to be added, 
    E: number of links to be distributed,
    m: centrality in use'''
    problem = False
    G2 = nx.Graph()
    G2 = G.copy()
    for v in N:
        G2.add_edge(v, random.choice(list(G2.nodes())))
    E = E - len(N)

    A = get_centrality(G2, m)
    C = {i: v for i, v in A}

    print(f'adding {E} edges to the attacked network')    
    while E>0 and not problem:        
        # centrality - preferential attachment
        u = preferrential_attachment(C, 1)[0] # selecting one node, preferentially based on centrality
        v = preferrential_attachment(C, 1)[0] # selecting one node, preferentially based on centrality
        if u=='X' or v=='X':
            _ = input('network dropped...')
            problem = True
        # candidates = list(G2.nodes() - G2.neighbors(u))
        # v = optimal_node(G2, candidates, C, u)
        if v != u:
            if (u,v) not in G2.edges() or (v, u) not in G2.edges():
                G2.add_edge(u, v)
                E = E - 1
    return G2.copy()
def preferrential_attachment(deg, n):
    '''deg: sorted list of pairs (Node: degrees), (Node: betweenness) .etc.., 
        n: number of nodes selected preferrentially from G
        return list of selected nodes'''
    degrees = list(deg.values())
    if sum(degrees)==0:
        return 'X'
        # return random.choice( [(n, deg[n]) for n in deg.keys()])
    else:
        Pi = [d/sum(degrees) for d in set(degrees)]
        X = []
        for _ in range(n):
            r = random.uniform(0, max(Pi))
            for k in Pi:
                if k>r:
                    #Now we got the selected k
                    #we need to pick random node with k degree.
                    degs = [(n, deg[n]) for n in deg.keys()]
                    X.append(random.choice(degs))
                    # X.append(k)
                    break
        return X[0]

def optimal_node(G, candidates, degs, u=None):
    C = {}
    for r in candidates:
        C[r] = degs[r]
    return preferrential_attachment(C, 1)[0]


