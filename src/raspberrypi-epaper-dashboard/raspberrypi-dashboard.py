#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : raspberrypi-dashboard.py
# Author            : Nathan Gilbert <nathan.gilbert@gmail.com>
# !/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import datetime
import logging
from typing import List
from src.plugins.aqi import get_air_quality
from src.plugins.stock_quotes import get_stock_price

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    from waveshare_epd import epd2in7
    from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(level=logging.DEBUG)


class RaspberryPiEpaperDashboard:
    def __init__(self):
        self._display = epd2in7.EPD()

    def create_display_text(self):
        pass

    def update_terminal_display(self):
        pass

    def update_epaper_display(self):
        """
        Updates the epaper
        :return:
        :rtype:
        """
        try:
            adbe = get_stock_price('ADBE')
            aqi = get_air_quality()

            logging.info("epd2in7 Dashboard")

            '''2Gray(Black and white) display'''
            logging.info("init and clear")
            self._display.init()
            self._display.Clear(0xFF)
            font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
            font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)

            # Drawing on the Vertical image
            logging.info("2.Drawing on the Vertical image...")
            # 255: clear the frame
            L_image = Image.new('1', (self._display.width, self._display.height), 255)
            draw = ImageDraw.Draw(L_image)
            current_time = datetime.datetime.now()
            formatted_date = current_time.strftime("%d %a %b")
            draw.text((2, 0), formatted_date, font=font34, fill=0)
            draw.text((5, 35), "ADBE: $" + str(adbe), font=font24, fill=0)
            offset = 0
            for q in aqi:
                draw.text((5, 70 + offset), q, font=font18, fill=0)
                offset += 15
            draw.text((90, 70 + offset + 80),
                      current_time.strftime("%I:%M %p"),
                      font=font12,
                      fill=0)
            self._display.display(self._display.getbuffer(L_image))

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd2in7.epdconfig.module_exit()
            exit()
