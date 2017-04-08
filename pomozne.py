######################################################################
## Pomozne funkcije

def binarno(n):
    """Pretvori število v dvojiški sistem, nato pa to pretvori v seznam Boolovih vrednosti."""
    # vrednosti binarno predstavljajo (luknja, barva, diagonala, kvadrat)
    assert n <= 15, 'neveljavna stevilka polja'
    seznam_string = "{0:b}".format(n).zfill(4)
    seznam_bool = []
    for i in range(len(seznam_string)):
        if seznam_string[i] == '1':
            seznam_bool.append(True)
        elif seznam_string[i] == '0':
            seznam_bool.append(False)
        else:
            assert False, 'napaka v seznamu lastnosti'
    return seznam_bool

def naredi_tag(seznam):
    """Spremeni seznam v nabor, da ga lahko uporabimo za tag figure"""
    string = ''
    for f in seznam:
        string = string + str(f)
    return string
