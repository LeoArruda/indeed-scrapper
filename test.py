from pprint import pprint
import json

l = [['String 1'],['String 2'],['String 3'],['String 4'],['String 5'],['String 6'],['String 7'],['String 8'],['String 9'],['String 10'],['String 11']] 
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

result = [{"title%d" % (i+1): chunk[i][0] for i in range(len(chunk))} for chunk in chunks(l, 7)]
#pprint(result)
a = [0, 'String 1',1,'String 3', 2,'String 5',6,'String 7',8,'String 9'] 
json.dumps(a)