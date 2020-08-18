"""This module allows the creation and parsing of Indeed.com URLs"""
import json
from pymongo import MongoClient


class dbAccess(object):
    """
    Turns a client query into a valid URL
    
    A client provides a dictionary of query parameters. An object of this class
    performs the necessary parsing to generate a URL compatible with Indeed.com.
    
    Attributes:
        job_title: A string to describe the job to search for.
        location: A string of a city, or a province (Default is unspecified).
        radius: An int minimum radius of search in km (Default is unspecified).
        job_type: A string specifying whether the job is full-time, part-time, etc. 
            (Default is unspecified). Accepts one of {fulltime, parttime, internship}.
        
    """


    def __init__(self, **params):
        """Initialize the query parameters"""
        self.job_title = params["job_title"]
        self.location = params["location"]
        self.radius = params["radius"]
        self.job_type = job_type_tokenizer(params["job_type"])
        self.url = ""

    
        
    