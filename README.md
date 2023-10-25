# Micropython-ESP32-W5500 (Wiznet)
Connect your ESP32 to W5500 (Wiznet) ethernet module and use Python requests as http client

![Untitled](https://user-images.githubusercontent.com/92551110/189515479-bfadad62-0bf1-4efc-84bb-ae88b58ec12a.png)



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

| ESP-32  | W5500 |
| ------------- | ------------- |
| 3V3  | V  |
| GND  | G  |
| GPIO5(VSPI_CS)  | CS  |
| GPIO18(VSPI_CLK)  | SCK  |
| GPIO23(VSPI_MOSI)  | MO  |
| GPIO19(VSPI_MISO)  | MI  |
| GPIO34  | RST  |

Instructions
-----
1) Upload wiznet5k.mpy, wiznet5k_dhcp.mpy, wiznet5k_dns.mpy, wiznet5k_socket.mpy,sma_esp32_w5500_requests with ampy

example: (replace COM9 with your esp32 connected serial port)
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

How to login in asp.net forms with getting a cookie (forms-based authentication)
-----------------
First we need to get login page after that we need to post the username and password with __VIEWSTATE of the page, Finally, we need to send the cookie for private pages. in this example the login page named logon.aspx and the private page is default.aspx .
```
from wiznet5k import WIZNET5K
from machine import Pin, SPI
import wiznet5k_socket as socket
import sma_esp32_w5500_requests as requests

def findVal(txt,tag):
    g=txt[txt.find(tag):]
    g=g[g.find("value"):]
    g=g[:g.find("/>")]
    g=g.strip()
    g=g.replace("value=\"","")
    g=g[:-1] # remove "
    return g

spi = SPI(2)
cs = Pin(5,Pin.OUT)
rst=Pin(34)
nic = WIZNET5K(spi,cs,rst)


print("Chip Version:", nic.chip)
print("MAC Address:", [hex(i) for i in nic.mac_address])
print("My IP address is:", nic.pretty_ip(nic.ip_address))


requests.set_socket(socket, nic)
url = 'http://win.smait.ir/logon.aspx'
g = requests.get(url).text
payload ={}
payload['__EVENTTARGET']=""
payload['__EVENTARGUMENT']=""
payload['__VIEWSTATE']=findVal(g,'__VIEWSTATE')
payload['__VIEWSTATEGENERATOR']=findVal(g,'__VIEWSTATEGENERATOR')
payload['__EVENTVALIDATION']=findVal(g,'__EVENTVALIDATION')
payload['txtUserName']="1"
payload['txtUserPass']="2"
payload['Button1']="Login"
print(payload)


p = requests.post(url, data=payload)
print(p.headers)
cookie=p.headers['set-cookie'].split('; expires=')[0]
print(cookie)
p2 = requests.get('http://win.smait.ir/default.aspx', headers={"Cookie":cookie})
print(p2.text)
```

