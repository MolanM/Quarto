import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak
import random

MINIMAX_GLOBINA = 2
zelene = ('midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green')
rumene = ('light goldenrod yellow',
    'light yellow', 'yellow', 'gold')
rdece = ('coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet')
barva1 = random.choice(zelene)
barva2 = random.choice(rumene)
barva3 = random.choice(rdece)


# opis načina igre se določi med igro
IGRA_QUARTO = ""

from igra import *
from clovek import *
from pomozne import *
from minimax import *
from racunalnik import *
######################################################################
## Uporabniški vmesnik

class Gui():
    # S to oznako so označeni vsi grafični elementi v self.plosca, ki se
    # pobrišejo, ko se začne nova igra.
    TAG_FIGURA = 'figura'

    # Oznaka za črte
    TAG_OKVIR = 'okvir'

    # Oznaka za zmagovalni okvir
    TAG_ZMAGA = 'zmagovalniokvir'

    # Velikost polja
    VELIKOST_POLJA = 100

    def __init__(self, master, globina):
        self.igralec_1 = None # Objekt, ki igra igro kot prvi igralec (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra igro kot drugi igralec (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)

        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Nova Igra
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Način igranja", menu=menu_igra)
        #menu_igra.add_command(label="Nova igra",
                              #command=lambda: self.zacni_igro())
        menu_igra.add_command(label="Človek vs. Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self), "Človek vs. Človek", master))
        menu_igra.add_command(label="Človek vs. Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(globina)), "Človek vs. Računalnik", master))
        menu_igra.add_command(label="Računalnik vs. Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Clovek(self), "Računalnik vs. Človek", master))
        menu_igra.add_command(label="Računalnik vs. Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)),
                                                              Racunalnik(self, Minimax(globina)), "Računalnik vs. Računalnik", master))

        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(master, value="Dobrodošli v Quarto!")
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Igralno območje
        self.plosca = tkinter.Canvas(master, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.plosca.grid(row=1, column=0)

        # Gumbi za izbiro figure
		#tkinter.Label(master, text='Mozne figure:').grid(row=0, column=3)
        self.gumbi = tkinter.Canvas(master, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.gumbi.grid(row=1, column=3)

        # Napis nad izbrano figuro
        tkinter.Label(master, text='Izbrana figura:').grid(row=0, column=1)

        # Platno za prikaz izbrane figure
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
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)), "Človek vs. Računalnik", master)


    def zacni_igro(self, igralec_1, igralec_2, nacin_igre, master):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vse igralce (ki morda razmišljajo)
        self.prekini_igralce()
        # Nastavimo igralce
        self.igralec_1 = igralec_1
        self.igralec_2 = igralec_2
        # Pobrišemo vse figure s polja
        self.plosca.delete(Gui.TAG_FIGURA)
        self.figura.delete(Gui.TAG_FIGURA)
        self.plosca.delete(Gui.TAG_ZMAGA)
        self.gumbi.delete('all')
        self.narisi_vse_gumbe()
        # Ustvarimo novo igro
        self.igra = Igra()
        self.igra.izbrana_figura = None
        self.igra.zmagovalec = NI_KONEC
        # Izpišemo način igre
        IGRA_QUARTO = nacin_igre
        master.title("Igra Quarto: " + nacin_igre)
        # Na potezi prvi igralec
        self.napis.set("Na potezi je " + PRVI_IGRALEC)
        self.igralec_1.igraj()

    def koncaj_igro(self, zmagovalec, cetverka):
        """Nastavi stanje igre na konec igre."""
        if zmagovalec != NEODLOCENO:
            self.napis.set("Zmagal je " + str(self.igra.zmagovalec))
            self.narisi_zmagovalno_cetvorko(cetverka)
        else:
            self.napis.set("Neodločeno.")

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_1: self.igralec_1.prekini()
        if self.igralec_2: self.igralec_2.prekini()

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
        (luknja, proto_barva, diagonala, kvadrat) = lastnosti
        if proto_barva:
            barva = barva1
        else:
            barva = barva2
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
        """Nariši figuro na polje (i, j)."""
        (luknja, proto_barva, diagonala, kvadrat) = figura
        if proto_barva:
            barva = barva1
        else:
            barva = barva2
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


    def narisi_zmagovalno_cetvorko(self, cetverka):
        (prvi, drugi, tretji, cetrti) = cetverka
        self.plosca.create_rectangle(prvi[0]*100, prvi[1]*100, prvi[0]*100 + 100, prvi[1]*100 + 100, outline = barva3, fill=barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(drugi[0]*100, drugi[1]*100, drugi[0]*100 + 100, drugi[1]*100 + 100, outline = barva3, fill=barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(tretji[0]*100, tretji[1]*100, tretji[0]*100 + 100, tretji[1]*100 + 100, outline = barva3, fill=barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(cetrti[0]*100, cetrti[1]*100, cetrti[0]*100 + 100, cetrti[1]*100 + 100, outline = barva3, fill=barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.tag_lower(Gui.TAG_ZMAGA)
        #self.plosca.create_line(prvi[0] * 100 + 50, prvi[1] * 100 + 50, cetrti[0] * 100 + 50, cetrti[1] * 100 + 50,
        #                        width=10, fill=barva3, tag=Gui.TAG_ZMAGA)

    def gumbi_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // 100
        j = event.y // 100
        if 0 <= i <= 3 and 0 <= j <= 3:
            if self.igra.na_potezi == PRVI_IGRALEC:
                self.igralec_1.gumb_klik((i, j))
            elif self.igra.na_potezi == DRUGI_IGRALEC:
                self.igralec_2.gumb_klik((i, j))
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
            if self.igra.na_potezi == PRVI_IGRALEC:
                self.igralec_1.klik((i,j))
            elif self.igra.na_potezi == DRUGI_IGRALEC:
                self.igralec_2.klik((i,j))
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
            (zmagovalec, cetverka, figura) = r
            self.narisi(p, figura)
            self.figura.delete(Gui.TAG_FIGURA)
            if zmagovalec == NI_KONEC:
                # Igra se nadaljuje
                pass
            else:
                # Igre je konec, koncaj
                self.koncaj_igro(zmagovalec, cetverka)

    def izberi_figuro(self, lastnosti):
        lastnosti_figure = lastnosti
        tag_lastnosti_figure = naredi_tag(lastnosti)
        if self.igra.izberi_figuro(lastnosti_figure) is None:
            pass
        else:
            self.figura.delete(Gui.TAG_FIGURA)
            self.gumbi.delete(tag_lastnosti_figure)
            self.narisi_gumbe_izbrana_figura(lastnosti_figure)

            if self.igra.na_potezi == PRVI_IGRALEC:
                    self.napis.set("Na potezi je " + PRVI_IGRALEC)
                    self.igralec_1.igraj()
            elif self.igra.na_potezi == DRUGI_IGRALEC:
                    self.napis.set("Na potezi je " + DRUGI_IGRALEC)
                    self.igralec_2.igraj()

    def narisi_gumbe_izbrana_figura(self, lastnosti):
        (luknja, proto_barva, diagonala, kvadrat) = lastnosti
        if proto_barva:
            barva = barva1
        else:
            barva = barva2
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
    parser = argparse.ArgumentParser(description="Igra Quarto")
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
    root.title("Igra Quarto")

    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    # sicer bo Python mislil, da je objekt neuporabljen in ga bo pobrisal
    # iz pomnilnika.
    aplikacija = Gui(root, args.globina)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
