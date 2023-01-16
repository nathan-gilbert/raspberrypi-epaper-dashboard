"""

"""
import csv
from typing import Dict, Union
from datetime import datetime

import requests


def get_air_quality() -> Dict[str, Union[float, str]]:
    """

    :return:
    :rtype:
    """
    api_url = "https://air.utah.gov/csvFeed.php?id=nr"
    format = "%m/%d/%Y %H:%M:%S"

    with requests.Session() as sesh:
        download = sesh.get(api_url)
        decoded_content = download.content.decode('utf-8')

        reader = csv.DictReader(decoded_content.splitlines(),
                                     delimiter='\t')
        for row in reader:
            return {
                "ozone": float(row["ozone"]),
                "ozone_8ht_avg": float(row["ozone_8hr_avg"]),
                "pm25": float(row["pm25"]),
                "pm25_24hr_avg": float(row["pm25_24hr_avg"]),
                "nox": float(row["nox"]),
                "no2": float(row["no2"]),
                "co": float(row["co"]),
                "timestamp": datetime.strptime(row["dtstamp"], format)
            }


if __name__ == "__main__":
    aqi = get_air_quality()
    print(aqi)
