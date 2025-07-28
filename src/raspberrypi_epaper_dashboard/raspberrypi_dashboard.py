"""
Raspberry Pi Epaper Dashboard Class
"""

import datetime
import logging
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from src.plugins.aqi import get_air_quality

pic_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../pic")
lib_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../lib")

if os.path.exists(lib_dir):
    sys.path.append(lib_dir)
    from waveshare_epd import epd2in7


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class RaspberryPiEpaperDashboard:
    """
    RaspberryPiEpaperDashboard

    Contains methods for updating an epaper screen as well can generate the
    text content of the screen. Also can print to the terminal for debugging
    purposes.
    """

    def __init__(self):
        self._display = epd2in7.EPD()

    def update_epaper_display(self) -> None:
        """
        Updates the epaper

        :return: Nothing
        :rtype: None
        """
        # Font setup
        font12 = ImageFont.truetype(os.path.join(pic_dir, "Font.ttc"), 12)
        font16 = ImageFont.truetype(os.path.join(pic_dir, "Font.ttc"), 16)
        font18 = ImageFont.truetype(os.path.join(pic_dir, "Font.ttc"), 18)
        # font24 = ImageFont.truetype(os.path.join(pic_dir, "Font.ttc"), 24)

        try:
            logger.info("epd2in7 Dashboard")

            # 2Gray(Black and white) display
            logger.info("Initialize and clear screen.")
            self._display.init()
            self._display.Clear(0xFF)

            # Drawing on the Vertical image
            logger.info("Drawing on the Vertical image...")
            # 255: clear the frame
            l_image = Image.new("1", (self._display.width, self._display.height), 255)
            draw = ImageDraw.Draw(l_image)

            current_time = datetime.datetime.now()

            # Header: Current date and time at top
            formatted_date = current_time.strftime("%a %b %d")
            formatted_time = current_time.strftime("%I:%M %p")

            # Date at top left, time at top right
            draw.text((2, 2), formatted_date, font=font18, fill=0)
            draw.text((120, 2), formatted_time, font=font16, fill=0)

            # Horizontal line separator
            draw.line((0, 25, self._display.width, 25), fill=0, width=1)

            # Get AQI data
            aqi = get_air_quality()

            # AQI Section header
            draw.text((2, 30), "Air Quality", font=font16, fill=0)

            y_offset = 50

            # Format AQI data for better display
            aqi_items = [
                ("O3", aqi.get("ozone", 0), aqi.get("ozone_level", "UNKNOWN")),
                ("PM2.5", aqi.get("pm25", 0), aqi.get("pm25_level", "UNKNOWN")),
                ("NO2", aqi.get("no2", 0), ""),
                ("CO", aqi.get("co", 0), ""),
            ]

            for label, value, level in aqi_items:
                # Format value display
                if isinstance(value, float):
                    if value < 1:
                        value_text = f"{value:.3f}"
                    elif value < 10:
                        value_text = f"{value:.2f}"
                    else:
                        value_text = f"{value:.1f}"
                else:
                    value_text = str(value)

                # Main metric line
                metric_text = f"{label}: {value_text}"
                draw.text((5, y_offset), metric_text, font=font16, fill=0)

                # Level indicator (for O3 and PM2.5)
                if level and level != "UNKNOWN":
                    # Color-code level text based on severity
                    level_color = 0  # Black for all levels on monochrome display

                    # Abbreviated level names for space
                    level_short = level.replace("UNHEALTHY", "UH").replace("HAZARDOUS", "HAZ")
                    draw.text((100, y_offset), level_short, font=font12, fill=level_color)

                y_offset += 18

            # Add data timestamp if available
            if "timestamp" in aqi:
                data_time = aqi["timestamp"].strftime("%H:%M")
                draw.text((5, y_offset + 10), f"Data: {data_time}", font=font12, fill=0)

            # Optional: Add a bottom border
            draw.line(
                (0, self._display.height - 2, self._display.width, self._display.height - 2),
                fill=0,
                width=1,
            )

            # Display the image
            self._display.display(self._display.getbuffer(l_image))

        except IOError as err:
            logger.info(f"IOError: {err}")

        except KeyboardInterrupt:
            logger.info("ctrl + c:")
            epd2in7.epdconfig.module_exit()
            sys.exit()

        except Exception as err:
            logger.error("Unexpected error: %s", err)
            # Optional: Display error message on screen
            try:
                l_image = Image.new("1", (self._display.width, self._display.height), 255)
                draw = ImageDraw.Draw(l_image)
                draw.text((5, 5), "Error updating", font=font16, fill=0)
                draw.text((5, 25), "display", font=font16, fill=0)
                self._display.display(self._display.getbuffer(l_image))
            except Exception as e:
                logger.fatal("Failed to display error message on screen: %s", e)
