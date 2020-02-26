# 蓝本中的路由和视图函数
from flask import render_template, redirect, url_for, flash,current_app,json,jsonify,request
import redis as rd
from . import ncov
import requests

def get_trend_data():
    headers = {
        'user-agent': '',
        'accept': ''
    }
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    res = requests.get(url, headers=headers).json()
    r = rd.Redis(host='49.234.72.130', port=6379, password='7889')
    r.set('trend', json.dumps(res))
    return res


def get_trend_data_redis():
    headers = {
        'user-agent': '',
        'accept': ''
    }
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    res = requests.get(url, headers=headers).json()
    r = rd.Redis(host='49.234.72.130', port=6379, password='7889')
    r.set('trend', json.dumps(res))
    return r


@ncov.route('/index',methods=['GET','POST'])
def index():
    if request.method == "GET":  # 判断请求方式是GET请求
        wy_ncov_data = get_trend_data_redis()
        ncov_data = json.loads(wy_ncov_data.get('trend'))
        res = jsonify(ncov_data)
        # 世界数据
        worldData = ncov_data['data']['areaTree']
        wd = {}
        for i in worldData[0:15]:
            wd[i['name']] = i['total']['confirm']
        regionName = list(wd.keys())
        regionData = list(wd.values())

        # 国内数据
        ChinaData = ncov_data['data']['areaTree'][0]['children']
        cd = {}
        for i in ChinaData:
            cd[i['name']] = i['total']['confirm']
        cityName = list(cd.keys())
        cityData = list(cd.values())

        # 国内确诊中：在院、治愈、死亡数
        category = ncov_data['data']['areaTree'][0]['total']
        cd = {}
        cd['确诊在院']=category['confirm'] - category['dead'] - category['heal']
        cd['确诊死亡'] = category['dead']
        cd['确诊治愈'] = category['heal']
        cd['现有疑似'] = category['suspect']
        categoryName = list(cd.keys())
        categoryData = list(cd.values())

        return render_template("ncov_dp.html", regionName= regionName, regionData=regionData,
                               cityName =cityName, cityData= cityData,
                               categoryName =categoryName, categoryData= categoryData,
                               )
        # return  jsonify(regionName)


@ncov.route('/trend', methods=['GET', 'POST'])
def trend():
    if request.method == 'GET':
        trend_data = get_trend_data()
        return jsonify(trend_data)


@ncov.route('/trend/ncovData', methods=['GET', 'POST'])
def ncovData():
    if request.method == 'GET':
        wy_ncon_data = get_trend_data_redis()
        ncov_data = json.loads(wy_ncon_data.get('trend'))
        res = jsonify(ncov_data)
        worldData = ncov_data['data']['areaTree']
        wd = {}
        for i in worldData:
            wd[i['name']] = i['total']['confirm']
        cnt = len(wd)
        return jsonify(wd)


