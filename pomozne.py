######################################################################
## Pomozne funkcije

def binarno(n):
    """pretvori število v dvojiški sistem in vrne niz dolg štiri"""
    return "{0:b}".format(n).zfill(4)