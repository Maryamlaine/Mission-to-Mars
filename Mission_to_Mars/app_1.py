from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars_test


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index_1.html", mars_mission=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars_test.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect('/', code=302)

# if __name__ == "__main__":
#     app.run(debug=True)
# @app.route("/scrape")
# def scrape():
#     # Run the scrape function
#     mars_data = scrape_mars_test.scrape()

#     # Update the Mongo database using update and upsert=True
#     mongo.db.collection.update({}, mars_data, upsert=True)
#     return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)