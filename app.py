from flask import Flask, render_template, redirect
import pymongo
from pymongo import MongoClient
from scrape_mars import scrape

mongo = MongoClient()


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
