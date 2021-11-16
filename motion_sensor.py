import RPi.GPIO as GPIO
import publish as publish
import threading

PIR_pin = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_pin, GPIO.IN)
# TODO - GPIO.OUT Camera?

# Pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

my_channel = "unipark-pi-channel"
sensors = ["camera", "barcode"]
data = {}

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'pub-c-d97bac76-5913-453f-80ac-3df34c710585'
pnconfig.publish_key = 'sub-c-e973009a-4250-11ec-96b3-4a48f5067549'
pnconfig.uuid = 'a4009a03-48a7-4742-a3b0-6969bf1ae10e'
pubnub = PubNub(pnconfig)


def vehicle_detection():
    while True:
        if GPIO.input(PIR_pin):
            print("Vehicle detected")
            # TODO - trigger camera to take a photo
            # TODO - get reg plate string from OCR code
            # TODO - publish car reg to Pubnub
            publish(my_channel, {"car_reg": ""})
        else:
            print("No vehicle detected")
            publish(my_channel, {"car_reg": "none"})
            # TODO - trigger barcode scanner prompt


def publish(channel, message):
    pubnub.publish().channel(my_channel).message(message).pn_async(my_publish_callback)


def my_publish_callback(envelope, status):
    if not status.is_error(): # check success or not
        print("Message published")
        pass
    else:
        pass


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass

        elif status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to Pubnub")
            pubnub.publish().channel(my_channel).message("Welcome to UniPark").pn_async(my_publish_callback)

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass


# TODO
def message(self, pubnub, message):
    try:
        print(message.message, ": ", type(message.message))
        message = message.message
        key = list(message.keys())
        if key[0] == "event":
            self.handleEvent(message)
    except Exception as e:
        print("Received: ", message.message)
        print(e)
        pass


def handle_event(self, msg):
    global data
    eventData = message["event"]
    key = list(eventData.keys())
    print(key)
    print(key[0])

    if key[0] in sensors:
        if eventData[key[0]] == "ON":
            print("Camera triggered")
            data["camera"] = True

        elif eventData[key[0]] == "OFF":
            print("camera NOT triggered")
            data["camera"] = False


vehicle_detection()

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=vehicle_detection)
    sensor_thread.start()
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()
    print(pubnub.get_subscribed_channels())
