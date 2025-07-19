# PAO Robot - Configuration et Installation

## Description
Le but de ce projet est de configurer un robot Pepper afin qu’il puisse interagir avec des personnes lors de la journée portes ouvertes de l’école.

Lorsque le robot détecte un visage, il doit s’avancer vers la personne détectée et lui tendre la main tout en la saluant de manière appropriée :

« Bonjour Monsieur », si c’est un homme ;

« Bonjour Madame », si c’est une femme.

Pour cela, nous avons entraîné un réseau de neurones convolutif (CNN) pour la classification de visages, et nous avons géré les interactions du robot à l’aide de ROS (Robot Operating System) et de la librairie Naoqi en Python.

---



## Étapes d'installation

### 1. Clonez le repository

Clonez le projet depuis GitHub avec la commande suivante :

```bash
git clone https://gitlab.insa-rouen.fr/baffolabi/pao_robot.git
```

### 2. Accédez au répertoire cloné

Entrez dans le répertoire du projet cloné :

```bash
cd pao_robot/Naoqi
```

### 3. Créez un environnement virtuel Python 2.7

Si vous n'avez pas encore virtualenv installé, vous pouvez l'installer avec :

```bash
pip install virtualenv
```

Ensuite, créez l'environnement virtuel avec :

```bash
virtualenv -p python2.7 venv
```

### 4. Activez l'environnement virtuel

Sur Linux/macOS :

```bash
source venv/bin/activate
```

Sur Windows :

```bash
.\venv\Scripts\activate
```

### 5. Installez les dépendances nécessaires

Installez toutes les dépendances nécessaires au projet en exécutant :

```bash
pip install -r requirements.txt
```

### 6. Configurez la variable d'environnement PYTHONPATH

Définissez la variable d'environnement PYTHONPATH pour que le robot puisse accéder aux modules nécessaires. Remplacez `path_de_ton_pc` par le chemin absolu du répertoire sur votre machine :

```bash
export PYTHONPATH=path_de_ton_pc/Naoqi/lib/python2.7/site-packages:$PYTHONPATH
```

### 7. Vérifiez l'installation

Pour vérifier que tout est bien installé, assurez-vous que l'environnement virtuel est bien activé en utilisant la commande suivante :

```bash
which python
```

Vous devriez voir un chemin qui pointe vers le répertoire `venv`.

---

## Lancer le projet

Une fois l'installation terminée, vous pouvez commencer à travailler avec le robot NAO en suivant les instructions du projet.

1. Connectez votre ordinateur et le robot au même réseau en vous assurant qu'ils sont reliés au même routeur.
2. Allumez le robot et appuyez sur le bouton situé sous l'écran pour obtenir son adresse IP.
3. Une fois l'adresse IP récupérée, remplacez-la dans la variable `ip_address` des fichiers `V0.py` ou `V1.py`.
4. Lancez le fichier souhaité avec Python 2.7 en utilisant les commandes suivantes :

   ```bash
   python V0.py
   ```
   ou
   ```bash
   python V1.py
   ```

Si vous avez respecté les étapes précédentes, le fichier devrait s'exécuter correctement.

---

## Notes

- Ce projet utilise l'API NAOqi pour interagir avec le robot NAO.
- Assurez-vous que votre robot est bien connecté au même réseau que votre machine de développement.
