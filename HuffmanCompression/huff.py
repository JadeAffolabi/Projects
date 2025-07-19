#!/usr/bin/env python3

import argparse
import os
from huffman.compresseur import compresser, decompresser

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("option_compression",choices=["c", "d"], help="commande : c pour compresser, d pour décompresser")
    parser.add_argument("nom_fichier_source", help="nom du fichier à compresser ou décompresser")
    parser.add_argument("nom_fichier_destination", help="nom du fichier à créer")
    args = parser.parse_args()
    if not os.path.exists(args.nom_fichier_source):
        print("Le fichier source n'existe pas")
    else:
        if args.option_compression == "c":
            print("Début de compression ...")
            with open(args.nom_fichier_source, "rb") as source, open(args.nom_fichier_destination, "wb") as destination :
                compresser(destination, source)
            print("Fin de compression.")
        
        if args.option_compression == "d":
            print("Début de décompression ...")
            with open(args.nom_fichier_source, "rb") as source, open(args.nom_fichier_destination, "wb") as destination :
                decompresser(destination, source)
            print("Fin de décompression.")

if __name__ == "__main__":
    main()