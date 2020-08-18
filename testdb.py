from pymongo import MongoClient
import json


#myfile = json.loads("./indeed_files/job_query-20200816-161725.json")
#print(myfile)
with open('./indeed_files/job_query-20200816-161725.json') as f:
    myfile = json.load(f)

#print(myfile)
#print(myfile.items())

client = MongoClient("mongodb+srv://dang:dang123@dangcluster0.kqvzm.azure.mongodb.net/jobs?retryWrites=true&w=majority")
db = client.jobs
collection = db['indeed']

for key, value in myfile.items():  #accessing keys
    try:
        collection.insert_one(value)
    except Exception as e:
        print(e)
    #print(value,end=',')
# if pymongo < 3.0, use insert()
#collection_currency.insert(file_data)
# if pymongo >= 3.0 use insert_one() for inserting one document
#collection_currency.insert_one(file_data)
# if pymongo >= 3.0 use insert_many() for inserting many documents
#collection_currency.insert_many(file_data)

#client.close()
