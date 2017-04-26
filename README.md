# Quarto

Za projektno nalogo pri Programiranju 2 bova izdelala igro Quarto v programskem jeziku Python 3.

## Struktura programa:

Igra je ločena v šest datotek:
 * 1 quarto.py
	* Grafični vmesnik (glavni program)
 * 2 igra.py
	* V tem modulu je shranjena logika igre. Igralna plošča je predstavljena z matriko, posamezne figure pa so predstavljene kot nabor bolleanov dolžine štiri (vsaka figura v igri quarto je namreč določena s štirimi lastnostmi). Zgodovina potez je seznam naborov, kjer posamezen nabor (se pravi trenutno ''stanje igre'') vsebuje stanje plošče (matrike ki predstavlja ploščo), igralca, ki je na potezi, izbrano figuro, seznam možnih figur (figur, ki še niso bile odigrane) in zmagovalca (eden od igralcev ali neodločeno).
Zmagovalne četvorke so v igri predstavljene kot matrike, ki vsebujejo položaje na katerih se preverja skupna lastnost figur. Stanje igre je lahko neodločeno (torej igra še poteka) ali pa je zmagovalec eden od igralcev (prvi ali drugi igralec) – v tem primeru igra vrne tudi zmagovalno četvorko. 

 * 3 clovek.py
	* Cloveški igralec
 * 4 racunalnik.py
	* Racunalnik
 * 5 pomozne.py
	* Zbrane pomožne funkcije ki so uporabljene v drugih modulih
 * 6 minimax.py
	* V tem modulu je implementiran minimx algoritem (z alfa beta rezi) in hevristična funkcija.

## Pravila igre:
[Hiter opis igre v angleščini](https://en.wikipedia.org/wiki/Quarto_(board_game))

Quarto je namizna igra za dva igralca. Igra se na plošči s 4x4 polji. Obstaja 16 različnih figur - vsaka ima 4 lastnosti:
* kvadrat ali krog
* rumena/oranžna ali zelena/modra
* ima ali nima luknje (krogec v sredini)
* ima ali nima simetrale (črta, ki seka lik na pol)

Igralca se izmenjujeta na potezah - izbirata figuro, ki jo mora naslednji postaviti na ploščo. Igralec zmaga, ko na ploščo postavi figuro, ki dopolonjuje navpično, diagonalno ali horizontalno četverico, katere figure imajo skupno lastost (isto obliko, isto barvo, ...).

## Plan dela:
* Izbor igre
* Git repozitorij z README in LICENSE
* Izdelava načrta dela
* Izdelava GUI
  * 4x4 polje
  * 16 figur za izbiranje
  * prikaz izbrane figure
  * brisanje izbrane figure
  * risanje izbrane figure
  * navodila za uporabnika
* Logika igre
* Igra med dvema človekoma
* Računalnik kot igralec
* Testiranje in odprava napak
* Dokumentiranje kode
* Poliranje GUI
* Čiščenje kode (imena funkcij, spremenljivk, brisanje nekoristnih delov)
* Oddaja projekta
