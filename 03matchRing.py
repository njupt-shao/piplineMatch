import json
from igraph import *
import sys
import pickle

zy_point_info = json.load(open(r'data\zy\zy_pointWithID.json','r',encoding='utf-8'))
zy_line_info = json.load(open(r'data\zy\zy_lineWithID.json','r',encoding='utf-8'))
zy_graph = pickle.load(open(r'data\zy\zy_line_points_0423.json_grapn.bin','rb'))

zh_point_info = json.load(open(r'data\zh\zh_pointWithID.json','r',encoding='utf-8'))
zh_line_info = json.load(open(r'data\zh\zh_lineWithID.json','r',encoding='utf-8'))
zh_graph = pickle.load(open(r'data\zh\zh_line_points_0423.json_grapn.bin','rb'))


def geAddLineInfo():
    zy_loclables = []
    zh_loclables = []

    zy_ring_lines = zy_graph.es['lid']
    zh_ring_lines = zh_graph.es['lid']

    zy_line_loclables = []
    zh_line_loclables = []

    zy_line_gjs = []
    zh_line_gjs = []

    zy_line_czs = []
    zh_line_czs = []

    for lid in zy_ring_lines:
        zy_line_loclables.append(zy_line_info[lid]['properties']['SZDL'])
        zy_line_czs.append(zy_line_info[lid]['properties']['CZ'])
        zy_line_gjs.append(zy_line_info[lid]['properties']['GJ'])
    for lid in zh_ring_lines:
        zh_line_loclables.append(zh_line_info[lid]['properties']['SZDL'])
        zh_line_czs.append(zh_line_info[lid]['properties']['CZ'])
        zh_line_gjs.append(zh_line_info[lid]['properties']['GJ'])

    zy_graph.es['cz'] = zy_line_czs
    zy_graph.es['gj'] = zy_line_gjs
    zy_graph.es['loclable'] = zy_line_loclables

    zh_graph.es['cz'] = zh_line_czs
    zh_graph.es['gj'] = zh_line_gjs
    zh_graph.es['loclable'] = zh_line_loclables

    zy_loclables =  list(set(zy_line_loclables))
    zh_loclables =  list(set(zh_line_loclables))

    return zy_loclables,zh_loclables

def classifyLines(zy_loclables):
    loclable = {}
    for lable in zy_loclables:
        print(lable)  
        es = zy_graph.es.select(loclable_eq = lable)
        lable = str(lable)
        loclable[lable] = [e for e in es['lid']]
    return loclable

def main(argv):
    zy_class_path =  r'result/zy_class.json'
    zy_lables , zh_lables = geAddLineInfo()
    zy_classes = classifyLines(zy_lables)

    json.dump(zy_classes,open(zy_class_path,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
    
    print(zy_classes)




if __name__ == "__main__":
    main(sys.argv)