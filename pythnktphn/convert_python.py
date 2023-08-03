from PyQt5 import uic #tasarladığımız form python koduna çevirme

with open("kitapEkle.py","w",encoding="utf-8") as fout:
    uic.compileUi("kitap_ekle.ui", fout)


