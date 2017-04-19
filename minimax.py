import logging
import random
import operator

from igra import PRVI_IGRALEC, DRUGI_IGRALEC, PRAZNO, NEODLOCENO, NI_KONEC, nasprotnik

######################################################################
## Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo
        self.figura = None

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra,globina):
        self.globina = globina
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        self.figura = None
        # Poženemo minimax
        (poteza, figura, vrednost) = self.minimax(self.globina, True, -Minimax.NESKONCNO, Minimax.NESKONCNO)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            self.figura = figura

    # Vrednosti igre
    ZMAGA = 100000 # Mora biti vsaj 10^5

    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def vrednost_pozicije(self):
        vrednost = 0
        lastnosti_cetvork_3 = [(0,0), (0,0), (0,0), (0,0)]
        lastnosti_cetvork_2 = [(0,0), (0,0), (0,0), (0,0)]
        lastnosti_cetvork_1 = [(0,0), (0,0), (0,0), (0,0)]
        lastnosti_figur = [(0,0), (0,0), (0,0), (0,0)]
        for t in self.igra.cetvorke:
            #((i1,j1),(i2,j2),(i3,j3),(i4,j4)) = t
            lastnosti = [(0,0), (0,0), (0,0), (0,0)]
            for (i, j) in t:
                if self.igra.plosca[i][j] is not PRAZNO:
                    for k in range(len(lastnosti)):
                        if self.igra.plosca[i][j][k] == True:
                            lastnosti[k] = tuple(map(operator.add, lastnosti[k], (1,0)))
                        else:
                            lastnosti[k] = tuple(map(operator.add, lastnosti[k], (0,1)))
            for i in range(len(lastnosti)):
                (x,y) = lastnosti[i]
                if x != 0 and y != 0:
                    continue
                elif x == 3:
                    if self.igra.izbrana_figura[i] == True:
                        return -Minimax.ZMAGA + 1
                    else:
                        lastnosti_cetvork_3[i] = tuple(map(operator.add, lastnosti_cetvork_3[i], (1,0)))
                elif y == 3:
                    if self.igra.izbrana_figura[i] == False:
                        return -Minimax.ZMAGA + 1
                    else:
                        lastnosti_cetvork_3[i] = tuple(map(operator.add, lastnosti_cetvork_3[i], (0,1)))
                elif x == 2:
                    if self.igra.izbrana_figura[i] == True:
                        lastnosti_cetvork_3[i] = tuple(map(operator.add, lastnosti_cetvork_3[i], (1,0)))
                    else:
                        lastnosti_cetvork_2[i] = tuple(map(operator.add, lastnosti_cetvork_2[i], (1,0)))
                elif y == 2:
                    if self.igra.izbrana_figura[i] == False:
                        lastnosti_cetvork_3[i] = tuple(map(operator.add, lastnosti_cetvork_3[i], (0,1)))
                    else:
                        lastnosti_cetvork_2[i] = tuple(map(operator.add, lastnosti_cetvork_2[i], (0,1)))
                elif x == 1:
                    if self.igra.izbrana_figura[i] == True:
                        lastnosti_cetvork_2[i] = tuple(map(operator.add, lastnosti_cetvork_2[i], (1,0)))
                    else:
                        lastnosti_cetvork_1[i] = tuple(map(operator.add, lastnosti_cetvork_1[i], (1,0)))
                elif y == 1:
                    if self.igra.izbrana_figura[i] == False:
                        lastnosti_cetvork_2[i] = tuple(map(operator.add, lastnosti_cetvork_2[i], (0,1)))
                    else:
                        lastnosti_cetvork_1[i] = tuple(map(operator.add, lastnosti_cetvork_1[i], (0,1)))
        for figura in self.igra.mozne_figure:
            for i in range(len(figura)):
                if figura[i] == True:
                    lastnosti_figur[i] = tuple(map(operator.add, lastnosti_figur[i], (1,0)))
                else:
                    lastnosti_figur[i] = tuple(map(operator.add, lastnosti_figur[i], (0,1)))
        for i in range(len(lastnosti_cetvork_3)):
            (x,y) = lastnosti_cetvork_3[i]
            if x != 0:
                if lastnosti_figur[i][1] % 2 == 1:
                    vrednost -= x*Minimax.ZMAGA/100
            elif y != 0:
                if lastnosti_figur[i][0] % 2 == 1:
                    vrednost -= y*Minimax.ZMAGA/100
        for i in range(len(lastnosti_cetvork_2)):
            (x,y) = lastnosti_cetvork_2[i]
            if x != 0:
                if lastnosti_figur[i][1] % 2 == 0:
                    vrednost -= x*Minimax.ZMAGA/1000
            if y != 0:
                if lastnosti_figur[i][0] % 2 == 0:
                    vrednost -= y*Minimax.ZMAGA/1000
        for i in range(len(lastnosti_cetvork_1)):
            (x,y) = lastnosti_cetvork_1[i]
            if x != 0:
                if lastnosti_figur[i][1] % 2 == 1:
                    vrednost -= x*Minimax.ZMAGA/10000
            if y != 0:
                if lastnosti_figur[i][0] % 2 == 1:
                    vrednost -= y*Minimax.ZMAGA/10000
        return vrednost

    def minimax(self, globina, maksimiziramo, alfa, beta):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, None, 0)
        (zmagovalec ,lst) = self.igra.stanje_igre()
        if zmagovalec in (PRVI_IGRALEC, DRUGI_IGRALEC, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, None, -Minimax.ZMAGA)
            else:
                return (None, None, 0)
        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljse_poteze = []
                    najboljsa_poteza = None
                    najboljsa_figura = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    if len(self.igra.veljavne_poteze()) == 16:
                        nesimetricne_poteze = [(0,0), (1,0), (1,1)]
                        for p in nesimetricne_poteze:
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost > vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                        #najboljsa_poteza = p
                                        #najboljsa_figura = f
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    alfa =max (alfa,vrednost_najboljse)
                                    if beta <= alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p
                                    najboljsa_figura = 'konec'
                                alfa = max(alfa,vrednost_najboljse)
                    else:
                        for p in self.igra.veljavne_poteze():
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost > vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                        #najboljsa_poteza = p
                                        #najboljsa_figura = f
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    alfa =max (alfa,vrednost_najboljse)
                                    if beta <= alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p
                                    najboljsa_figura = 'konec'
                                alfa = max(alfa,vrednost_najboljse)
                else:
                    # Minimiziramo
                    najboljse_poteze = []
                    najboljsa_poteza = None
                    najboljsa_figura = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    if len(self.igra.veljavne_poteze()) == 16:
                        nesimetricne_poteze = [(0,0), (1,0), (1,1)]
                        for p in nesimetricne_poteze:
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost < vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                        #najboljsa_poteza = p
                                        #najboljsa_figura = f
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    beta = min(beta,vrednost_najboljse)
                                    if beta <= alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p
                                    najboljsa_figura = 'konec'
                                beta = min(beta, vrednost_najboljse)
                    else:
                        for p in self.igra.veljavne_poteze():
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost < vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                        #najboljsa_poteza = p
                                        #najboljsa_figura = f
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    beta = min(beta,vrednost_najboljse)
                                    if beta <= alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljsa_poteza = p
                                    najboljsa_figura = 'konec'
                                beta = min(beta, vrednost_najboljse)
                if len(najboljse_poteze) != 0:
                    # Naključna poteza izmed tistih, ki so imele enako najboljšo vrednost
                    (najboljsa_poteza, najboljsa_figura) = random.choice(najboljse_poteze)
                    # Prva možna poteza
                    #(najboljsa_poteza, najboljsa_figura) = najboljse_poteze[0]
                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, najboljsa_figura, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"

    # def minimax(self, globina, maksimiziramo, alfa, beta):
    #     """Glavna metoda minimax."""
    #     if self.prekinitev:
    #         # Sporočili so nam, da moramo prekiniti
    #         logging.debug ("Minimax prekinja, globina = {0}".format(globina))
    #         return (None, None, 0)
    #     (zmagovalec ,lst) = self.igra.stanje_igre()
    #     if zmagovalec in (PRVI_IGRALEC, DRUGI_IGRALEC, NEODLOCENO):
    #         # Igre je konec, vrnemo njeno vrednost
    #         if zmagovalec == self.jaz:
    #             return (None, None, Minimax.ZMAGA)
    #         elif zmagovalec == nasprotnik(self.jaz):
    #             return (None, None, -Minimax.ZMAGA)
    #         else:
    #             return (None, None, 0)
    #     elif zmagovalec == NI_KONEC:
    #         # Igre ni konec
    #         if globina == 0:
    #             return (None, None, self.vrednost_pozicije())
    #         else:
    #             # Naredimo eno stopnjo minimax
    #             if maksimiziramo:
    #                 # Maksimiziramo
    #                 najboljse_poteze = []
    #                 najboljsa_poteza = None
    #                 najboljsa_figura = None
    #                 vrednost_najboljse = -Minimax.NESKONCNO
    #                 for p in self.igra.veljavne_poteze():
    #                     if len(self.igra.mozne_figure) != 0:
    #                         for f in self.igra.mozne_figure:
    #                             self.igra.povleci_potezo(p)
    #                             self.igra.izberi_figuro(f)
    #                             vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
    #                             self.igra.razveljavi()
    #                             if vrednost > vrednost_najboljse:
    #                                 vrednost_najboljse = vrednost
    #                                 najboljse_poteze = []
    #                                 najboljse_poteze.append((p,f))
    #                                 #najboljsa_poteza = p
    #                                 #najboljsa_figura = f
    #                             elif vrednost == vrednost_najboljse:
    #                                 najboljse_poteze.append((p,f))
    #                             alfa =max (alfa,vrednost_najboljse)
    #                             if beta <= alfa:
    #                                 break
    #                     else:
    #                         self.igra.povleci_potezo(p)
    #                         vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
    #                         self.igra.razveljavi()
    #                         if vrednost > vrednost_najboljse:
    #                             vrednost_najboljse = vrednost
    #                             najboljsa_poteza = p
    #                             najboljsa_figura = 'konec'
    #                         alfa = max(alfa,vrednost_najboljse)
    #             else:
    #                 # Minimiziramo
    #                 najboljse_poteze = []
    #                 najboljsa_poteza = None
    #                 najboljsa_figura = None
    #                 vrednost_najboljse = Minimax.NESKONCNO
    #                 for p in self.igra.veljavne_poteze():
    #                     if len(self.igra.mozne_figure) != 0:
    #                         for f in self.igra.mozne_figure:
    #                             self.igra.povleci_potezo(p)
    #                             self.igra.izberi_figuro(f)
    #                             vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
    #                             self.igra.razveljavi()
    #                             if vrednost < vrednost_najboljse:
    #                                 vrednost_najboljse = vrednost
    #                                 najboljse_poteze = []
    #                                 najboljse_poteze.append((p,f))
    #                                 #najboljsa_poteza = p
    #                                 #najboljsa_figura = f
    #                             elif vrednost == vrednost_najboljse:
    #                                 najboljse_poteze.append((p,f))
    #                             beta = min(beta,vrednost_najboljse)
    #                             if beta <= alfa:
    #                                 break
    #                     else:
    #                         self.igra.povleci_potezo(p)
    #                         vrednost = self.minimax(globina-1, not maksimiziramo,alfa,beta)[2]
    #                         self.igra.razveljavi()
    #                         if vrednost < vrednost_najboljse:
    #                             vrednost_najboljse = vrednost
    #                             najboljsa_poteza = p
    #                             najboljsa_figura = 'konec'
    #                         beta = min(beta, vrednost_najboljse)
    #             if len(najboljse_poteze) != 0:
    #                 # Naključna poteza izmed tistih, ki so imele enako najboljšo vrednost
    #                 (najboljsa_poteza, najboljsa_figura) = random.choice(najboljse_poteze)
    #                 # Prva možna poteza
    #                 #(najboljsa_poteza, najboljsa_figura) = najboljse_poteze[0]
    #             assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
    #             return (najboljsa_poteza, najboljsa_figura, vrednost_najboljse)
    #     else:
    #         assert False, "minimax: nedefinirano stanje igre"
