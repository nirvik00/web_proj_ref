import os
from django.conf import settings
import networkx as nx
from matplotlib import pyplot as plt


def read_local():
    #file=open("adj_graph.dat", "r")
    file=open(os.path.join(settings.PROJECT_ROOT,'adj_graph.dat'))
    dept_li=[]
    rel_li=[]

    di={}
    k=0
    for line in file:
        #print(str(k) + ") "+ line)
        s0=line.split(",")[0]
        s1=line.split(",")[1]
        s2=line.split(",")[2]
        rel_li.append([s0,s1,s2])
        di[s0]=s1
        k+=1

    node_li=[]
    for i in rel_li:
        a=i[0]
        if(a in node_li):
            pass
        else:
            node_li.append(a)
            print(a)

    edge_li=[]
    for i in rel_li:
        a=i[0]
        b=i[1]
        edge_li.append((a,b))
        #print(i)

    for d in di:
        print("dict: "+str(d)+ ","+(di[d]))

    G=nx.Graph()
    #n=[1,2,3,4]
    G.add_nodes_from(node_li)
    #e=[(1,2),(2,3),(3,4),(2,4)]
    G.add_edges_from(edge_li)
    nx.draw(G)
    #plt.show()
    return rel_li
