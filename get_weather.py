import os
import requests
import json

api_key = os.getenv('YANDEX_WEATHER_TOKEN')

day_mapping = {
    'morning': 'утро',
    'day': 'день',
    'night': 'ночь'
}
precipitation_mapping = {
    0: "без осадков",
    0.25: "слабый дождь/слабый снег",
    0.5: "дождь/снег",
    0.75: "сильный дождь/сильный снег",
    1: "сильный ливень/очень сильный снег"
}
cloudiness_mapping = {
    0: "ясно",
    0.25: "малооблачно",
    0.5: "облачно с прояснениями",
    0.75: "облачно с прояснениями",
    1: "пасмурно"
}
condition_mapping = {
    'clear': 'ясно',
    'partly-cloudy': 'малооблачно',
    'cloudy': 'облачно с прояснениями',
    'overcast': 'пасмурно',
    'drizzle': 'морось',
    'light-rain': 'небольшой дождь',
    'rain': 'дождь',
    'moderate-rain': 'умеренно сильный дождь',
    'heavy-rain': 'сильный дождь',
    'continuous-heavy-rain': 'длительный сильный дождь',
    'showers': 'ливень',
    'wet-snow': 'дождь со снегом',
    'light-snow': 'небольшой снег',
    'snow': 'снег',
    'snow-showers': 'снегопад',
    'hail': 'град',
    'thunderstorm': 'гроза',
    'thunderstorm-with-rain': 'дождь с грозой',
    'thunderstorm-with-hail': 'гроза с градом'
}


def get_weather():
    url = 'https://api.weather.yandex.ru/v2/forecast?lat=55.751244&lon=37.618423&lang=ru_RU&limit=1&hours=true'
    headers = {
        'X-Yandex-API-Key': '28ce4a90-4c27-486c-8ae8-a263d20039af'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        fact = data['fact']
        daily_info = ''
        for dp_name, dp in data['forecasts'][0]['parts'].items():
            if dp_name in list(day_mapping.keys()):
                daily_info += f'{day_mapping[dp_name]}: {dp["temp_avg"]}°C, {cloudiness_mapping[dp["cloudness"]]}, {precipitation_mapping[dp["prec_strength"]]}\n'
        w = f"Температура: {fact['temp']}°C, ощущаемая: {fact['feels_like']}°C\nПогода: {condition_mapping[fact['condition']]}\nСкорость ветра: {fact['wind_speed']} м/с\n"
        w += daily_info
        hourly_info = ''
        for dp in data['forecasts'][0]['hours']:
            if int(dp['hour']) > 6:
                hourly_info += f'{dp["hour"]}: {dp["temp"]}°C, {cloudiness_mapping[dp["cloudness"]]}, {precipitation_mapping[dp["prec_strength"]]}\n'
        w += hourly_info
        return w
    except requests.exceptions.RequestException as e:
        result = "Ошибка при выполнении запроса:"
        print(e)
        return result
