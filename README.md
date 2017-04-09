# Quarto

Za projektno nalogo pri Programiranju 2 bova izdelala igro Quarto v programskem jeziku Python 3.

Igra je ločena v šest datotek:
 * 1 quarto.py
	* Glavni program (GUI)
 * 2 igra.py
	* Pravila igre
 * 3 clovek.py
	* Cloveški igralec
 * 4 racunalnik.py
	* Racunalnik
 * 5 pomozne.py
	* Uporabljene pomožne funkcije
 * 6 minimax.py
	* Minmax algoritem

## Pravila igre:
[Hiter opis igre v angleščini](https://en.wikipedia.org/wiki/Quarto_(board_game))

Quarto je namizna igra za dva igralca. Igra se na plošči s 4x4 polji. Obstaja 16 različnih figur - vsaka ima 4 lastnosti:
* Kvadrat ali krog
* Rumena ali zelena
* Ima ali nima luknje (krogec v sredini)
* Ima ali nima diagonale

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
* Testiranje in doprava napak
* Dokumentiranje kode
* Poliranje GUI
* Čiščenje kode (imena funkcij, spremenljivk, brisanje nekoristnih delov)
* Oddaja projekta
