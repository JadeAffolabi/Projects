#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytest
import io
from huffman.compresseur import statistiques, arbre_de_huffman, codes_binaire
from huffman.compteur import Compteur
from huffman.arbre_huffman import ArbreHuffman
from huffman.code_binaire import Bit, CodeBinaire

# A b'A', B b'B', C b'C', D b'D', E b'E', F b'F', G b'G'
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
    assert stat.sont_egaux(Compteur({b'A':4, b'B':2, b'C':3, b'D':2, b'E':1, b'F':1, b'G':2}))

def test_arbre_huffman(flux_donnees):
    stat, nb = statistiques(flux_donnees)
    arbre_huffman_calcule = arbre_de_huffman(stat)
    arbre_huffman_voulu = ArbreHuffman(
        fils_gauche = ArbreHuffman(
                fils_gauche = ArbreHuffman(b'C',3),
                fils_droit = ArbreHuffman(b'A',4)
        ),
        fils_droit = ArbreHuffman(
                fils_gauche = ArbreHuffman(
                    fils_gauche = ArbreHuffman(b'B',2),
                    fils_droit = ArbreHuffman(b'D',2)
                ),
            fils_droit = ArbreHuffman(
                fils_gauche = ArbreHuffman(b'G',2),
                fils_droit = ArbreHuffman(
                    fils_gauche = ArbreHuffman(b'E',1),
                    fils_droit = ArbreHuffman(b'F',1)
                )
            )
        )
    )
    assert arbre_huffman_voulu.equivalent(arbre_huffman_calcule)

def test_codes_binaire(flux_donnees):
    stat, nb = statistiques(flux_donnees)
    arbre = arbre_de_huffman(stat)
    codes_binaires_calcules = codes_binaire(arbre)
    assert len(codes_binaires_calcules[b'A']) == 2
    assert len(codes_binaires_calcules[b'B']) == 3
    assert len(codes_binaires_calcules[b'C']) == 2
    assert len(codes_binaires_calcules[b'D']) == 3
    assert len(codes_binaires_calcules[b'E']) == 4
    assert len(codes_binaires_calcules[b'F']) == 4
    assert len(codes_binaires_calcules[b'G']) == 3
