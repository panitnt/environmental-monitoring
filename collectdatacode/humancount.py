from machine import Pin, ADC
import math
import network
import time
import json
import uasyncio as asyncio
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)

led_wifi = Pin(2, Pin.OUT)
led_wifi.value(1)  # turn the red led off
led_iot = Pin(12, Pin.OUT)
led_iot.value(1)   # intial turn the green led off

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
print("WIFI Connected")
led_wifi.value(0)  # turn the red led on


mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
mqtt.connect()
print("MQTT Connected")

ir = ADC(Pin(32))

data = {
    'lat' :  13.5,
    'lon' : 100.25,
    'count' : 1,
}

while True:
    while ir.read() <= 500: # no one walk
        if ir.read() == 0: # condition for not detecting googgoo
            continue
        time.sleep(0.1)
        print(ir.read())
    mqtt.publish('daq2023/group5/humancount', json.dumps(data))
    time.sleep(0.1)
    while ir.read() > 500: # walk pass
        time.sleep(0.1)
        print(ir.read())
