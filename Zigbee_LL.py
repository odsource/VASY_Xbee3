# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from machine import Pin, PWM
import time
import xbee
import machine

LED_PIN_ID = "D4"
PWM_PIN_ID = "P0"

endpoint = 0x11

light_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02, "On/Off": 0x03}
light_commands = {"Off": 0x00, "On": 0x01, "Toggle": 0x02}

payload = ""
transition_time = 0

dim_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02,
                  "On/Off": 0x03, "Level control": 0x04}
dim_commands = {"Move to Level": 0x00, "Move": 0x01, "Step": 0x02,
                "Stop": 0x03, "Move to Level(with On/Off)": 0x04,
                "Move (with On/Off": 0x05, "Step (with On/Off)": 0x06}


def dim(dest_endpoint, cluster_id, rec_command, rec_payload):
    print("Dim")
    if dest_endpoint == endpoint:
        print("Right endpoint")
        if cluster_id == dim_cluster_id["Level control"]:
            print("dim it")
            if rec_command == dim_commands["Move to Level(with On/Off)"]:
                actual_level = pwm_pin.duty()
                level = rec_payload
                transition_level = level - actual_level
                if transition_level == 0:
                    level = rec_payload
                else:
                    step = (transition_time / transition_level)*1000
                print("Transition time")
                print(transition_time)
                print("actual_level")
                print(actual_level)
                print("level")
                print(level)
                print("transition_level")
                print(transition_level)
                print("step")
                print(step)

                if transition_time == 0:
                    pwm_pin.duty(rec_payload)
                else:
                    print("Dim steps")
                    while True:
                        if pwm_pin.duty() == level:
                            break
                        next_step = pwm_pin.duty() + 1  # int(step)
                        # if next_step > 1000:
                        #     next_step = 1000
                        pwm_pin.duty(next_step)
                        time.sleep_ms(int(step))


def light(dest_endpoint, cluster_id, rec_command, rec_payload):
    if dest_endpoint == endpoint:
        print("Right endpoint")
        print(rec_payload)
        if cluster_id == light_cluster_id["On/Off"]:
            if rec_command == light_commands["Off"] or rec_command == light_commands["On"]:
                led_pin.value(rec_payload)
            else:
                led_pin.toggle()


device_func = {0x0000: light, 0x0100: dim}

print(" +--------------------------------------+")
print(" | XBee MicroPython Blinking LED Sample |")
print(" +--------------------------------------+\n")

# Set up the LED pin object to manage the LED status. Configure the pin
# as output and set its initial value to off (0).
led_pin = Pin(LED_PIN_ID, Pin.OUT, value=1)
pwm_pin = PWM(PWM_PIN_ID)

while True:
    # Check if the XBee has any message in the queue.
    received_msg = xbee.receive()
    if received_msg:
        print("Message received")
        if received_msg['source_ep'] == 0x11:
            f = device_func[received_msg['profile']]
            payload = received_msg['payload']
            payload = payload.split()
            transition_time = 0
            print(len(payload))
            if len(payload) == 3:
                transition_time = int(payload[2])
                print(transition_time)
            f(received_msg['dest_ep'], received_msg['cluster'], int(payload[0]), int(payload[1]))
