#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : update_display.py
# Author            : Nathan Gilbert <nathan.gilbert@gmail.com>
# Date              : 01.23.2022 16:28:48
# Last Modified Date: 01.23.2022 16:55:37
#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import datetime
import logging
from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont

from weather_air import get_air_quality
from get_stock_quotes import get_stock_price

logging.basicConfig(level=logging.DEBUG)

try:
    adbe = get_stock_price('ADBE')
    aqi = get_air_quality()

    logging.info("epd2in7 Dashboard")
    epd = epd2in7.EPD()

    '''2Gray(Black and white) display'''
    logging.info("init and clear")
    epd.init()
    epd.Clear(0xFF)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)

    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    # 255: clear the frame
    Limage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Limage)
    current_time = datetime.datetime.now()
    formatted_date = current_time.strftime("%d %a %b")
    draw.text((2, 0), formatted_date, font=font34, fill=0)
    draw.text((5, 35), "ADBE: $" + str(adbe), font=font24, fill=0)
    offset = 0
    for q in aqi:
        draw.text((5, 70 + offset), q, font=font18, fill=0)
        offset += 15
    draw.text((90, 70 + offset + 80), current_time.strftime("%I:%M %p"), font=font12, fill=0)
    epd.display(epd.getbuffer(Limage))

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
