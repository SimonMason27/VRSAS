import cv2
import numpy as np

input_file = '/home/pi/Documents/Images_from_Pi/22-Sep-2022_01:19:33.png' #this should be full path to image
image = cv2.imread(input_file)

original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours and filter for QR code
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
        cv2.rectangle(image, (x-5, y-5), (x + w+5, y + h+5), (36,255,12), 2)
        ROI = original[y:y+h, x:x+w]
        cv2.imwrite('ROI.png', ROI)


#Resize image to fit to screen
image = cv2.resize(image,(1040,1040))
#Shows all bounding boxes
cv2.imwrite('/home/pi/Documents/Images_from_Pi/22-Sep-2022_01:19:33.png', image)

#wait keys
cv2.waitKey(0)
cv2.destroyAllWindows()