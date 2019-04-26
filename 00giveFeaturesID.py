import sys
import json


def getFeaturs(jsonpath):
    jfile = open(jsonpath,'r',encoding='utf-8')
    jobject = json.load(jfile)
    features = jobject['features']
    return features

def main(argv):
    id_feature_dic ={}
    jsonpath = argv[1]
    jsonpath2 = argv[1][:-5]+'WithID.json'

    features = getFeaturs(jsonpath)
    ftypeID = ''
    if argv[2] == 'l':
        ftypeID = 'lid'
    if argv[2]=='p':
        ftypeID = 'pid'
    for feature in features:
        id_feature_dic[str(feature['properties'][ftypeID])]=feature
    json.dump(id_feature_dic,open(jsonpath2,'w',encoding='utf-8'),indent=4,ensure_ascii=False)
    return json.dumps(id_feature_dic,indent=4,ensure_ascii=False)



if __name__ == "__main__":
   print (main(sys.argv))