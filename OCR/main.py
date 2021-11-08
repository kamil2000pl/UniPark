import pytesseract
import cv2
import os
import matplotlib.pyplot as plt
import glob


#pytesseract.pytesseract.tesseract_cmd

#print(pytesseract.image_to_string(r'car.png'))

test_license_plate = cv2.imread(os.getcwd() + "/briancarzoom.jpg")
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