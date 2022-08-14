from wiznet5k import WIZNET5K
from machine import Pin, SPI
import wiznet5k_socket as socket
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