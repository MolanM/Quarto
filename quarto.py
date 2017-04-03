import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak

MINIMAX_GLOBINA = 2

from igra import *
from clovek import *
from pomozne import *
from minimax import *
from racunalnik import *
######################################################################
## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.plosca, ki se
    # pobrišejo, ko se začne nova igra (torej, križci in krožci)
    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Velikost polja
    VELIKOST_POLJA = 100

    def __init__(self, master, globina):
        self.igralec_x = None # Objekt, ki igra X (nastavimo ob začetku igre)
        self.igralec_o = None # Objekt, ki igra O (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)

        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Nova Igra
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        #menu_igra.add_command(label="Nova igra",
                              #command=lambda: self.zacni_igro())
        menu_igra.add_command(label="Človek, Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self)))
        menu_igra.add_command(label="Človek, Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="Računalnik, Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Clovek(self)))
        menu_igra.add_command(label="Računalnik, Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Racunalnik(self, Minimax(globina))))

        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value="Dobrodošli v Quarto!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.plosca = tkinter.Canvas(master, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.plosca.grid(row=1, column=0)

        # Gumbi za izbiro figure

        self.gumbi = tkinter.Canvas(master, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.gumbi.grid(row=2, column=0)

        #platno za prikaz izbranege figure
        self.figura = tkinter.Canvas(master, width = Gui.VELIKOST_POLJA, height=4* Gui.VELIKOST_POLJA)
        self.figura.grid(row=1,column = 1)


        # Črte na igralnem polju
        self.narisi_crte()
        self.narisi_vse_gumbe()

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Naročimo se na dogodek Button-1 na self.gumbi,
        self.gumbi.bind("<Button-1>", self.gumbi_klik)

        # Prični igro v načinu človek proti računalniku
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)))


    def zacni_igro(self, igralec_x, igralec_o):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vse igralce (ki morda razmišljajo)
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_x = igralec_x
        self.igralec_o = igralec_o
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        self.figura.delete(Gui.TAG_FIGURA)
        self.gumbi.delete('all')
        self.narisi_vse_gumbe()
        # Ustvarimo novo igro
        self.igra = Igra()
        self.igra.izbrana_figura = None
        self.igra.zmagovalec = NI_KONEC
        # Križec je prvi na potezi
        self.napis.set("Na potezi je 1.")
        self.igralec_x.igraj()

    def koncaj_igro(self, zmagovalec, trojka):
        """Nastavi stanje igre na konec igre."""
        if zmagovalec != NEODLOCENO:
            self.napis.set("Zmagal je " + str(self.igra.zmagovalec))
        else:
            self.napis.set("Neodločeno.")
        #if zmagovalec == IGRALEC_1:
        #    self.napis.set("Zmagal je 1.")
        #    self.narisi_zmagovalno_trojico(zmagovalec, trojka)
        #elif zmagovalec == IGRALEC_2:
        #    self.napis.set("Zmagal je 2.")
        #    self.narisi_zmagovalno_trojico(zmagovalec, trojka)
        #else:
        #    self.napis.set("Neodločeno.")

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_x: self.igralec_x.prekini()
        if self.igralec_o: self.igralec_o.prekini()

    def zapri_okno(self, master):
        """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Igralcem povemo, da morajo končati (to bo pomembno, ko
        # bo razmišljal računalnik v vzporednem vlaknu in bo treba vlakno
        # ustaviti).
        self.prekini_igralce()
        # Dejansko zapremo okno.
        master.destroy()

    def narisi_crte(self):
        """Nariši črte v igralnem polju"""
        self.plosca.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.plosca.create_line(1*d, 0*d, 1*d, 4*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(2*d, 0*d, 2*d, 4*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(3*d, 0*d, 3*d, 4*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d, 1*d, 4*d, 1*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d, 2*d, 4*d, 2*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d, 3*d, 4*d, 3*d, tag=Gui.TAG_OKVIR)
        self.plosca.create_line(0*d, 4*d, 4*d, 4*d, tag=Gui.TAG_OKVIR)

    def narisi_vse_gumbe(self):
        self.gumbi.delete(Gui.TAG_OKVIR)
        d = Gui.VELIKOST_POLJA
        self.gumbi.create_line(1 * d, 0 * d, 1 * d, 4 * d, tag=Gui.TAG_OKVIR)
        self.gumbi.create_line(2 * d, 0 * d, 2 * d, 4 * d, tag=Gui.TAG_OKVIR)
        self.gumbi.create_line(3 * d, 0 * d, 3 * d, 4 * d, tag=Gui.TAG_OKVIR)
        self.gumbi.create_line(0 * d, 1 * d, 4 * d, 1 * d, tag=Gui.TAG_OKVIR)
        self.gumbi.create_line(0 * d, 2 * d, 4 * d, 2 * d, tag=Gui.TAG_OKVIR)
        self.gumbi.create_line(0 * d, 3 * d, 4 * d, 3 * d, tag=Gui.TAG_OKVIR)
        for i in range(4):
            for j in range(4):
                lastnosti = binarno(i*4 + j)
                self.narisi_gumbe([i,j], lastnosti)



    def narisi_gumbe(self, p, lastnosti):
        (luknja, barva, diagonala, kvadrat) = lastnosti
        x = p[0] * 100
        y = p[1] * 100
        sirina = 3
        oznaka = naredi_tag(lastnosti)
        if kvadrat:
            self.gumbi.create_rectangle(x + 5, y + 5, x + 95, y + 95, width=sirina, fill=barva, tag=oznaka)
            if luknja:
                self.gumbi.create_oval(x + 35, y + 35, x + 65, y + 65, width=sirina, tag=oznaka)
            if diagonala:
                self.gumbi.create_line(x + 5, y + 5, x + 95, y + 95, width=sirina, tag=oznaka)
        else:
            self.gumbi.create_oval(x + 5, y + 5, x + 95, y + 95, width=sirina, fill=barva, tag=oznaka)
            if luknja:
                self.gumbi.create_oval(x + 35, y + 35, x + 65, y + 65, width=sirina, tag=oznaka)
            if diagonala:
                self.gumbi.create_line(x + 18, y + 18, x + 82, y + 82, width=sirina, tag=oznaka)



    def narisi(self, p, figura, zmagovalni=False): #kvadrat
        """Nariši križec v polje (i, j)."""
        (luknja, barva, diagonala, kvadrat) = figura
        x = p[0] * 100
        y = p[1] * 100
        sirina = (6 if zmagovalni else 3)
        if kvadrat:
            self.plosca.create_rectangle(x + 5, y + 5, x + 95, y + 95, width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.plosca.create_oval(x + 35, y + 35, x + 65, y + 65, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.plosca.create_line(x + 5, y + 5, x + 95, y + 95, width=sirina, tag=Gui.TAG_FIGURA)
        else:
            self.plosca.create_oval(x + 5, y + 5, x + 95, y + 95, width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.plosca.create_oval(x + 35, y + 35, x + 65, y + 65, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.plosca.create_line(x + 18, y + 18, x + 82, y + 82, width=sirina, tag=Gui.TAG_FIGURA)


    def narisi_zmagovalno_trojico(self, zmagovalec, trojka):
        #TODO
        pass
        #for p in trojka:
        #    if zmagovalec == IGRALEC_1:
        #        self.narisi_X(p, zmagovalni=True)
        #    elif zmagovalec == IGRALEC_2:
        #        self.narisi_O(p, zmagovalni=True)

    def gumbi_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // 100
        j = event.y // 100
        if 0 <= i <= 3 and 0 <= j <= 3:
            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_x.gumb_klik((i, j))
            elif self.igra.na_potezi == IGRALEC_2:
                self.igralec_o.gumb_klik((i, j))
            else:
                # Nihče ni na potezi, ne naredimo nič
                pass
        else:
            logging.debug("klik izven plošče {0}, polje {1}".format((event.x, event.y), (i, j)))


    def plosca_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // 100
        j = event.y // 100
        if 0 <= i <= 3 and 0 <= j <= 3:
            if self.igra.na_potezi == IGRALEC_1:
                self.igralec_x.klik((i,j))
            elif self.igra.na_potezi == IGRALEC_2:
                self.igralec_o.klik((i,j))
            else:
                # Nihče ni na potezi, ne naredimo nič
                pass
        else:
            logging.debug("klik izven plošče {0}, polje {1}".format((event.x,event.y), (i,j)))

    def povleci_potezo(self, p):
        """Povleci potezo p, če je veljavna. Če ni veljavna, ne naredi nič."""
        # Najprej povlečemo potezo v igri, še pred tem si zapomnimo, kdo jo je povlekel
        # (ker bo self.igra.povleci_potezo spremenil stanje igre).
        # GUI se *ne* ukvarja z logiko igre, zato ne preverja, ali je poteza veljavna.
        # Ta del za njega opravi self.igra.
        igralec = self.igra.na_potezi
        r = self.igra.povleci_potezo(p)
        if r is None:
            # Poteza ni bila veljavna, nič se ni spremenilo
            pass
        else:
            # Poteza je bila veljavna, narišemo jo na zaslon
            # Ugotovimo, kako nadaljevati
            (zmagovalec, trojka, figura) = r
            self.narisi(p, figura)
            self.figura.delete(Gui.TAG_FIGURA)
            if zmagovalec == NI_KONEC:
                # Igra se nadaljuje
                pass
            else:
                # Igre je konec, koncaj
                self.koncaj_igro(zmagovalec, trojka)

    def izberi_figuro(self, lastnosti):
        lastnosti_figure = lastnosti
        tag_lastnosti_figure = naredi_tag(lastnosti)
        if self.igra.izberi_figuro(lastnosti_figure) is None:
            pass
        else:
            self.figura.delete(Gui.TAG_FIGURA)
            self.gumbi.delete(tag_lastnosti_figure)
            self.narisi_gumbe_izbrana_figura(lastnosti_figure)

            if self.igra.na_potezi == IGRALEC_1:
                    self.napis.set("Na potezi je 1.")
                    self.igralec_x.igraj()
            elif self.igra.na_potezi == IGRALEC_2:
                    self.napis.set("Na potezi je 2.")
                    self.igralec_o.igraj()

    def narisi_gumbe_izbrana_figura(self, lastnosti):
        (luknja, barva, diagonala, kvadrat) = lastnosti
        sirina = 3
        if kvadrat:
            self.figura.create_rectangle(5, 5,95, 95, width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.figura.create_oval(35, 35, 65, 65, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.figura.create_line(5,5,95, 95, width=sirina, tag=Gui.TAG_FIGURA)
        else:
            self.figura.create_oval(5, 5, 95,95, width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.figura.create_oval(35,35, 65,65, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.figura.create_line(18, 18, 82, 82, width=sirina, tag=Gui.TAG_FIGURA)



######################################################################
## Glavni program

# Glavnemu oknu rečemo "root" (koren), ker so grafični elementi
# organizirani v drevo, glavno okno pa je koren tega drevesa

# Ta pogojni stavek preveri, ali smo datoteko pognali kot glavni program in v tem primeru
# izvede kodo. (Načeloma bi lahko datoteko naložili z "import" iz kakšne druge in v tem
# primeru ne bi želeli pognati glavne kode. To je standardni idiom v Pythonu.)

if __name__ == "__main__":
    # Iz ukazne vrstice poberemo argumente, uporabimo
    # modul argparse, glej https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Igrica tri v vrsto")
    # Argument --debug, ki vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')

    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = tkinter.Tk()
    root.title("Tri v vrsto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, args.globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
