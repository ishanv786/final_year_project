from machine import Pin, Signal, ADC, Timer
from dht import DHT11
adc = ADC(0)

# On my board on = off, need to reverse.
led = Signal(Pin(2, Pin.OUT), invert=True)

MAX_HISTORY = 250
p = Pin(5, Pin.IN)
d = DHT11(p)


# Maintain a log of previous values to 
# determine min, max and threshold.
history = []
beat = False
beats = 0

def calculate_bpm(t):
    global beats
    print('BPM:', beats/6) 
    beats = 0
    d.measure()
    temp = d.temperature()
    print('Temperature:', temp)
    hum = d.humidity()
    print('Humidity', hum)
    value = p.value()
    print(value)

timer = Timer(1)
timer.init(period=10000, mode=Timer.PERIODIC, callback=calculate_bpm)

while True:
    v = adc.read()

    history.append(v)

    # Get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]

    minima, maxima = min(history), max(history)

    threshold_on = (minima + maxima * 3) // 4   # 3/4
    threshold_off = (minima + maxima) // 2      # 1/2

    if not beat and v > threshold_on:
        beat = True
        beats += 1
        led.on()

    if beat and v < threshold_off:
        beat = False
        led.off()

