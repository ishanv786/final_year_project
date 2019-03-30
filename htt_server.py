from machine import Pin, Signal, ADC, Timer
from dht import DHT11

adc = machine.ADC(0)

pin = Pin(5, Pin.IN)
d = DHT11(pin)


html = """<!DOCTYPE html>
<html>
    <head> <title>Pi4IoT</title> </head>
    <body> 
      <h1>Sensor Data</h1>
        <table border="1" > 
            <tr>
                <th>Patient</th><th>Heart Beats</th><th>Temperature</th><th>Humidity</th>
            </tr> %s 
        </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('192.168.43.153', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)
history = []
d.measure()
temp = d.temperature()
hum = d.humidity()
beats = (adc.read()/6)


print('listening on', addr)

while True:
    
    cl, addr = s.accept()
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>Ishan</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (beats,temp, hum)]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
