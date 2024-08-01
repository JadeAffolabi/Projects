"""Module qui contient : classe CodeBinaire, type Bit"""

from enum import Enum
from typing_extensions import Self

class Bit(Enum):
    """ Type énuméré qui représente les bits 0 et 1"""
    BIT_0 = 0
    BIT_1 = 1

class CodeBinaire:
    """ Classe qui représente un code binaire"""

    def __init__(self, bit: Bit, *bits: Bit):
        self._bits = [bit] + list(bits)

    def ajouter(self, bit: Bit) -> None:
        """
        ajouter : Permet d'ajouter un bit (à la fin)

        Parameters
        ----------
        bit : Bit
            Le bit à ajouter
        """
        self._bits.append(bit)

    @property
    def bits(self) -> tuple[Bit]:
        """
        bits : Renvoie un tuple des bits du code binaire

        Returns
        -------
        tuple[Bit]
            Un tuple de bit
        """
        return tuple(self._bits)

    def __len__(self):
        return len(self._bits)

    def __setitem__(self, indice_ou_slice: int|slice, bit_ou_bits: Bit|list[Bit]|tuple[Bit]|Self):
        if isinstance(indice_ou_slice, slice):
            if isinstance(bit_ou_bits, Bit):
                self._bits[indice_ou_slice] = (bit_ou_bits for i in self._bits[indice_ou_slice])
            else:
                if isinstance(bit_ou_bits, CodeBinaire):
                    self._bits[indice_ou_slice] = bit_ou_bits.bits
                elif isinstance(bit_ou_bits, (list, tuple)):
                    self._bits[indice_ou_slice] = bit_ou_bits
        else:
            assert isinstance(bit_ou_bits, Bit), f"{bit_ou_bits} devrait être un Bit"
            self._bits[indice_ou_slice] = bit_ou_bits

    def __getitem__(self, indice_ou_slice: int|slice) -> Bit|Self:

        if isinstance(indice_ou_slice, slice):
            return CodeBinaire(*self._bits[indice_ou_slice])

        return self._bits[indice_ou_slice]

    def __delitem__(self, indice_ou_slice: int|slice) -> None:
        del self._bits[indice_ou_slice]

    def __iter__(self):
        return iter(self._bits)

    def __eq__(self, code_binaire: Self):

        if not isinstance(code_binaire, CodeBinaire):
            return False

        return all((self._bits[i] == code_binaire.bits[i] for i in range(len(code_binaire))))

    def __hash__(self):

        hash_code = 0

        for bit in self._bits :
            hash_code += hash(bit)

        return  hash_code

    def __repr__(self):
        description = [str(b) for b in self._bits]
        return f"CodeBinaire({', '.join(description)})"

    def __str__(self):
        description = [str(b.value) for b in self._bits]
        return " ".join(description)
