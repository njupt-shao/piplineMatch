from igraph import *
import json
import sys
import pickle



def importVertices(point_path):
    fin = open(point_path,'r',encoding='utf-8')
    points = json.load(fin)
    vertices = points.keys()
    return vertices

def importEdges(edge_path):
    fin = open(edge_path,'r',encoding='utf-8')
    edges = json.load(fin)
    edges_info = {}
    edge_names = edges.keys()
    for name in edge_names:
        pids = edges[name][:2]
        pids = sorted(pids)
        pids.append(edges[name][-1])
        edges_info[name] = pids
    return edges_info

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

def main(argv):
    g = Graph()
    print("generate Vs")
    vs = importVertices(argv[1])
    # print(vs)
    print("generate es")
    es = importEdges(argv[1])
    # print(es)
    print("build g")
    g = buildGrapg(vs,es)
    print(g)



if __name__ == "__main__":
    main(sys.argv)