from igraph import *
import json
import sys
import pickle


def importEdges(edge_path):
    fin = open(edge_path,'r',encoding='utf-8')
    edges = json.load(fin)
    Vertices = []
    edges_info = {}
    edge_names = edges.keys()
    for name in edge_names:
        pids = edges[name][:2]
        pids = sorted(pids)
        pids = [item for item in map(str,pids)]
        Vertices.extend(pids)
        pids.append(edges[name][-1])
        edges_info[name] = pids
    return Vertices,edges_info

def buildGrapg(vs,edges_info):
    g = Graph()
    g.add_vertices(vs)
    enames = []
    pidPairs = []
    weights = []
    for ename in edges_info:
        enames.append(ename)
        pidPair = edges_info[ename][:2]
        map(str,pidPair)
        pidPairs.append(pidPair)
        weights.append(edges_info[ename][-1])
    g.add_edges(pidPairs)
    g.es['lid'] = enames
    g.es['weight'] = weights
    return g

def cutleaves(g):
    nodesinfo = {}
    for edge in g.get_edgelist():
        pid1index = edge[0]
        pid2index = edge[1]
        vs = g.vs['name']
        pid1 = vs[pid1index]
        pid2 = vs[pid2index]
        if g.degree(pid1index)==g.degree(pid2index) and g.degree(pid2index)==1:
            nodesinfo[pid1]='no-parent'
            nodesinfo[pid2]='no-parent'
        if g.degree(pid1index)>g.degree(pid2index) and g.degree(pid2index)==1:
            nodesinfo[pid2]=pid1
        if g.degree(pid1index)<g.degree(pid2index) and g.degree(pid1index)==1:
            nodesinfo[pid1]=pid2
    g.delete_vertices(nodesinfo.keys())
    return nodesinfo,g

def cuttrees(g):
    degree1s = g.vs.select(_degree = 1)["name"]
    son_par_table = {}
    while len(degree1s) != 0:
        degree1s =  g.vs.select(_degree = 1)["name"]
        n,g = cutleaves(g)
        son_par_table.update(n)   
        # print(len(g.vs),len(degree1s))
    degree0s = g.vs.select(_degree = 0)
    g.delete_vertices(degree0s)
    return son_par_table,g
    



def main(argv):
    x = argv[1]
    # x = 'data/zh/zh_line_points_0423.json'

    print("generate es")
    vs,es = importEdges(x)
    # print(es)
    print("build g")
    g = buildGrapg(vs,es)

    print('cut leaves')
    n,g = cutleaves(g)

    print('cut trees')
    s_p,g = cuttrees(g)
    print(len(g.vs),len(g.es))

    print('output result')
    s_p_path = x + '_son_parent.json'
    g_path = x + '_grapn.bin'

    json.dump(s_p,open(s_p_path,'w'),indent=2)
    pickle.dump(g,open(g_path,'wb'))

    print('done')

    



if __name__ == "__main__":
    main(sys.argv)