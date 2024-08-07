
""" script principal du module """
from typing import Dict
import io
import logging
from HuffmanCompression.huffman.compteur import Compteur
from HuffmanCompression.huffman.arbre_huffman import ArbreHuffman
from HuffmanCompression.huffman.file_de_priorite import FileDePriorite, FileDePrioriteVideErreur
from HuffmanCompression.huffman.code_binaire import CodeBinaire, Bit

LOGGER = logging.getLogger()

NB_OCTETS_CODAGE_INT = 4

def statistiques(source: io.BufferedReader) -> (Compteur, int):
    """
    statistiques Calcul les statistiques de chaque octets présent dans
                 le flux binaire

    Parameters
    ----------
    source : io.BufferedReader
        flux binaire initial

    Returns
    -------
    Compteur
        Ensemble de tous les octets avec leur nombre d'occurrences
    int
        Nombre d'octets total du flux binaire
    """
    nombre_octets = 0
    compteur = Compteur()
    octet = source.read(1)
    while octet:
        nombre_octets += 1
        compteur.incrementer(int.from_bytes(octet, 'big'))
        octet = source.read(1)
    return (compteur, nombre_octets)

def arbre_de_huffman(stat: Compteur) -> ArbreHuffman:
    """
    arbre_de_huffman Créer l'arbre de Huffman correspondant aux statisques

    Parameters
    ----------
    stat : Compteur
        Statistiques des octets du flux binaire

    Returns
    -------
    ArbreHuffman
        Arbre de Huffman
    """
    #Création de la file de priorité
    file = FileDePriorite()
    for octet in stat.elements:
        file.enfiler(ArbreHuffman(element=octet, nb_occurrences=stat.nb_occurrences(octet)))

    #Création de l'arbre de Huffman
    while not file.est_vide:
        try:
            arbre_gauche = file.defiler()
            arbre_droit = file.defiler()
        except FileDePrioriteVideErreur:
            break
        file.enfiler(ArbreHuffman(fils_gauche=arbre_gauche, fils_droit=arbre_droit))

    return arbre_gauche

def _codage(abr: ArbreHuffman, code : CodeBinaire, table: Dict[bytes, CodeBinaire]):

    if abr.est_une_feuille:
        code_final = CodeBinaire(*code.bits)
        table.update({abr.element:code_final})
    else:
        if (fils_gauche := abr.fils_gauche):
            code.ajouter(Bit.BIT_0)
            _codage(fils_gauche, code, table)
            del code[-1]

        if (fils_droit := abr.fils_droit):
            code.ajouter(Bit.BIT_1)
            _codage(fils_droit, code, table)
            del code[-1]

def codes_binaire(abr: ArbreHuffman) -> Dict[bytes, CodeBinaire]:
    """
    codes_binaire Dictionnare qui regroupe chaque octet et son code binaire

    Parameters
    ----------
    abr : ArbreHuffman
        Arbre de Huffman issu du flux binaire

    Returns
    -------
    Dict[bytes, CodeBinaire]
        Table de codage
    """
    table_codage = {}
    if abr.est_une_feuille:
        table_codage.update({abr.element:CodeBinaire(Bit.BIT_0)})
    else:
        if (fils_gauche := abr.fils_gauche):
            _codage(fils_gauche, CodeBinaire(Bit.BIT_0), table_codage)

        if (fils_droit := abr.fils_droit):
            _codage(fils_droit, CodeBinaire(Bit.BIT_1), table_codage)
    return table_codage


if __name__ == "__main__":
    pass
