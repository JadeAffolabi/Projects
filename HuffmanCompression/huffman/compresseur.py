""" script principal du module """
from typing import Dict
import io
import logging
import pickle
from huffman.compteur import Compteur
from huffman.arbre_huffman import ArbreHuffman
from huffman.file_de_priorite import FileDePriorite, FileDePrioriteVideErreur
from huffman.code_binaire import CodeBinaire, Bit


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
        compteur.incrementer(octet) #int.from_bytes(octet, 'big')
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

def compresser(destination: io.RawIOBase, source: io.RawIOBase) -> None:
    """
    compresser Compresse le fichier "source" en fichier "destination"
    Parameters
    ----------
    destination : io.RawIOBase
        Fichier compressé
    source : io.RawIOBase
        Fichier à compresser
    """
    #Calcul des statistiques
    stats, nb_octets = statistiques(source)

    #Ecriture de l'identifiant de compression 52 50 soit 34 30 en hex
    destination.write(b'\x34\x32')

    #Ecriture de l'état du fichier source
    nb_octets_differents = len(stats.elements)
    if nb_octets_differents == 0:
        destination.write(b'\x00') # fichier vide
    elif nb_octets_differents == 1:
        destination.write(b'\x01') # fichier contenant le même octet
    else:
        destination.write(b'\x02') # autres cas
        arbre_huffman = arbre_de_huffman(stats)
        table_de_codage = codes_binaire(arbre_huffman)

    #Ecriture de la longeur du fichier source
    destination.write(int(nb_octets).to_bytes(NB_OCTETS_CODAGE_INT, 'big'))

    #Ecriture des statistiques
    if nb_octets != 0 :
        pickle.dump(stats, destination)

    #Ecriture des données compressées
    if nb_octets_differents > 1:
        source.seek(0)                      #On se positionne au début du fichier
        octet_source = source.read(1)       #Lecture du premier octet
        octet_destination = 0
        nb_bits = 0
        i = 0
        code_correspondant_fini = True
        while octet_source:
            if code_correspondant_fini:
                code_correspondant = table_de_codage[octet_source] #int.from_bytes(octet_source, 'big')

            while nb_bits < 8 and i < (longeur_code_binaire := len(code_correspondant)):
                b = code_correspondant[i]
                if b == Bit.BIT_1:
                    octet_destination = octet_destination | 2**nb_bits
                nb_bits += 1
                i += 1

            if nb_bits == 8:
                destination.write(int(octet_destination).to_bytes(1,'big'))
                octet_destination = 0
                nb_bits = 0

            if i == longeur_code_binaire:
                octet_source = source.read(1)
                i = 0
                code_correspondant_fini = True
            else:
                code_correspondant_fini = False
        if nb_bits != 8:
            destination.write(int(octet_destination).to_bytes(1,'big'))

def decompresser(destination: io.RawIOBase, source: io.RawIOBase) -> None:

    octets_identifiant = source.read(1) + source.read(1)
    if not octets_identifiant == b'\x34\x32':
        print("Ce fichier ne peut pas être décompressé en utilisant 'huff'.")
    
    octet_etat_fichier = source.read(1)
    if octet_etat_fichier == b'\x00':
        print("Le fichier est vide")
    elif octet_etat_fichier == b'\x01':
        print("Fichier avec octet unique")
        nb_octets_original = int.from_bytes(source.read(NB_OCTETS_CODAGE_INT), 'big')
        stats = pickle.load(source)
        i = 0
        while i < nb_octets_original:
            destination.write(stats.elements[0])
            i += 1
    else:
        nb_octets_original = int.from_bytes(source.read(NB_OCTETS_CODAGE_INT), 'big')
        stats = pickle.load(source)
        arbre = arbre_de_huffman(stats)
        temp_arbre = arbre
        i = 0
        while i < nb_octets_original:
            code_binaire = format(int.from_bytes(source.read(1),'big'), 'b')[::-1]
            while len(code_binaire) < 8:
                code_binaire += '0'
            for bit in code_binaire:
                if bit == '0':
                    temp_arbre = temp_arbre.fils_gauche
                elif bit == '1':
                    temp_arbre = temp_arbre.fils_droit
                
                if temp_arbre.est_une_feuille:
                    destination.write(temp_arbre.element)
                    temp_arbre = arbre
                    i +=1
