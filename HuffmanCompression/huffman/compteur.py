""" Module qui contient la  classe Compteur"""

from collections import Counter


class Compteur:
    """Classe Compteur"""
    def __init__(self, dict_init = None):
        if dict_init is None:
            self._dict = {}
        else:
            self._dict = dict_init

    def incrementer(self, key):
        """méthode incrementer"""
        has_key = lambda x : self._dict.get(x) is not None
        if has_key(key):
            self._dict.update({key : self._dict[key]+1})
        else:
            self._dict.update({key : 1})

    def fixer(self, key, values):
        """méthode fixer"""
        self._dict.update({key : values})

    def nb_occurrences(self, key):
        """méthode nb_occurrences"""
        if key in self._dict.keys():
            return self._dict[key]
        return 0

    @property
    def elements(self):
        """méthode elements"""
        return list(self._dict.keys())

    def __elements_x_frequents(self, x_frequents = lambda x,y : x == y):
        res = [list(self._dict.keys())[0]]
        for key in self._dict.keys():
            if x_frequents(self._dict[key], self._dict[res[0]]):
                res = [key]
            elif self._dict[key] == self._dict[res[0]]:
                res.append(key)
        return res

    def elements_moins_frequents(self):
        """méthode elements_moins_frequents"""
        return self.__elements_x_frequents(lambda x,y : x < y)

    def elements_plus_frequents(self):
        """méthode elements_plus_frequents"""
        return self.__elements_x_frequents(lambda x,y : x > y)

    def elements_par_nb_occurrences(self):
        """méthode elements_par_nb_occurences"""
        return {val : [key for key in self._dict.keys() if self._dict[key] == val]
                 for val in self._dict.values()}

    def sont_egaux(self, compteur):
        """méthode sont_egaux"""
        if len(self.elements()) != len(compteur.elements()):
            return False
        return all((Counter(self.elements_par_nb_occurrences().get(occur)) == Counter(liste)
                 for occur,liste in compteur.elements_par_nb_occurrences().items()))

if __name__ == "__main__":

    compt1 = Compteur()
    compt1.incrementer("A")
    compt1.incrementer("B")
    compt1.incrementer("A")
    compt1.fixer("C", 5)
    compt1.fixer("D", 1)
    compt1.fixer("E", 2)
    print(compt1.elements())
    print(f"Le nombre d'occurrences de C est : {compt1.nb_occurrences('C')}")
    print(f"L'élement le moins fréquent est : {compt1.elements_moins_frequents()}")
    print(f"L'élement le plus fréquent est : {compt1.elements_plus_frequents()}")
    print(compt1.elements_par_nb_occurrences())

    compt2 = Compteur({"A":2, "B":1, "C":5, "D":1, "E":2})
    print(compt2.elements())

    print(compt1.sont_egaux(compt2))
