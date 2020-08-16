"""This module contains the user interface"""
import scrapper
import url_utilities
import configparser
import time
import json


def main():
    config = configparser.ConfigParser()
    config.read('./config.ini')
    print(config['DEFAULT'])
    JOB_TITLE = config['DEFAULT']['JOB_TITLE']
    JOB_LOCATION = config['DEFAULT']['LOCATION']
    JOB_RADIUS = config['DEFAULT']['RADIUS']
    JOB_TYPE = config['DEFAULT']['JOB_TYPE']
    FILE_DESTINATION = config['DEFAULT']['FILE_DESTINATION'].strip('"')
    timeStr = time.strftime("%Y%m%d-%H%M%S")
    try:
        JOB_RADIUS = int(JOB_RADIUS)
    except ValueError:
        JOB_RADIUS = 0
    #job_type = input("Job Type [Full-time, Part-time, Internship]: ")
    url_maker = url_utilities.urlMaker(job_title = JOB_TITLE, location = JOB_LOCATION, radius = JOB_RADIUS, job_type = JOB_TYPE)
    url_maker.build_url()
    print(url_maker.url)
    query = scrapper.Query(url_maker.url)
    num_matches = query.num_jobs
    num_pages = (num_matches // 11)
    print("A total of {} matches have been found".format(num_matches))
    for i in range(1):
        print("Extracting data: page ({}/{})".format(i+1, num_pages))
        query.parse_soup()
        url_maker.next_page()
        query.update_soup(url_maker.url)
        print("Displaying results:")
    
    # print('JSON Dumps Data Items')
    # print(json.dumps(query.data.items()))
    # print('------------------------------')
    #print('JSON Dumps Data')
    #print(json.dumps(query.data))
    for key, value in query.data.items():
        print(value)
        # print("Job Title: {}".format(value[0][1:-1])) # ignore quote marks
        # print("Job Location: {}".format(value[2][1:-1])) # ignore quote marks
        # print("Employer: {}".format(value[1][1:-1])) # ignore quote marks
        # print("Apply here: {}".format(value[3]))
        # print("Job Description: {}".format(value[4][0:200]))
        # print("\n")
    print(FILE_DESTINATION+"job_query-{}.csv".format(timeStr))
    try:
        json.dump(query.data, open(FILE_DESTINATION+"job_query-{}.json".format(timeStr),"w"))
        # f = open(FILE_DESTINATION+"job_query-{}.json".format(timeStr), "w")
        # f.write('[')
        # f.write(json.dumps(query.data))
        # f.write(']')
        # f.close()
        print("File written successfully.")
    except Exception:
        print("An error has occurred in writing the file. ")
        print("Make sure the directory you provided is correct.")
        print("If you are using Windows, please ensure you are escaping the slashes.")
    finally:
        if f:
            f.close()

if __name__ == "__main__":
    main()

