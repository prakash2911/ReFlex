from tensorflow.keras import models
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2





def imageProcess(img):
    img_shape = (224, 224)
    img = img.resize(img_shape)
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img

def EyeImageProcessing(img):
    image_shape = (24,24)
    eye_model = models.load_model('model/cnnCat2.h5')
    img = img.convert("L")
    img = img.resize(image_shape)
    img = np.array(img)
    img = img.reshape(24,24,-1)
    img = np.expand_dims(img,axis=0)
    img = eye_model.predict(img)[0]

    return np.argmax(img)
def processEye(eye_image):
    resEye =-1
    leye = cv2.CascadeClassifier('haarcascade/haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haarcascade/haarcascade_righteye_2splits.xml')
    ans = ['1', '0', '0', '1']
    gray = eye_image.convert("L")
    gray_cv = cv2.cvtColor(np.array(gray), cv2.COLOR_GRAY2BGR)
    leyes = leye.detectMultiScale(gray_cv, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    reyes = reye.detectMultiScale(gray_cv, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    leye_image=None
    reye_image=None
    for (ex, ey, ew, eh) in leyes:
        leye_image = eye_image.crop((ex, ey, ex + ew, ey + eh))
    for (ex, ey, ew, eh) in reyes:
        reye_image = eye_image.crop((ex, ey, ex + ew, ey + eh))

    if leye_image !=None and reye_image!=None :
        reslEye = EyeImageProcessing(leye_image)
        resrEye = EyeImageProcessing(reye_image)
        if resrEye == reslEye:
            resEye = ans[reslEye]
        else:
            resEye = 1
    return resEye


def find(img):
    face = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_alt.xml')
    model = models.load_model('./model/model.h5')
    ans = ['1', '0', '0', '1']
    resYarn = -1
    resEye = processEye(img)
    gray = img.convert("L")
    gray_cv = cv2.cvtColor(np.array(gray), cv2.COLOR_GRAY2BGR)
    detectedFace = face.detectMultiScale(gray_cv, scaleFactor=1.1, minNeighbors=5, minSize=(25, 25))
    imgCropped = None
    for (ex, ey, ew, eh) in detectedFace:
        imgCropped = img.crop((ex, ey, ex + ew, ey + eh))
    if imgCropped!=None:
        imgCropped = imgCropped.convert('RGB')
        imgCropped = imageProcess(imgCropped)
        predictyarn = model.predict(imgCropped)
        resYarn = np.argmax(predictyarn[0])
        resYarn = ans[resYarn]
    return resEye,resYarn