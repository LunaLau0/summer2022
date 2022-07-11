import os.path
import sys
from flask import Flask, request
import querydb
import json
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def check():
    return 'alive'

@app.route('/getdbdata')
def get_db_data():
    data = querydb.get_data(request.args['parkid'], request.args['modelname'], request.args['polltype'],
                            request.args['st'], request.args['et'])
    return json.dumps(data)

@app.route('/provmonthly')
def provmonthly():
    return json.dumps(querydb.provmonthly(request.args['modelname'], request.args['polltype'], request.args['year']))

@app.route('/getalldbdata')
def get_alldb_data():
    data = querydb.get_data(request.args['parkid'], request.args['modelname'], None, request.args['st'], request.args['et'])
    tmp = {}
    for k in data.keys():
        if k == "CO":
            tmp['CO'] = data['CO']
        elif k == "NO2":
            tmp['NO'] = data['NO2']
        elif k == "PM10":
            tmp['PMTWO'] = data['PM10']
        elif k == "PM25":
            tmp['PMONE'] = data['PM25']
        elif k == "SO2":
            tmp['SO'] = data['SO2']
        else:
            tmp[k] = data[k]
    return json.dumps(tmp)

@app.route('/timeseries')
def get_ts_data():
    data = querydb.get_ts(request.args['parkid'], request.args['modelname'], request.args['polltype'],
                            request.args['st'], request.args['et'])
    return json.dumps(data)

@app.route('/detaildata')
def get_detail_data():
    filename = f'{INTERMID_PATH}{request.args["parkid"]}_{request.args["modelname"]}_{request.args["polltype"]}_{request.args["datetime"]}.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            jsonobj = json.load(f)
        if jsonobj['status'] == 0:
            if isinstance(jsonobj['grid'], dict):
                #old version
                tmp = []
                for k in jsonobj['grid'].keys():
                    tmp.append(jsonobj['grid'][k])
                jsonobj['grid'] = tmp
            return jsonobj
        else:
            return jsonobj
    else:
        return querydb.get_mongo_detail(request.args["parkid"], request.args["modelname"], request.args["polltype"],
                                           request.args["datetime"])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)