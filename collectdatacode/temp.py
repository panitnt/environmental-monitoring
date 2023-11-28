from machine import Pin, ADC, UART
import network
import time
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
import struct
import kidbright as kb
import json


wifi = Pin(2, Pin.OUT)

kb.init()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    wifi.value(1)
    time.sleep(0.5)
wifi.value(0)

mqtt = MQTTClient(client_id="",
                    server=MQTT_BROKER,
                    user=MQTT_USER,
                    password=MQTT_PASS)
mqtt.connect()
print(f"MQTT are connected")


while True:
    # Reconnect to Wi-Fi if disconnected
    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            wifi.value(1)
            time.sleep(0.5)
        wifi.value(0)
    mqtt.connect()
    print(f"MQTT are connected")
    data = {
        'temp' : kb.temperature(),
        'lat' :  13.5,
        'lon' : 100.25,
    }
    print(data)
    mqtt.publish('daq2023/group5/temp', json.dumps(data))
    mqtt.disconnect()
    wlan.disconnect()
    time.sleep(600)
