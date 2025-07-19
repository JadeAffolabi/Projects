import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
IMAGE_FILE_PATH = "./img/visages/"
class Gender_Classifier(): 
    def __init__(self):
        self._prototxt = "./models/gender_deploy.prototxt"
        self._caffemodel = "./models/gender_net.caffemodel"
        self._MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        self._clf = cv2.dnn.readNet(self._caffemodel, self._prototxt)
        self._classes = ["Male", "Female"]
    
    def predict(self, face):
        blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), self._MODEL_MEAN_VALUES, swapRB=False)
        self._clf.setInput(blob)
        genderPrediction = self._clf.forward()
        predicted_gender = self._classes[genderPrediction[0].argmax()]
        accuracy = genderPrediction[0].max()
        return predicted_gender, accuracy

# This function is not used in order to well predict gender using the opencv model.
# def image_preprocessing(img):
#     IMG_SIZE = 96
#     size = (IMG_SIZE,IMG_SIZE)
#     img_data = cv2.resize(img, size)
#     img_data = img_data.astype("float32")
#     img_data /= 255 # Normalization 
#     return img_data

def gender_prediction(img, clf):
    return clf.predict(img)

def main(args=None):
    list_img_name = os.listdir(IMAGE_FILE_PATH)
    gender_clf = Gender_Classifier()

    for img_name in list_img_name:
        print(img_name)
        img_input = cv2.imread(IMAGE_FILE_PATH+img_name)

        predicted_gender, accuracy = gender_prediction(img_input, gender_clf)

        if predicted_gender == "Male":
            print("This is a male : {:.1f}".format(accuracy))
        elif predicted_gender == "Female":
            print("This is a female : {:.1f}".format(accuracy))

if __name__ == "__main__":
    main()
