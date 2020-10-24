import re
from urllib import error
from urllib import request
import json
import os
import pymongo


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


def get_page_code(url):
    try:
        rqs = request.Request(url)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1)'
        rqs.add_header("User-Agent", user_agent)
        rqs.add_header("method", "GET")
        rqs = request.urlopen(rqs)
        pagecode = rqs.read().decode('utf-8')
        return pagecode
    except error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


def get_info(pagecode):
    data_re = re.compile('<span class="jsx-2915694336">(.*?)</span>', re.DOTALL)
    result = re.findall(data_re, pagecode)
    return result[4:]


def get_global_info(json_str):
    global_info = json.loads(json_str)
    # print(global_info)
    res = []
    for info in global_info["features"]:
        attrs = info["attributes"]
        info_needed = {"Country_Region": attrs["Country_Region"], "Confirmed": attrs["Confirmed"],
                       "Recovered": attrs["Recovered"], "Deaths": attrs["Deaths"]}
        res.append(info_needed)
    return res


def output_result(result):
    dic = {}
    with open("states.txt", 'r') as f:
        for line in f.readlines():
            strs = line[:-1].split(",")
            dic[strs[0]] = strs[1]
    with open("data.csv", "w") as f:
        f.write("State,Confirmed,Recovered,Deaths\n")
        for i in range(len(result)):
            if i % 4 == 0:
                state = result[i]
                if state in dic:
                    result[i] = dic[state]
                    res_str = ""
                    for idx in range(4):
                        res_str += result[i + idx] + ","
                    f.write(res_str[:-1] + "\n")


def to_database(state_info, global_info):
    client = create_client()
    db = client["virusinfo"]
    if db is None:
        print("can not access database")
        exit(-1)
    # output state_info to db
    dic = {}
    with open("states.txt", 'r') as f:
        for line in f.readlines():
            strs = line[:-1].split(",")
            dic[strs[0]] = strs[1]
    for i in range(len(state_info)):
        if i % 4 == 0:
            state = state_info[i]
            if state in dic:
                state_info[i] = dic[state]
                query_result = db.us.find_one({"State": state_info[i]})
                if query_result is not None:
                    db.us.delete_one({"State": state_info[i]})
                state_json = {"State": state_info[i], "Confirmed": state_info[i + 1],
                              "Recovered": state_info[i + 2], "Deaths": state_info[i + 3]}
                db.us.insert_one(state_json)

    # output global_info to db
    for item in global_info:
        query_result = db.globalinfo.find_one({"Country_Region": item["Country_Region"]})
        if query_result is not None:
            db.globalinfo.delete_one({"Country_Region": item["Country_Region"]})
        db.globalinfo.insert_one(item)


def begin():
    print('Fetching source code...')
    url = "https://coronavirus.1point3acres.com/"
    pagecode = get_page_code(url)
    print('Getting info...')
    result = get_info(pagecode)
    global_url = "https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=Confirmed%20%3E%200&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Confirmed%20desc&resultOffset=0&resultRecordCount=200&cacheHint=true"
    json_str = get_page_code(global_url)
    info = get_global_info(json_str)
    print('Writing result...')
    # output_result(result)
    to_database(result, info)


begin()
