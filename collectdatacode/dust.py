from machine import Pin, ADC, UART
import network
import time
from umqtt.robust import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
import struct
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS
)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(WIFI_SSID, WIFI_PASS)
while not wlan.isconnected():
    time.sleep(0.5)
red = Pin(2,Pin.OUT)


class PMS7003:
    """Provide a wrapper with decoding mechanism for serial data coming from a
    PMS7000 device over a specified UART instance.
    """
    
    PMS_FRAME_LENGTH = 0
    PMS_PM1_0 = 1
    PMS_PM2_5 = 2
    PMS_PM10_0 = 3
    PMS_PM1_0_ATM = 4
    PMS_PM2_5_ATM = 5
    PMS_PM10_0_ATM = 6
    PMS_PCNT_0_3 = 7
    PMS_PCNT_0_5 = 8
    PMS_PCNT_1_0 = 9
    PMS_PCNT_2_5 = 10
    PMS_PCNT_5_0 = 11
    PMS_PCNT_10_0 = 12
    PMS_CHECKSUM = 15




    def __init__(self, uart):
        """Create a wrapper over the specified UART instance, uart"""
        self.uart = uart




    def read(self):
        """Read and decode the next measurement data from the device and
        return the decoded values in a dict.  Calls to this method will be
        blocked until the data is available.
        """
        while True:
            # scan for start characters
            if self.uart.read(1) != b'\x42':
                continue
            if self.uart.read(1) != b'\x4D':
                continue


            # wait and read the remaining 30 bytes of data
            while self.uart.any() < 30:
                pass
            read_buffer = self.uart.read(30)
            data = struct.unpack('!HHHHHHHHHHHHHBBH', read_buffer)
            checksum = 0x42 + 0x4D
            for c in read_buffer[0:28]:
                checksum += c
            if checksum != data[self.PMS_CHECKSUM]:
                # bad checksum; ignore this reading and try the next one
                continue  # ignore this reading and try the next one


            return {
                'PM1_0': data[self.PMS_PM1_0],
                'PM2_5': data[self.PMS_PM2_5],
                'PM10_0': data[self.PMS_PM10_0],
                'PM1_0_ATM': data[self.PMS_PM1_0_ATM],
                'PM2_5_ATM': data[self.PMS_PM2_5_ATM],
                'PM10_0_ATM': data[self.PMS_PM10_0_ATM],
                'PCNT_0_3': data[self.PMS_PCNT_0_3],
                'PCNT_0_5': data[self.PMS_PCNT_0_5],
                'PCNT_1_0': data[self.PMS_PCNT_1_0],
                'PCNT_2_5': data[self.PMS_PCNT_2_5],
                'PCNT_5_0': data[self.PMS_PCNT_5_0],
                'PCNT_10_0': data[self.PMS_PCNT_10_0],
            }




    async def aread(self):
        """Asynchronously read and decode the next measurement data from the
        device and return the decoded values in a dict.  Unlike the
        synchronous read method, calls to this method will not be blocked, but
        this method needs to be called from a coroutine.
        """
        import uasyncio
        while True:
            # scan for start characters
            while self.uart.any() < 2:
                await uasyncio.sleep_ms(1)
            if self.uart.read(1) != b'\x42':
                continue
            if self.uart.read(1) != b'\x4D':
                continue


            # wait and read the remaining 30 bytes of data
            while self.uart.any() < 30:
                await uasyncio.sleep_ms(1)
            read_buffer = self.uart.read(30)
            data = struct.unpack('!HHHHHHHHHHHHHBBH', read_buffer)
            checksum = 0x42 + 0x4D
            for c in read_buffer[0:28]:
                checksum += c
            if checksum != data[self.PMS_CHECKSUM]:
                # bad checksum; ignore this reading and try the next one
                continue


            return {
                'PM1_0': data[self.PMS_PM1_0],
                'PM2_5': data[self.PMS_PM2_5],
                'PM10_0': data[self.PMS_PM10_0],
                'PM1_0_ATM': data[self.PMS_PM1_0_ATM],
                'PM2_5_ATM': data[self.PMS_PM2_5_ATM],
                'PM10_0_ATM': data[self.PMS_PM10_0_ATM],
                'PCNT_0_3': data[self.PMS_PCNT_0_3],
                'PCNT_0_5': data[self.PMS_PCNT_0_5],
                'PCNT_1_0': data[self.PMS_PCNT_1_0],
                'PCNT_2_5': data[self.PMS_PCNT_2_5],
                'PCNT_5_0': data[self.PMS_PCNT_5_0],
                'PCNT_10_0': data[self.PMS_PCNT_10_0],
            }
uart = UART(1, rx=23, tx=9, baudrate=9600)
pms = PMS7003(uart)
red.value(0)

while (True):
    mqtt = MQTTClient(client_id="",
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
    mqtt.connect()
    print("connect")
    pms_read = pms.read()
    p25 = pms_read["PM2_5"]
    mqtt.publish("daq2023/group5/dust", str(p25))
    print(p25)
    mqtt.disconnect()
    print('disconnect')
    red.value(1)
    time.sleep(600)

