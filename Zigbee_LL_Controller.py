from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import ZigBeeDevice
from digi.xbee.models.mode import APIOutputModeBit
from digi.xbee.util import utils

data = ""

########### Local XBee ############
# Control bridge 0x0840
device = ZigBeeDevice("COM21", 115200)

switch_endpoint = 0x11

# Control bridge
device_switch_controller_id = 0x0840
switch_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02,
                     "On/Off": 0x03, "Level control": 0x04, "Color control": 0x05}

########### Remote ############
REMOTE_NODE_ID = "REMOTE"

light_endpoint = 0x11

# On/Off light 0x0000
device_light_id = 0x0000
light_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02, "On/Off": 0x03}
light_commands = {"Off": "0x00", "On": "0x01", "Toggle": "0x02"}

# Dimmable light 0x0100
device_dim_id = 0x0100
dim_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02,
                  "On/Off": 0x03, "Level control": 0x04}
dim_commands = {"Move to Level": "0x00", "Move": "0x01", "Step": "0x02",
                "Stop": "0x03", "Move to Level(with On/Off)": "0x04",
                "Move (with On/Off": "0x05", "Step (with On/Off)": "0x06"}

device.open()

# Command format (Payload)

# Move-to-Level Command:
# Octet: 1, Data Type: unsigned 8-bit integer, Field Name: Level
# Octet: 2, Data Type: unsigned 16-bit integer, Field Name: Transition time
# Reach Level in Transition time

# Move Command:
# Octet: 1, Data Type: 8-bit enumeration, Field Name: Move mode
# Octet: 2, Data Type: unsigned 8-bit integer, Field Name: Rate
# Move mode (up or down) is reached in the Rate of movement in units per second
# 0x00 = Up (increase light level)
# 0x01 = Down (decrease light level)

# Obtain the remote XBee device from the XBee network.

xbee_network = device.get_network()
remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
print(remote_device)
print("Start")
if remote_device is None:
    print("Could not find the remote device")
    exit(1)

while True:
    print("For dimming, type in value between 0 and 1000 and a second value for the time in s: ")
    key_input = input()
    if key_input.isdecimal():
        key_input = key_input + " " + "0"
    key_input = key_input.split(' ')
    if key_input[0] == 'on':
        print("Set light on")
        data = light_commands["On"] + " " + "0"
        device.send_expl_data(remote_xbee_device=remote_device, data=data,
                              src_endpoint=switch_endpoint, dest_endpoint=light_endpoint,
                              cluster_id=light_cluster_id["On/Off"], profile_id=device_light_id)
    elif key_input[0] == "off":
        print("Set light off")
        data = light_commands["Off"] + " " + "1"
        device.send_expl_data(remote_xbee_device=remote_device, data=data,
                              src_endpoint=switch_endpoint, dest_endpoint=light_endpoint,
                              cluster_id=light_cluster_id["On/Off"], profile_id=device_light_id)
    elif key_input[0] == "toggle":
        print("Toggle light")
        data = light_commands["Toggle"] + " " + "1"
        device.send_expl_data(remote_xbee_device=remote_device, data=data,
                              src_endpoint=switch_endpoint, dest_endpoint=light_endpoint,
                              cluster_id=light_cluster_id["On/Off"], profile_id=device_light_id)
    elif key_input[0].isdecimal() and key_input[1].isdecimal():
        print("Dim light to")
        print(key_input)
        data = dim_commands["Move to Level(with On/Off)"] + " " + key_input[0] + ' ' + key_input[1]
        print(data)
        device.send_expl_data(remote_xbee_device=remote_device, data=data,
                              src_endpoint=switch_endpoint, dest_endpoint=light_endpoint,
                              cluster_id=dim_cluster_id["Level control"], profile_id=device_dim_id)
    elif key_input == "exit":
        break

    print("")


device.close()
