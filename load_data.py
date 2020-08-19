import base64
import json
import logging
from datetime import datetime
import time
import os
import traceback
import time
import shutil
import logging
import configparser
from pymongo import MongoClient



    

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    allFiles = list()

    for (dirpath, dirnames, filenames) in os.walk(dirName):
        for file in filenames:
            if file.endswith(".json"):
                allFiles += [os.path.join(dirpath, file)]
                
    return allFiles

def moveFilesTo(source, dest):
    # move a file to a new location
    print('Moving content from [{}] to [{}]'.format(source, dest))
    try:
        shutil.copy2(source, dest)
        os.remove(source)
    except Exception as e:
        print(type(e))
        logging.error('Error: {}'.format(e))

def ingestData(filename, dbUrl, dbUser, dbPass):
    try:
        with open(filename) as f:
            data = json.load(f)
    except Exception as e:
        logging.error('Error: {}'.format(e))
    
    client = MongoClient("mongodb+srv://rocket:Cerberus#08@rocketanalytics.rhjcr.azure.mongodb.net/Jobs?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
    db = client.Jobs
    collection = db['Indeed']
    try:
        collection.insert_many(data)
    except Exception as e:
        logging.error('Error: {}'.format(e))


def ingestFiles(sourceFolder, archiveFolder, dbUrl, dbUser, dbPass):
    # Get the list of all files in directory tree at given path
    print('Getting the list of files {}'.format(sourceFolder))
    listOfFiles = getListOfFiles(sourceFolder)
    print(listOfFiles)
    counter = 0
    
    # Print the files    
    for elem in listOfFiles:
        counter += 1
        try:
            ingestData(elem, dbUrl, dbUser, dbPass)
        except Exception as e:
            logging.error('Error: {}'.format(e))
            
        logging.info("{} Processing file {}".format(counter, elem.replace("\\","/")))
			
    # Archive files
    for origin in listOfFiles:
        logging.info('Moving: {} '.format(origin.replace("\\","/")))
        moveFilesTo(origin.replace("\\","/"), archiveFolder.replace("\\","/"))
         
 
def main():
    logging.info('== START ==')
    config = configparser.ConfigParser()
    try:
        config.read('./config.ini')
    except Exception as e:
        print('ERROR: Cannot read configuration file. [{}]'.format(e))
        logging.info('ERROR: Cannot read configuration file. [{}]'.format(e))

    source_folder = config['INGEST']['SOURCE_LOCATION'].strip("'")
    archive_folder =  config['INGEST']['ARCHIVE_LOCATION'].strip("'")
    dbUrl =  config['DATABASE']['URL'].strip("'")
    dbUser =  config['DATABASE']['USER'].strip("'")
    dbPass =  config['DATABASE']['PASSWD'].strip("'")

    ingestFiles(source_folder, archive_folder, dbUrl, dbUser, dbPass) 
    
    logging.info('== END ==')

        
if __name__ == '__main__':

    LOG_FILENAME = datetime.now().strftime('./log/IngestFiles_%H_%M_%S_%d_%m_%Y.log')
		
    #Log format
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	
    main()
