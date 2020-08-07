#################################################
# Dependencies
#################################################
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

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


@app.route('/')
def index():
    
    mars = mongo.db.mars.find_one() 
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )



if __name__ == "__main__":
    app.run(debug=True)