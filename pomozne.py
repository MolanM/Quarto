######################################################################
## Pomozne funkcije

def binarno(n):
    """pretvori število v dvojiški sistem in vrne niz dolg štiri"""
    assert n <= 15, 'neveljavna stevilka polja'
    seznam_string = "{0:b}".format(n).zfill(4)
    seznam_bool = []
    for i in range(len(seznam_string)):
        if i == 1 and seznam_string[1] == '1':
            seznam_bool.append('green')
        elif i == 1 and seznam_string[1] == '0':
            seznam_bool.append('yellow')
        elif seznam_string[i] == '1':
            seznam_bool.append(True)
        elif seznam_string[i] == '0':
            seznam_bool.append(False)
        else:
            assert False, 'napaka v seznamu lastnosti'
    return seznam_bool




def naredi_tag(seznam):
    string = ''
    for f in seznam:
        string = string + str(f)
    return string

print(naredi_tag(binarno(15)))

print(str(binarno(15)))
# vrednosti binarno predstavljajo (luknja, barva, diagonala, kvadrat)
