import pytest
from huffman.code_binaire import Bit, CodeBinaire, AuMoinsUnBitErreur


@pytest.fixture(scope="function")
def un_code():
    return CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)

def test_bits(un_code):
    assert un_code.bits == (Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)

def test_ajouter(un_code):
    un_code.ajouter(Bit.BIT_1)
    assert un_code.bits == (Bit.BIT_0, Bit.BIT_1, Bit.BIT_0, Bit.BIT_1)

def test_len(un_code):
    assert len(un_code) == 3

def test_set(un_code):
    un_code[1] = Bit.BIT_0
    assert un_code.bits == (Bit.BIT_0, Bit.BIT_0, Bit.BIT_0)
    un_code[0:2] = [Bit.BIT_1, Bit.BIT_1]
    assert un_code.bits == (Bit.BIT_1, Bit.BIT_1, Bit.BIT_0)
    un_code[1:] = CodeBinaire(Bit.BIT_0, Bit.BIT_0)
    assert un_code.bits == (Bit.BIT_1, Bit.BIT_0, Bit.BIT_0)

def test_get(un_code):
    assert un_code[1] == Bit.BIT_1
    assert un_code[0:2] == CodeBinaire(Bit.BIT_0, Bit.BIT_1)

@pytest.mark.parametrize("indices, resultat", [(1, (Bit.BIT_0, Bit.BIT_0)), (slice(2),(Bit.BIT_0,))])
def test_del(un_code, indices, resultat):
    del un_code[indices]
    assert un_code.bits == resultat

def test_iter(un_code):
    for i,b in enumerate(un_code):
        assert b == un_code[i]

def test_eq(un_code):
    code1 = CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)
    code2 = CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_1)
    code3 = CodeBinaire(Bit.BIT_0)
    assert un_code == code1
    assert un_code != code2
    assert un_code != code3

def test_add(un_code):
    assert un_code+CodeBinaire(Bit.BIT_1) == CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0, Bit.BIT_1)

def test_hash(un_code):
    code1 = CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)
    assert hash(un_code) == hash(code1)

def test_AuMoinsUnBitErreur(un_code):
    del un_code[:2]
    with pytest.raises(AuMoinsUnBitErreur):
        del un_code[0]

def test_TypeError(un_code):
    with pytest.raises(TypeError):
        code1 = CodeBinaire(Bit.BIT_0, 1, Bit.BIT_1)
    
    with pytest.raises(TypeError):
        un_code[:2] = [Bit.BIT_1, 0]
    
    with pytest.raises(TypeError):
        un_code.ajouter(1)

def test_repr(un_code):
    assert repr(un_code) == "CodeBinaire(Bit.BIT_0, Bit.BIT_1, Bit.BIT_0)"

def test_str(un_code):
    assert str(un_code) == "0 1 0"
