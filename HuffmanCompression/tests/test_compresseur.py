#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
import io
from huffman.compresseur import statistiques, arbre_de_huffman, codes_binaire
from huffman.compteur import Compteur
from huffman.arbre_huffman import ArbreHuffman
from huffman.code_binaire import Bit, CodeBinaire

# A 65, B 66, C 67, D 68, E 69, F 70, G 71
import itertools
octets_a_compresser = b"BACFGABDDACEACG"
donnees_compressees = bytes([52,50,2] + \
                            list(int.to_bytes(15, 4, byteorder='big')) + \
                            list(itertools.chain(*[list(int.to_bytes(octets_a_compresser.count(i), 4,  byteorder='big')) for i in range(256)])) + \
                            [145,159,105,229,100])

@pytest.fixture(scope="function")
def flux_donnees():
    return io.BytesIO(octets_a_compresser)

def test_statistiques(flux_donnees):
    stat, nb = statistiques(flux_donnees)
    assert nb == 15
    assert stat.sont_egaux(Compteur({65:4, 66:2, 67:3, 68:2, 69:1, 70:1, 71:2}))

def test_arbre_huffman(flux_donnees):
    stat, nb = statistiques(flux_donnees)
    arbre_huffman_calcule = arbre_de_huffman(stat)
    arbre_huffman_voulu = ArbreHuffman(
        fils_gauche = ArbreHuffman(
                fils_gauche = ArbreHuffman(67,3),
                fils_droit = ArbreHuffman(65,4)
        ),
        fils_droit = ArbreHuffman(
                fils_gauche = ArbreHuffman(
                    fils_gauche = ArbreHuffman(66,2),
                    fils_droit = ArbreHuffman(68,2)
                ),
            fils_droit = ArbreHuffman(
                fils_gauche = ArbreHuffman(71,2),
                fils_droit = ArbreHuffman(
                    fils_gauche = ArbreHuffman(69,1),
                    fils_droit = ArbreHuffman(70,1)
                )
            )
        )
    )
    assert arbre_huffman_voulu.equivalent(arbre_huffman_calcule)

def test_codes_binaire(flux_donnees):
    stat, nb = statistiques(flux_donnees)
    arbre = arbre_de_huffman(stat)
    codes_binaires_calcules = codes_binaire(arbre)
    assert len(codes_binaires_calcules[65]) == 2
    assert len(codes_binaires_calcules[66]) == 3
    assert len(codes_binaires_calcules[67]) == 2
    assert len(codes_binaires_calcules[68]) == 3
    assert len(codes_binaires_calcules[69]) == 4
    assert len(codes_binaires_calcules[70]) == 4
    assert len(codes_binaires_calcules[71]) == 3
