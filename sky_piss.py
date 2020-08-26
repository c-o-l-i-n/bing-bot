import bing_bot as bb
import requests

response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=4509177&appid=48036d8b91dc62762efc28095e51b57d')

weather = response.json()['weather'][0]['main'].lower()

if 'rain' in weather or 'storm' in weather:
    bb.send_message('the sky is full of piss')
