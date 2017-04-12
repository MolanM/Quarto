import threading  # za vzporedno izvajanje
import random # za naključen izbor prve poteze


from minimax import *

######################################################################
## Igralec računalnik

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki izračuna potezo
        self.mislec = None # Vlakno (thread), ki razmišlja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sprožimo vzporedno vlakno, ki računa potezo. Ker tkinter ne deluje,
        # če vzporedno vlakno direktno uporablja tkinter (glej http://effbot.org/zone/tkinter-threads.htm),
        # zadeve organiziramo takole:
        # - poženemo vlakno, ki poišče potezo
        # - to vlakno nekam zapiše potezo, ki jo je našlo
        # - glavno vlakno, ki sme uporabljati tkinter, vsakih 100ms pogleda, ali
        #   je že bila najdena poteza (metoda preveri_potezo spodaj).
        # Ta rešitev je precej amaterska. Z resno knjižnico za GUI bi zadeve lahko
        # naredili bolje (vlakno bi samo sporočilo GUI-ju, da je treba narediti potezo).

        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        if self.gui.igra.izbrana_figura == None:
            # Naključen izbor prve igralne figure
            self.gui.izberi_figuro(random.choice(self.gui.igra.mozne_figure))
            # Izbor prve možne igralne figure
            #self.gui.izberi_figuro(self.gui.igra.mozne_figure[0])
        else:
            self.mislec = threading.Thread(
                target=lambda: self.algoritem.izracunaj_potezo(self.gui.igra.kopija()))

            # Poženemo vlakno:
            self.mislec.start()

            # Gremo preverjat, ali je bila najdena poteza:
            self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem že izračunal potezo."""
        if (self.algoritem.poteza is not None) and (self.algoritem.figura is not None):
            # Algoritem je našel potezo, povleci jo, če ni bilo prekinitve
            self.gui.povleci_potezo(self.algoritem.poteza)
            if self.algoritem.figura != 'konec':
                self.gui.izberi_figuro(self.algoritem.figura)
            # Vzporedno vlakno ni več aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100ms
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo kliče GUI, če je treba prekiniti razmišljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporočimo, da mora nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Računalnik ignorira klike na igralno ploščo
        pass

    def gumb_klik(self, p):
        # Računalnik ignorira klike na proste figure
        pass
