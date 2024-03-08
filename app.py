from flask import Flask, render_template, request
from datetime import datetime
import requests
from matplotlib import pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():

    x_time = [0,1,2,3,4,5,6]
    y_temp = [18,15,13,9,8,8,11]
    plt.plot(x_time, y_temp)
    plt.savefig("test_chart")

    return render_template('home.html')


@app.route('/results', methods=["GET", "POST"])
def results():
    api_key = "935a752109a96c2d444323711cadcb03"
    form_city = request.form.get('city')


    url = "https://api.openweathermap.org/data/2.5/weather?q=" + form_city + "&APPID=" + api_key
    response = requests.get(url).json()
    print(url)
    print(response)

    weather_list = response.get("weather", [{}])
    weather_one = weather_list[0]
    location = response.get("name")
    timezone = response.get("timezone")
    timestamp = response.get("dt")
    timestamp_local = datetime.fromtimestamp(timestamp)
    description = weather_one.get("description")
    temp_k = response.get("main", {}).get("temp")
    temp_c = int(temp_k) - 273.15
    wind_speed = response.get("wind", {}).get("speed")
    icon = weather_one.get("icon")

    weather_dict = {
        "location": location,
        "timezone": timezone,
        "timestamp_local": timestamp_local,
        "description": description,
        "temp_c": temp_c,
        "wind_speed": wind_speed,
        "icon": icon
    }

    weather_list = [location, timezone, timestamp_local, description, temp_c, wind_speed, icon]


    return render_template('results.html', weather_dict=weather_dict,response=response)


if __name__ == '__main__':
    app.run(debug=True)
