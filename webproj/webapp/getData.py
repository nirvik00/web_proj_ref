import os
import networkx as nx
from operator import itemgetter
from matplotlib import pyplot as plt
from django.conf import settings


def readfile():
    file = open(os.path.join(settings.PROJECT_ROOT, 'adj_graph.dat'))
    rel_li=[]
    di={}
    k=0
    for line in file:
        #print(str(k) + ") "+ line)
        s0=line.split(",")[0] # node being queried
        s1=line.split(",")[1] # connected to
        s2=line.split(",")[2] # weight of connection
        rel_li.append([s0,s1,s2])
        di[s0]=s1
        k+=1
    return rel_li


def cell_belongs_dept(cell, dt_di):
    req_dt=""
    for i in dt_di:
        cells=dt_di[i]
        if len(cells)>0:
            for j in cells:
                if(j==cell):
                    #print(i+","+cell)
                    req_dt=i
                    break
    if req_dt=="":
        for i in dt_di:
            if i==cell:
                req_dt=i
                break
    return req_dt


def rem_dup(rel_li):
    cell_rel_li=[]
    for i in rel_li:
        #print("initial : %s , %s , %s" % (i[0], i[1], i[2]))
        try:
            u0=i[0].split("-")[1]
        except:
            u0=i[0]
        try:
            u1 = i[1].split("-")[1]
        except:
            u1 = i[1]
        w=i[2]
        #print("adding : %s , %s , %s" %(u0,u1,w))
        cell_rel_li.append([u0,u1,w])

    rem_li=[]
    for i in cell_rel_li:
        u0=i[0]
        u1=i[1]
        w0=i[2]
        for j in cell_rel_li:
            v0=j[0]
            v1=j[1]
            w1=j[2]
            if u0==v1 and u1==v0:
                rem_li.append(j)

    for i in rem_li:
        try:
            cell_rel_li.remove(i)
        except:
            pass

    for i in cell_rel_li:
        #print(i)
        pass
    return  cell_rel_li


def getDept(rel_li):
    dept_li=[] # dept list [names...]
    dept_di={} # dept dictionary {dept:cells,...,...}

    for i in rel_li:
        s0=i[0]
        s0_li=s0.split("-")
        s1=s0_li[0]
        if(s1 not in dept_li):
            dept_li.append(s1)

    for i in dept_li:
        cell_li = []
        for j in rel_li:
            try:
                s0 = j[0].split("-")[0] # dept
                s1 = j[0].split("-")[1] # cell
                if(s0==i):
                    cell_li.append(s1)
            except:
                pass
        cell_set=set(cell_li)
        cell_li=list(cell_set)
        dept_di.update({i:cell_li})

    for i in dept_di:
        #print("- "+i)
        if(len(dept_di[i])>0):
            #print(" . "+str(dept_di[i]))
            pass

    return dept_di


def getNodes():
    file = open(os.path.join(settings.PROJECT_ROOT, 'adj_graph_node_wt.dat'))
    hc_nodes=[]
    for line in file:
        s0=line.split(";")[0] # node being queried
        try:
            s01=s0.split("-")[1]
            pass
        except:
            s01=s0
        w0 = line.split(";")[1]  # node being queried
        hc_nodes.append([s01,w0])

    node_li=[]
    for i in hc_nodes:
        if(i not in node_li):
            node_li.append(list(i))

    return node_li


def getEdges_as_indices(rel_lix, nodes_li):
    edge_li=[]
    for i in rel_lix:
        u = i[0]
        v = i[1]
        w = i[2]
        req_idx_u = 0
        req_idx_v = 0
        for j in range(0, len(nodes_li),1):
            if(u==nodes_li[j][0]):
                req_idx_u=j
                break
        for j in range(0, len(nodes_li),1):
            if(v==nodes_li[j][0]):
                req_idx_v=j
                break
        edge_li.append( [ req_idx_u, req_idx_v, w ] )
        #print(i)
    return edge_li



def getDept_asNodes(dept_di, node_li):
    dept_nodes=[]
    f_dept_li=[]
    for i in dept_di:
        sum=0
        cell_li=dept_di[i]
        if(len(cell_li)>0):
            for j in node_li:#node_li=[name, headcount]
                for k in cell_li:#cell_li=[name]
                    if(k==j[0]):
                        sum+=int(j[1])
        else:
            for j in node_li:#node_li=[name, headcount]
                if(i==j[0]):
                    sum+=int(j[1])

        if i not in dept_nodes:
            dept_nodes.append([i,sum])

    return dept_nodes


def getDeptConn_as_Indices(rel_lix, dept_di, dept_nodes):
    dt_rel_li=[]
    for i in rel_lix:
        #print("rel_lix : %s -> %s = %s" %(i[0], i[1], i[2]))
        s0=i[0]
        s1=i[1]
        w0=i[2]
        x=cell_belongs_dept(s0, dept_di)
        y=cell_belongs_dept(s1, dept_di)
        if y=="":
            #print( "not defined : %s -> %s "%(s0,s1))
            pass
        #print("dept : %s -> %s = %s" % (x, y, w0))
        dt_rel_li.append([x,y,w0])

    dtf_rel_li=[]
    for i in dt_rel_li:
        #print(" f = " + str(i))
        s0 = i[0]
        s1 = i[1]
        w0 = i[2]
        w = float(w0)
        x_dt=[]
        for j in dt_rel_li:
            u0 = j[0]
            u1 = j[1]
            w1 = j[2]
            if u0==s0 and u1==s1:
                w+=float(w1)
        x_dt.append([s0,s1,w])
        if x_dt not in  dtf_rel_li:
            dtf_rel_li.append([s0,s1,w])

    dtf_rel_idx_li=[]
    for i in dtf_rel_li:
        #print(str(i))
        u=i[0]
        v=i[1]
        w=i[2]
        reqS=0
        reqT=0
        for j in range(0,len(dept_nodes),1):
            if(u==dept_nodes[j][0]):
                reqS=j
                break

        for j in range(0,len(dept_nodes),1):
            if(v==dept_nodes[j][0]):
                reqT=j
                break
        li=[reqS, reqT, w]
        if reqT>0 and reqS>0 and li not in dtf_rel_idx_li:
            dtf_rel_idx_li.append(li)

    fi_li=[]
    for i in dtf_rel_idx_li:
        fi_li.append([i[0], i[1], i[2]])
        #print(i)
        pass
    return fi_li


def getDeptConn_as_Str(dt_id_li, dept_node_li):
    dt_li=[]
    for i in dt_id_li:
        u=int(i[0])
        v=int(i[1])
        w=int(i[2])
        a=dept_node_li[u][0]
        b=dept_node_li[v][0]
        li=[a,b,w]
        if(li not in dt_li):
            dt_li.append(li)

    for i in dt_li:
        #print("final : "+str(i))
        pass

    return dt_li


"""
1. UNIQUE DATA SET
# relationship list between cells
     # if a->b => b->a (redundant relations)
     # based on greater weight, either a->b@w0 or b->a@w1

2. TREE LOGIC IS NOT POSSIBLE
{a,b,c,d,e,f,g}
a->b
b->g
c->f
d->g
e->g
"""
