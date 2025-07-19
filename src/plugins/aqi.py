""" """

import csv
from datetime import datetime
from typing import Dict, Union

import requests


def ozone_metrics(ozone_level: float) -> str:
    """

    :param ozone_level:
    :type ozone_level:
    :return:
    :rtype:
    """
    if ozone_level <= 0.054:
        return "GOOD"
    if 0.054 < ozone_level <= 0.070:
        return "MODERATE"
    if 0.070 < ozone_level <= 0.085:
        return "UNHEALTHY 1"
    if 0.080 < ozone_level <= 0.105:
        return "UNHEALTHY 2"
    if 0.105 < ozone_level <= 0.2:
        return "UNHEALTHY 3!"
    if ozone_level > 0.2:
        return "HAZARDOUS!!"
    return "UNKNOWN"


def pm25_metrics(pm25_level: float) -> str:
    """

    :param pm25_level:
    :type pm25_level:
    :return:
    :rtype:
    """
    if pm25_level <= 12.0:
        return "GOOD"
    if 12.0 < pm25_level <= 35.4:
        return "MODERATE"
    if 35.4 < pm25_level <= 55.4:
        return "UNHEALTHY 1"
    if 55.4 < pm25_level <= 150.4:
        return "UNHEALTHY 2"
    if 150.4 < pm25_level <= 250.4:
        return "UNHEALTHY 3!"
    if pm25_level > 250.4:
        return "HAZARDOUS!!"
    return "UNKNOWN"


def get_air_quality() -> Dict[str, Union[float, datetime]]:
    """

    :return:
    :rtype:
    """
    api_url = "https://air.utah.gov/csvFeed.php?id=nr"
    timestamp_format = "%m/%d/%Y %H:%M:%S"

    with requests.Session() as sesh:
        download = sesh.get(api_url)
        decoded_content = download.content.decode("utf-8")

        reader = csv.DictReader(decoded_content.splitlines(), delimiter="\t")
        for row in reader:
            return {
                "ozone": float(row["ozone"]),
                "ozone_level": ozone_metrics(float(row["ozone"])),
                "ozone_8hr": float(row["ozone_8hr_avg"]),
                "pm25": float(row["pm25"]),
                "pm25_level": pm25_metrics(float(row["pm25"])),
                "pm25_24hr": float(row["pm25_24hr_avg"]),
                "nox": float(row["nox"]),
                "no2": float(row["no2"]),
                "co": float(row["co"]),
                "timestamp": datetime.strptime(row["dtstamp"], timestamp_format),
            }


if __name__ == "__main__":
    aqi = get_air_quality()
    print(aqi)
