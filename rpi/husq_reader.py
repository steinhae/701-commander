#!/usr/bin/env python

import sys
import binascii
import os
from panda import Panda
from paho.mqtt import client as mqtt_client
from time import sleep

SLEEP_TIME = 1
DEBUG = os.getenv('DEBUG_READER')
if DEBUG is None:
  DEBUG = False
else:
  DEBUG = True

DEBUG_PANDA_TEST = False
WIFI = False

broker = 'localhost'
port = 1883
topic = "husq"
client_id = 'python-mqtt'
client = None 

def connect_mqtt():
  def on_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Connected to MQTT Broker!")
    else:
      print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
  c = mqtt_client.Client(client_id)
  c.on_connect = on_connect
  c.connect(broker, port)
  global client
  client = c


def husq_reader():
  if DEBUG_PANDA_TEST:
    p = Panda("TEST")
  else:
    connected = False
    while not connected:
      try:
        print("Trying to connect to Panda over USB...")
        p = Panda()
        connected = True
      except AssertionError:
        print("USB connection failed")
        if WIFI:
          print("USB connection failed. Trying WiFi...")
          try:
            p = Panda("WIFI")
            connected = True
          except:
            print("WiFi connection timed out. Please make sure your Panda is connected and try again.")
            sys.exit(0)   
      sleep(SLEEP_TIME)
  body_bus_speed = 500
  p.set_can_speed_kbps(0, body_bus_speed)
  
  global client

  rpm = -1
  gear = -1

  while True:
    try:
      can_recv = p.can_recv()
      for address, _, dat, src  in can_recv:
        if address == 288: # 0x120 is RPM / throttle
          rpm = binascii.hexlify(dat)[0:4]
          rpm = int(rpm, 16)
          client.publish(topic + "/rpm", rpm)
        if address == 297: # 0x129 is gear
          #print(binascii.hexlify(dat))
          gear = int(binascii.hexlify(dat)[:1])
          client.publish(topic + "/gear", gear)
          #print("Gear: " + str(gear))
        if address == 1344: # 0x540 is coolant
          temp = int(int(binascii.hexlify(dat)[12:], 16) / 10)
          client.publish(topic + "/temp", temp)
        #sleep(0.025)
      sleep(0.001) 
    except:
      print("Error while reading")
      sys.exit(0)

if __name__ == "__main__":
  connect_mqtt()
  husq_reader()
