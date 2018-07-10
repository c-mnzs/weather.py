from flask import Flask, render_template, request, redirect, url_for
from pprintpp import pprint as pp
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import requests

api_key_weather = "862c4b28a2592489c1b9d0bb501127e8"
api_key_map = "AIzaSyCq0hz9mC6-zbcfjTUvMGfIUBgD9kIG8r0"

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = api_key_map
GoogleMaps(app)

@app.route('/index', methods=['GET', 'POST'])
def redirectIndex():
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "POST":
        print("METHOD IS POST")
        data = request.form['city']
        return redirect(url_for('weather', loc=data))

    
    r = requests.get("http://ip-api.com/json/").json()
    lat, lon = r['lat'], r['lon']

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&APPID={api_key_weather}"
    weather = requests.get(weather_url).json()


    country = r['country']

    city, country, country_code = r['regionName'], weather["sys"]["country"], r['countryCode']
    temp, main, description = weather['main']['temp'], weather['weather'][0]['main'], weather['weather'][0]['description']
    icon = weather['weather'][0]['icon']

    loc_map = Map(
        identifier="view-side",
        lat=lat,
        lng=lon,
        markers=[(lat, lon)],
        zoom=15,
        style="height: 350px; width: 100%;"
    )

    return render_template("index.html", loc_map=loc_map, city=city, lat=lat, lon=lon, api_key_map=api_key_map, country=country, icon=icon, main=main, description=description, temp=temp)

    # https://translation.googleapis.com/language/translate/v2

@app.route('/weather/<string:loc>', methods=['GET', 'POST'])
def weather(loc):
    
    if request.method == "POST":
        print("METHOD IS POST")
        data = request.form['city']
        return redirect(url_for('weather', loc=data))

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&units=metric&APPID={api_key_weather}"
    weather = requests.get(weather_url).json()

    if weather['cod'] == '404':
        return render_template("404.html")

    city, country = weather["name"], weather["sys"]["country"] # r['regionName'], r['country'], r['countryCode']
    temp, main, description = weather['main']['temp'], weather['weather'][0]['main'], weather['weather'][0]['description']
    icon = weather['weather'][0]['icon']
    lat, lon = weather['coord']['lat'], weather['coord']['lon']

    loc_map = Map(
        identifier="view-side",
        lat=lat,
        lng=lon,
        markers=[(lat, lon)],
        zoom=15,
        style="height: 350px; width: 100%;"
    )

    return render_template("index.html", loc=loc, weather_url=weather_url, weather=weather, loc_map=loc_map, city=city, lat=lat, lon=lon, api_key_map=api_key_map, country=country, icon=icon, main=main, description=description, temp=temp)

if __name__ == '__main__':
    app.run(debug=True)