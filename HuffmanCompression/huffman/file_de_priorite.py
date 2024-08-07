""" Module File de priorité"""
# La manière dont la fonction 'enfiler' est codée n'est pas la meilleure.
# Il aurait fallu itérer en commençant par la tête de file

from typing import TypeVar

T = TypeVar('T')

class FileDePriorite:
    """Classe FileDePriorite"""

    def __init__(self, elements: list[T] = (), cle=lambda e:e):
        self._elements = []
        self._priorite = cle
        for i in elements:
            self.enfiler(i)

    @property
    def est_vide(self) -> bool:
        """
        est_vide Renvoie l'état de la liste
        
        Returns
        -------
        bool
            true : liste vide
            false : liste non vie
        """
        return not self._elements

    def enfiler(self, element: T) -> None:
        """
        enfiler Insère un élément à la bonne position dans la file

        Parameters
        ----------
        element : T
            Élément à insérer dans la file
        """
        try:
            element < element
        except Exception as ex:
            raise ElementNonComparableErreur\
            (f"{element} ne possède pas les méthode de comparaison") from ex

        try:
            if self.est_vide or not self._priorite(element) < self._priorite(self._elements[-1]):
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
        except TypeError as ex:
            raise ElementNonComparableErreur\
            (f"{element} ne peut pas être comparé aux autres éléments") from ex

    def defiler(self) -> T:
        """
        defiler Retire et Renvoie l'élément en tête de la file

        Returns
        -------
        T
            Élément en tête de file
        """
        if self.est_vide:
            raise FileDePrioriteVideErreur("Opération impossible car la file est vide.")

        return self._elements.pop(0)

    @property
    def element(self) -> T:
        """
        element Renvoie l'élément en tête de la file

        Returns
        -------
        T
            Élément en tête de file
        """
        if self.est_vide:
            raise FileDePrioriteVideErreur("Opération impossible car la liste est vide.")

        return self._elements[0]

    def __iter__(self):
        return iter(self._elements)

    def __repr__(self):
        if self.est_vide:
            return "FileDePriorite ()"
        return f"FileDePriorite({', '.join(map(str,self._elements))})"

class FileDePrioriteVideErreur(Exception):
    """
    Exception File de priorite vide
    """
class ElementNonComparableErreur(Exception):
    """
    Exception élément non comparable
    """
