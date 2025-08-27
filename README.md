
# Micropython-ESP32-W5500 (Wiznet)
**Enhanced and SSL support version (untested)**: Check [ESP32-Wiznet-W5500-SSL-Micropython](https://github.com/Ayyoubzadeh/ESP32-Wiznet-W5500-SSL-Micropython).

Connect your ESP32 to the W5500 (Wiznet) Ethernet module and use Python's `requests` as an HTTP client.

![ESP32 and W5500](https://user-images.githubusercontent.com/92551110/189515479-bfadad62-0bf1-4efc-84bb-ae88b58ec12a.png)

## Hardware
- **ESP32 ESP-WROOM-32**
- **W5500** (or W5100)

## Firmware
- **Micropython**

## Tools
- **Python**
- **ampy** (Install using pip)
    ```bash
    pip install adafruit-ampy
    ```

## Wiring

| ESP32  | W5500 |
|--------|-------|
| 3V3    | V     |
| GND    | G     |
| GPIO5 (VSPI_CS)  | CS    |
| GPIO18 (VSPI_CLK) | SCK   |
| GPIO23 (VSPI_MOSI) | MO   |
| GPIO19 (VSPI_MISO) | MI   |
| GPIO34  | RST   |

## Instructions

### 1. Upload Required Files
Upload the following files to your ESP32 using `ampy`:
- `wiznet5k.mpy`
- `wiznet5k_dhcp.mpy`
- `wiznet5k_dns.mpy`
- `wiznet5k_socket.mpy`
- `sma_esp32_w5500_requests.mpy`

Example (replace `COM9` with your ESP32’s serial port):
```bash
ampy --port COM9 put wiznet5k.mpy
ampy --port COM9 put wiznet5k_dhcp.mpy
ampy --port COM9 put wiznet5k_dns.mpy
ampy --port COM9 put wiznet5k_socket.mpy
ampy --port COM9 put sma_esp32_w5500_requests.mpy
```

### 2. Run the Code
Upload the following code to your ESP32 to fetch data over HTTP using the W5500 module.

```python
from wiznet5k import WIZNET5K
from machine import Pin, SPI
import wiznet5k_socket as socket
import time
import struct
import sma_esp32_w5500_requests as requests

# Initialize SPI and W5500
spi = SPI(2)
cs = Pin(5, Pin.OUT)
rst = Pin(34)
nic = WIZNET5K(spi, cs, rst)

# Define the URL to fetch data from
TEXT_URL = "http://quietlushbrightverse.neverssl.com/online/"

# Display chip info and network status
print("Chip Version:", nic.chip)
print("MAC Address:", [hex(i) for i in nic.mac_address])
print("My IP address is:", nic.pretty_ip(nic.ip_address))
print("IP lookup google.com: %s" % nic.pretty_ip(nic.get_host_by_name("google.com")))

# Initialize requests object with socket and Ethernet interface
requests.set_socket(socket, nic)

# Fetch and print content from the URL
print("Fetching text from", TEXT_URL)
r = requests.get(TEXT_URL)
print('-' * 40)
print(r.text)
print('-' * 40)
r.close()

print("Done!")
```

### Limitations
- Works only with HTTP (not HTTPS). For SSL support, check out the enhanced version [here](https://github.com/Ayyoubzadeh/ESP32-Wiznet-W5500-SSL-Micropython).

---

## How to Log in to ASP.NET Forms (Forms-Based Authentication)

If you need to log in to an ASP.NET form and retrieve a cookie for subsequent private page requests, follow these steps. The login page is `logon.aspx`, and the private page is `default.aspx`.

### 1. Get the Login Page
Fetch the login page and extract the necessary form values.

### 2. Post Username, Password, and ViewState
Send a POST request with the username, password, and `__VIEWSTATE` from the page.

### 3. Send the Cookie for Private Pages
Once logged in, capture the cookie and use it to access private pages.

Here is the code to log in and get the cookie:

```python
from wiznet5k import WIZNET5K
from machine import Pin, SPI
import wiznet5k_socket as socket
import sma_esp32_w5500_requests as requests

def findVal(txt, tag):
    g = txt[txt.find(tag):]
    g = g[g.find("value"):]
    g = g[:g.find("/>")]
    g = g.strip()
    g = g.replace('value="', "")
    g = g[:-1]  # remove the trailing quote
    return g

# Initialize SPI and W5500
spi = SPI(2)
cs = Pin(5, Pin.OUT)
rst = Pin(34)
nic = WIZNET5K(spi, cs, rst)

# Display chip info and network status
print("Chip Version:", nic.chip)
print("MAC Address:", [hex(i) for i in nic.mac_address])
print("My IP address is:", nic.pretty_ip(nic.ip_address))

# Initialize requests object with socket and Ethernet interface
requests.set_socket(socket, nic)

# Log in to the website
url = 'http://win.smait.ir/logon.aspx'
g = requests.get(url).text

# Extract the __VIEWSTATE and other hidden form values
payload = {
    '__EVENTTARGET': "",
    '__EVENTARGUMENT': "",
    '__VIEWSTATE': findVal(g, '__VIEWSTATE'),
    '__VIEWSTATEGENERATOR': findVal(g, '__VIEWSTATEGENERATOR'),
    '__EVENTVALIDATION': findVal(g, '__EVENTVALIDATION'),
    'txtUserName': "1",
    'txtUserPass': "2",
    'Button1': "Login"
}
print(payload)

# Send POST request to log in
p = requests.post(url, data=payload)
print(p.headers)

# Get the cookie from the response headers
cookie = p.headers['set-cookie'].split('; expires=')[0]
print(cookie)

# Use the cookie to access the private page
p2 = requests.get('http://win.smait.ir/default.aspx', headers={"Cookie": cookie})
print(p2.text)
```

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
