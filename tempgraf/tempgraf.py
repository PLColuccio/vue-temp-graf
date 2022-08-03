#!/usr/bin/env python3

import datetime
import json
import signal
import sys
import time
import traceback
import requests
import influxdb
from threading import Event

class VueGraf:
    interval_seconds = None
    database = None
    complete_url = None
    influx_host = None
    influx_port = None
    influx_user = None
    influx_pass = None
    influx_client = None
    city_name = None


    def log(self, level, msg):
        now = datetime.datetime.utcnow()
        print('{} | {} | {}'.format(now, level.ljust(5), msg), flush=True)


    def info(self, msg):
       self.log("INFO", msg)


    def error(self, msg):
        self.log("ERROR", msg)


    def handleExit(self, signum, frame):
        global running
        error('Caught exit signal')
        running = False
        pauseEvent.set()

    def __init__(self):
        if len(sys.argv) != 2:
            print('Usage: python {} <config-file>'.format(sys.argv[0]))
            sys.exit(1)

        configFilename = sys.argv[1]
        config = {}
        
        with open(configFilename) as configFile:
            config = json.load(configFile)

        self.interval_seconds = config['interval_seconds']
        self.database = "weather"
        api_key = config['api_key']
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        self.city_name = config['city_name']
        self.complete_url = base_url + "appid=" + api_key + "&q=" + self.city_name + "&units=imperial"
        self.influx_host = config['influx_host']
        self.influx_port = config['influx_port']
        self.influx_user = config['influx_user']
        self.influx_pass = config['influx_pass']


    def get_client(self):
        if self.influx_client is None:
            self.influx_client = influxdb.InfluxDBClient(
                host=self.influx_host,
                port=self.influx_port,
                username=self.influx_user,
                password=self.influx_pass,
                database=self.database,
                ssl=False,
                verify_ssl=False)
                
            self.influx_client.create_database(self.database)

        return self.influx_client


    def get_weather(self):
        response = requests.get(self.complete_url)
        response_json = response.json()
        return response.ok, response_json


    def generate_point(self, response_json):
        return [
            {
                "measurement": "weather",
                "tags": {
                    "city": vuegraf.city_name
                },
                "fields": {
                    "weather_id": response_json['weather'][0]['id'],
                    "weather_main": response_json['weather'][0]['main'],
                    "weather_description": response_json['weather'][0]['description'],
                    "main_temp": float(response_json['main']['temp']),
                    "main_feels_like": float(response_json['main']['feels_like']),
                    "main_pressure": float(response_json['main']['pressure']),
                    "main_humidity": float(response_json['main']['humidity']),
                    "wind_speed": float(response_json['wind']['speed']),
                    "wind_degrees": float(response_json['wind']['deg']),
                    "wind_gust": float(response_json['wind']['gust']),
                    "clouds_all": response_json['clouds']['all']
                }
            }
        ]


if __name__ == "__main__":
    vuegraf = VueGraf()

    startupTime = datetime.datetime.utcnow()
    try:
        influx = vuegraf.get_client()

        signal.signal(signal.SIGINT, vuegraf.handleExit)
        signal.signal(signal.SIGHUP, vuegraf.handleExit)

        pauseEvent = Event()

        detailedStartTime = startupTime

        while True:
            now = datetime.datetime.utcnow()

            response_ok, response_json = vuegraf.get_weather()

            if response_ok:
                data_point = vuegraf.generate_point(response_json)
                vuegraf.info('Submitting datapoint to database; tenp="{}"; humidity={}'
                    .format(
                        response_json['main']['temp'], 
                        response_json['main']['humidity'] ))
                influx.write_points(data_point)

            pauseEvent.wait(vuegraf.interval_seconds)

        vuegraf.info('Finished')
    except:
        vuegraf.error('Fatal error: {}'.format(sys.exc_info())) 
        traceback.print_exc()
