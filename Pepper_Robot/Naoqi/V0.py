# -*- coding: utf-8 -*-

# Importation des modules nécessaires
from naoqi import ALProxy  # Pour l'accès aux modules du robot Pepper
from utils import *  # Importation des utilitaires définis par l'utilisateur
from gender_classifier import *  # Importation de la fonction de classification du genre
#import mouvement # Module commenté (peut-être pour la gestion des mouvements du robot)
#import time  # Module pour la gestion des délais

# Adresse IP et port du robot Pepper
ip_address = "192.168.0.101"
port = 9559 

# Création des proxies pour accéder aux modules du robot : moteur, voix, vidéo, détection de visages
motion = ALProxy("ALMotion", ip_address, port)  # Proxy pour les mouvements du robot
tts = ALProxy("ALTextToSpeech", ip_address, port)  # Proxy pour la synthèse vocale
video = ALProxy("ALVideoDevice", ip_address, port)  # Proxy pour la caméra
face_detection = ALProxy("ALFaceDetection", ip_address, port)  # Proxy pour la détection des visages

# Réglage de l'angle de la tête du robot
motion.setAngles("HeadPitch", -0.2, 0.2)  # Incline la tête vers le haut, ajustable

# Configuration de la langue pour la synthèse vocale
tts.setLanguage("French")

# Définition des angles pour le mouvement de la tête (gauche à droite et droite à gauche)
angles_gauche_droite = np.linspace(-1.5, 1.5, 5)  # Série d'angles pour faire bouger la tête de gauche à droite
angles_droite_gauche = np.linspace(-1.5, 1.5, 5)  # Série d'angles pour faire bouger la tête de droite à gauche
vitesse = 0.4  # Vitesse du mouvement de la tête

# Direction initiale du mouvement de la tête
sens_de_rotation_tete = "gauche_a_droite"

# ---- Début de l'exécution principale ------

while(1):  # Boucle infinie pour que le robot continue à fonctionner

    # Alterner la direction de la rotation de la tête à chaque itération
    if sens_de_rotation_tete == "gauche_a_droite":
        tab_angles_tete = angles_gauche_droite  # On définit les angles pour un mouvement gauche à droite
        sens_de_rotation_tete = "droite_a_gauche"  # Change la direction pour la prochaine itération
    else: 
        tab_angles_tete = angles_droite_gauche  # On définit les angles pour un mouvement droite à gauche
        sens_de_rotation_tete = "gauche_a_droite"  # Change la direction pour la prochaine itération
    
    # Réglage de l'inclinaison de la tête pour chaque cycle
    motion.setAngles("HeadPitch", -0.2, 0.2)  # Valeur négative pour incliner la tête vers le haut

    # Parcours des angles définis précédemment pour faire bouger la tête
    for angle in tab_angles_tete:

        # Mouvement de la tête avec l'angle défini
        motion.setAngles("HeadYaw", angle, vitesse)  # On fait tourner la tête sur l'axe horizontal (HeadYaw)
        time.sleep(1)  # Pause pour donner le temps au robot de tourner la tête

        # Prendre une capture d'image de la caméra du robot
        prendreCapture(video, tts)
        
        # Chargement de l'image capturée et traitement
        capture = cv2.imread("./img/captured_image.jpg")
        if(detecterVisage(capture, tts)):  # Si un visage est détecté dans l'image

            # Lecture de l'image avec les visages détectés et encadrés
            visages_encadres = cv2.imread("./img/visages_avec_rectangles.jpg")
            
            # Extraction des visages à partir de l'image encadrée
            extrairesVisages(visages_encadres, tts)
            
            # Conversion de l'image en niveaux de gris pour la détection des visages
            visages_encadres_gray = cv2.cvtColor(visages_encadres, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  # Chargement du classificateur de visages
            faces = face_cascade.detectMultiScale(visages_encadres_gray, 1.1, 5)  # Détection des visages

            if len(faces):  # Si des visages sont détectés
                # Pivoter le robot pour mieux aligner la tête avec le visage
                motion.moveTo(0, 0, angle)  # Mouvement du robot pour s'orienter vers l'angle de la tête
                
                motion.setAngles("HeadYaw", angle, vitesse)  # Pivoter la tête à l'angle souhaité
                
                # Sélection du premier visage détecté
                face = faces[0, :]
                print(face)

                # Calcul de la distance entre le robot et le visage détecté
                distance = calculerDistance(visages_encadres, face)
                
                # Déplacement du robot vers le visage
                deplacerVersVisage(motion, distance, 0)
                
                # Traitement de l'image du visage pour la prédiction du genre
                tete = cv2.imread("./img/visages/visage1.jpg")  # Chargement d'une image de visage à classifier
                img_data = image_preprocessing(tete)  # Prétraitement de l'image pour la classification
                predicted_gender, accuracy = gender_prediction(img_data)  # Prédiction du genre
                
                # Annonce du genre avec la synthèse vocale
                if predicted_gender == 1:
                    tts.say("Bonjour Monsieur, je suis sur à {:.2f} pourcent ".format(accuracy * 100))
                elif predicted_gender == 0:
                    tts.say("Bonjour Madame, je suis sur à {:.2f} pourcent ".format(accuracy * 100))
                
                # Exécution d'un mouvement spécifique (coucou avec le bras droit)
                coucou_bras_droit(motion)
                    
                # Réinitialisation de l'inclinaison de la tête
                motion.setAngles("HeadPitch", -0.2, 0.2)

                break  # Fin de la détection et des actions liées à ce visage

    # Affichage du statut de la rotation de la tête
    print("Déplacement complet de la tête terminé.")

    # Mouvement pour effectuer un demi-tour
    print("Demi-tour en cours...")
    motion.moveTo(0, 0, 3.14159)  # 3.14159 radians = 180 degrés
    print("Demi-tour terminé.")
