import pytesseract
import cv2
import os
import matplotlib.pyplot as plt

import glob

reg_plate_data = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Read car image and convert color to RGB
#image = cv2.imread('/briancar.jpg')


def plt_show(image, title="", gray = False, size=(100,100)):
    temp = image
    if gray == False:
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        plt.title(title)
        plt.imshow(temp, cmap='gray')
        plt.show()


def detect_number(img):
    temp = img
    gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    number = reg_plate_data.detectMultiScale(img,1.2)
    print("number plate detected:"+str(len(number)))
    for numbers in number:
        (x,y,w,h) = numbers
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+h]
        cv2.rectangle(temp, (x,y), (x+w,y+h), (0,0,255), 5)

    plt_show(temp)


img = cv2.imread("briancar.jpg")
#plt_show(img)
detect_number(img)


#detected_carplate_img = carplate_detect(carplate_img_rgb)
#plt.imshow(detected_carplate_img)
#pytesseract.pytesseract.tesseract_cmd

#print(pytesseract.image_to_string(r'car.png'))

"""
test_license_plate = cv2.imread(os.getcwd() + "/briancar.jpg")
plt.imshow(test_license_plate)
plt.axis('off')

resize_test_license_plate = cv2.resize(
    test_license_plate, None, fx = 2, fy = 2,
    interpolation = cv2.INTER_CUBIC)

grayscale_resize_test_license_plate = cv2.cvtColor(
    resize_test_license_plate, cv2.COLOR_BGR2GRAY)

gaussian_blur_license_plate = cv2.GaussianBlur(
    grayscale_resize_test_license_plate, (5, 5), 0)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
img = cv2.imread('reg.jpg')
#img = cv2.resize(img, (600, 360))
print(pytesseract.image_to_string(gaussian_blur_license_plate, lang ='eng', config ='--oem 3 -l eng --psm 6 -c tessedit_char_whitelist=ACDEGHJKLMNOQRSTUVWXY123456789'))
#cv2.imshow('',grayscale_resize_test_license_plate)
#cv2.waitKey(0)
"""