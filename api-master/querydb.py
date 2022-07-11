import dbconn
import numpy as np
import conf
import datetime

def get_data(parkid, modelname, pollutant_type, fromdt, enddt):
    db = dbconn.MySQLConn(dbhost, dbport, dbusr, dbpswd, dbname)
    if pollutant_type is not None:
        query_comm = f'SELECT emit_datetime, emit_amount, relerr FROM {tablename} WHERE pollutant_type="{pollutant_type}" ' \
                     f'AND cal_model="{modelname}" AND park_id="{parkid}" AND ' \
                     f'emit_datetime >= "{fromdt[:10]} {fromdt[-2:]}:00:00" AND emit_datetime<="{enddt[:10]} {enddt[-2:]}:00:00"'
    else:
        query_comm = f'SELECT pollutant_type FROM {tablename} WHERE cal_model="{modelname}" AND park_id="{parkid}" AND ' \
                     f'emit_datetime >= "{fromdt[:10]} {fromdt[-2:]}:00:00" AND emit_datetime<="{enddt[:10]} {enddt[-2:]}:00:00"'
        res = db.excute_all(query_comm)
        pollutants = [x[0] for x in res]
        pollutants = np.unique(pollutants)
        resobj = {}
        for p in pollutants:
            resobj[p] = get_data(parkid, modelname, p, fromdt, enddt)
        return resobj
    # print(query_comm)
    res = db.excute_all(query_comm)
    db.conn.close()
    days = [x[0].strftime('%Y-%m-%d') for x in res]
    month = [x[0].strftime('%Y-%m') for x in res]
    jsonobj = {}
    jsonobj['hour'] = {'data': []}
    daydata = {}
    monthdata = {}
    total_emit = 0
    for i, r in enumerate(res):
        jsonobj['hour']['data'].append({'st': r[0].strftime('%Y-%m-%d-%H'), 'value': r[1]})
        total_emit += r[1]
        if days[i] not in daydata.keys():
            daydata[days[i]] = 0.0
        daydata[days[i]] += r[1]
        if month[i] not in monthdata.keys():
            monthdata[month[i]] = 0.0
        monthdata[month[i]] += r[1]
    jsonobj['day'] = {'data': [{'st': x, 'value': daydata[x]} for x in daydata.keys()]}
    jsonobj['month'] = {'data': [{'st': x, 'value': monthdata[x]} for x in monthdata.keys()]}
    durhour = (res[-1][0] - res[0][0]).total_seconds()/3600
    jsonobj['est_annual_emit'] = total_emit*365*24/durhour if durhour > 0 else -1.0
    jsonobj['total_emit'] = total_emit
    return jsonobj

def get_ts(parkid, modelname, pollutant_type, fromdt, enddt):
    db = dbconn.MySQLConn(dbhost, dbport, dbusr, dbpswd, dbname)
    query_comm = f'SELECT emit_datetime, emit_amount, relerr FROM {tablename} WHERE pollutant_type="{pollutant_type}" ' \
                 f'AND cal_model="{modelname}" AND park_id="{parkid}" AND ' \
                 f'emit_datetime >= "{fromdt[:10]} {fromdt[-2:]}:00:00" AND emit_datetime<="{enddt[:10]} {enddt[-2:]}:00:00" ORDER BY emit_datetime'
    # print(query_comm)
    res = db.excute_all(query_comm)
    sdatetime = datetime.datetime.strptime(fromdt, '%Y-%m-%d-%H')
    edatetime = datetime.datetime.strptime(enddt, '%Y-%m-%d-%H')
    nhour = (edatetime - sdatetime).total_seconds()/3600
    db.conn.close()
    if len(res) == 0:
        return {'status': 1}
    days = [x[0].strftime('%Y-%m-%d') for x in res]
    month = [x[0].strftime('%Y-%m') for x in res]
    jsonobj = {'status': 0}
    jsonobj['hour'] = {'x': [], 'y': [], 'relerr': []}
    daydata = {}
    monthdata = {}
    total_emit = 0
    for i, r in enumerate(res):
        jsonobj['hour']['x'].append(r[0].strftime('%Y-%m-%d-%H'))
        jsonobj['hour']['y'].append(r[1])
        jsonobj['hour']['relerr'].append(r[2])
        total_emit += r[1]
        if days[i] not in daydata.keys():
            daydata[days[i]] = 0.0
        daydata[days[i]] += r[1]
        if month[i] not in monthdata.keys():
            monthdata[month[i]] = 0.0
        monthdata[month[i]] += r[1]
    total_emit = total_emit/len(res)*nhour
    jsonobj['day'] = {'x': list(daydata.keys()), 'y': [daydata[x] for x in daydata.keys()]}
    jsonobj['month'] = {'x': list(monthdata.keys()), 'y': [monthdata[x] for x in monthdata.keys()]}
    jsonobj['est_annual_emit'] = total_emit * 365 * 24 / nhour
    jsonobj['total_emit'] = total_emit
    return jsonobj

def provmonthly(modelname, pollutant_type, year):
    npark = len(conf.parks_list)
    data = np.zeros((npark, 12))
    for i in range(12):
        for j, p in enumerate(conf.parks_list):
            data[j,i] = monthlydata(p, modelname, pollutant_type, year, i+1)
    return list(data.sum(axis=0))

def monthlydata(parkid, modelname, pollutant_type, year, month):
    db =  dbconn.MySQLConn(dbhost, dbport, dbusr, dbpswd, dbname)
    res = db.excute_all(f'SELECT emit_amount, relerr, emit_datetime FROM {tablename} WHERE park_id = "{parkid}" AND cal_model = "{modelname}" AND '
                        f'pollutant_type = "{pollutant_type}" AND year(emit_datetime) = "{year}" AND month(emit_datetime) = "{month}"')
    return np.array([x[0] for x in res]).sum()

def urldt2dbdt(urldt:str) -> str:
    parts = urldt.split('-')
    return f'{parts[0]}-{parts[1]}-{parts[2]} {parts[3]}:00:00'

def get_mongo_detail(parkid, modelname, pollutant_type, st):
    mondb = dbconn.MongoConn(host=monhost, port=monport, user=monusr, password=monpwd, dbname=mondbname)
    res = mondb.cursor['modelout'].find_one({
        'parkid': parkid,
        'modelname': modelname,
        'pollname': pollutant_type,
        'emit_datetime': urldt2dbdt(st)
    })
    if res:
        return res['intermid_data']
    else:
        return {'status': -2}

