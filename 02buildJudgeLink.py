import json
import sys

def buildLink(s_p_path):
    s_p = json.load(open(s_p_path,'r'))
    sons = s_p.keys()
    parents = []
    for son in s_p:
        parents.append(s_p[son])
    sons = set(sons)
    parents = set(parents) 
    true_parent = parents - sons
    s_l = {}
    for son in s_p:
        logiclink = []
        p = s_p[son]
        while p not in true_parent:
            logiclink.append(p)
            newson = p
            p = s_p[newson]
        logiclink.append(p)
        s_l[son] = logiclink
    return s_l

    # print(true_parent,len(true_parent))


def main(argv):
    print(argv[1])
    x = argv[1]#'data/zy/zy_line_points_0423.json_son_parent.json'
    s_l = buildLink(x)

    json.dump(s_l,open(x+'_link.json','w'),indent=2)

if __name__ == '__main__':
    main(sys.argv)
    