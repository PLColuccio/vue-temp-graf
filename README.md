# vue-temp-graf
A combination of vuegraf and tempgraf for Emporia Vue data logging

TempGraf is my own creation mostly based on VueGraf's python file. Essentially it works by quering the OpenWeather API, then outputting that data to Influx for consumption. THe docker-compose file includes TempGraf, VueGraf, Influx, and Grafana for a complete working solution, developed for use on a Raspberry Pi.

## Installing
```
sudo apt update
sudo apt install docker docker-compose git
systemctl unmask docker
systemctl enable docker
systemctl start docker
sudo usermod -aG docker pi
git clone git@github.com:PLColuccio/vue-temp-graf.git
```

Edit example configuration files in ~/vue-temp-graf/config and remove .example from the filename.
To create your own api key go to the OpenWeatherMap site: https://openweathermap.org/api

```
cd vue-temp-graf
docker-compose up
```


