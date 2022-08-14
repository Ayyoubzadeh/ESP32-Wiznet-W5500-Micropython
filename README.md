# Micropython-ESP32-W5500 (Wiznet)

Hardware
--------
ESP32 ESP-WROOM-32
<br/>
W5500 (or W5100)
<br/>

Firmware
--------
Micropython
<br/>

Tools
--------
python
ampy (install with pip install ampy)

Wiring
-------
<b>ESP-32----------------W5500</b>
<br/>
3V3-----------------------V
<br/>
GND----------------------G
<br/>
D5------------------------CS
<br/>
D18----------------------SCK
<br/>
D23----------------------MO
<br/>
D19----------------------MI
<br/>
D34----------------------RST

Instructions
-----
1) Upload wiznet5k.mpy, wiznet5k_dhcp.mpy, wiznet5k_dns.mpy, wiznet5k_socket.mpy,sma_esp32_w5500_requests with ampy

example
-------
ampy --port COM9 put wiznet5k.mpy
ampy --port COM9 put wiznet5k_dhcp.mpy
ampy --port COM9 put wiznet5k_dns.mpy
ampy --port COM9 put wiznet5k_socket.mpy
ampy --port COM9 put sma_esp32_w5500_requests.mpy



2) run main.py or below code:

from wiznet5k import WIZNET5K
from machine import Pin, SPI
import wiznet5k_socket as socket
import time
import struct
import sma_esp32_w5500_requests as requests



spi = SPI(2)
cs = Pin(5,Pin.OUT)
rst=Pin(34)
nic = WIZNET5K(spi,cs,rst)

TEXT_URL = "http://quietlushbrightverse.neverssl.com/online/"


print("Chip Version:", nic.chip)
print("MAC Address:", [hex(i) for i in nic.mac_address])
print("My IP address is:", nic.pretty_ip(nic.ip_address))
print("IP lookup google.com: %s" %nic.pretty_ip(nic.get_host_by_name("google.com")))

# Initialize a requests object with a socket and ethernet interface
requests.set_socket(socket, nic)


#eth._debug = True
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print('-'*40)
print(r.text)
print('-'*40)
r.close()

print("Done!")



