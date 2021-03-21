#!/usr/bin/env python3
#
# proSmart <-> MQTT Gateway
#

import asyncio
import pathlib
import ssl
import json
import websockets
import paho.mqtt.client as mqtt
import argparse

uri = "wss://sys.prosmartsystem.com/ws"
topic_root = "prosmart"

parser = argparse.ArgumentParser(description='proSmart <-> MQTT Gateway')
parser.add_argument("-H", "--mqtthost", type=str, default="localhost", help="MQTT host (default: localhost)")
parser.add_argument("-p", "--mqttport", type=int, default=1883, help="MQTT port (default: 1883)")
parser.add_argument("-u", "--mqttusername", type=str, default="", help="MQTT username")
parser.add_argument("-P", "--mqttpassword", type=str, default="", help="MQTT password")
parser.add_argument("-i", "--userid", type=int, help="proSmart UserID", required=True)
parser.add_argument("-t", "--accesstoken", type=str, help="proSmart Access Token", required=True)
args = parser.parse_args()

user_id = args.userid
access_token = args.accesstoken

async def get_user_devices():
    async with websockets.connect(uri) as websocket:
        p1 = {"action":"api_call","route":"get_user_devices","data":{"_hl":"en","user_id":user_id},"access_token":access_token,"callback_id":1}
        await websocket.send(json.dumps(p1))
        greeting = json.loads(await websocket.recv())

        device = greeting['data']['data']
        device = device[next(iter(device))]

        return device

def search_json(arr, key, value):
    for item in arr:
        try:
            if item[key] == value:
                return item
        except:
            pass
    return {}

async def poll_data_forever(device):
    async with websockets.connect(uri) as websocket:
        while True:
            p2 = {"action":"init_devices","data":{"user_id":user_id,"device_list":[device]},"access_token":access_token,"callback_id":2}
            await websocket.send(json.dumps(p2))
            greeting = json.loads(await websocket.recv())

            if 'callback_id' in greeting.keys():
                if greeting['callback_id'] == 2:
                    r = search_json(search_json(greeting['data'], 'msg_topic', 'curr_readings')['msg_payload'], 'src', device['DeviceType'])
                    s = search_json(greeting['data'], 'msg_topic', 'curr_schedule')['msg_payload']['manual_setpoint']

                    client.publish(topic=topic+"/temperature", payload=r['t_reading_1'], retain=True)
                    client.publish(topic=topic+"/humidity", payload=r['h_reading_1'], retain=True)
                    client.publish(topic=topic+"/ldr", payload=r['ldr_reading_1'], retain=True)
                    client.publish(topic=topic+"/setpoint", payload=s, retain=True)

            await asyncio.sleep(5)

async def set_temp(device_id, setpoint):
    async with websockets.connect(uri) as websocket:
        p3 = {"action":"emit_config","data":{"user_id":user_id,"device_id":device_id,"relay":1,"config_data":[{"key":"mode","value":2},{"key":"manualsetpoint","value":setpoint}]},"access_token":access_token,"callback_id":8}
        await websocket.send(json.dumps(p3))

device = asyncio.get_event_loop().run_until_complete(get_user_devices())
print("[*] " + str(device))
topic = "{}/{}".format(topic_root, device['device_sets']['device_name'])
print("[*] topic: {}".format(topic))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("{}/#".format(topic))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))

    if (msg.topic == topic+"/set_temp"):
        setpoint = int(float(msg.payload)*100)
        print("[*] Setting target temperature to {} ({})".format(msg.payload.decode(), setpoint))
        asyncio.new_event_loop().run_until_complete(set_temp(device['ID'], setpoint))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if ((args.mqttusername != "") and (args.mqttpassword != "")):
    client.username_pw_set(args.mqttusername, args.mqttpassword)
client.connect(args.mqtthost, args.mqttport, 60)

client.loop_start()
asyncio.get_event_loop().run_until_complete(poll_data_forever(device))
