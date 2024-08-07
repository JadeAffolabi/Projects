#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pytest
from huffman.arbre_huffman import ArbreHuffmanIncoherentErreur, NeDoitPasEtreUneFeuilleErreur, DoitEtreUneFeuilleErreur, ArbreHuffman

@pytest.fixture(scope="function")
def feuille():
    return ArbreHuffman('a', 1)

@pytest.fixture(scope="function")
def feuille2():
    return ArbreHuffman('a', 1)

@pytest.fixture(scope="function")
def feuille3():
    return ArbreHuffman('b', 2)

@pytest.fixture(scope="function")
def arbre():
    return ArbreHuffman(fils_gauche=ArbreHuffman('a', 1),fils_droit=ArbreHuffman('b', 2))

@pytest.fixture(scope="function")
def arbre2():
    return ArbreHuffman(fils_gauche=ArbreHuffman('a', 1),fils_droit=ArbreHuffman('b', 2))

@pytest.fixture(scope="function")
def arbre3():
    return ArbreHuffman(fils_gauche=ArbreHuffman('b', 2),fils_droit=ArbreHuffman('a', 1))

def test_arbre_incoherent_erreur1(feuille):
    with pytest.raises(ArbreHuffmanIncoherentErreur):
        ArbreHuffman()

def test_arbre_incoherent_erreur2(feuille):
    with pytest.raises(ArbreHuffmanIncoherentErreur):
        ArbreHuffman(fils_gauche=feuille, fils_droit=feuille)
        
@pytest.mark.parametrize("ab, resultat",
                         [("feuille", True),
                          ("arbre", False),
                         ])  
def test_est_une_feuille(ab, resultat, request):
    ab = request.getfixturevalue(ab)
    assert ab.est_une_feuille == resultat

def test_doit_etre_feuille_erreur(arbre):
    with pytest.raises(DoitEtreUneFeuilleErreur):
        arbre.element

def test_element(feuille):
    assert feuille.element == 'a'

@pytest.mark.parametrize("ab, resultat",
                         [("feuille", 1),
                          ("arbre", 3),
                        ])  
def test_nb_occurences(ab, resultat, request):
    ab = request.getfixturevalue(ab)
    assert ab.nb_occurrences == resultat    

def test_ne_doit_etre_feuille_erreur(feuille):
    with pytest.raises(NeDoitPasEtreUneFeuilleErreur):
        feuille.fils_gauche
        feuille.fils_droit

@pytest.mark.parametrize("ab1, ab2, resultat",
                         [("feuille", "feuille2", True),
                          ("feuille", "feuille3", False),
                          ("arbre", "arbre2", True),
                          ("arbre", "arbre3", False),
                          ("feuille", "arbre2", False),
                          ("arbre", "feuille", False)
                        ])  
def test_equivalent(ab1, ab2, resultat, request):
    ab1 = request.getfixturevalue(ab1)
    ab2 = request.getfixturevalue(ab2)
    assert (ab1.equivalent(ab2)) == resultat

def test_fils_gauche(arbre, feuille):
    assert arbre.fils_gauche.equivalent(feuille)

def test_fils_droit(arbre, feuille3):
    assert arbre.fils_droit.equivalent(feuille3)

def test_add(arbre, feuille, feuille3):
    assert arbre.equivalent(feuille + feuille3)

@pytest.mark.parametrize("ab1, ab2, resultat",
                         [("feuille", "feuille2", False),
                          ("feuille", "feuille3", True),
                          ("feuille", "arbre", True)
                        ])      
def test_plus_petit(ab1, ab2, resultat, request):
    ab1 = request.getfixturevalue(ab1)
    ab2 = request.getfixturevalue(ab2)
    assert (ab1 < ab2) == resultat

@pytest.mark.parametrize("ab1, ab2, resultat",
                         [("feuille", "feuille2", True),
                          ("feuille", "feuille3", True),
                          ("feuille", "arbre", True)
                        ])      
def test_plus_petit_ou_egal(ab1, ab2, resultat, request):
    ab1 = request.getfixturevalue(ab1)
    ab2 = request.getfixturevalue(ab2)
    assert (ab1 <= ab2) == resultat

@pytest.mark.parametrize("ab1, ab2, resultat",
                         [("feuille", "feuille2", False),
                          ("feuille", "feuille3", False),
                          ("arbre", "feuille", True)
                        ])      
def test_plus_grand(ab1, ab2, resultat, request):
    ab1 = request.getfixturevalue(ab1)
    ab2 = request.getfixturevalue(ab2)
    assert (ab1 > ab2) == resultat

    
@pytest.mark.parametrize("ab1, ab2, resultat",
                         [("feuille", "feuille2", True),
                          ("feuille", "feuille3", False),
                          ("arbre", "feuille", True)
                        ])      
def test_plus_grand_ou_egal(ab1, ab2, resultat, request):
    ab1 = request.getfixturevalue(ab1)
    ab2 = request.getfixturevalue(ab2)
    assert (ab1 >= ab2) == resultat 
