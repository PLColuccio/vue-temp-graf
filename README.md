# vue-temp-graf
A combination of vuegraf and tempgraf for Emporia Vue data logging

TempGraf is my own creation mostly based on VueGraf's python file. Essentially it works by quering the OpenWeather API, then outputting that data to Influx for consumption. THe docker-compose file includes TempGraf, VueGraf, Influx, and Grafana for a complete working solution, developed for use on a Raspberry Pi.
