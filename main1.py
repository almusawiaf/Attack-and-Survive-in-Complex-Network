# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:55:24 2022

@author: Ahmad Al Musawi
"""
import networkx as nx
from itertools import combinations
import numpy as np
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #visualisation
import LP 
import Graph_Reading as GR

centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
networks_path = "D:/Documents/Research Projects/Complex Networks Researches/Link Prediction in dynamic networks/Python/standard networks dataset/"
myPath = "D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/"

all_standard_metrics =  ["CN","AA","RA","PA","JA","SA","SO","HPI","HDI","LLHN","CAR", "CH2_L2", 'CH2_L3']
standard_metrics =  ["CN","PA","CAR"]#, "CH2_L2"]



Sampling_Nodes = ['Random', 'HDN', 'HBN', 'HCN']
work_path = 'D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/Plots/'
Dataset = GR.DS


def properties():
    new_db = [(name, LCC(g)) for name, g in Dataset]
    details = []
    for n, g in new_db:
        print(n)
        if n != "Erdos Renyi":
            details.append([n] + features2(g))
    df = DataFrame(details, columns=['network', 'N', 'E', 'Rn', 'Re', 'ASP', 'r', 'Density', 'diameter', 'c', 'T', 'M'])
    df.to_csv(f'{myPath}properties.csv')


def lines_plot():
    centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
    for cen in centr:
        title = '10.0, 10 times'
        df = pd.read_csv(f'{myPath}Results/Rn, {cen} based Node Attack, {title}.csv')
        df.columns = ['steps'] + GR.standard_networks
        df = df[[i for i in GR.standard_networks if i!= 'Erdos Renyi']]
        df.plot(kind = 'line')
        plt.xlabel('iterations')
        plt.ylabel('Robustness')
        plt.xticks(rotation=90)
        ticks = df.index.tolist()
        plt.xticks(ticks, [i for i in range(11)])
        plt.title(cen)
        # plt.tight_layout()
        plt.savefig(f'{myPath}Results/Rn, {cen} based Node Attack, {title}.png', dpi = 300)
        plt.show()
def collect():
    centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
    title = '10.0, 10 times'
    for net in GR.standard_networks:
        dd = []
        for r in ['Rn', 'Re']:
            for cen in centr:
                df1 = pd.read_csv(f'{myPath}Results/{r}, {cen} based Node Attack, {title}.csv')
                df1.columns = ['steps'] + GR.standard_networks
                dd.append(df1[net])
        df = DataFrame(dd).transpose()
        df.columns = ['Rn, Degree', 'Rn, Betweenness', 'Rn, Closeness', 'Rn, Clustering', 'Re, Degree', 'Re, Betweenness', 'Re, Closeness', 'Re, Clustering']
        fig, axe = plt.subplots(dpi=300)
        axe.plot(df[['Rn, Degree', 'Rn, Betweenness', 'Rn, Closeness', 'Rn, Clustering']])
        axe.plot(df[['Re, Degree', 'Re, Betweenness', 'Re, Closeness', 'Re, Clustering']], linestyle = 'dashed')
        axe.legend(['Rn, Degree', 'Rn, Betweenness', 'Rn, Closeness', 'Rn, Clustering', 'Re, Degree', 'Re, Betweenness', 'Re, Closeness', 'Re, Clustering'])
        # df[['Rn, Degree', 'Rn, Betweenness', 'Rn, Closeness', 'Rn, Clustering']].plot(kind = 'line')
        # df[['Re, Degree', 'Re, Betweenness', 'Re, Closeness', 'Re, Clustering']].plot(kind = 'line', linestyle = 'dashed')
        plt.xlabel('iterations')
        plt.ylabel('Robustness')
        # plt.xticks(rotation=90)
        ticks = df.index.tolist()
        plt.xticks(ticks, [i for i in range(11)])
        plt.title(net)
        plt.tight_layout()
        plt.savefig(f'{myPath}Results/{net}.png', dpi = 300)
        plt.show()
    


def NodeAttack():
    '''Delete 1% of the nodes based on given centrality and measure the resulted centrality'''
    centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
    cen = int(input('Enter centrality:\n1- Degree\n2- Betweenness\n3- Closeness\n4- Clustering...'))
    perc = float(input('Enter deleting percentage..(0.01 to 0.25)...'))
    iterations = int(input('Enter number of iterations...'))
    title = f'{perc*100}, {iterations} times'
    nets = []
    results_E = []
    results_N = []
    for n, G in Dataset:
        g = LCC(G)
        nets.append(n)
        result_e = [edge_robustness2(g)]
        result_n = [node_robustness2(g)]
        for _ in range(iterations):
            new_g = attack0(g, perc, cen)
            result_e.append(edge_robustness2(new_g))
            result_n.append(node_robustness2(new_g))
            g = new_g.copy()
        results_E.append(result_e)
        results_N.append(result_n)
    
    DataFrame(results_N).transpose().to_csv(f'{myPath}Results/Rn, {centr[cen-1]} based Node Attack, {title}.csv')
    DataFrame(results_E).transpose().to_csv(f'{myPath}Results/Re, {centr[cen-1]} based Node Attack, {title}.csv')

def EdgeAttack():
    '''Delete 1% of the nodes based on given centrality and measure the resulted centrality'''
    centr = ['Degree', 'Betweenness', 'Closeness', 'Clustering']
    cen = int(input('Enter centrality:\n1- Degree\n2- Betweenness\n3- Closeness\n4- Clustering...'))
    perc = float(input('Enter deleting percentage..(0.01 to 0.25)...'))
    iterations = int(input('Enter number of iterations...'))
    title = f'{perc*100}, {iterations} times'
    nets = []
    results_E = []
    results_N = []
    for n, G in Dataset:
        g = LCC(G)
        nets.append(n)
        result_e = [edge_robustness2(g)]
        result_n = [node_robustness2(g)]
        for _ in range(iterations):
            new_g = attack_edges(g, perc, cen)
            result_e.append(edge_robustness2(new_g))
            result_n.append(node_robustness2(new_g))
            g = new_g.copy()
        results_E.append(result_e)
        results_N.append(result_n)
    
    DataFrame(results_N).transpose().to_csv(f'{myPath}Results/Rn, {centr[cen-1]} based Edge Attack, {title}.csv')
    DataFrame(results_E).transpose().to_csv(f'{myPath}Results/Re, {centr[cen-1]} based Edge Attack, {title}.csv')



    
    
    # data.plot()
    # for j in range(len(Dataset)):
    #     plt.plot([i for i in range(10)], results[j] , marker = 'x')
    # # plt.plot(C, [x[0] for x in RECEIVED], marker = 'o', label = 'Received')            

    # plt.legend()
    # plt.title(f'Deleting {int(perc*100)}% of highest {centr[cen-1]} nodes')
    # plt.xlabel('Iterations')
    # plt.ylabel(f'Nodes Robustness', fontsize = 10)
    # # plt.ylabel(f'Average {centr[cen-1]} value', fontsize = 10)
    
    # plt.tight_layout()
    
    # plt.savefig(f'fig2 {centr[cen-1]}.png', dpi = 300)
    # plt.show()


def run():
    '''Delete 1% of the nodes based on given centrality and measure the resulted centrality'''
    cen = int(input('Enter centrality:\n1- Degree\n2- Betweenness\n3- Closeness\n4- Clustering...'))
    for j in range(len(Dataset)):
        print(f'{j} -  {info(Dataset[j][1])} \t\t {Dataset[j][0]} ')
    selected_G = int(input('Enter network index..'))
    print(f'{GR.standard_networks[selected_G]} is selected...')
    perc = float(input('Enter deleting percentage..(0.01 to 0.25)...'))
    iterations = int(input('Enter number of iterations...'))
    ot = int(input('Optimal node selection\nt==1 --> Link prediciton method\nt==2 -----> centrality preferrential attachment'))
    networks = [g for _, g in Dataset]
    ex = input('Enter extra info for title of plot..')
    
        
    g = networks[selected_G]
    results = []
    print(f'Working on {Dataset[selected_G][0]}')
    print(info(g))
    for i in range(iterations):
        print(f'iteration # {i}')
        C = get_centralities(g, cen)           
        results.append(features2(g))
        # results.append(node_robustness(g))
        print(info(g))
        NAA = attack(g, perc, cen, C) # network after attack
        print(info(NAA))
        Ns = list(g.nodes() - NAA.nodes())
        Es = len(g.edges()) - len(NAA.edges()) 
        new_g = construct_e(NAA, Ns, Es, cen, C, ot)
        # new_g = construct_random(NAA, Ns, Es, cen, C, ot)
        print(info(new_g))
        print('-----------------------------------\n')
        g = new_g.copy()


    print(results)
    cols = ['R','ASP', 'r', 'D','d', 'c', 'b', 'cl']
    df = DataFrame(results, columns= cols)
    # df = normalize(DataFrame(results, columns= ['r', 'd', 'c', 'b', 'cl', 'p', 'h']))
    plt.plot([i for i in range(len(results))], df, marker = 'x') 
    # plt.plot([i for i in range(len(results))], results , marker = 'x') 
    plt.legend(cols)
    plt.title(f'{Dataset[selected_G][0]}, {centr[cen-1]}, attacking {perc*100}%')
    plt.xlabel('Iterations')
    plt.ylabel('LCC (Robustness)', fontsize = 10)
    # plt.ylabel(f'Average {centr[cen-1]} value', fontsize = 10)
    
    plt.tight_layout()
    
    plt.savefig(f'fig2 {Dataset[selected_G][0]}, {centr[cen-1]}, {perc}, {ex}.png', dpi = 300)
    plt.show()
        


def preferrential_attachment(deg, n):
    '''deg: sorted list of pairs (Node: degrees), (Node: betweenness) .etc.., 
        n: number of nodes selected preferrentially from G
        return list of selected nodes'''
    degrees = list(deg.values())
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

def construct(G, N, E, cen, C, ot):
    '''G: network to construct,
    N: nodes to be added, 
    E: number of links to be distributed,
    cen: centrality in use
    ot: optimal_node_t'''
    print('Constructing...')
    Nodes_to_add = [n for n in C.keys() if n not in G.nodes()]
    G.add_nodes_from(Nodes_to_add)
            
    G2 = nx.Graph()
    G2 = G.copy()
    # for v in N:
    #     G2.add_edge(v, random.choice(list(G2.nodes())))
    # E = E - len(N)
    # NOT ADAPTIVE UPDATING. 
    print(f'adding {E} edges to the attacked network')
    
    while E>0:        
        # centrality - preferential attachment
        u = preferrential_attachment(C, 1)[0] # selected preferentially based on centrality
        candidates = list(G2.nodes() - G2.neighbors(u))
        v = optimal_node(G2, candidates, C, ot, u)
        if v != u:
            if (u,v) not in G2.edges() or (v, u) not in G2.edges():
                G2.add_edge(u, v)
                E = E - 1
    return G2.copy()


def construct_random(G, N, E, cen, C, ot):
    '''G: network to construct,
    N: nodes to be added, 
    E: number of links to be distributed,
    cen: centrality in use
    ot: optimal_node_t'''
    print('Constructing...')
    Nodes_to_add = [n for n in C.keys() if n not in G.nodes()]
    G.add_nodes_from(Nodes_to_add)
            
    G2 = nx.Graph()
    G2 = G.copy()
    # NOT ADAPTIVE UPDATING. 
    print(f'adding {E} edges to the attacked network')
    
    while E>0:        
        # centrality - preferential attachment
        u = random.choice(list(G2.nodes()))
        candidates = list(G2.nodes() - G2.neighbors(u))
        v = random.choice(candidates)
        if v != u:
            if (u,v) not in G2.edges() or (v, u) not in G2.edges():
                G2.add_edge(u, v)
                E = E - 1
    return G2.copy()

def construct_e(G, N, E, cen, C, ot):
    '''
    Constructing the network based on the product of selected centrality
    G: network to construct,
    N: nodes to be added, 
    E: number of links to be distributed,
    cen: centrality in use
    ot: optimal_node_t'''
    print('Constructing...')
    Nodes_to_add = [n for n in C.keys() if n not in G.nodes()]
    G.add_nodes_from(Nodes_to_add)
            
    G2 = nx.Graph()
    G2 = G.copy()
    print(f'adding {E} edges to the attacked network')
    # printing('C  = ', C)
    r = [i for i in C.items()]
    R = []
    for i in range(len(r)-1):
        for j in range(i+1, len(r)):
            u = r[i][0]
            v = r[j][0]
            if (u,v) not in G.edges():
                du = r[i][1]
                dv = r[j][1]
                R.append((u,v,du*dv))
    newR = sorted(R, key=lambda x: x[2],reverse=True)
    # printing('newR', newR[:E])
    for i in range(E):
        G2.add_edge(newR[i][0],newR[i][1])
    return G2.copy()

    


    
def optimal_node(G, candidates, degs, t, u=None):
    '''t==1 --> Link prediciton method
    t==2 -----> centrality preferrential attachment'''
    if t==1:
        total = []
        for lp in standard_metrics:
            #for the current LP, we get its results for all not neighbor nodes 
            sub_total = [LP.LP(lp, G, G.neighbors(u), G.neighbors(r), u, r) for r in candidates]
            total.append(sub_total)  
        norm = list(normalize(DataFrame(total, columns=candidates)).mean())
        return candidates[norm.index(max(norm))]
    elif t==2:
        C = {}
        for r in candidates:
            C[r] = degs[r]
        return preferrential_attachment(C, 1)[0]

    


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result



def attack(G, perc, cen, C):
    '''G: network, 
    perc: percentage of nodes to be deleted
    cen: selected centrality
    return Gd after removing selected nodes!'''
    print('Attacking...')
    p = round(len(G.nodes())*perc)
    N = sorted(C.items(), key=lambda x: x[1], reverse=True)        
    G2 = nx.Graph()
    G2 = G.copy()
    G2.remove_nodes_from([x for x,_ in N[:p]])
    return G2




    



def centralities(G, cen):
    N = get_centralities(G, cen)
    return sum([i for _, i in N.items()])/len(N)



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


def node_robustness(G):
    N = len(G.nodes())
    t = []
    G2 = nx.Graph()
    G2 = G.copy()
    for q in range(N):
        d = q * len(G2.nodes())
        D = sample(G2.nodes(), d)
        G2.remove_nodes_from(D)
        t.append(len(LCC(G2).nodes()))
    print(t)
    return sum(t)/N


def edge_robustness(G):
    E = len(G.edges())
    t = []
    G2 = nx.Graph()
    G2 = G.copy()
    for q in range(E):
        d = q * len(G2.edges())
        D = sample(G2.edges(), d)
        G2.remove_edges_from(D)
        t.append(len(LCC(G2).edges()))
    print(t)
    return sum(t)/E





    



def printing(cont, v):
    print(f'{cont} = {v}')
    _ = input('Press any key...')

def info(G):
    return f'|V|\t=\t{len(G.nodes())}\t|E|\t=\t{len(G.edges())}'


def features(network):
    N = len(network.nodes())
    E = len(network.edges())
    ASP = nx.average_shortest_path_length(network)
    r = nx.degree_assortativity_coefficient(network)
    d = nx.density(network)
    diam = nx.diameter(network)
    c = nx.average_clustering(network)
    b = nx.betweenness_centrality(network)
    cl = nx.closeness_centrality(network)
    p = nx.pagerank(network)
    # h = nx.harmonic_centrality(network)
    b_av, b_std = ave_std([i for _, i in b.items()])
    cl_av, cl_std = ave_std([i for _, i in cl.items()])
    p_av, p_std = ave_std([i for _, i in p.items()])
    # h_av, h_std = ave_std([i for _, i in h.items()])
    # eg = nx.eigenvector_centrality(network.to_undirected())
    # k = nx.katz_centrality(network)
    return N, E, r, d,diam, c, ASP, b_av, b_std, cl_av, cl_std, p_av, p_std#, h_av, h_std


def features2(network):    
    import networkx.algorithms.community as nx_comm
    g = LCC(network) 
    Rn = node_robustness2(network)
    Re = edge_robustness2(network)
    ASP = nx.average_shortest_path_length(g)
    r = nx.degree_assortativity_coefficient(network)
    d = nx.density(network)
    diam = nx.diameter(g)
    c = nx.average_clustering(network)
    t = nx.transitivity(network)
    m = nx_comm.modularity(network, next(nx_comm.girvan_newman(network)))
    # b = nx.betweenness_centrality(network)
    # cl = nx.closeness_centrality(network)
    # p = nx.pagerank(network)
    # h = nx.harmonic_centrality(network)
    # b_av, _ = ave_std([i for _, i in b.items()])
    # cl_av, _ = ave_std([i for _, i in cl.items()])
    # p_av, _ = ave_std([i for _, i in p.items()])
    # h_av, _ = ave_std([i for _, i in h.items()])
    # eg = nx.eigenvector_centrality(network.to_undirected())
    # k = nx.katz_centrality(network)
    return [len(network.nodes()), len(network.edges()), Rn, Re, ASP, r, d, diam, c, t, m]#, b_av, cl_av#, p_av#, h_av




def ave_std(L):
    arr = np.array(L)
    return np.mean(arr), np.std(arr)

def heat():
    import seaborn as sb
    a = pd.read_csv(f'{myPath}properties.csv')
    attrb =  ['N', 'E', 'ASP', 'Assortativity', 'Density','diameter', 'Clustering', 'Transitivity', 'Modularity', 'Rn', 'Re']
    df = a[attrb]
    corr = df.corr()
    from matplotlib import pyplot
    pyplot.figure(figsize=(7.5, 4), dpi = 600) # width and height in inches
    sb.heatmap(corr, cmap="Blues", annot=True)
    
def CorrMtx():
    dropDuplicates = False
    a = pd.read_csv(f'{myPath}Attack and Survive - Sheet2.csv')
    attrb =  ['Rn', 'Re', 'ASP', 'r', 'Density', 'diameter', 'c']#['network', 'N', 'E', 
    df = a[attrb]

    # Exclude duplicate correlations by masking uper right values
    if dropDuplicates:    
        mask = np.zeros_like(df, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

    # Set background color / chart style
    sns.set_style(style = 'white')

    # Set up  matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Add diverging colormap from red to blue
    cmap = sns.diverging_palette(250, 10, as_cmap=True)

    # Draw correlation plot with or without duplicates
    if dropDuplicates:
        sns.heatmap(df, mask=mask, cmap=cmap, 
                square=True,
                linewidth=.5, cbar_kws={"shrink": .5}, ax=ax)
    else:
        sns.heatmap(df, cmap=cmap, 
                square=True,
                linewidth=.5, cbar_kws={"shrink": .5}, ax=ax)