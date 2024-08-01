""" Module File de priorité"""
# La manière dont la fonction 'enfiler' est codée n'est pas la meilleure.
# Il aurait fallu itérer en commençant par la tête de file

class FileDePriorite:
    """Classe FileDePriorite"""

    def __init__(self, elements=(), cle=lambda e:e):
        self._elements = []
        self._priorite = cle
        for i in elements:
            self.enfiler(i)

    def est_vide(self):
        """Fonction qui permet de savoir si la file de priorité est vide"""
        return not self._elements

    def enfiler(self, element):
        """Fonction qui permet d'enfiler un élement dans la file"""
        if self.est_vide() or not self._priorite(element) < self._priorite(self._elements[-1]):
        # Cas d'une liste vide et cas d'ajout en fin de la file
            self._elements.append(element)
        else:
            indice = -2
            while (abs(indice) <= len(self._elements)) \
                  and (self._priorite(element) < self._priorite(self._elements[indice])):
                indice -= 1

            if abs(indice) > len(self._elements):
                self._elements.insert(0, element) #Ajout en tête de file
            else:
                self._elements.insert(indice+1, element) #Ajout avant l'élément prioritaire

    def defiler(self):
        """Fonction pour défiler l'élément en tête de file"""
        return self._elements.pop(0)

    def element(self):
        """Fonction pour obtenir l'élément en tête de file"""
        return self._elements[0]

    def __iter__(self):
        return iter(self._elements)

    def __repr__(self):
        if self.est_vide():
            return "FileDePriorite ()"
        return f"FileDePriorite ({', '.join(map(str,self._elements))})"
