import time
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import requests
import json


# 定时任务
class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'No1',
            'func': 'app:getAllData',
            'args': '',
            'trigger': {
                'type': 'cron',
                'hour': '1',

            }
        }
    ]


app = Flask(__name__)


def getAllData():
    global times
    global gnTotal
    global deathTotal
    global addConNew
    global addDeathNew
    global topCityName
    global topCityData
    global confirms
    global heals
    global deads
    global storeConfirms
    global dates
    global sichuan_city_name
    global sichuan_city_data
    global left_panel_shuffling_data
    global map_data
    global data_xinlang_province
    url_xinlang = "https://interface.sina.cn/news/wap/fymap2020_data.d.json"
    url_wangyi = "https://c.m.163.com/ug/api/wuhan/app/data/list-total"
    headers_wangyi = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3880.400 QQBrowser/10.8.4554.400'
    }
    r1 = requests.get(url=url_xinlang)
    r2 = requests.get(url=url_wangyi, headers=headers_wangyi)
    data_get_xinlang = json.loads(r1.text)
    data_get_wangyi = json.loads(r2.text)
    data_xinlang = data_get_xinlang["data"]
    data_wangyi = data_get_wangyi["data"]
    data_xinlang_province = data_xinlang["list"]
    dailyData = data_xinlang['add_daily']
    topData = data_xinlang["jwsrTop"]  # top10数据
    otherHistoryData = data_xinlang['otherhistorylist']  # 近一个月的数据

    # middle_up_panel
    times = data_xinlang['times']  # 统计时间
    gnTotal = data_xinlang['gntotal']  # 国内总数
    deathTotal = data_xinlang['deathtotal']  # 死亡总数
    addConNew = dailyData['addcon_new']  # 新增确诊
    addDeathNew = dailyData['adddeath_new']  # 新增死亡

    # left_pie_panel
    topCityName = []  # top10城市名字
    topCityData = []  # top10城市数据
    for i in range(len(topData)):
        topCityName.append(topData[i]['name'])
        topCityData.append(int(topData[i]['jwsrNum']))

    # left_line_panel
    def conversion_time(s):
        """
        :param s:时间
        :return: 格式为xx月xx日的时间
        """
        timeStruct = time.strptime(s, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeStruct))
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%m{m}%d{d}", localTime).format(m='月', d='日')
        if strTime[0] == '0':
            return strTime[1:]
        return strTime

    def reverse_list(lst):
        # 逆置列表
        return lst[::-1]

    chinaDatyList = data_wangyi['chinaDayList']  # 所有数据
    chinaDatyList.sort(reverse=True, key=lambda x: x['date'])
    confirms = []  # 确证
    heals = []  # 治愈
    deads = []  # 死亡人数
    storeConfirms = []  # 无症状
    dates = []  # 时间
    for i in range(10):
        date = conversion_time(chinaDatyList[i]['date'])
        dates.append(date)

        total_data = chinaDatyList[i]['total']
        confirms.append(total_data['confirm'])
        heals.append(total_data['heal'])
        deads.append(total_data['dead'])
        storeConfirms.append(total_data['storeConfirm'])
    confirms = reverse_list(confirms)  # 确证
    heals = reverse_list(heals)  # 治愈
    deads = reverse_list(deads)  # 死亡人数
    storeConfirms = reverse_list(storeConfirms)  # 无症状
    dates = reverse_list(dates)  # 时间

    # right_panel_pie
    data_sichuan = data_xinlang_province[8]
    sichuan_all = int(data_sichuan['value'])  # 四川所有患病的
    data_sichuan_city = data_sichuan["city"]  # 四川城市数据
    sichuan_city_name = []  # 四川城市名称
    sichuan_city_data = []  # 城市所对应数据
    for i in range(len(data_sichuan_city)):
        city_name = data_sichuan_city[i]['name']
        city_data = int(data_sichuan_city[i]['conNum'])
        if city_data / sichuan_all <= 0.05:
            continue
        sichuan_city_name.append(city_name)
        temp = {
            "value": city_data,
            "name": city_name
        }
        sichuan_city_data.append(temp)

    # left_panel_shuffling
    left_panel_shuffling_data = []  # 传的数据是一个二维列表

    for i in range(len(data_sichuan_city)):
        lst_instance = [data_sichuan_city[i]['mapName'], data_sichuan_city[i]['conNum'],
                        data_sichuan_city[i]['cureNum'], data_sichuan_city[i]['deathNum']]  # 内部数据[name,all,death,cure]
        left_panel_shuffling_data.append(lst_instance)

    # middle_map
    map_data = []  # 地图数据api
    for i in range(len(data_xinlang_province)):
        map_city_name = data_xinlang_province[i]['name']
        map_city_data = data_xinlang_province[i]['value']
        map_data.append({
            "name": map_city_name,
            "value": map_city_data
        })


getAllData()


@app.route('/api/total/')
def total_number():
    data_total = {
        'gnTotal': gnTotal,
        'deathTotal': deathTotal,
        'times': times,
        'addConNew': addConNew,
        'addDeathNew': addDeathNew
    }
    return jsonify(data_total)


@app.route('/api/top/')
def top10():
    data_total = {
        'topCityName': topCityName,
        'topCityData': topCityData,

    }
    return jsonify(data_total)


@app.route('/api/left/line/')
def left_line_panel():
    data_total = {
        'storeConfirms': storeConfirms,
        'confirms': confirms,
        'heals': heals,
        'deads': deads,
        'dates': dates

    }
    return jsonify(data_total)


@app.route('/api/right/pie/')
def left_pie_panel():
    data_total = {
        "sichuanCityName": sichuan_city_name,
        "sichuanCityData": sichuan_city_data
    }
    return jsonify(data_total)


@app.route('/api/right/shuffling/')
def left_shuffling_panel():
    data_total = {
        "PanelShufflingData": left_panel_shuffling_data,
    }
    return jsonify(data_total)


@app.route('/api/right/map/')
def middle_map_panel():
    data_total = {
        "mapData": map_data,
    }
    return jsonify(data_total)


def filter_data(provinceName):
    global city_all
    for i in range(len(data_xinlang_province)):
        if data_xinlang_province[i]['name'] == provinceName:
            city_all = int(data_xinlang_province[i]['value'])
            city_data = data_xinlang_province[i]['city']
            return city_data


def get_shuffling_data(cityData):
    shuffling_data = []  # 传的数据是一个二维列表

    for i in range(len(cityData)):
        if cityData[i]['mapName'] == '':
            lst_instance = [cityData[i]['name'], cityData[i]['conNum'],
                            cityData[i]['cureNum'], cityData[i]['deathNum']]
        else:
            lst_instance = [cityData[i]['mapName'], cityData[i]['conNum'],
                            cityData[i]['cureNum'], cityData[i]['deathNum']]  # 内部数据[name,all,death,cure]
        shuffling_data.append(lst_instance)
    return shuffling_data


@app.route('/api/left/shuffling/change/', methods=['POST'])
def change_right_shuffling():
    provinceName = request.get_data()
    provinceName = json.loads(provinceName)
    provinceName = provinceName['provinceName']
    city_data = filter_data(provinceName)
    city_value = get_shuffling_data(city_data)
    data_total = {
        "provinceName": provinceName,
        "newData": city_value
    }
    return jsonify(data_total)


def get_pie_data(cityData):
    city_name_all = []  # 四川城市名称
    city_data_all = []  # 城市所对应数据
    for i in range(len(cityData)):
        city_name = cityData[i]['name']
        city_data = int(cityData[i]['conNum'])
        if city_data / city_all <= 0.05:
            continue
        city_name_all.append(city_name)
        temp = {
            "value": city_data,
            "name": city_name
        }
        city_data_all.append(temp)
    return city_data_all


@app.route('/api/right/pie/change/', methods=['POST'])
def change_right_pie():
    provinceName = request.get_data()
    provinceName = json.loads(provinceName)
    provinceName = provinceName['provinceName']
    city_data = filter_data(provinceName)
    new_data = get_pie_data(city_data)
    data_total = {
        "provinceName": provinceName,
        "newData": new_data
    }
    return jsonify(data_total)


if __name__ == '__main__':
    # 定时任务，导入配置
    app.config.from_object(APSchedulerJobConfig)
    # 初始化Flask-APScheduler，定时任务
    scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))
    scheduler.init_app(app)
    scheduler.start()
    app.config["SCHEDULER_TIMEZONE"] = 'Asia/Shanghai'
    app.run(debug=True, port=8000)
