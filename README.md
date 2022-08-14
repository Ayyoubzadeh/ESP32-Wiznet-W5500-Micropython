# Micropython-ESP32-W5500 (Wiznet)
Connect your ESP32 to W5500 (Wiznet) ethernet module.

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
ampy (install using pip)
```
pip install adafruit-ampy
```

Wiring
-------
<b>ESP-32----------------W5500</b>
<br/>
3V3-----------------------V
<br/>
GND----------------------G
<br/>
GPIO5(VSPI_CS)----------CS
<br/>
GPIO18(VSPI_CLK)-------SCK
<br/>
GPIO23(VSPI_MOSI)-----MO
<br/>
GPIO19(VSPI_MISO)-----MI
<br/>
GPIO34------------------RST

Instructions
-----
1) Upload wiznet5k.mpy, wiznet5k_dhcp.mpy, wiznet5k_dns.mpy, wiznet5k_socket.mpy,sma_esp32_w5500_requests with ampy

example:
```
ampy --port COM9 put wiznet5k.mpy
ampy --port COM9 put wiznet5k_dhcp.mpy
ampy --port COM9 put wiznet5k_dns.mpy
ampy --port COM9 put wiznet5k_socket.mpy
ampy --port COM9 put sma_esp32_w5500_requests.mpy
```



2) run main.py or below code:

```
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


#nic._debug = True
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print('-'*40)
print(r.text)
print('-'*40)
r.close()

print("Done!")
```
Limitations
----------
Only Works with http (not https)

