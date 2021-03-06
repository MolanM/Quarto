######################################################################
## Igra

from pomozne import *

PRVI_IGRALEC = "prvi"
DRUGI_IGRALEC = "drugi"
PRAZNO = "."
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"
KONEC = "je konec"

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == PRVI_IGRALEC:
        return DRUGI_IGRALEC
    elif igralec == DRUGI_IGRALEC:
        return PRVI_IGRALEC
    else:
        # Do sem ne smemo priti, če pridemo, je napaka v programu.
        assert False, "neveljaven nasprotnik"


class Igra():
    def __init__(self):
        self.plosca = [[PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO],
                      [PRAZNO, PRAZNO, PRAZNO, PRAZNO]]
        self.na_potezi = PRVI_IGRALEC
        self.zgodovina = []
        self.izbrana_figura = None
        self.mozne_figure = []
        self.generiraj_figure()
        self.trajanje = NI_KONEC

    def generiraj_figure(self):
        '''generira vse mozne figure'''
        for i in range(4):
            for j in range(4):
                lastnosti = binarno(i * 4 + j)
                self.mozne_figure.append(lastnosti)

    def shrani_pozicijo(self):
        """Shrani trenutno pozicijo, da se bomo lahko kasneje vrnili vanjo
           z metodo razveljavi."""
        p = [self.plosca[i][:] for i in range(4)]
        seznam_moznih_figur = self.mozne_figure[:]
        self.zgodovina.append((p, self.na_potezi, self.izbrana_figura, seznam_moznih_figur, self.trajanje))

    def kopija(self):
        """Vrni kopijo te igre, brez zgodovine."""
        # Kopijo igre naredimo, ko poženemo na njej algoritem.
        # Če bi algoritem poganjali kar na glavni igri, ki jo
        # uporablja GUI, potem bi GUI mislil, da se menja stanje
        # igre (kdo je na potezi, kdo je zmagal) medtem, ko bi
        # algoritem vlekel poteze
        k = Igra()
        k.plosca = [self.plosca[i][:] for i in range(4)]
        k.na_potezi = self.na_potezi
        k.izbrana_figura = self.izbrana_figura
        k.mozne_figure = self.mozne_figure[:]
        k.trajanje = self.trajanje
        return k

    def razveljavi(self):
        """Razveljavi potezo in se vrni v prejšnje stanje."""
        (self.plosca, self.na_potezi, self.izbrana_figura, self.mozne_figure, self.trajanje) = self.zgodovina.pop()

    def veljavne_poteze(self):
        """Vrni seznam veljavnih potez."""
        poteze = []
        for i in range(4):
            for j in range(4):
                if self.plosca[i][j] is PRAZNO:
                    poteze.append((i,j))
        return poteze

    def izberi_figuro(self, lastnosti):
        '''ce je mozno funkcija izbere figuro'''
        figura = self.izbrana_figura
        if (self.trajanje == KONEC) or (figura != None) or (lastnosti not in self.mozne_figure):
            return None
        else:
            self.izbrana_figura = lastnosti
            self.mozne_figure.remove(lastnosti)
            self.na_potezi = nasprotnik(self.na_potezi)
            return True #?

    def povleci_potezo(self, p):
        """Povleci potezo p, ne naredi nič, če je neveljavna.
           Vrne stanje_igre() po potezi ali None, ce je poteza neveljavna."""
        (i,j) = p
        i = int(i)
        j = int(j)
        if (self.trajanje == KONEC) or (self.plosca[i][j] != PRAZNO) or (self.izbrana_figura == None):
            # neveljavna poteza
            return None
        else:
            self.shrani_pozicijo()
            figura = self.izbrana_figura
            self.plosca[i][j] = figura
            self.izbrana_figura = None
            (zmagovalec, cetvorka) = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # Igre ni konec, zdaj je na potezi nasprotnik
                pass
            else:
                pass
                # Igre je konec
            return (zmagovalec, cetvorka, figura)

    # Tabela vseh cetvork, ki nastopajo v igralnem polju
    cetvorke = [
        # Vodoravne
        [(0,0), (0,1), (0,2), (0,3)],
        [(1,0), (1,1), (1,2), (1,3)],
        [(2,0), (2,1), (2,2), (2,3)],
        [(3,0), (3,1), (3,2), (3,3)],
        # Navpične
        [(0,0), (1,0), (2,0), (3,0)],
        [(0,1), (1,1), (2,1), (3,1)],
        [(0,2), (1,2), (2,2), (3,2)],
        [(0,3), (1,3), (2,3), (3,3)],
        # Diagonali
        [(0,0), (1,1), (2,2), (3,3)],
        [(0,3), (1,2), (2,1), (3,0)]
        #kvadrati totdo kakšni kvadrati?
    ]

    def stanje_igre(self):
        '''vrne stanje igre in zmagovalno četvorko (če igra ni neodločena)'''
        for t in Igra.cetvorke:
           for l in range(4):
                ((i1,j1),(i2,j2),(i3,j3), (i4,j4)) = t
                p = self.plosca[i1][j1]
                if p != PRAZNO and self.plosca[i2][j2] != PRAZNO and self.plosca[i3][j3] != PRAZNO and self.plosca[i4][j4] != PRAZNO and \
                p[l] == self.plosca[i2][j2][l] == self.plosca[i3][j3][l] == self.plosca[i4][j4][l]:
                    # Našli smo zmagovalno cetvorko
                    self.trajanje = KONEC
                    return (self.na_potezi, [t[0], t[1], t[2], t[3]])
        # Ni zmagovalca, ali je igre konec?
        for i in range(4):
            for j in range(4):
                if self.plosca[i][j] is PRAZNO:
                    # Našli smo prazno plosca, igre ni konec
                    return (NI_KONEC, None)
        # Vsa polja so polna, rezultat je neodločen
        return (NEODLOCENO, None)
