"""Module qui contient la classe Arbre de Huffman"""

from typing import TypeVar
from typing_extensions import Self

T = TypeVar('T')

class ArbreHuffman:
    """
    Classe Arbre de Huffman : un arbre binaire non vide tel que :
    -les feuilles possèdent deux informations : un élément et un nombre d'occurences
    -les noeuds possèdent, un fils gauche et un fils droit ainsi qu'un nombre d'occurences
     égale à la somme des nombres d'occurrences des racines des deux fils
    """

    def __init__(self, element: T=None, nb_occurrences: int=None,\
                 fils_gauche: Self=None, fils_droit: Self=None):
        """
        __init__ Règle d'initialisation : L'utilisation de element et nb_occurrences
                 exclue l'utilisation de fils_gauche et de fils_droit, et inversement.
                 Aussi, le fils_gauche et le fils_droit ne doivent pas être identique

        Parameters
        ----------
        element : T, optional
            un élément si l'instance créé est une feuille rien si c'est un noeud, by default None
        nb_occurrences : int, optional
            nombre d'occurrences de l'élément ou somme des nombres d'occurrences aux racines des fils,
            by default None
        fils_gauche : Self, optional
            fils gauche, by default None
        fils_droit : Self, optional
            fils droit, by default None

        Raises
        ------
        ArbreHuffmanIncoherentErreur
            Exception lever lorsque les règles d'initialisation ne sont pas respectées
        """
        if (element and nb_occurrences) and (not fils_gauche and not fils_droit):
            self._element = element
            self._nb_occ = nb_occurrences
            self._fils_gauche = None
            self._fils_droit = None
        elif (not element and not nb_occurrences) and (fils_gauche and fils_droit) and (fils_droit is not fils_gauche) :
            self._element = None
            self._fils_gauche = fils_gauche
            self._fils_droit = fils_droit
            self._nb_occ = fils_gauche.nb_occurrences + fils_droit.nb_occurrences
        else:
            raise ArbreHuffmanIncoherentErreur("Noeud/Feuille incohérent(e)")

    @property
    def est_une_feuille(self) -> bool:
        """
        est_une_feuille Permet de savoir si un arbre est une feuille

        Returns
        -------
        bool
            Oui : c'est une feuille
            Non : c'est un noeud
        """
        return not self._fils_droit and not self._fils_gauche

    @property
    def nb_occurrences(self) -> int:
        """
        nb_occurrences Renvoie le nombre d'occurrences de la racine de l'arbre

        Returns
        -------
        int
            nombre d'occurrences
        """
        return self._nb_occ

    @property
    def element(self) -> T:
        """
        element Renvoie l'élément que contient une feuille

        Returns
        -------
        T
            Élément contenu par la feuille

        Raises
        ------
        DoitEtreUneFeuilleErreur
            Exception lever si la méthode est appelée sur un noeud
        """
        if not self.est_une_feuille:
            raise DoitEtreUneFeuilleErreur("Impossible d'accéder à l'élément d'un noeud")
        return self._element

    @property
    def fils_gauche(self) -> Self:
        """
        fils_gauche Renvoie le fils gauche

        Returns
        -------
        Self
            Le fils gauche de l'arbre

        Raises
        ------
        NeDoitPasEtreUneFeuilleErreur
            Exception lever lorsque la méthode est appelée sur une feuille
        """
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("Impossible d'accéder au fils gauche d'une feuille")
        return self._fils_gauche

    @property
    def fils_droit(self) -> Self:
        """
        fils_droit Renvoie le fils droit

        Returns
        -------
        Self
            Le fils droit de l'arbre

        Raises
        ------
        NeDoitPasEtreUneFeuilleErreur
            Exception lever lorsque la méthode est appelée sur une feuille
        """
        if self.est_une_feuille:
            raise NeDoitPasEtreUneFeuilleErreur("Impossible d'accéder au fils droit d'une feuille")
        return self._fils_droit

    def equivalent(self, autre_arbre: Self) -> bool:
        """
        equivalent Permet de savoir si deux arbres ont la même structure

        Parameters
        ----------
        autre_arbre : Self
            Un arbre de Huffman

        Returns
        -------
        bool
            Oui : Ils ont la même structure
            Non : Ils n'ont pas la même structure
        """
        if autre_arbre.est_une_feuille:
            if not self.est_une_feuille:
                return False

            return self.nb_occurrences == autre_arbre.nb_occurrences
        if self.est_une_feuille:
            return False

        return self.fils_gauche.equivalent(autre_arbre.fils_gauche)\
                and self.fils_droit.equivalent(autre_arbre.fils_droit)

    def __gt__(self, autre_arbre):
        return self.nb_occurrences > autre_arbre.nb_occurrences

    def __ge__(self, autre_arbre):
        return (self > autre_arbre) or self.equivalent(autre_arbre)

    def __lt__(self, autre_arbre):
        return self.nb_occurrences < autre_arbre.nb_occurrences

    def __le__(self, autre_arbre):
        return (self < autre_arbre) or self.equivalent(autre_arbre)

    def __add__(self, autre_arbre):
        return ArbreHuffman(fils_gauche=self, fils_droit=autre_arbre)

    def __repr__(self):
        description = f"ArbreHuffman(element : {self._element}, occurrences : {self.nb_occurrences})\
                      \n fils gauche : {self._fils_gauche} \n fils droit : {self._fils_droit}"
        return description

class ArbreHuffmanErreur(Exception):
    """Exception générale pour un arbre de Huffman"""

class DoitEtreUneFeuilleErreur(ArbreHuffmanErreur):
    """Exception"""

class NeDoitPasEtreUneFeuilleErreur(ArbreHuffmanErreur):
    """Exception"""

class ArbreHuffmanIncoherentErreur(ArbreHuffmanErreur):
    """Exception"""
