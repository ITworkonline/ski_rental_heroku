#!/usr/bin/env python
import pika
import requests
import time

def get_weather_result(api_key):
    # Geo API call: To get lat and lon for weather api; Need to add "city" as function's parameter
    # geo_api_url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}".format(city, api_key)
    # location = requests.get(geo_api_url)
    # lat = location.json()[1]["lat"]
    # lon = location.json()[1]["lon"]

    lat = -30.7822161
    lon = 121.487932

    # weather api
    weather_api_url = "http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}".format(lat, lon, api_key)
    r1 = requests.get(weather_api_url).json()

    # get the five temperature
    count = 0
    TEMP = ""
    while count < 5:
        temp = r1["list"][count]["main"]["temp"]
        temp = temp - 273.15
        temp = temp * 9 / 5
        temp += 32
        temp = str(round(temp, 2))
        TEMP = TEMP + temp + " "
        count += 1
    TEMP = TEMP.rstrip()
    return TEMP


tempurature = get_weather_result("79a907a33e59170de5a57eb9b33bf69d")


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

channel.queue_declare(queue='hello')

while True:
    channel.basic_publish(exchange='', routing_key='hello', body=tempurature)
    time.sleep(1)

channel.close()
