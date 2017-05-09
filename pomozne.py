######################################################################
## Pomozne funkcije

def binarno(n):
    """Pretvori število v dvojiški sistem, nato pa to pretvori v seznam Boolovih vrednosti."""
    # vrednosti binarno predstavljajo (luknja, barva, diagonala, kvadrat)
    assert n <= 15, 'neveljavna stevilka polja'
    lastnosti_string = "{0:b}".format(int(n)).zfill(4)
    lastnosti_bool = []
    for i in range(len(lastnosti_string)):
        if lastnosti_string[i] == '1':
            lastnosti_bool.append(True)
        elif lastnosti_string[i] == '0':
            lastnosti_bool.append(False)
        else:
            assert False, 'napaka v seznamu lastnosti'
    return tuple(lastnosti_bool)

def naredi_tag(lastnosti):
    """Spremeni lastnosti v niz, da jih lahko uporabimo za tag figure"""
    tag = ''
    for f in lastnosti:
        tag = tag + str(f)
    return tag
