from pymongo import MongoClient
import json


#myfile = json.loads("./indeed_files/job_query-20200816-161725.json")
#print(myfile)
# with open('./job_query-20200818-134504') as f:
#     myfile = json.load(f)

try:
    with open('./indeed_files/job_query-20200818-134504.json') as f:
        data = json.load(f)
        #print(data)
    #myfile = json.loads(data)
except Exception as e:
    print(e)

print(type(data))
#print(myfile)
#print(myfile.items())

#client = MongoClient("mongodb+srv://dang:dang123@dangcluster0.kqvzm.azure.mongodb.net/jobs?retryWrites=true&w=majority")
client = MongoClient("mongodb+srv://rocket:Cerberus#08@rocketanalytics.rhjcr.azure.mongodb.net/Jobs?retryWrites=true&w=majority")
db = client.Jobs
collection = db['Indeed']
collection.insert_many(data)

# for key, value in myfile.items():  #accessing keys
#     try:
#         collection.insert_many(value)
#     except Exception as e:
#         print(e)
    #print(value,end=',')
# if pymongo < 3.0, use insert()
#collection_currency.insert(file_data)
# if pymongo >= 3.0 use insert_one() for inserting one document
#collection_currency.insert_one(file_data)
# if pymongo >= 3.0 use insert_many() for inserting many documents
#collection_currency.insert_many(file_data)

#client.close()
