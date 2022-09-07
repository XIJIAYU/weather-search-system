import os

import requests
from flask import Flask, jsonify, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from flask import send_from_directory
import json
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import os
#前端的地址 static
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"
#字典类型
all_info = {
        'state': None,
        'city': None,
        'country': None,
        'postal': None,
        'auto': None,
        'first_load': None,
        'weather': None,
        'in1': None,
        'in2': None,
        'in3': None,
    }
@app.route('/getJsonFile', methods=['GET','POST'])
def getJsonFile():
    return json.dumps(all_info,ensure_ascii=False)



#@app.route('/getJsonFile'，methods=['GET', 'POST'])
#def getJsonFile():
 #   return json.dumps(all_info, ensure_ascii=False)
@app.route('/getBanner')
def getBanner():
    return send_from_directory(root, "banner.jpg")
@app.route('/getUp')
def getUp():
    return send_from_directory(root, "point-up-512.png")
@app.route('/getDown')
def getDown():
    return send_from_directory(root, "point-down-512.png")



@app.route('/')
@app.route('/login1', methods=['GET', 'POST'])
def login1():
    # if form.validate_on_submit():
    if request.method == "GET":
        first_load = 1
        street = request.args.get("street")
        city = request.args.get("city")
        state = request.args.get("state")
        auto = request.args.get("auto")
        in1 = street
        in2 = city
        in3 = state

        if city == None and auto == None:

            in1 = ''
            in2 = ''
            in3 = ''
        else:
            first_load=0
        infos = weathInfo(street=street, state=state, city=city, auto=auto)
        city = infos['city']
        country = infos['country']
        state = infos['state']
        postal = infos['postal']
        infos = infos['weather']
        all_info['state'] = state
        all_info['city'] = city
        all_info['country'] = country
        all_info['postal'] = postal
        all_info['auto'] = auto
        all_info['first_load'] = first_load
        all_info['weather'] = infos
        all_info['in1'] = in1
        all_info['in2'] = in2
        all_info['in3'] = in3


            # return render_template('login.html')
        return send_from_directory(root, "index.html")


class LoginForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired(message='Please Fill in this field')])
    city = StringField('City', validators=[DataRequired(message='Please Fill in this field')])
    state = SelectField(
        label='state',
        validators=[DataRequired('Please Fill in this field')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, 'CA'), (2, 'dezou'), (3, 'niuyue')],
        default=1,
        coerce=int)
    auto_detect = BooleanField('Want us to auto_detect your location?Check here')
    submit = SubmitField('SUBMIT')


stateCode = {'Alabama': "AL", 'Alaska': "AK", 'Arizona': "AZ", 'Arkansas': "AR", 'California': "CA", 'Colorado': "CO",
             'Connecticut': "CT", 'Delaware': "DE", 'District Of Columbia': "DC", 'Florida': "FL", 'Georgia': "GA",
             'Hawaii': "HI", 'Idaho': "ID", 'Illinois': "IL", 'Indiana': "IN", 'Iowa': "IA", 'Kansas': "KS",
             'Kentucky': "KY", 'Louisiana': "LA", 'Maine': "ME", 'Maryland': "MD", 'Massachusetts': "MA",
             'Michigan': "MI", 'Minnesota': "MN", 'Mississippi': "MS", 'Missouri': "MO", 'Montana': "MT",
             'Nebraska': "NE", 'Nevada': "NV", 'New Hampshire': "NH", 'New Jersey': "NJ", 'New Mexico': "NM",
             'New York': "NY", 'North Carolina': "NC", 'North Dakota': "ND", 'Ohio': "OH", 'Oklahoma': "OK",
             'Oregon': "OR", 'Pennsylvania': "PA", 'Rhode Island': "RI", 'South Carolina': "SC", 'South Dakota': "SD",
             'Tennessee': "TN", 'Texas': "TX", 'Utah': "UT", 'Vermont': "VT", 'Virginia': "VA", 'Washington': "WA",
             'West Virginia': "WV", 'Wisconsin': "WI", 'Wyoming': "WY"}


def weathInfo(street, state, city, auto):
    url = "https://api.tomorrow.io/v4/timelines"
    if (auto == None):
        addr = str(street) + " " + str(city) + " " + str(state)
        url_go = "https://maps.googleapis.com/maps/api/geocode/json"
        querystring_go = {"address": addr,
                          "key": "AIzaSyBf_7TV1urBv7dEa4x1h6cbt7aY8FDYwYk"}
        local = requests.request("GET", url_go, params=querystring_go).json()
        for component in local.get('results')[0].get('address_components'):
            if component.get('types')[0] == 'locality':
                city = component.get('short_name')
            elif component.get('types')[0] == 'country':
                country = component.get('short_name')
            elif component.get('types')[0] == 'postal_code':
                postal = component.get('short_name')
            elif component.get('types')[0] == 'administrative_area_level_1':
                state = component.get('short_name')
            else:
                postal= 0
        loc1 = local.get("results")[0].get("geometry").get(
            "location")

        loc = str(loc1.get("lat")) + ',' + str(loc1.get("lng"))

    else:
        url_ipinfo = "https://ipinfo.io/?token=c28368f5d3086e"
        querystring_ip = {"token": "c28368f5d3086e"}
        local = requests.request("GET", url_ipinfo, params=querystring_ip).json()
        city = local.get('city')
        country = local.get('country')
        postal = local.get('postal')
        state = local.get('region')
        state = stateCode[state]

        loc = local.get('loc')
    querystring = {"location": loc, "timezone": "America/Los_Angeles",
                   "fields": ["temperature", "temperatureApparent", "temperatureMin", "temperatureMax", "windSpeed",
                              "windDirection", "humidity", "pressureSeaLevel", "uvIndex", "weatherCode",
                              "precipitationProbability", "precipitationType", "sunriseTime", "sunsetTime",
                              "visibility", "moonPhase", "cloudCover"], "units": "imperial", "timesteps": "1d",
                   "apikey": "VubtIsgBVJ5HiC5uFA3hvDYLoxLVigWR"}

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    # 将response变成json格式
    json_res = response.json()

    intervald = json_res.get('data').get('timelines')[0].get('intervals')
    # jsonify({'json_res': json_res})
    result = {'city': city, 'country': country, 'postal': postal, 'state': state, 'weather': intervald}
    return result


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
