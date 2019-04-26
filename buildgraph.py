from igraph import *
import json

g = Graph()

def importVertices(point_path):
    point_file = open(point_path,'r')
    lines = point_file.readlines()
    for line in lines:
        line = line.strip()
        g.add_vertices(line)
    

def importEdges(edges_path):
    edges = []
    edges_file = open(edges_path,'r')
    lines = edges_file.readlines()
    num = len(lines)
    for line in lines:
        line = line.strip()
        info = line.split(',')
        edges.append((str(info[0]),str(info[1])))
    g.add_edges(edges)

def cutleaves1(g):
    nodesinfo = {}
    m_edges = []
    for edge in g.get_edgelist():
        m_edges.append([g.vs[edge[0]]['name'],g.vs[edge[1]]['name']])

    for edge in m_edges:
        if g.degree(edge[0])==g.degree(edge[1]) and g.degree(edge[1])==1:
            nodesinfo[edge[0]]='no-parent'
            nodesinfo[edge[1]]='no-parent'
        if g.degree(edge[0])>g.degree(edge[1]) and g.degree(edge[1])==1:
            nodesinfo[edge[1]]=edge[0]
        if g.degree(edge[0])<g.degree(edge[1]) and g.degree(edge[0])==1:
            nodesinfo[edge[0]]=edge[1]
    g.delete_vertices(nodesinfo.keys())
    return nodesinfo


def cuttrees(son_par_path,gfile):
    son_par_json = open(son_par_path,'w',encoding='utf-8')
    new_edges = open(gfile,'w',encoding='utf-8')
    dgree1s =  g.vs.select(_degree = 1)["name"]
    son_par_table = {}
    while len(dgree1s)!=0:
        dgree1s =  g.vs.select(_degree = 1)["name"]
        son_par_table.update(cutleaves1(g)) 
    print(len(g.vs))
    json.dump(son_par_table,son_par_json,indent=2)
    for edge in g.get_edgelist():
        print(g.vs[edge[0]]['name'] + ','+g.vs[edge[1]]['name'])
        new_edges.write(g.vs[edge[0]]['name'] + ','+g.vs[edge[1]]['name']+'\n')

importVertices(r'E:\0327不规则分区\raw_data\points_name.csv')
importEdges(r'E:\0327不规则分区\raw_data\edges_buguize.csv')
print(len(g.vs))
cuttrees('son_par.json','cutted_new_edgs.csv')

