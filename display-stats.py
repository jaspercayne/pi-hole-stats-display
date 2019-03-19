import json
import subprocess
import time

import Adafruit_SSD1306
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

api_url = 'http://localhost/admin/api.php'

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

disp.begin() # Initialize library
disp.clear()# Clear display
disp.display() # Start the display

width = disp.width # Store the display width
height = disp.height # Store the display height
image = Image.new('1', (width, height)) # Create a blank image for drawing.
#  ^
# /|\ Make sure to create image with mode '1' for 1-bit colour

draw = ImageDraw.Draw(image) # Store the drawing object so we can draw on the image
draw.rectangle((0, 0, width, height), outline=0, fill=0) # Draw a solid black box to clear any displayed images

# First define some constants to allow easy navigation around the image
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position
# for drawing shapes.
x = 0

# Load silkscreen bold font for labels
font = ImageFont.truetype("/home/pi/.pihole-display/fonts/slkscrb.ttf", 8)

# Create labels
draw.text((x, top),"IP: ", font=font, fill=255)
draw.text((x, top+8),"Status:            ", font=font, fill=255)
draw.text((x, top+16),"Ads Blocked:      ", font=font, fill=255)
draw.text((x, top+24),"Clients Today:    ", font=font, fill=255)
draw.text((x, top+32),"Clients Today:    ", font=font, fill=255)
draw.text((x, top+40),"DNS Queries:      ", font=font, fill=255)
draw.text((x, top+48),"Ad Percentage:    ", font=font, fill=255)
draw.text((x, top+48),"Blocked Domains:  ", font=font, fill=255)

# Load silkscreen standard font for values
font = ImageFont.truetype("/home/pi/.pihole-display/fonts/slkscr.ttf", 8)

while True:
    # Draw a black filled box to clear the last displayed info.
    draw.rectangle((0, 19, width-19, height), outline=0, fill=0)

    cmd = "hostname -I | cut -d\' \' -f1 | tr -d \'\\n\'"
    IP = subprocess.check_output(cmd, shell=True)
    cmd = "hostname | tr -d \'\\n\'"
    HOST = subprocess.check_output(cmd, shell=True)

    # Pi Hole data retrieval
    try:
        r = requests.get(api_url)
        data = json.loads(r.text)
        STATUS = data['status']
        ADSBLOCKED = data['ads_blocked_today']
        LIFECLIENTS = DATA['clients_ever_seen']
        CLIENTS = data['unique_clients']
        DNSQUERIES = data['dns_queries_today']
        ADS = data['ads_percentage_today']
        BLOCKED = daata['domains_being_blocked']
    except:
      time.sleep(1)
      continue

    draw.text((19, top), str(IP) + "( " + HOST + ")", font=font, fill=255)
    draw.text((19, top + 8), str(STATUS), font=font, fill=255)
    draw.text((19, top + 16), str(ADSBLOCKED), font=font, fill=255)
    draw.text((19, top + 24), str(LIFECLIENTS), font=font, fill=255)
    draw.text((19, top + 32), str(CLIENTS), font=font, fill=255)
    draw.text((19, top + 40), str(ADS), font=font, fill=255)
    draw.text((19, top + 48), str(BLOCKED)[:4] + "%", font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
