# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:48:59 2022

@author: Ahmad Al Musawi
"""
import networkx as nx
import math

def LP(a, gT, Nx, Ny, x, y):
    if a=="CN":
        return CN(gT, Nx, Ny)
    if a=="AA":
        return AA(gT, Nx, Ny)
    if a=="RA":
        return RA(gT, Nx, Ny)
    if a=="PA":
        return PA(gT, Nx, Ny)
    if a=="JA":
        return JA(gT, Nx, Ny)
    if a=="SA":
        return SA(gT, Nx, Ny)
    if a=="SO":
        return SO(gT, Nx, Ny)
    if a=="HPI":
        return HPI(gT, Nx, Ny)
    if a=="HDI":
        return HDI(gT, Nx, Ny)
    if a=="LLHN":
        return LLHN(gT, Nx, Ny)
    if a=="CAR":
        return CAR(gT, Nx, Ny)
    if a=="DAGI":
        return DAGI(gT, Nx, Ny)
    if a=="DALI":
        return DALI(gT, Nx, Ny)
    if a=="inDAGI":
        return inDAGI(gT, Nx, Ny)
    if a=="inDALI":
        return inDALI(gT, Nx, Ny)
    if a=="distance":
        return distance(gT, x, y)
    if a=="PAGI":
        return PAGI(gT, Nx, Ny)
    if a=="PALI":
        return PALI(gT, Nx, Ny)
    if a=='CH2_L2':
        return CH2_L2(gT, Nx, Ny, x, y)
    if a=='CH2_L3':
        return CH2_L3(gT, Nx, Ny, x, y)

    
    
    
def distance(G, s, t):
    try:
        dd =  nx.shortest_path_length(G, s, t)
        if dd > 0 :
            return len(G.nodes())/nx.shortest_path_length(G, s, t)
        else:
            return 0
    except (nx.NetworkXNoPath, ValueError):
        return 0


def DAGI(G, x, y):
    """Global Influence: abstract value of the difference in influence between x, y in comparison to network average degree"""
    deg = sum(d for _, d in G.degree()) / float(G.number_of_nodes())   
    tu = len(x)/deg
    tv = len(y)/deg
    potential  = abs(tu-tv)
    return potential

def DALI(G, x, y):
    """Local Influence: abstract value of the difference in influence between x, y in comparison to nodes' neighbor average degree"""
    ax = set(x)
    ay = set(y)
    if len(ax)!= 0:
        sum1 = sum([G.degree(i) for i in ax])/len(ax)
        tu = len(x)/(sum1)
    else:
        tu = 0
    if len(ay)!= 0 :
        sum2 = sum([G.degree(i) for i in ay])/len(ay)
        tv = len(y)/(sum2)
    else:
        tv = 0

    potential  = abs(tu - tv)
    return potential


def inDAGI(G, x, y):
    """Global Influence: abstract value of the difference in influence between x, y in comparison to network average degree"""
    deg = sum(d for _, d in G.degree()) / float(G.number_of_nodes())   
    tu = len(x)/deg
    tv = len(y)/deg
    potential  = abs(tu-tv)
    if potential==0:
        return 1
    else:
        return (1/potential)

def inDALI(G, x, y):
    """Local Influence: abstract value of the difference in influence between x, y in comparison to nodes' neighbor average degree"""
    ax = set(x)
    ay = set(y)
    if len(ax)!= 0:
        sum1 = sum([G.degree(i) for i in ax])/len(ax)
        tu = len(x)/(sum1)
    else:
        tu = 0
    if len(ay)!= 0 :
        sum2 = sum([G.degree(i) for i in ay])/len(ay)
        tv = len(y)/(sum2)
    else:
        tv = 0
    potential  = abs(tu - tv)
    if potential==0:
        return 1
    else:
        return (1/potential)



def PAGI(G, x, y):
    """Pereferential Attachment based abstract value of the difference in influence between x, y 
    in comparison to network average degree"""
    deg = sum(d for n, d in G.degree()) / float(G.number_of_nodes())   
    tu = len(x)/deg
    tv = len(y)/deg
    potential  = tu * tv
    return (potential)

def PALI(G, x, y):
    """Pereferential Attachment based abstract value of the difference in influence between x, y 
    in comparison to nodes' neighbor average degree"""
   
    ax = set(x)
    ay = set(y)
    if len(ax)!= 0:
        sum1 = sum([G.degree(i) for i in ax])/len(ax)
        tu = len(x)/(sum1)
    else:
        tu = 0
    if len(ay)!= 0 :
        sum2 = sum([G.degree(i) for i in ay])/len(ay)
        tv = len(y)/(sum2)
    else:
        tv = 0
    potential  = tu * tv
    return (potential)

def CN(G, x, y):
    'common neighbor'
    ax = set(x)
    ay = set(y)
    return  abs(len(ax.intersection(ay)))

def AA(G,x,y):
    'Adamic-Adar index'
    ax = set(x)
    ay = set(y)
    az = ax.intersection(ay)
    sum = 0
    for z in az:
        L = math.log(len(list(G.neighbors(z))))
        # print (L)
        if L != 0 :
            sum = sum + (1/L)
    return sum 

def RA(G, x, y):
    ax = set(x)
    ay = set(y)
    sum = 0 
    for z in (ax.intersection(ay)):
        sum = sum + abs(1/len(list(G.neighbors(z))))
    return sum 

    
def PA(G, x, y):
    'Preferential Attachment'
    ax = set(x)
    ay = set(y)
    return  len(ax)*len(ay)

def JA(G, x, y):
    'Jaccard Index'
    ax = set(x)
    ay = set(y)
    if len(ax.union(ay))!=0 :
        return  len(ax.intersection(ay))/len(ax.union(ay))
    else:
        return 0

def SA(G, x, y):
    'Salton Index'
    ax = set(x)
    ay = set(y)
    if len(ax)!=0 and len(ay)!=0:
        return len(ax.intersection(ay))/math.sqrt(len(ax)*len(ay))
    else:
        return 0

def SO(G, x, y):
    'Sorensen Index'
    ax = set(x)
    ay = set(y)
    if (len(ax)+len(ay))!=0:
        return  2* len(ax.intersection(ay))/(len(ax)+len(ay))
    else:
        return 0

def HPI(G, x, y):
    'Hub Pronoted Index'
    ax = set(x)
    ay = set(y)
    if len(ax)!=0 and len(ay)!=0:
        return  len(ax.intersection(ay))/min(len(ax), len(ay))
    else:
        return 0

def HDI(G, x, y):
    'Hub Depressed Index'
    ax = set(x)
    ay = set(y)
    if max(len(ax), len(ay))!=0:
        return  len(ax.intersection(ay))/max(len(ax), len(ay))
    else:
        return 0
    
def LLHN(G, x, y):
    'Local Leicht-Homle-Newman Index'
    ax = set(x)
    ay = set(y)
    if len(ax)!=0 and len(ay)!=0:
        return  len(ax.intersection(ay))/len(ax)*len(ay)
    else:
        return 0

def CAR(G, x, y):
    ax = set(x)
    ay = set(y)
    sum = 0 
    for z in (ax.intersection(ay)):
        az = G.neighbors(z)
        if len(list(az)) != 0:
            dom = len(ax.intersection(ay.intersection(set(G.neighbors(z)))))
            nom = len(list(G.neighbors(z)))
            sum = sum + (dom/nom)
    return sum

def CH2_L2(G, Nx, Ny, x, y):
    ai = set(Nx)
    aj = set(Ny)
    S = 0
    for x in (ai.intersection(aj)):
        c_x = len(set(G.neighbors(x)).intersection(ai.intersection(aj)))
        A = set(G.neighbors(x))
        B = set(ai.intersection(aj))
        ij= set([x,y])
        o_x = len(A-B-ij)
        S += (1 + c_x)/(1 + o_x)
    if S== None:
        return 0
    else:
        return S
    
def CH2_L3(G, Nx, Ny, i, j):
    ai = set(Nx)
    aj = set(Ny)
    S = 0
    for x in ai:
        for y in aj:
            if G.has_edge(x,y):
                setx = set()
                for p in nx.all_simple_paths(G, i, j, cutoff=3):
                    set_px = set(p)
                    for it in set_px:
                        # if it != i and it != j:
                        setx.add(it)
                sety = set()
                for p in nx.all_simple_paths(G, i, j, cutoff=3):
                    set_py = set(p)
                    for it in set_py:
                        # if it != i and it != j:
                        sety.add(it)
                cdx = sum([1 for k in setx if G.has_edge(k,x)])
                cdy = sum([1 for k in sety if G.has_edge(k,y)])
                
                NNx = list(G.neighbors(x))
                NNy = list(G.neighbors(y))   
                for e in [i,j] + [k for k in setx if G.has_edge(k,x)]:
                    if e in NNx:
                        NNx.remove(e)
                for e in [i,j] + [k for k in setx if G.has_edge(k,x)]:
                    if e in NNy:
                        NNy.remove(e)
                odx = len(NNx)
                ody = len(NNy)
                S+= math.sqrt((1+cdx)*(1+cdy))/math.sqrt((1+odx)*(1+ody))
    if S== None:
        return 0
    else:
        return S
