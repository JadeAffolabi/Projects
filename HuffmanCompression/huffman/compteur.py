""" Module qui contient la  classe Compteur"""

from collections import Counter


class Compteur:
    """Classe Compteur"""
    def __init__(self, dict_init = None):
        if dict_init is None:
            self._dict = {}
        else:
            self._dict = dict_init

    def incrementer(self, key) -> None:
        """méthode incrementer"""
        has_key = lambda x : self._dict.get(x) is not None
        if has_key(key):
            self._dict.update({key : self._dict[key]+1})
        else:
            self._dict.update({key : 1})

    def fixer(self, key, values) -> None:
        """méthode fixer"""
        self._dict.update({key : values})

    def nb_occurrences(self, key) -> int:
        """méthode nb_occurrences"""
        if key in self._dict.keys():
            return self._dict[key]
        return 0

    @property
    def elements(self) -> list:
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

    def sont_egaux(self, compteur) -> bool:
        """méthode sont_egaux"""
        if len(self.elements) != len(compteur.elements):
            return False
        return all((Counter(self.elements_par_nb_occurrences().get(occur)) == Counter(liste)
                 for occur,liste in compteur.elements_par_nb_occurrences().items()))

