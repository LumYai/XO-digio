from flask import Flask, render_template, jsonify, request
import pymongo
from pymongo import MongoClient




app = Flask(__name__)


#Database
client = MongoClient(host='test_mongodb',
                        port=27017, 
                        username='root', 
                        password='pass',
                        authSource="admin")
db = client["test_db"]

@app.route('/')
def index():
    # Retrieve data from MongoDB (you can modify this part according to your needs)
    data = db.mycollection.find()
    return render_template('index.html', data=data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)