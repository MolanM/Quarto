import tkinter    # za uporabniški vmesnik
import argparse   # za argumente iz ukazne vrstice
import logging    # za odpravljanje napak
import random
import re # za About okno

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

    VELIKOST_POLJA = 100


    def __init__(self, master, globina):

        self.igralec_1 = None # Objekt, ki igra igro kot prvi igralec (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra igro kot drugi igralec (nastavimo ob začetku igre)
        self.igra = None # Objekt, ki predstavlja igro (nastavimo ob začetku igre)
        self.rezultat = [0,0] #začetni rezltat
        self.tezavnost = tkinter.IntVar(master, value = globina)


        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno



        # Nova Igra
        menu_igra = tkinter.Menu(menu, tearoff=0)
        menu.add_cascade(label="Nova igra", menu=menu_igra)
        #menu_igra.add_command(label="Nova igra",
                              #command=lambda: self.zacni_igro())
        menu_igra.add_radiobutton(label="Človek vs. Človek",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Clovek(self), "Človek vs. Človek", master))
        menu_igra.add_radiobutton(label="Človek vs. Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self),
                                                              Racunalnik(self, Minimax(self.tezavnost.get())), "Človek vs. Računalnik", master))
        menu_igra.add_radiobutton(label="Računalnik vs. Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(self.tezavnost.get())),
                                                              Clovek(self), "Računalnik vs. Človek", master))
        menu_igra.add_radiobutton(label="Računalnik vs. Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(self.tezavnost.get())),
                                                              Racunalnik(self, Minimax(self.tezavnost.get())), "Računalnik vs. Računalnik", master))

        helpmenu = tkinter.Menu(menu, tearoff=0)
        helpmenu.add_command(label="Opis in pravila", command=self.opis)
        menu.add_cascade(label="Pomoč", menu=helpmenu)

        #izberi tezavnost
        tezavnost_menu = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Izberi težavnost", menu = tezavnost_menu)
        tezavnost_menu.add_radiobutton(label="Lahko",
                              variable = self.tezavnost, value = 1)
        tezavnost_menu.add_radiobutton(label="Srednje",
                                       variable=self.tezavnost, value=2)
        #tezavnost_menu.add_radiobutton(label="Srednje",
        #                           command=lambda: self.spremeni_tezavnost(2))
        tezavnost_menu.add_radiobutton (label="Težko",
                                   variable = self.tezavnost, value = 3)

        #resetiraj stevec za zmage
        resetiraj_menu = tkinter.Menu(menu, tearoff = 0)
        menu.add_cascade(label = "Resetiraj rezultat", command = self.resetiraj_rezultat)





        #Frame za napise:
        self.frame1 = tkinter.Frame(master,width=900,height=50,
                                    relief=tkinter.GROOVE,  borderwidth=5)
        self.frame1.pack(side=tkinter.TOP, anchor=tkinter.NW, fill = tkinter.X)
        #self.frame1.grid_propagate(0)

        #Frame za igro:
        self.frame2 = tkinter.Frame(master, width=8*self.VELIKOST_POLJA, height=7*self.VELIKOST_POLJA,
                                    relief=tkinter.GROOVE, borderwidth=5)

        self.frame2.pack(fill=tkinter.BOTH, expand=1, side=tkinter.BOTTOM)

        # Napis, ki prikazuje stanje igre
        self.napis = tkinter.StringVar(self.frame1, value="Dobrodošli v Quarto!")
        self.naslov = tkinter.Label(self.frame1, textvariable=self.napis, font = "Times 15")
        self.naslov.pack()

        # Napis, ki prikazuje rezultat
        self.izpis_rezultat = tkinter.StringVar(self.frame1, value="Rezultat: " + str(self.rezultat))
        self.izpis_rezultata_n = tkinter.Label(self.frame1, textvariable=self.izpis_rezultat, font="Times 15")
        self.izpis_rezultata_n.pack()

        # Igralno območje
        self.plosca = tkinter.Canvas(self.frame2, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.plosca.pack(side = tkinter.LEFT, expand = 1)

        # Napis nad izbrano igralno ploščo
        tkinter.Label(self.frame1, text='Igralna plošča:').pack(side = tkinter.LEFT, expand = 1)


        # Napis nad izbrano figuro
        tkinter.Label(self.frame1, text='Izbrana figura:').pack(side = tkinter.LEFT, expand = 1)

        # Platno za prikaz izbrane figure
        self.figura = tkinter.Canvas(self.frame2, width = Gui.VELIKOST_POLJA, height=Gui.VELIKOST_POLJA*4)
        self.figura.pack(side = tkinter.LEFT, expand = 1)


        # Gumbi za izbiro figure
        self.gumbi = tkinter.Canvas(self.frame2, width=4*Gui.VELIKOST_POLJA, height=4*Gui.VELIKOST_POLJA)
        self.gumbi.pack(side = tkinter.LEFT, expand = 1)
        tkinter.Label(self.frame1, text='Možne figure:').pack(side = tkinter.LEFT, expand = 1)

        # Črte na igralnem polju
        #self.narisi_crte()
        #self.narisi_vse_gumbe()

        #spreminjanje velikosti polja
        self.frame2.bind('<Configure>', self.spremeni_velikost)
        self.height = self.plosca.winfo_reqheight()
        self.width = self.plosca.winfo_reqwidth()

        #spreminjanje velikosti polja
        self.height = self.plosca.winfo_reqheight()
        self.width = self.plosca.winfo_reqwidth()

        # Naročimo se na dogodek Button-1 na self.plosca,
        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Naročimo se na dogodek Button-1 na self.gumbi,
        self.gumbi.bind("<Button-1>", self.gumbi_klik)

        # Prični igro v načinu človek proti računalniku
        self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(self.tezavnost.get())), "Človek vs. Računalnik", master)

    def resetiraj_rezultat(self):
        self.rezultat = [0,0]
        self.izpis_rezultat.set("Rezultat: " + str(self.rezultat))

    def opis (self):
        win = tkinter.Toplevel()
        win.title("About")
        about = '''Quarto je namizna igra za dva igralca. Igra se na plošči s 4x4 polji.
        Obstaja 16 različnih figur - vsaka ima 4 lastnosti:
        - kvadrat ali krog
        - rumeno/oranžen ali zeleno/moder
        - ima ali nima luknje (krogec v sredini)
        - Ima ali nima simetrale (črta, ki seka lik na pol)
        Igralca se izmenjujeta na potezah - izbirata figuro, ki jo mora naslednji postaviti na ploščo. Igralec zmaga, ko na ploščo postavi figuro, ki dopolonjuje navpično, diagonalno ali horizontalno četverico, katere figure imajo skupno lastost (isto obliko, isto barvo, ...).'''
        about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
        t=tkinter.Text(win, wrap="word", width=100, height=10, borderwidth=0,background = "gray95")
        t.pack(sid="top",fill="both",expand=True)
        t.insert("1.0", about)
        t.config(state=tkinter.DISABLED)
        tkinter.Button(win, text='OK', command=win.destroy).pack()

    def spremeni_velikost(self, event):
        '''Ta funkcija nam prilagaja velikost polja igralnega območja
            glede na velikost celotnega okna.'''
        self.plosca.delete('all')
        self.gumbi.delete('all')
        self.figura.delete('all')
        (w, h) = (event.width, event.height)
        Gui.VELIKOST_POLJA = min(w / 9, h / 4) - 3
        self.plosca.config(width=4*Gui.VELIKOST_POLJA,height=4*Gui.VELIKOST_POLJA)
        self.gumbi.config(width=4*Gui.VELIKOST_POLJA,height=4*Gui.VELIKOST_POLJA)
        self.figura.config(width=Gui.VELIKOST_POLJA,height=4*Gui.VELIKOST_POLJA)
        self.narisi_crte()
        self.narisi_preostale_gumbe()
        if self.igra.izbrana_figura != None:
            self.narisi_gumbe_izbrana_figura(self.igra.izbrana_figura)
        self.narisi_odigrane_figure()
        if self.igra.na_potezi is None:
            (zmagovalec, stirka) = self.igra.stanje_igre()
            self.koncaj_igro(zmagovalec, stirka)

    def narisi_odigrane_figure(self):
        for i in range(4):
            for j in range(4):
                if self.igra.plosca[i][j] != PRAZNO:
                    self.narisi((i,j), self.igra.plosca[i][j])

    def narisi_preostale_gumbe(self):
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
                lastnost = binarno(i * 4 + j)
                if lastnost in self.igra.mozne_figure :
                    self.narisi_gumbe([i, j], lastnost)

    def zacni_igro(self, igralec_1, igralec_2, nacin_igre, master):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vse igralce (ki morda razmišljajo)
        self.barva1 = random.choice(zelene)
        self.barva2 = random.choice(rumene)
        self.barva3 = random.choice(rdece)
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
        self.naslov.config(fg = "black")
        self.napis.set("Na potezi je " + PRVI_IGRALEC + ", da izbere figuro.")
        self.igralec_1.igraj()

    def koncaj_igro(self, zmagovalec, cetverka):
        """Nastavi stanje igre na konec igre."""
        if zmagovalec != NEODLOCENO:
            self.naslov.config(fg = "red")
            self.napis.set("Zmagal je " + str(self.igra.zmagovalec) + "!")
            self.narisi_zmagovalno_cetvorko(cetverka)
            if self.igra.zmagovalec == PRVI_IGRALEC:
                self.rezultat[0] = self.rezultat[0] +1
                self.izpis_rezultat.set("Rezultat: " + str(self.rezultat))
            elif self.igra.zmagovalec == DRUGI_IGRALEC:
                self.rezultat[1] = self.rezultat[1] +1
                self.izpis_rezultat.set("Rezultat: " + str(self.rezultat))
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
            barva = self.barva1
        else:
            barva = self.barva2
        x = p[0] * Gui.VELIKOST_POLJA
        y = p[1] * Gui.VELIKOST_POLJA
        sirina = 3
        oznaka = naredi_tag(lastnosti)
        if kvadrat:
            self.gumbi.create_rectangle(x + 5, y + 5, x + (Gui.VELIKOST_POLJA-5), y + (Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=oznaka)
            if luknja:
                self.gumbi.create_oval(x + (Gui.VELIKOST_POLJA/3), y + (Gui.VELIKOST_POLJA/3), x + (Gui.VELIKOST_POLJA/3)*2, y + (Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=oznaka)
            if diagonala:
                self.gumbi.create_line(x + Gui.VELIKOST_POLJA / 2, y + 5, x + Gui.VELIKOST_POLJA / 2,
                                       y + Gui.VELIKOST_POLJA - 5, width=sirina, tag=oznaka)
        else:
            self.gumbi.create_oval(x + 5, y + 5, x + (Gui.VELIKOST_POLJA-5), y + (Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=oznaka)
            if luknja:
                self.gumbi.create_oval(x + (Gui.VELIKOST_POLJA/3), y + (Gui.VELIKOST_POLJA/3), x + (Gui.VELIKOST_POLJA/3)*2, y + (Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=oznaka)
            if diagonala:
                self.gumbi.create_line(x + Gui.VELIKOST_POLJA/2, y + 5 , x + Gui.VELIKOST_POLJA/2, y + Gui.VELIKOST_POLJA -5 , width=sirina, tag=oznaka)

    def narisi(self, p, figura): #kvadrat
        """Nariši figuro na polje (i, j)."""
        (luknja, proto_barva, diagonala, kvadrat) = figura
        if proto_barva:
            barva = self.barva1
        else:
            barva = self.barva2
        x = p[0] * Gui.VELIKOST_POLJA
        y = p[1] * Gui.VELIKOST_POLJA
        sirina = 3
        if kvadrat:
            self.plosca.create_rectangle(x + 5, y + 5, x + (Gui.VELIKOST_POLJA-5), y + (Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.plosca.create_oval(x + (Gui.VELIKOST_POLJA/3), y + (Gui.VELIKOST_POLJA/3), x + (Gui.VELIKOST_POLJA/3)*2, y + (Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.plosca.create_line(x + Gui.VELIKOST_POLJA / 2, y + 5, x + Gui.VELIKOST_POLJA / 2,
                                        y + Gui.VELIKOST_POLJA - 5, width=sirina, tag=Gui.TAG_FIGURA)
        else:
            self.plosca.create_oval(x + 5, y + 5, x + (Gui.VELIKOST_POLJA-5), y + (Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.plosca.create_oval(x + (Gui.VELIKOST_POLJA/3), y + (Gui.VELIKOST_POLJA/3), x + (Gui.VELIKOST_POLJA/3)*2, y + (Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.plosca.create_line(x + Gui.VELIKOST_POLJA / 2, y + 5, x + Gui.VELIKOST_POLJA / 2,
                                       y + Gui.VELIKOST_POLJA - 5, width=sirina, tag=Gui.TAG_FIGURA)


    def narisi_zmagovalno_cetvorko(self, cetverka):
        (prvi, drugi, tretji, cetrti) = cetverka
        self.plosca.create_rectangle(prvi[0]*Gui.VELIKOST_POLJA, prvi[1]*Gui.VELIKOST_POLJA, prvi[0]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, prvi[1]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, outline = self.barva3, fill=self.barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(drugi[0]*Gui.VELIKOST_POLJA, drugi[1]*Gui.VELIKOST_POLJA, drugi[0]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, drugi[1]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, outline = self.barva3, fill=self.barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(tretji[0]*Gui.VELIKOST_POLJA, tretji[1]*Gui.VELIKOST_POLJA, tretji[0]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, tretji[1]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, outline = self.barva3, fill=self.barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.create_rectangle(cetrti[0]*Gui.VELIKOST_POLJA, cetrti[1]*Gui.VELIKOST_POLJA, cetrti[0]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, cetrti[1]*Gui.VELIKOST_POLJA + Gui.VELIKOST_POLJA, outline = self.barva3, fill=self.barva3, tag=Gui.TAG_ZMAGA)
        self.plosca.tag_lower(Gui.TAG_ZMAGA)

    def gumbi_klik(self, event):
        """Obdelaj klik na ploščo."""
        # Tistemu, ki je na potezi, povemo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo p.
        i = event.x // Gui.VELIKOST_POLJA
        j = event.y // Gui.VELIKOST_POLJA
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
        i = event.x // Gui.VELIKOST_POLJA
        j = event.y // Gui.VELIKOST_POLJA
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
            if igralec == PRVI_IGRALEC:
                    self.napis.set("Na potezi je " + PRVI_IGRALEC + ", da izbere figuro.")
            elif igralec == DRUGI_IGRALEC:
                    self.napis.set("Na potezi je " + DRUGI_IGRALEC + ", da izbere figuro.")
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
                    self.napis.set("Na potezi je " + PRVI_IGRALEC + ", da položi izbrano figuro na igralno ploščo.")
                    self.igralec_1.igraj()
            elif self.igra.na_potezi == DRUGI_IGRALEC:
                    self.napis.set("Na potezi je " + DRUGI_IGRALEC + ", da položi izbrano figuro na igralno ploščo.")
                    self.igralec_2.igraj()

    def narisi_gumbe_izbrana_figura(self, lastnosti):
        (luknja, proto_barva, diagonala, kvadrat) = lastnosti
        if proto_barva:
            barva = self.barva1
        else:
            barva = self.barva2
        sirina = 3
        if kvadrat:
            self.figura.create_rectangle(5, 5,(Gui.VELIKOST_POLJA-5), (Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.figura.create_oval((Gui.VELIKOST_POLJA/3), (Gui.VELIKOST_POLJA/3), (Gui.VELIKOST_POLJA/3)*2, (Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.figura.create_line(Gui.VELIKOST_POLJA / 2, 5, Gui.VELIKOST_POLJA / 2,
                                        Gui.VELIKOST_POLJA - 5, width=sirina, tag=Gui.TAG_FIGURA)
        else:
            self.figura.create_oval(5, 5, (Gui.VELIKOST_POLJA-5),(Gui.VELIKOST_POLJA-5), width=sirina, fill=barva, tag=Gui.TAG_FIGURA)
            if luknja:
                self.figura.create_oval((Gui.VELIKOST_POLJA/3),(Gui.VELIKOST_POLJA/3), (Gui.VELIKOST_POLJA/3)*2,(Gui.VELIKOST_POLJA/3)*2, width=sirina, tag=Gui.TAG_FIGURA)
            if diagonala:
                self.figura.create_line(Gui.VELIKOST_POLJA / 2, 5, Gui.VELIKOST_POLJA / 2,
                                       Gui.VELIKOST_POLJA - 5, width=sirina, tag=Gui.TAG_FIGURA)



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
    root.minsize(900,450)

    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
