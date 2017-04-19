from pomozne import *

######################################################################
## Igralec človek

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        # čakamo, da uporabnik klikne na igralno ploščo ali možne figure
        pass

    def prekini(self):
        # Pri človeku ni treba ničesar prekinjati
        pass

    def klik(self, p):
        # Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.
        self.gui.povleci_potezo(p)

    def gumb_klik(self,p):
        # Izberemo figuro (na katero smo kliknili), če lahko.
        (x, y) = p
        self.gui.izberi_figuro(binarno(4*x +y))