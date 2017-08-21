import os

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import json
from .models import Info
from . import getData


def home(request):
    return render(request, "webapp/home.html")

"""
#################
# display data  #
#################
"""
def display_data(request):
    # parse data and construct list of cellular relationships
    global_rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes()

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)

    return render(request, "webapp/data.html", {'nodes': global_nodes,
                                                'global_ucell_rel_li': global_ucell_rel_li,
                                                'req_dept_cell_str': req_dept_cell_str,
                                                'req_dept_unique_str':req_dept_unique_str,
                                                'dt_conn_li_str':dt_conn_li_str})


"""
####################
# display contact  #
####################
"""

def contact(request):
    return render(request, "webapp/contact.html")





"""
###################################
# display example Layout - force  #
###################################
"""

def layout_ex(request):
    return render(request, "webapp/py_example_conx.html")




"""
#####################################################
# force layout : connect cells and query by weight  #
#####################################################
"""
def layout_cells(request):
    # parse data and construct list of cellular relationships
    rel_li=getData.readfile()
    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)
    # department cell dictionary - with cells (no Values)
    dept_di=getData.getDept(rel_li)
    # nodes=getNodes(global_dept_di)
    nodes=getData.getNodes()
    # edges as links=[(1,2),(2,3),(3,4),(2,4)]
    edges=getData.getEdges_as_indices(rel_lix,nodes)
    return render(request,"webapp/py_cells_conx.html",{'node_li':nodes,'edge_li':edges, 'edge_li_str':rel_lix })


"""
#############################################################
# force layout : connect departments and query by weight    #
#############################################################
"""
def layout_dept(request):
    # parse data and construct list of cellular relationships
    rel_li=getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di=getData.getDept(rel_li)

    # nodes=getNodes(global_dept_di)
    nodes=getData.getNodes()

    # edges as links=[(1,2),(2,3),(3,4),(2,4)]
    edges=getData.getEdges_as_indices(rel_lix, nodes)

    # department cell dictionary - with Values
    dept_di=getData.getDept(rel_li)

    # department as nodes
    dept_node_li = getData.getDept_asNodes(dept_di, nodes)
    print(dept_node_li)

    # calculate connection between departments INDICES (int,int,float)
    dept_conn_li_idx=getData.getDeptConn_as_Indices(rel_lix, dept_di, dept_node_li)
    print(dept_conn_li_idx)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dept_conn_li_idx, dept_node_li)

    return render(request,"webapp/py_dept_conx.html",{ 'node_li':dept_node_li , 'edge_li':dept_conn_li_idx, 'edge_li_str':dt_conn_li_str })

"""
#################################################################################################
# treemap layout : of cells in one department (only department which have more than 0 cells)    #
#################################################################################################
"""
def dept_cells(request):
    # parse data and construct list of cellular relationships
    rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str=[]
    req_dept_unique_str = []
    for i in dept_di:
        str=i+"-"
        if(len(dept_di[i])>0):
            for j in dept_di[i]:
                print(j)
                str+=j+","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes()

    return render(request, "webapp/py_dept_cells.html", {'req_dept_cell_str':req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str , 'nodes': nodes})

"""
#########################################################
#   treemap layout : of all departments taken together  #
#########################################################
"""
def dept_dept(request):
    # parse data and construct list of cellular relationships
    rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str = []
    req_dept_unique_str = []
    for i in dept_di:
        str = i + "-"
        if (len(dept_di[i]) > 0):
            for j in dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes()
    return render(request, "webapp/py_dept_dept.html",
    {'req_dept_cell_str': req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str, 'nodes': nodes})

"""
#############################################################
#   treemap layout : of all cells in all departments        #
#############################################################
"""
def cells_treemap(request):
    # parse data and construct list of cellular relationships
    rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    rel_lix = getData.rem_dup(rel_li)

    # department cell dictionary - with cells (no Values)
    dept_di = getData.getDept(rel_li)
    req_dept_cell_str = []
    req_dept_unique_str = []
    for i in dept_di:
        str = i + "-"
        if (len(dept_di[i]) > 0):
            for j in dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    nodes = getData.getNodes()
    return render(request, "webapp/py_cells_TM.html",
    {'req_dept_cell_str': req_dept_cell_str, 'req_dept_unique_str': req_dept_unique_str, 'nodes': nodes})

"""
#########################################################################
#   force layout : select multiple departments and draw connections     #
#########################################################################
"""
def se_dept(request):
    # parse data and construct list of cellular relationships
    global_rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes()

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)

    return render(request, "webapp/py_search_dept.html", {'req_dept_cell_str': req_dept_cell_str,
                                                          'req_dept_unique_str': req_dept_unique_str,
                                                          'nodes': global_nodes,
                                                          'dt_conn_li_str':dt_conn_li_str})


"""
##################################################################################
#   force layout : select multiple departments and draw connections for cells   #
##################################################################################
"""
def se_dept_cells(request):
    # parse data and construct list of cellular relationships
    global_rel_li = getData.readfile()

    # from rel_li remove duplicates  a->b = b->a : greater weight
    global_ucell_rel_li = getData.rem_dup(global_rel_li)

    # department cell dictionary - with cells (no Values)
    global_dept_di = getData.getDept(global_rel_li)

    req_dept_cell_str = []
    req_dept_unique_str = []

    for i in global_dept_di:
        str = i + "-"
        if (len(global_dept_di[i]) > 0):
            for j in global_dept_di[i]:
                print(j)
                str += j + ","
            req_dept_cell_str.append(str)
        else:
            req_dept_unique_str.append(i)

    # nodes=getNodes(global_dept_di)
    global_nodes = getData.getNodes()

    # department as nodes
    global_dept_node_li = getData.getDept_asNodes(global_dept_di, global_nodes)

    # calculate connection between departments
    dt_conn_index_li = getData.getDeptConn_as_Indices(global_ucell_rel_li, global_dept_di, global_dept_node_li)

    # calculate connection between departments NAMES (string)
    dt_conn_li_str = getData.getDeptConn_as_Str(dt_conn_index_li, global_dept_node_li)

    return render(request, "webapp/py_search_dept_cells.html", {'req_dept_cell_str': req_dept_cell_str,
                                                          'req_dept_unique_str': req_dept_unique_str,
                                                          'nodes': global_nodes,
                                                          'dt_conn_li_str':dt_conn_li_str})

