import RPi.GPIO as GPIO

PIR_pin = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
# TODO - GPIO.OUT Camera?


def vehicle_detection():
    while True:
        if GPIO.input(PIR_pin):
            print("Vehicle detected")
            # TODO - take photo
        else:
            print("No vehicle detected")


vehicle_detection()

# TODO - link with Pubnub

