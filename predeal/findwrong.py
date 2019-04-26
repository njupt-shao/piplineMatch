import json
import sys

def OutputLID(path):
    fin = open(path,'r')
    fout = open(path+'correct','w')
    jsonObj = json.load(fin)
    for item in jsonObj:
        if len(jsonObj[item])!=3:
            print(item)
            fout.write(item+'\t'+str(jsonObj[item])+'\n')


def main():
    OutputLID(r'E:\01sci\code\predeal\zy_line_points_0423.json')

if __name__ == "__main__":
    main()