"""This module contains the user interface"""
import scrapper
import url_utilities
import configparser
import time
import json
import csv


def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    JOB_TITLE = config['DEFAULT']['JOB_TITLE']
    JOB_LOCATION = config['DEFAULT']['LOCATION']
    JOB_RADIUS = config['DEFAULT']['RADIUS']
    JOB_TYPE = config['DEFAULT']['JOB_TYPE']
    JOB_AGE = config['DEFAULT']['JOB_AGE']
    FILE_DESTINATION = config['DEFAULT']['FILE_DESTINATION'].strip('"')
    timeStr = time.strftime("%Y%m%d-%H%M%S")
    try:
        JOB_RADIUS = int(JOB_RADIUS)
    except ValueError:
        JOB_RADIUS = 0
    
    try:
        JOB_AGE = int(JOB_AGE)
    except ValueError:
        JOB_AGE = 0
        
    url_maker = url_utilities.urlMaker(job_title = JOB_TITLE, location = JOB_LOCATION,radius = JOB_RADIUS,job_type = JOB_TYPE, age=JOB_AGE)
    url_maker.build_url()
    print(url_maker.url)
    query = scrapper.Query(url_maker.url)
    num_matches = query.num_jobs
    num_pages = (num_matches // 11)
    print("A total of {} matches have been found".format(num_matches))
    for i in range(num_pages):
        print("Extracting data: page ({}/{})".format(i+1, num_pages))
        query.parse_soup()
        url_maker.next_page()
        query.update_soup(url_maker.url)
    
    new_dict = []
    for key, value in query.data.items():
        new_dict.append(value)
    
    try:
        json.dump(new_dict, open(FILE_DESTINATION+"job_query-{}.json".format(timeStr),"w"))
        print("File written successfully.")
    except Exception as e:
        print("An error has occurred in writing the file. ")
        print("Make sure the directory you provided is correct.")
        print("If you are using Windows, please ensure you are escaping the slashes.")
        print(e)
    # finally:
    #     if f:
    #         f.close()

if __name__ == "__main__":
    main()

