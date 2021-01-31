from corrector.Pauli import Pauli

TEST_X = Pauli(+1, 'XXXXXXXX')
TEST_Z = Pauli(+1, 'ZZZZZZZZ')#
TEST_Y = Pauli(+1, 'YYYYYYYY')
TEST_I = Pauli(+1, 'IIIIIIII')

def test_mul():
    TEST_X*TEST_X == TEST_I
    TEST_Z*TEST_X == TEST_Y
    TEST_I*TEST_I == TEST_I
    
def test_neg():
    -TEST_X == Pauli(-1, 'XXXXXXXX')
    --TEST_X == TEST_X
    
def test_commutes():
    TEST_X.commutes(TEST_X) == True
    TEST_X.commutes(TEST_Z) == False
    TEST_I.commutes(TEST_Y) == True