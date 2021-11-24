import cv2
import matplotlib.pyplot as plt
import pytesseract
#import RPi.GPIO as GPIO
import publish as publish
import threading

PIR_pin = 23

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PIR_pin, GPIO.IN)
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
pnconfig.subscribe_key = ''
pnconfig.publish_key = ''
pnconfig.uuid = 'a4009a03-48a7-4742-a3b0-6969bf1ae10e'
pubnub = PubNub(pnconfig)

# Set tesseract path to where the tesseract exe file is located
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# Read car image and convert color to RGB
def read_reg():
    carplate_img = cv2.imread('briancar2.jpg')
    carplate_img_rgb = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)

    # plt.imshow(carplate_img_rgb)
    carplate_img_rgb_crop = carplate_extract(carplate_img_rgb)
    carplate_img_rgb_resize = enlarge_img(carplate_img_rgb_crop,1.2)
    carplate_string = read_plate(carplate_img_rgb_resize)
    return carplate_string


# Function to enlarge the plt display for user to view more clearly
# def enlarge_plt_display(image, scale_factor):
#     width = int(image.shape[1] * scale_factor / 100)
#     height = int(image.shape[0] * scale_factor / 100)
#     dim = (width, height)
#     plt.figure(figsize = dim)
#     plt.axis('off')
#     plt.imshow(image)


# Import Haar Cascade XML file for Russian car plate numbers
carplate_haar_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


# Function to retrieve only the car plate sub-image itself
def carplate_extract(image):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in carplate_rects:
        carplate_img = image[y + 15:y + h - 10, x + 15:x + w - 20]

    return carplate_img


# Enlarge image and apply greyscale
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    resized_image_greyscale = cv2.cvtColor(resized_image, cv2.COLOR_RGB2GRAY)

    return resized_image_greyscale


# Read registration plate
def read_plate(image):
    reg_string = pytesseract.image_to_string(image,
                                config=f'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return reg_string

#
# # Display extracted car license plate image
# carplate_extract_img = carplate_extract(carplate_img_rgb)
# carplate_extract_img = enlarge_img(carplate_extract_img, 150)
# cv2.imshow('test',carplate_extract_img)
# cv2.waitKey(0)
#
# carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
#
# # Apply median blur + grayscale
# carplate_extract_img_gray_blur = cv2.medianBlur(carplate_extract_img_gray,3)
#
# print(pytesseract.image_to_string(carplate_extract_img_gray_blur,
#                                   config = f'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))

def vehicle_detection():
    while True:
        if GPIO.input(PIR_pin):
            print("Vehicle detected")
            # TODO - trigger camera to take a photo
            read_reg()
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