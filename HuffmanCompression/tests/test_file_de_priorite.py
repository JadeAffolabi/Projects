import pytest
from huffman.file_de_priorite import FileDePriorite, FileDePrioriteVideErreur, ElementNonComparableErreur

@pytest.fixture(scope = "function")
def une_file():
    return FileDePriorite([1, 2, 4])

def test_est_vide(une_file):
    assert not une_file.est_vide
    assert FileDePriorite().est_vide

def test_element(une_file):
    assert une_file.element == 1
    assert repr(une_file) == repr(FileDePriorite([1, 2, 4]))

def test_defiler(une_file):
    assert une_file.defiler() == 1
    assert repr(une_file) == repr(FileDePriorite([2, 4]))

def test_enfiler(une_file):
    une_file.enfiler(0)
    une_file.enfiler(3)
    une_file.enfiler(5)
    assert repr(une_file) == repr(FileDePriorite([0, 1, 2, 3, 4, 5]))

def test_iter(une_file):
    assert all((x == y for x,y in zip(une_file, [1, 2, 4])))

def test_repr(une_file):
    assert repr(une_file) == "FileDePriorite(1, 2, 4)"

def test_FileDePrioriteVideErreur():
    with pytest.raises(FileDePrioriteVideErreur):
        FileDePriorite().defiler()
    
    with pytest.raises(FileDePrioriteVideErreur):
        FileDePriorite().element

def test_ElementNonComparableErreur(une_file):
    with pytest.raises(ElementNonComparableErreur):
        une_file.enfiler(complex(1,2))
    
    with pytest.raises(ElementNonComparableErreur):
        une_file.enfiler("A")