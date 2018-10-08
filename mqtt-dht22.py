import os
import time
import sys
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'ec2-52-15-68-221.us-east-2.compute.amazonaws.com'
ACCESS_TOKEN = '8TrOW1H8IBQVyXDcWjTQ'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL=2

sensor_data = {'temperature': 0, 'humidity': 0, 'battery': 0, 'status': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(52.6, 31.1))
        sensor_data['temperature'] = 52.6
        sensor_data['humidity'] = 31.1
	sensor_data['battery'] = 8.5
	sensor_data['status'] = 1

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()