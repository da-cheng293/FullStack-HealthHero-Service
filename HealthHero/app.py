from flask import Flask, abort, jsonify
import flask
from flask_cors import *
from urllib import request
import json
import os
import pymongo

app = Flask(__name__)
CORS(app, supports_credentials=True)


def create_client():
    try:
        f = open(os.getcwd() + '/profile.json', 'r')
    except IOError:
        f = open(os.getcwd() + '/default_profile.json', 'r')
    data = json.load(f)
    username = data['username']
    password = data['password']
    f.close()
    client = pymongo.MongoClient(
        "mongodb+srv://" + username + ":" + password + "@cluster0-ln98b.mongodb.net/test?retryWrites=true&w=majority")
    return client


def query_number(querytype, location):
    client = create_client()
    db = client["virusinfo"]
    query_result = db.globalinfo.find_one({"Country_Region": {"$regex": ".*"+location+".*"}})
    if query_result is None:
        query_result = db.us.find_one({"State": {"$regex": ".*" + location + ".*"}})
        if query_result is None:
            return "No cases found in this area"
    # print(query_result)
    if querytype == 'confirmed':
        return str(query_result["Confirmed"]) + " people were confirmed infected in " + location
    elif querytype == 'death':
        return str(query_result["Deaths"]) + " people were reported dead in " + location
    elif querytype == 'recovered':
        return str(query_result["Recovered"]) + " people recovered from illness in " + location
    else:
        return "No cases found in this area"


def query_safety(location):
    # get info from db
    client = create_client()
    db = client["virusinfo"]
    query_result = db.globalinfo.find_one({"Country_Region": {"$regex": ".*" + location + ".*"}})
    if query_result is None:
        query_result = db.us.find_one({"State": {"$regex": ".*" + location + ".*"}})
        if query_result is None:
            return "It's safe to travel to " + location

    # answer question according to data
    threshold = 50
    confirmed = int(query_result["Confirmed"])
    deaths = int(query_result["Deaths"])
    recovered = int(query_result["Recovered"])
    if confirmed + deaths + recovered > threshold:
        return "It's dangerous to travel to " + location +", to many people infected."
    else:
        return "It's safe to travel to " + location


@app.route('/query', methods=['GET'])
def query():
    # request wit.ai to get entities
    sentence = flask.request.args.get("q")
    sentence = sentence.replace(' ', '%20')
    url = "https://api.wit.ai/message?q=" + sentence
    rqs = request.Request(url)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1)'
    rqs.add_header("User-Agent", user_agent)
    rqs.add_header("method", "GET")
    rqs.add_header("Authorization", "Bearer 7BCMZ62DFIYWFZDAWHRI2TOTSS4PJXQY")
    rqs = request.urlopen(rqs)
    json_str = rqs.read().decode('utf-8')

    # get attributes
    response_obj = json.loads(json_str)
    intent = ""
    location = ""
    if "intent" in response_obj["entities"]:
        intent = response_obj["entities"]["intent"][0]["value"]
    if "location" in response_obj["entities"]:
        location = response_obj["entities"]["location"][0]["value"]
    if intent == "" or location == "":
        abort(404)
    else:
        answer = "sorry, I don't understand"
        # deal with different cases
        if intent == "number":
            querytype = ""
            if "type" in response_obj["entities"]:
                querytype = response_obj["entities"]["type"][0]["value"]
            if querytype != "":
                answer = query_number(querytype, location)
        elif intent == "safety":
            answer = query_safety(location)
        return jsonify({"status": "OK", "answer": answer})


@app.route('/getquestions', methods=['GET'])
def get_questions():
    client = create_client()
    db = client["virusinfo"]
    results = db.translation.find()
    answer = []
    for result in results:
        temp = {"Question": result["Question"], "Response": result["Response"],
                "details": result["details"], "Answer": result["Answer"]}
        answer.append(temp)
    return jsonify({"answer": answer})


if __name__ == '__main__':
    app.run()
