
import requests
from bs4 import BeautifulSoup

HOLLADAY = \
    "https://weather.com/en-IN/forecast/air-quality/l/" + \
    "7a87bfd6aca8dc71d5731457ddbc672ee9dcb925d93b7a54066e5bc4ab935577"


def get_data(url):
    r = requests.get(url)
    return r.text


def parse_units(data):
    desc = data[data.find("(")+1:data.find(")")]
    tokens = data.split(' ')
    pollutant = tokens[0]
    units = tokens[-1]

    return pollutant, units, desc


def severity(res):
    remark = ''
    impact = ''
    if res <= 50:
        remark = "Good"
        impact = "Minimal impact"
    elif 100 >= res > 51:
        remark = "Satisfactory"
        impact = "Minor breathing discomfort to sensitive people"
    elif 200 >= res >= 101:
        remark = "Moderate"
        impact = "Breathing discomfort to the people with lungs, asthma and " \
                 "heart diseases"
    elif 400 >= res >= 201:
        remark = "Very Poor"
        impact = "Breathing discomfort to most people on prolonged exposure"
    elif 500 >= res >= 401:
        remark = "Severe"
        impact = "Affects healthy people and seriously impacts those with " \
                 "existing diseases"
    return remark, impact


def get_air_quality():
    htmldata = get_data(HOLLADAY)
    soup = BeautifulSoup(htmldata, 'html.parser')

    # Get all the air quality pollutants, levels and severities
    pollution_data = []
    for item in (soup.find_all('div', class_="AirQuality--dial--3TK5w")):
        pollution_data.append(item.get_text())

    pollution_number = []
    for pollutant_item in (
        soup.find_all('text',
                      class_='DonutChart--innerValue--2rO41 ' +
                             'AirQuality--pollutantDialText--3Y7DJ')):
        pollution_number.append(pollutant_item.get_text())

    results = zip(pollution_number, pollution_data)
    text_results = []
    for r in results:
        clean_str = r[1].replace(r[0], '', 1)
        data = parse_units(clean_str)
        remark = severity(int(r[0]))[0]
        t = f"{data[0]} {r[0]} {remark}"
        text_results.append(t)
    return text_results
