import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('images2/Seat_7.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
result = pytesseract.image_to_string(img).split()
# result = pytesseract.image_to_string(img)
print(result)
for a in result:
    a = a.replace(',', '')
    try:
        float(a)
        print(f'stack size is {a}')
    except ValueError:
        print(f'not a number: {a}')

cv2.imshow('results',img)
cv2.waitKey(0)


