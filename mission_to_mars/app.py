#################################################
# Dependencies
#################################################
from bs4 import BeautifulSoup
from splinter import Browser
from pprint import pprint
import pymongo
import pandas as pd
import requests
from flask import Flask, render_template
import time
import numpy as np
import json
from selenium import webdriver
from urllib.parse import urlsplit

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_data
mars = db.mars_collection
mars.insert_one(scrape_mars.scrape())

@app.route("/")
def index():
    mars = mongodb.mars_data.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Successful!"


if __name__ == "__main__":
    app.run()
