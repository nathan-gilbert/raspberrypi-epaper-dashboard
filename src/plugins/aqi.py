"""

"""
import csv
from typing import Dict
from collections import namedtuple

import requests


AQI = namedtuple("AQI", ["ozone", "ozone_8hr_avg", "pm25",
                         "pm25_24hr_avg", "nox", "no2", "co", "timestamp"])

def get_air_quality() -> AQI:
    """

    :return:
    :rtype:
    """
    api_url = "https://air.utah.gov/csvFeed.php?id=nr"

    with requests.Session() as sesh:
        download = sesh.get(api_url)
        decoded_content = download.content.decode('utf-8')

        reader = csv.DictReader(decoded_content.splitlines(),
                                     delimiter='\t')
        for row in reader:
            return AQI(row["ozone"], row["ozone_8hr_avg"], row["pm25"], \
                row["pm25_24hr_avg"], row["nox"], row["no2"], row["co"],
                       row["dtstamp"])

if __name__ == "__main__":
    aqi = get_air_quality()
    print(aqi)
