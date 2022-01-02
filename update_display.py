#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:

    logging.info("epd2in7 Demo")
    epd = epd2in7.EPD()

    '''2Gray(Black and white) display'''
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)

    # Drawing on the Vertical image
    logging.info("2.Drawing on the Vertical image...")
    Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    draw.text((2, 0), 'hello world', font = font34, fill = 0)
    draw.line((10, 90, 60, 140), fill = 0)
    draw.line((60, 90, 10, 140), fill = 0)
    draw.rectangle((10, 90, 60, 140), outline = 0)
    draw.line((95, 90, 95, 140), fill = 0)
    draw.line((70, 115, 120, 115), fill = 0)
    draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    draw.rectangle((10, 150, 60, 200), fill = 0)
    draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    epd.display(epd.getbuffer(Limage))
    #time.sleep(2)

    #logging.info("Clear...")
    #epd.Clear(0xFF)
    #logging.info("Goto Sleep...")
    #epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
