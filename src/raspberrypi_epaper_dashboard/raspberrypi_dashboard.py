"""
Raspberry Pi Epaper Dashboard Class
"""
import os
import sys
import datetime
import logging
from src.plugins.aqi import get_air_quality
from src.plugins.stock_quotes import get_stock_price

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    # pylint: disable=import-error
    from waveshare_epd import epd2in7
    # pylint: disable=import-error
    from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(level=logging.DEBUG)


class RaspberryPiEpaperDashboard:
    """
    RaspberryPiEpaperDashboard

    Contains methods for updating an epaper screen as well can generate the
    text content of the screen. Also can print to the terminal for debugging
    purposes.
    """
    def __init__(self):
        self._display = epd2in7.EPD()

    def create_display_text(self):
        """

        :return:
        :rtype:
        """
        # TODO
        pass

    def update_terminal_display(self):
        """

        :return:
        :rtype:
        """
        # TODO
        pass

    def update_epaper_display(self):
        """
        Updates the epaper
        :return:
        :rtype:
        """
        try:

            logging.info("epd2in7 Dashboard")

            # 2Gray(Black and white) display
            logging.info("Initialize and clear screen.")
            self._display.init()
            self._display.Clear(0xFF)
            font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
            font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            font34 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 34)

            # Drawing on the Vertical image
            logging.info("Drawing on the Vertical image...")
            # 255: clear the frame
            l_image = Image.new('1', (self._display.width, self._display.height), 255)
            draw = ImageDraw.Draw(l_image)
            current_time = datetime.datetime.now()
            formatted_date = current_time.strftime("%d %a %b")

            # adbe = get_stock_price('ADBE')
            # draw.text((2, 0), formatted_date, font=font34, fill=0)
            # draw.text((5, 35), f"ADBE: ${adbe:.2f}", font=font24, fill=0)

            offset = 0
            aqi = get_air_quality()
            for aq_metric, val in aqi.items():
                if aq_metric == "timestamp":
                    continue

                if aq_metric.endswith("_level"):
                    draw.text((5, 70 + offset),
                              f"{aq_metric}: {val}",
                              font=font18, fill=0)
                else:
                    draw.text((5, 70 + offset),
                              f"{aq_metric}: {val:.2f}",
                              font=font18, fill=0)
                offset += 15
            draw.text((90, 70 + offset + 40),
                      current_time.strftime("%I:%M %p"),
                      font=font12,
                      fill=0)
            self._display.display(self._display.getbuffer(l_image))

        except IOError as err:
            logging.info(err)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd2in7.epdconfig.module_exit()
            sys.exit()
