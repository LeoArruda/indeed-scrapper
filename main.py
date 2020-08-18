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
    #job_type = input("Job Type [Full-time, Part-time, Internship]: ")
    url_maker = url_utilities.urlMaker(job_title = JOB_TITLE, location = JOB_LOCATION,radius = JOB_RADIUS,job_type = JOB_TYPE, age=JOB_AGE)
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
    new_dict = []
    for key, value in query.data.items():
        print(value)
        # job_id= value[0]
        # job_title= value[1]
        # job_employer= value[2]
        # job_location= value[3]
        # job_link= value[4]
        # job_description= value[5]
        # job_collect_date= value[6]
        # jobRecord = {job_id, job_title, job_employer, job_location, job_link, job_description, job_collect_date }
        # print(jobRecord)
        #print("KEY: {}   VALUE: {}".format(key, value))
        #print(json.dumps(value))
        # print(str(query))

        # print("Job Title: {}".format(value[0][1:-1])) # ignore quote marks
        # print("Job Location: {}".format(value[2][1:-1])) # ignore quote marks
        # print("Employer: {}".format(value[1][1:-1])) # ignore quote marks
        # print("Apply here: {}".format(value[3]))
        # print("Job Description: {}".format(value[4][0:200]))
        # print("\n")
    #print(FILE_DESTINATION+"job_query-{}.csv".format(timeStr))
    try:
        #json.dump(query.data, open(FILE_DESTINATION+"job_query-{}.json".format(timeStr),"w"))
        csv_columns = ["job_id","job_title","job_employer","job_location","job_link","job_description","job_collect_date"]
        # with open(FILE_DESTINATION+"job_query-{}.csv".format(timeStr), 'w') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        #     writer.writeheader()
            #for data in dict_data:
            # writer.writerow(query.data.items())
            # for key, value in query.data.items():
            #     writer.writerow(value)

        # f = open(FILE_DESTINATION+"job_query-{}.csv".format(timeStr), "w")
        # f.write(str(query))
        # f.close()
        # print("File written successfully.")
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

