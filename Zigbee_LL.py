from machine import Pin
import time
import xbee

# Pin D9 (ON/SLEEP/DIO9)
LED_PIN_ID = "D4"

payload = "0";

print(" +--------------------------------------+")
print(" | XBee MicroPython Blinking LED Sample |")
print(" +--------------------------------------+\n")

# Set up the LED pin object to manage the LED status. Configure the pin
# as output and set its initial value to off (0).
led_pin = Pin(LED_PIN_ID, Pin.OUT, value=0)

# Start blinking the LED by toggling its value every second.
while True:
    # Check if the XBee has any message in the queue.
    received_msg = xbee.receive()
    if received_msg:
        # Get the sender's 64-bit address and payload from the received message.
        payload = received_msg['payload']
        print(int(payload))
        # payload = payload.decode()

    print("- LED OFF")
    led_pin.value(0)
    time.sleep_ms(int(payload))

    print("- LED ON")
    led_pin.value(1)
    time.sleep_ms(int(payload))

