import requests

def get_weather():
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=4509177&appid=48036d8b91dc62762efc28095e51b57d')
    return response.json()['weather'][0]['main'].lower()

def get_temperature():
    response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=4509177&appid=48036d8b91dc62762efc28095e51b57d')
    return f"{(response.json()['main']['temp'] * (9 / 5) - 459.67):.0f} °F"
