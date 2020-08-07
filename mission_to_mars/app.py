from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db
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