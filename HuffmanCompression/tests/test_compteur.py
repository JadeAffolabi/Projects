import pytest
from huffman.compteur import Compteur

@pytest.fixture(scope="function")
def un_compteur():
    return Compteur({"A":2, "B":3, "C":10, "D":1})


@pytest.mark.parametrize("key, val", [("A",2), ("B",3), ("C",10), ("D",1)])
def test_nb_occurrences(un_compteur, key, val):
    assert un_compteur.nb_occurrences(key) == val

def test_incrementer(un_compteur):
    un_compteur.incrementer("C")
    un_compteur.incrementer("Z")
    assert un_compteur.nb_occurrences("C") == 11
    assert un_compteur.nb_occurrences("Z") == 1

def test_fixer(un_compteur):
    un_compteur.fixer("A", 30)
    assert un_compteur.nb_occurrences("A") == 30

def test_elements(un_compteur):
    assert un_compteur.elements == ["A", "B", "C", "D"]

def test_element_moins_frequent(un_compteur):
    un_compteur.incrementer("E")
    assert un_compteur.elements_moins_frequents() == ["D", "E"]

def test_element_plus_frequent(un_compteur):
    assert un_compteur.elements_plus_frequents() == ["C"]

def test_elements_par_nb_occurrences(un_compteur):
    un_compteur.fixer("E", 2)
    un_compteur.incrementer("F")
    a_tester = un_compteur.elements_par_nb_occurrences() 
    resultat = {2:["A", "E"], 3:["B"], 10:["C"], 1:["D", "F"]}
    assert len(resultat) == len(a_tester)
    assert all((resultat[k] == v for k,v in a_tester.items()))

def test_sont_egaux(un_compteur):
    compteur2 = Compteur({"A":2, "B":3, "C":10, "D":1})
    compteur3 = Compteur({"A":2, "B":3, "C":1, "D":1})
    compteur4 = Compteur({"A":2, "B":3})
    assert un_compteur.sont_egaux(compteur2)
    assert not un_compteur.sont_egaux(compteur3)
    assert not un_compteur.sont_egaux(compteur4)