# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 07:31:42 2021

@author: Ahmad Al Musawi

Title: Evaluating Complex Networks Evolution [Overleaf.com]
Goal: Use network features for attacking and surviving. 
How can network survive an attack. 
Network survival is defined as keeping network overall properties.

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

networks_path = "standard networks dataset/"
standard_metrics =  ["CN","AA","RA","PA","JA","SA","SO","HPI","HDI","LLHN","CAR", "CH2_L2", 'CH2_L3']
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
         'soc-firm-hi-tech']
datasets = ["\dolphins\out2.txt",
            "\polbooks\out2.txt",
            "\\word_adjacencies.gml\out2.txt",
            "\\arenas-email\out2.txt",
            "Karate",
            "Erdos Renyi",
            "\\USAir97\\USAir97.txt", 
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
            '\\soc-firm-hi-tech\\soc-firm-hi-tech.txt']
Sampling_Nodes = ['Random', 'HDN', 'HBN', 'HCN']
work_path = 'D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/Plots/'
Centr     =['GCC', 'ACC', 'ASP', 'r', 'diam', 'd']



def plot1():
    '''Delete 1% of the nodes based on given centrality and measure the resulted centrality'''
    

def start():
    '''Welcome to Vulnerability and resilience of complex networks'''
    Dataset = [(standard_networks[g], read_graph2(g)) for g in range(len(standard_networks))]
    for i in range(len(Dataset)):
        print(f'{i}- {Dataset[i][0]} - {info(Dataset[i][1])}')
    g = int(input("Enter number of network.. "))
    print(f'You select.... {standard_networks[g]}')
    AT = int(input('Enter attachment/deletion based method\n0- Random\n1- Degree\n2-Betweenness\n3- Clustering...'))
    perc = int(input('Enter value between 0-100 as sampling/attacking percentage...'))/100
    itrs  = int(input('Enter number of iterations...'))
    G = Dataset[g][1]
    C = []
    for i in range(itrs):
        print()
        C.append(centralities(G))
        Gd, Ed = attack(G, perc, AT)  
        D = G.nodes() - Gd.nodes()
        print(f'difference in nodes = {len(D)}')
        if D!= []:
            Gd.add_edges_from([(d, random.choice(list(Gd.nodes()))) for d in D])#randomly attaching deleted nodes
            G = construct(Gd, Ed-len(D), AT)
        else:
            break
    df =  DataFrame(C, columns=Centr)
    
    # df.plot.set_xlabel('Iterations', fontsize=8)
    # df.plot.set_title(standard_networks[g])
    df.plot.area(stacked=False);


def construct(G, E, AT):
    '''G: graph to reconstruct
       D: Nodes to be added.
       E: number of edges to be added to G
       AT: attachment type(0: RND, 1:DGR, 2: BTW, 3: CLST'''

    if AT==0:
        for _ in range(E):
            x = random.choice(list(G.nodes()))
            y = random.choice(list(G.nodes()))
            G.add_edge(x,y)
    elif AT==1:
        #Degree based Preferrential Attachment...
        degrees = [(n, d) for n, d in G.degree()]
        selected_nodes = preferrential_attachment(degrees, E)
        # print(f'Connecting Nodes...\n{len(selected_nodes)}')
        # print(f'Number of edges....\n{E}')
        G = LinkPrediction(G, selected_nodes)
        
    return G

def LinkPrediction(G, SN):
    '''G: Graph
    SN: selected nodes
    Aim: for each node in Selected_Nodes, we search all not-neighbors,
    and for all given LP metrics we select the node with the most significant
    result. 
    However, we will got 2d matrix, columns are metrics and rows are non-neighbor nodes.'''
    final_links = []
    for x in SN:
        Nei_x = G.neighbors(x)
        Not_Nei_x = G.nodes() - Nei_x
        P = [[(x, y, LP(a, G, Nei_x, G.neighbors(y), x, y), a) for y in Not_Nei_x] for a in standard_metrics]
        for L in P:
            print(f'L = {L}\n')
            final, mx = 0, 0
            for x, y, v, a in L:
                if v>mx:
                    final = v
            if v!=0:
                final_links.append((x,final))    
            else:
                final_links.append((x, random.choice(list(Not_Nei_x))))
    G.add_edges_from(final_links)
    return G




def attack(G, perc, AT):
    '''Return 
    Gd: graph G after removing D nodes.
    D: deleted nodes, 
    Ed: number of deleted edges
    AT: Attachment type...'''
    D = []
    e1 = len(G.edges())
    Gd = nx.Graph()
    Gd = G.copy()

    N = int(len(G.nodes())*perc)
    D = Sampling(G, AT, N) #Top dominant nodes (degree, betweenness etc..)
    print(f'Attacking {N} out of {len(G.nodes())}...')
    print(f'D = {len(D)}')
    Gd.remove_nodes_from(D)
    Gd.remove_nodes_from([n for n, d in Gd.degree() if d==0])
    e2 = len(Gd.edges())
    # return G, D + zero_degree_nodes, e1-e2 
    return Gd, e1-e2 


def Sampling(G, AT, sh):
    '''G: graph to sample;
       AT: attachment type;
       sh: number of nodes to retreive..'''
    if AT==0:
        return sample(list(G.nodes()), sh)
    elif AT==1:
        N = sorted(G.degree, key=lambda x: x[1], reverse=True)
        return [x for x,_ in N[:sh]]
    elif AT==2:
        N = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)
        return [x for x,_ in N[:sh]]
    elif AT==3:
        N = sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)
        return [x for x,_ in N[:sh]]

def centralities(G):
    
    GCC = nx.transitivity(G)
    ACC = nx.average_clustering(G)
    d = nx.density(G)
    r = nx.degree_assortativity_coefficient(G)    
    lcg = sorted(nx.connected_components(G), key=len, reverse=True)
    LCG = G.subgraph(lcg[0])    
    ASP = nx.average_shortest_path_length(LCG)
    diam = nx.diameter(LCG)
    return [ GCC, ACC, ASP, r, diam, d]


def read_graph2(g):
    if g==4:
        G = nx.karate_club_graph()
    elif g==5:
        # nodes = int(input("enter number of nodes?"))
        # edges= int(input("enter number of edges?"))
        G = nx.gnm_random_graph(500, 1500)
    elif g==11:
        # nodes = int(input("enter number of nodes?"))
        # edges= int(input("enter number of edges?"))
        # p = int(input("enter P value?"))
        G = nx.barabasi_albert_graph(500, 3)
    elif g in [6,7, 12,13,14,15,16,17]:
        file = open(networks_path + datasets[int(g)])
        lines=  file.readlines()
        G = nx.Graph()
        for line in lines:
            N = line.split(" ")
            G.add_edge(N[0], N[1])
    else:
        G = nx.read_adjlist(networks_path + datasets[int(g)], create_using = nx.Graph(), nodetype = int)
    return G
def info(G):
    return f'|V|\t=\t{len(G.nodes())}\t|E|\t=\t{len(G.edges())}'

# def attack(G, s):
#     '''Attaaaaack!'''
#     print('Attaaaaaaaaaaack')
#     g, name = read_graph2(G), networks[G]
#     print(info(g))
#     # what is the attack scenario?
#     results = [centralities(g)]
#     thresh = int(len(g.nodes())/4)
#     shell  = int(len(g.nodes())/25)
#     # s = int(input(f'Enter {Sampling_Nodes}'))
#     # print(f'You selected {Sampling_Nodes[s]}...')
#     while len(g.nodes())>= thresh:
#         print(f'{info(g)} : {thresh}')
#         to_be_deleted = Sampling(g, s, shell)
#         g.remove_nodes_from(to_be_deleted)
#         results.append(centralities(g))
#     df = DataFrame(results, columns=(cols))
#     title = f'{name}, Shell = {thresh}, {Sampling_Nodes[s]}, 0.25'
#     # df.plot(y=df.columns, kind='line')
#     # plt.title(title)
#     # plt.savefig(work_path+title+'.png')
#     df.to_csv(work_path +  title + '.csv')

#     plt.show()
#     return df


       
    
# def centralities(network):
#     degrees = [network.degree[i] for i in network.nodes()]
#     lcg = sorted(nx.connected_components(network), key=len, reverse=True)
#     LCG = network.subgraph(lcg[0])
    
#     GCC = nx.transitivity(network)
#     ACC = nx.average_clustering(network)
#     ASP = nx.average_shortest_path_length(LCG)
#     diam = nx.diameter(LCG)
    
#     g = gini(np.array(sorted(degrees)))
#     d = nx.density(network)
#     # r = nx.degree_assortativity_coefficient(network)

#     cl = ave(nx.closeness_centrality(network))
#     b = ave(nx.betweenness_centrality(network))
#     PR = ave(nx.pagerank(network))
#     h = ave(nx.harmonic_centrality(network))
#     # k = nx.katz_centrality(LCG)

#     return [GCC, ACC, ASP, h, diam, g, d, cl, b, PR]
#     # eg = nx.eigenvector_centrality(network.to_undirected())

def ave(X):
    return sum([i for i in X.values()])/len(X)

def gini(x):
    # (Warning: This is a concise implementation, but it is O(n**2)
    # in time and memory, where n = len(x).  *Don't* pass in huge
    # samples!)

    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g


def plotting_csv():
    my_path = 'D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/Results/'
    from os import listdir
    from os.path import isfile, join
    myFiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    for i in myFiles:
        print(i)
    All = [(sh, pd.read_csv(my_path+sh)[cols]) for sh in myFiles]
    for f in cols:
        for a in ['HDN', 'HBN', 'HCN']:
            df = DataFrame()
            for name, data in All:
                network_name = name.split(',')[0]
                attack_method = name.split(',')[-2].replace(" ", "")
                print(attack_method)
                if a ==attack_method:
                    print('matched')
                    df[f'{network_name}'] = data[f]
            df.plot(y=df.columns, kind='line')
            plt.title(f'{f} performance, {a}')
            # plt.savefig(work_path+title+'.png')
            plt.show()


def corr_analysis():
    my_path = 'D:/Documents/Research Projects/Complex Networks Researches/Attack and Survive Model/Programming/Results/'
    from os import listdir
    from os.path import isfile, join
    myFiles = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    for i in myFiles:
        print(i)
    All = [(sh, pd.read_csv(my_path+sh)) for sh in myFiles]
    df = pd.concat([a for _, a in All])[cols]
    print(df)
    corr = df.corr()
    sns.heatmap(corr)
    return df

def loglog(df):
    x = np.log(df['GCC'])
    y = np.log(df['ACC'])
    fig = plt.figure()
    plt.scatter(x, y, c='blue', alpha=0.05)
    
    

