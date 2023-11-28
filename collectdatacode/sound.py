import time
import network
from machine import Pin, ADC, I2C
from config import WIFI_SSID, WIFI_PASS, MQTT_BROKER, MQTT_USER, MQTT_PASS
from umqtt.robust import MQTTClient


sound = ADC(Pin(34)) # I3 = In3

# Wi-Fi Configuration
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Connecting to WiFi...")
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
print("WiFi connected")

# MQTT Configuration
mqtt = MQTTClient(client_id="", server=MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS)
print("Connecting to MQTT broker...")
mqtt.connect()
print("MQTT broker connected")

TOPIC_SOUND = "daq2023/group5/sound"

while (True):
    x = sound.read()
    if (x>=2000):
        print(f'Sound: {sound.read()}')
        mqtt.publish(TOPIC_SOUND, str(x))
        time.sleep(0.1)
