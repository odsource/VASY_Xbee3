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

LED_PIN_ID = "D4"

endpoint = 0x11

light_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02, "On/Off": 0x03}
light_commands = {"Off": 0x00, "On": 0x01, "Toggle": 0x02}

payload = ""

dim_cluster_id = {"Identify": 0x00, "Groups": 0x01, "Scenes": 0x02,
                  "On/Off": 0x03, "Level control": 0x04}
dim_commands = {"Move to Level": 0x00, "Move": 0x01, "Step": 0x02,
                "Stop": 0x03, "Move to Level(with On/Off)": 0x04,
                "Move (with On/Off": 0x05, "Step (with On/Off)": 0x06}


def dim(rec_endpoint, cluster_id, rec_payload):
    print("Dim")
    if rec_endpoint == endpoint:
        print("Right endpoint")
        if cluster_id == 0x04:
            pwm_pin.freq(rec_payload)


def light(rec_endpoint, cluster_id, rec_payload):
    if rec_endpoint == endpoint:
        print("Right endpoint")
        led_pin.value(cluster_id)


device_func = {0x0000: light, 0x0100: dim}

print(" +--------------------------------------+")
print(" | XBee MicroPython Blinking LED Sample |")
print(" +--------------------------------------+\n")

# Set up the LED pin object to manage the LED status. Configure the pin
# as output and set its initial value to off (0).
led_pin = Pin(LED_PIN_ID, Pin.OUT, value=0)
pwm_pin = PWM(LED_PIN_ID)

# Start blinking the LED by toggling its value every second.
while True:
    # Check if the XBee has any message in the queue.
    received_msg = xbee.receive()
    if received_msg:
        f = device_func[received_msg['profile']]
        f(received_msg['endpoint'], received_msg['cluster'], received_msg['payload'])



