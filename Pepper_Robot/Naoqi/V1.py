# -*- coding: utf-8 -*-

from naoqi import ALProxy
import time
import cv2
from utils import *
from gender_classifier import *
#from mouvement import *


ip_address = "192.168.0.101"
port = 9559

# création des proxies pour les moteurs, la voix, et le flux vidéo
motion = ALProxy("ALMotion", ip_address, port)
tts = ALProxy("ALTextToSpeech", ip_address, port)
video = ALProxy("ALVideoDevice", ip_address, port)
face_detection = ALProxy("ALFaceDetection", ip_address, port)

# Incliner la tête vers le haut (valeur positive pour "HeadPitch")
motion.setAngles("HeadPitch", -0.2, 0.2)  # Inclinaison vers le haut

# config de la voix
tts.setLanguage("French")

angles_gauche_droite = [-0.8, 0.0, 0.8]
angles_droite_gauche = [0.8, 0.0, -0.8]
vitesse = 0.2  # Vitesse de déplacement de la tête

sens_de_rotation_tete = "gauche_a_droite"

# ---- main ------
while True:
    if sens_de_rotation_tete == "gauche_a_droite":
        tab_angles_tete = angles_gauche_droite
        sens_de_rotation_tete = "droite_a_gauche"
    else:
        tab_angles_tete = angles_droite_gauche
        sens_de_rotation_tete = "gauche_a_droite"

    # Maintenir l'inclinaison de la tête vers le haut

    for angle in tab_angles_tete:
        motion.setAngles("HeadPitch",-0.2, 0.2)  # Inclinaison vers le haut
        motion.setAngles("HeadYaw", angle, vitesse)
        #time.sleep(1)
        prendreCapture(video, tts)

        capture = cv2.imread("./img/captured_image.jpg")
        if detecterVisage(capture, tts):
            visages_encadres = cv2.imread("./img/visages_avec_rectangles.jpg")

            # Pour Jade
            extrairesVisages(visages_encadres, tts)

            # Détection des visages
            visages_encadres_gray = cv2.cvtColor(visages_encadres, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(visages_encadres_gray, 1.1, 5)

            if len(faces):
                # Prendre le premier visage détecté
                face = faces[0, :]
                print(face)
                motion.setAngles("HeadPitch", -0.2, 0.2)  

                distance = calculerDistance(visages_encadres, face)
                print(distance)

                # Le robot se déplace vers le visage
                motion.moveTo(0, 0, angle)
                #motion.setAngles("HeadYaw", 0.0, 0.2)  # Retour à 0° horizontal
                motion.setAngles("HeadPitch", -0.2, 0.2)  # Inclinaison maintenue vers le haut
                time.sleep(0.5)
                deplacerVersVisage(motion, distance, 0)


                # ---- Bonjour madame ou monsieur
                tete = cv2.imread("./img/visages/visage1.jpg")
                #img_data = image_preprocessing(tete)
                clf = Gender_Classifier()
                predicted_gender, accuracy = gender_prediction(tete, clf)

                if predicted_gender == "Male":
                    tts.say("Bonjour Monsieur, je suis sûr à {:.1f}%".format(accuracy * 100))
                elif predicted_gender == "Female":
                    tts.say("Bonjour Madame, je suis sûr à {:.1f}%".format(accuracy * 100))

                # Si une interaction avec les bras est nécessaire
                coucou_bras_droit(motion)

                # Reculer après avoir détecté et interagi avec le visage
                reculerDepuisVisage(motion, distance, angle)

                break  # Sortir de la boucle après avoir détecté un visage et interagi
