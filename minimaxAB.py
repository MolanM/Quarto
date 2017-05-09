import logging #za debug
import random #za izbiranje enakovrednih potez
import operator #za seštevanje naborov

from igra import PRVI_IGRALEC, DRUGI_IGRALEC, PRAZNO, NEODLOCENO, NI_KONEC, nasprotnik

######################################################################
## Algoritem minimax z implementiranimi alfa beta rezi

class MinimaxAB:

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro
        self.jaz = None  # katerega igralca igramo
        self.poteza = None # sem napišemo potezo, ko jo najdemo
        self.figura = None # shranimo figuro, ki jo bomo izbrali
        self.vrednost = 0

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra, globina):
        """Izračunaj potezo za trenutno stanje dane igre."""
        self.globina = globina
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        self.figura = None
        # Poženemo minimax
        (poteza, figura, vrednost) = self.alphabeta(self.globina, True, -MinimaxAB.NESKONCNO, MinimaxAB.NESKONCNO)
        self.vrednost = vrednost
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("alphabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            self.figura = figura

    # Vrednosti igre
    ZMAGA = 100000 # Mora biti vsaj 10^5

    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def vrednost_pozicije(self):
        #ta cenilka se je s poskušanjem izkazala za najboljšo
        #v povprečju je premegala računalnike, ki so igrali z ostalimi cenilkami
        vrednost = 0
        lastnosti_figur = [(0,0), (0,0), (0,0), (0,0)] #lastnosti možnih figur
        for figura in self.igra.mozne_figure: #preštejemo posamezne lastnosti pri možnih figurah
            for i in range(len(figura)):
                if figura[i] == True:
                    lastnosti_figur[i] = tuple(map(operator.add, lastnosti_figur[i], (1,0)))
                else:
                    lastnosti_figur[i] = tuple(map(operator.add, lastnosti_figur[i], (0,1)))
        for t in self.igra.cetvorke: #pregledamo vse četvorke
            lastnosti = [(0,0), (0,0), (0,0), (0,0)]
            for (i, j) in t: #preštejemo lastnosti figur v tej četvorki
                if self.igra.plosca[i][j] is not PRAZNO:
                    for k in range(len(lastnosti)):
                        if self.igra.plosca[i][j][k] == True:
                            lastnosti[k] = tuple(map(operator.add, lastnosti[k], (1,0)))
                        else:
                            lastnosti[k] = tuple(map(operator.add, lastnosti[k], (0,1)))
            for i in range(len(lastnosti)): #ovrednotimo lastnosti glede na izbrano figuro in preostale možne figure
                (x,y) = lastnosti[i]
                if x != 0 and y != 0:
                    continue
                elif x == 3:
                    if self.igra.izbrana_figura[i] == True:
                        return -MinimaxAB.ZMAGA + 1
                    elif lastnosti_figur[i][0] >= 1:
                        if lastnosti_figur[i][1] == 1:
                            vrednost -= MinimaxAB.ZMAGA/100
                        elif lastnosti_figur[i][1] == 3:
                            vrednost -= MinimaxAB.ZMAGA/300
                        elif lastnosti_figur[i][1] % 2 == 1:
                            vrednost -= MinimaxAB.ZMAGA/700
                elif y == 3:
                    if self.igra.izbrana_figura[i] == False:
                        return -MinimaxAB.ZMAGA + 1
                    elif lastnosti_figur[i][1] >= 1:
                        if lastnosti_figur[i][0] == 1:
                            vrednost -= MinimaxAB.ZMAGA/100
                        elif lastnosti_figur[i][0] == 3:
                            vrednost -= MinimaxAB.ZMAGA/300
                        elif lastnosti_figur[i][0] % 2 == 1:
                            vrednost -= MinimaxAB.ZMAGA/700
                elif x == 2:
                    if self.igra.izbrana_figura[i] == True and lastnosti_figur[i][0] >= 1:
                        if lastnosti_figur[i][1] == 1:
                            vrednost -= MinimaxAB.ZMAGA/200
                        elif lastnosti_figur[i][1] == 3:
                            vrednost -= MinimaxAB.ZMAGA/400
                        elif lastnosti_figur[i][1] % 2 == 1:
                            vrednost -= MinimaxAB.ZMAGA/900
                    elif lastnosti_figur[i][0] >= 2:
                        if lastnosti_figur[i][1] == 0:
                            vrednost -= MinimaxAB.ZMAGA/1000
                        elif lastnosti_figur[i][1] == 2:
                            vrednost -= MinimaxAB.ZMAGA/3000
                        elif lastnosti_figur[i][1] % 2 == 0:
                            vrednost -= MinimaxAB.ZMAGA/7000
                elif y == 2:
                    if self.igra.izbrana_figura[i] == False and lastnosti_figur[i][1] >= 1:
                        if lastnosti_figur[i][0] == 1:
                            vrednost -= MinimaxAB.ZMAGA/200
                        elif lastnosti_figur[i][0] == 3:
                            vrednost -= MinimaxAB.ZMAGA/400
                        elif lastnosti_figur[i][0] % 2 == 1:
                            vrednost -= MinimaxAB.ZMAGA/900
                    elif lastnosti_figur[i][1] >= 2:
                        if lastnosti_figur[i][0] == 0:
                            vrednost -= MinimaxAB.ZMAGA/1000
                        elif lastnosti_figur[i][0] == 2:
                            vrednost -= MinimaxAB.ZMAGA/3000
                        elif lastnosti_figur[i][0] % 2 == 0:
                            vrednost -= MinimaxAB.ZMAGA/7000
                elif x == 1:
                    if self.igra.izbrana_figura[i] == True and lastnosti_figur[i][0] >= 2:
                        if lastnosti_figur[i][1] == 0:
                            vrednost -= MinimaxAB.ZMAGA/2000
                        elif lastnosti_figur[i][1] == 2:
                            vrednost -= MinimaxAB.ZMAGA/4000
                        elif lastnosti_figur[i][1] % 2 == 0:
                            vrednost -= MinimaxAB.ZMAGA/9000
                    elif lastnosti_figur[i][0] >= 3:
                        if lastnosti_figur[i][1] == 1:
                            vrednost -= MinimaxAB.ZMAGA/10000
                        elif lastnosti_figur[i][1] == 3:
                            vrednost -= MinimaxAB.ZMAGA/30000
                        elif lastnosti_figur[i][1] % 2 == 1:
                            vrednost -= MinimaxAB.ZMAGA/70000
                elif y == 1:
                    if self.igra.izbrana_figura[i] == False and lastnosti_figur[i][1] >= 2:
                        if lastnosti_figur[i][0] == 0:
                            vrednost -= MinimaxAB.ZMAGA/2000
                        elif lastnosti_figur[i][0] == 2:
                            vrednost -= MinimaxAB.ZMAGA/4000
                        elif lastnosti_figur[i][0] % 2 == 0:
                            vrednost -= MinimaxAB.ZMAGA/9000
                    elif lastnosti_figur[i][1] >= 3:
                        if lastnosti_figur[i][0] == 1:
                            vrednost -= MinimaxAB.ZMAGA/10000
                        elif lastnosti_figur[i][0] == 3 and lastnosti_figur[i][1] >= 3:
                            vrednost -= MinimaxAB.ZMAGA/30000
                        elif lastnosti_figur[i][0] % 2 == 1 and lastnosti_figur[i][1] >= 3:
                            vrednost -= MinimaxAB.ZMAGA/70000
        return vrednost

    def alphabeta(self, globina, maksimiziramo, alfa, beta):
        """Glavna metoda minimax z implementiranimi alfa beta rezi"""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("MinimaxAB prekinja, globina = {0}".format(globina))
            return (None, None, 0)
        (zmagovalec ,lst) = self.igra.stanje_igre()
        if zmagovalec in (PRVI_IGRALEC, DRUGI_IGRALEC, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, None, MinimaxAB.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, None, -MinimaxAB.ZMAGA)
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
                    vrednost_najboljse = -MinimaxAB.NESKONCNO
                    if len(self.igra.veljavne_poteze()) == 16: #na začetku gremo le skozi tri poteze, ker so ostale simetrične
                        nesimetricne_poteze = [(0,0), (1,0), (1,1)]
                        for p in nesimetricne_poteze:
                            for f in self.igra.mozne_figure:
                                self.igra.povleci_potezo(p)
                                self.igra.izberi_figuro(f)
                                vrednost = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost > vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljse_poteze = []
                                    najboljse_poteze.append((p,f))
                                elif vrednost == vrednost_najboljse:
                                    najboljse_poteze.append((p,f))
                                alfa = max(alfa, vrednost_najboljse)
                                if beta < alfa:
                                    break
                            if beta < alfa:
                                break
                    else:
                        for p in self.igra.veljavne_poteze():
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost > vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    alfa = max(alfa, vrednost_najboljse)
                                    if beta < alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost_najboljse = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                najboljse_poteze = []
                                najboljsa_poteza = p
                                najboljsa_figura = 'konec'
                                alfa = max(alfa, vrednost_najboljse)
                            if beta < alfa:
                                break
                else:
                    # Minimiziramo
                    najboljse_poteze = []
                    najboljsa_poteza = None
                    najboljsa_figura = None
                    vrednost_najboljse = MinimaxAB.NESKONCNO
                    if len(self.igra.veljavne_poteze()) == 16:
                        nesimetricne_poteze = [(0,0), (1,0), (1,1)] #ostale so simetrične
                        for p in nesimetricne_poteze:
                            for f in self.igra.mozne_figure:
                                self.igra.povleci_potezo(p)
                                self.igra.izberi_figuro(f)
                                vrednost = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                if vrednost < vrednost_najboljse:
                                    vrednost_najboljse = vrednost
                                    najboljse_poteze = []
                                    najboljse_poteze.append((p,f))
                                elif vrednost == vrednost_najboljse:
                                    najboljse_poteze.append((p,f))
                                beta = min(beta, vrednost_najboljse)
                                if beta < alfa:
                                    break
                            if beta < alfa:
                                break
                    else:
                        for p in self.igra.veljavne_poteze():
                            if len(self.igra.mozne_figure) != 0:
                                for f in self.igra.mozne_figure:
                                    self.igra.povleci_potezo(p)
                                    self.igra.izberi_figuro(f)
                                    vrednost = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                    self.igra.razveljavi()
                                    if vrednost < vrednost_najboljse:
                                        vrednost_najboljse = vrednost
                                        najboljse_poteze = []
                                        najboljse_poteze.append((p,f))
                                    elif vrednost == vrednost_najboljse:
                                        najboljse_poteze.append((p,f))
                                    beta = min(beta, vrednost_najboljse)
                                    if beta < alfa:
                                        break
                            else:
                                self.igra.povleci_potezo(p)
                                vrednost_najboljse = self.alphabeta(globina-1, not maksimiziramo,alfa,beta)[2]
                                self.igra.razveljavi()
                                najboljse_poteze = []
                                najboljsa_poteza = p
                                najboljsa_figura = 'konec'
                                beta = min(beta, vrednost_najboljse)
                            if beta < alfa:
                                break
                if len(najboljse_poteze) != 0:
                    # Naključna poteza izmed tistih, ki so imele enako najboljšo vrednost
                    (najboljsa_poteza, najboljsa_figura) = random.choice(najboljse_poteze)
                    # Prva možna poteza
                    #(najboljsa_poteza, najboljsa_figura) = najboljse_poteze[0]
                assert (najboljsa_poteza is not None), "alphabeta: izračunana poteza je None"
                return (najboljsa_poteza, najboljsa_figura, vrednost_najboljse)
        else:
            assert False, "alphabeta: nedefinirano stanje igre"
