# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from io import BytesIO
import cv2
import time

#import os

def prendreCapture(video,tts):
    """
    Prend une capture d'image à partir de la caméra connectée au robot.

    :param video: Proxy ALVideoDevice pour accéder à la caméra.
    :param tts: Proxy ALTextToSpeech pour les notifications vocales.
    :raises Exception: Si une erreur survient lors de la capture d'image.
    """
    
    # Créer un client vidéo
    resolution = 2  # 640x480
    color_space = 11  # RGB
    fps = 5  # images par seconde
    video_client = video.subscribe("capture", resolution, color_space, fps)

    try:
        # Capturer une image
        frame = video.getImageRemote(video_client)

        # Convertir l'image en format utilisable
        width = frame[0]
        height = frame[1]
        array = np.frombuffer(frame[6], dtype=np.uint8).reshape((height, width, 3))

        # Afficher l'image avec PIL
        img = Image.fromarray(array)
        #img.show()

        # Sauvegarder l'image
        img.save("./img/captured_image.jpg")
        #tts.say("Une photo a été prise")

    except Exception as e:
        print("Erreur lors de la capture de l'image:")

    finally:
        # Se désabonner pour libérer la caméra
        video.unsubscribe(video_client)


def detecterVisage(image,tts):
    
    """
    Détecte les visages dans une image donnée.

    Args:
        image (numpy.ndarray): L'image source en format BGR.
        tts (object): Proxy ALTextToSpeech pour les notifications vocales.

    Returns:
        bool: True si au moins un visage est détecté, False sinon.
    """
    
    
    # Vérifier si l'image a été chargée correctement
    if image is None:
        print("Erreur lors du chargement de l'image. Vérifiez le chemin ou le fichier image.")
    else:
        print("Dimensions de l'image: ", image.shape)

        # Convertir l'image en noir et blanc (prétraitement)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Charger le modèle de détection de visages
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Vérifier si le modèle a été chargé correctement
        if face_cascade.empty():
            print("Le fichier du modèle n'a pas été chargé correctement.")
        else:
            print("Le modèle de détection de visages est chargé.")

            # Détecter les visages dans l'image
            faces = face_cascade.detectMultiScale(image_gray, 1.1, 5)
            
            # visage(s) detecté(s) dans limage
            if len(faces)!=0:
                

                # Afficher le nombre de visages détectés
                print("{} visages détectés dans l'image.".format(len(faces)))
                tts.say("{} visages détectés dans l'image.".format(len(faces)))

                # Dessiner un rectangle autour de chaque visage détecté
                for x, y, width, height in faces:
                    cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)

                print("Détection terminée, visages encadrés.")

                # Sauvegarder l'image modifiée avec les rectangles
                cv2.imwrite("./img/visages_avec_rectangles.jpg", image)
                print("L'image modifiée a été sauvegardée sous 'visages_avec_rectangles.jpg'.")
                
                return True
            
            # 0 visage detecté dans limage
            else:
                print("zero visage detecté")
                return False

        
        
def extrairesVisages(image,tts):
    
    """
    Détecte et extrait les visages d'une image en utilisant un modèle Haar Cascade.
    
    :param image: Image en entrée (format BGR).
    :param tts: Optionnel, instance de Text-To-Speech pour les messages audio.
    """
    
        
    # Vérifier si l'image a été chargée correctement
    if image is None:
        print("Erreur lors du chargement de l'image. Vérifiez le chemin ou le fichier image.")
    else:
        print("Dimensions de l'image: ", image.shape)

        # Convertir l'image en noir et blanc (prétraitement)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Charger le modèle de détection de visages
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Vérifier si le modèle a été chargé correctement
        if face_cascade.empty():
            print("Le fichier du modèle n'a pas été chargé correctement.")
        else:
            print("Le modèle de détection de visages est chargé.")

            # Détecter les visages dans l'image
            faces = face_cascade.detectMultiScale(image_gray, 1.1, 5)

            # Afficher le nombre de visages détectés
            print("{} visages détectés dans l'image.".format(len(faces)))

            # Dessiner un rectangle autour de chaque visage détecté et extraire les visages
            for i, (x, y, width, height) in enumerate(faces):
                # Dessiner un rectangle autour du visage
                cv2.rectangle(image, (x, y), (x + width, y + height), color=(0, 255, 0), thickness=2)  # Rectangle vert

                # Extraire la région de l'image correspondant au visage
                face_image = image[y:y + height, x:x + width]

                # Sauvegarder l'image du visage extrait
                cv2.imwrite("./img/visages/visage{}.jpg".format(i+1), face_image)
                print("Le visage {} a été extrait et sauvegardé sous 'visage_extrait{}.jpg'.".format(i+1, i+1))
                #tts.say("Le visage     {} enregistré, pret aux traitements".format(i+1))


            print("Détection terminée, visages encadrés et extraits.")
            
            


def calculerDistance(image, face, focal_length=600, real_width=15):
    """
    Calcule la distance estimée entre la caméra et un visage détecté.

    :param image: L'image d'entrée
    :param face: Les coordonnées du visage (x, y, largeur, hauteur)
    :param focal_length: Distance focale en pixels (à ajuster selon la caméra)
    :param real_width: Largeur réelle du visage en cm (valeur moyenne : 15 cm)
    :return: Distance estimée en cm
    """
    _, _, width, _ = face
    distance = (focal_length * real_width) / width
    print("Distance estimée : {distance:.2f} cm")
    return distance


def deplacerVersVisage(motion, distance, angle):
    """
    Déplace le robot vers la position d'un visage détecté.

    :param motion: Proxy ALMotion
    :param distance: Distance à parcourir en cm
    :param angle: Angle à ajuster en radians pour faire face au visage
    """
    if distance > 30:  # Seulement si le visage est suffisamment éloigné
        print("Déplacement vers le visage : distance={distance:.2f} cm, angle={angle:.2f} radians")
        motion.moveTo(distance / 100.0, 0, angle)
        print("Déplacement terminé.")
    else:
        print("Le visage est déjà proche. Aucun déplacement nécessaire.")
        
def reculerDepuisVisage(motion, distance, angle):
    """
    Déplace le robot dans le chemin inverse depuis la position d'un visage détecté.

    :param motion: Proxy ALMotion
    :param distance: Distance à parcourir en cm
    :param angle: Angle à ajuster en radians pour faire face au visage
    """
    if distance > 30:  # Seulement si le visage est suffisamment éloigné
        print("Reculer depuis le visage : distance={distance:.2f} cm, angle={angle:.2f} radians")
        motion.moveTo(-distance / 100.0, 0, 0)  # Reculer dans l'axe inverse
        motion.moveTo(0, 0, -angle)
        print("Déplacement terminé.")
    else:
        print("Le visage est déjà trop proche. Aucun recul nécessaire.")


def coucou_bras_droit(motion, vitesse=0.2, repetitions=3):
    """
    Lève le bras droit et effectue un mouvement de coucou avec le robot Nao.

    :param motion: Instance du proxy ALMotion
    :param vitesse: Vitesse du mouvement (par défaut 0.2)
    :param repetitions: Nombre d'oscillations pour le coucou
    """
    # Lever le bras droit
    articulations_bras_droit = [
        "RShoulderPitch",  # Mouvement avant/arrière de l'épaule
        "RShoulderRoll",   # Mouvement latéral de l'épaule
        "RElbowYaw",       # Rotation du coude
        "RElbowRoll",      # Mouvement de flexion du coude
        "RWristYaw"        # Rotation du poignet
    ]

    angles_bras_droit = [
        -1.0,  # Inclinaison vers l'avant
         0.3,  # Léger écartement vers l'extérieur
         1.0,  # Rotation du coude
         0.5,  # Flexion du coude
         0.0   # Poignet en position neutre
    ]

    # Appliquer les angles pour lever le bras droit
    motion.setAngles(articulations_bras_droit, angles_bras_droit, vitesse)

    # Mouvement de coucou avec le poignet
    for _ in range(repetitions):
        motion.setAngles("RWristYaw", 0.5, vitesse)  # Rotation vers la droite
        time.sleep(0.5)  # Pause pour le mouvement
        motion.setAngles("RWristYaw", -0.5, vitesse)  # Rotation vers la gauche
        time.sleep(0.5)  # Pause pour le mouvement

    # Remettre le poignet en position neutre après le coucou
    motion.setAngles("RWristYaw", 0.0, vitesse)
