# RaspberryPi ePaper Dashboard

Simple dashboard for a Waveshare 2.7" e-Paper Display for a Raspberry Pi.

Currently displays the date, a stock I want to track and the Air Quality
near my home (via weather.com)

## Information

- <https://dev.to/ranewallin/getting-started-with-the-waveshare-2-7-epaper-hat-on-raspberry-pi-41m8>
- <https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/examples/epd_2in7_test.py>
- <https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT_(B)>

## Running

- Must link the `lib` and `pic` directories from the Waveshare repo into
  this repo
- Follow the instructions in the links above to connect the display to your Pi
- Install dependencies: `pip3 install -r requirements.txt`
- Run: `sudo python3 update_display`

## TODO

- finish module refactor
- Read config from a file
- Fix lint errors
