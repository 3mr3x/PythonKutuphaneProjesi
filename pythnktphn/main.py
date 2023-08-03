import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * #widgetlerin önüne ekleme yapmadan kurtulduk qtwidgets yazmıcaz hepsine
from kitapEkle import *

uygulama= QApplication(sys.argv)# tüm argümanları çağırdık argv
pencere= QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)#form ile ilişkilendirme
pencere.show()


#veritabanı başlıyor
import sqlite3

baglanti=sqlite3.connect("kitablar.db")
islem= baglanti.cursor()
baglanti.commit() #veritabanıkayıtcommit

table = islem.execute("create table if not exists kitablar(urunKodu int, urunAdi text, birimfiyat int,stokMiktari int, kullanicii int, urunAciklaması text, kategori text)")
baglanti.commit()

def kayit_ekle():
    UrunKodu=ui.lneurunkodu.text()
    UrunAdi=ui.lneurunad.text()
    BirimFiyat=ui.lnebrmfyt.text()
    StokMiktari=ui.lineEdit.text()
    UrunAciklama=ui.lneuruncklm.text()
    Kullanici=ui.kullanici.text()
    Kategori= ui.cmbkategor.currentText()  # cmbkategor'dan seçilen değeri Kategori değişkenine atıyoruz


    try:
        ekle= "insert into kitablar (urunKodu,urunAdi,birimfiyat,stokMiktari,urunAciklaması,kategori,kullanicii) values (?,?,?,?,?,?,?)"
        islem.execute(ekle,(UrunKodu,UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Kategori,Kullanici, ))
        baglanti.commit()
        kayit_listele()
        ui.statusbar.showMessage("bağlantı başarılı ",10000)
    except Exception as error:
        ui.statusbar.showMessage("Kayıt eklenemedi:==="+str(error))

def kayit_listele():
    ui.tbllistele.clear()
    ui.tbllistele.setHorizontalHeaderLabels(("Isbn No","Kitap adı ","Birim Süre","Stok Miktar","Kullanıcı No","Kitap Yayınevi","İçerik Türü"))
    ui.tbllistele.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)# allttaki tool çubuğu gitti listelieyince tam sığdı

    sorgu="select * from kitablar"
    islem.execute(sorgu) #enumarate methodu listenin her bir elemana index değeri verir

    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSütun in enumerate(kayitNumarasi):
            ui.tbllistele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSütun)))


def kategoriye_göre_listele():
    listelenecek_kategori=ui.cmbkatgorilstl.currentText()

    sorgu="select * from kitablar where kategori = ?"
    islem.execute(sorgu,(listelenecek_kategori,))
    ui.tbllistele.clear()
    for indexSatir,kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSütun in enumerate(kayitNumarasi):
            ui.tbllistele.setItem(indexSatir,indexSutun,QTableWidgetItem(str(kayitSütun)))

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz ?", QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbllistele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()

        sorgu = "DELETE FROM kitablar WHERE urunKodu = ?"

        try:
            islem.execute(sorgu, (silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
            kayit_listele()
        except Exception as error:
            ui.statusbar.showMessage("Kayıt silinirken hata meydana geldi: " + str(error))
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")

def kayit_güncelle():
    güncelle_mesaj=QMessageBox.question(pencere,"Güncelleme Onayı","Bu kaydı Güncllemek İstediğinizden Emin misiniz?",QMessageBox.Yes|QMessageBox.No)

    if güncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu= ui.lneurunkodu.text()
            UrunAdi=ui.lneurunad.text()
            BirimFiyat=ui.lnebrmfyt.text()
            StokMiktari=ui.lineEdit.text()
            UrunAciklama=ui.lneuruncklm.text()
            Kullanici=ui.kullanici.text()
            Kategori=ui.cmbkategor.currentText()

            if UrunAdi=="" and BirimFiyat =="" and StokMiktari =="" and UrunAciklama == "" and Kullanici == "":
                islem.execute("update kitablar set kategori = ? where urunKodu =?",(Kategori, UrunKodu))
                
            elif UrunAdi=="" and BirimFiyat =="" and StokMiktari =="" and UrunAciklama == "" and Kategori == "":
                islem.execute("update kitablar set kullanicii = ? where urunKodu =?",(Kullanici, UrunKodu))
            elif UrunAdi=="" and BirimFiyat =="" and StokMiktari =="" and Kullanici == "" and Kategori == "":
                islem.execute("update kitablar set urunaciklama = ? where urunKodu =?",(UrunAciklama, UrunKodu))

            elif UrunAdi=="" and BirimFiyat =="" and UrunAciklama =="" and Kullanici == "" and Kategori == "":
                islem.execute("update kitablar set stokMiktarı = ? where urunKodu =?",(UrunAciklama, UrunKodu))

            elif UrunAdi=="" and StokMiktari =="" and StokMiktari =="" and UrunAciklama == "" and Kategori == "":
                islem.execute("update kitablar set birimFiyat = ? where urunKodu =?",(BirimFiyat, UrunKodu))

            elif BirimFiyat=="" and StokMiktari =="" and StokMiktari =="" and UrunAciklama == "" and Kategori == "":
                islem.execute("update kitablar set urunAdi = ? where urunKodu =?",(UrunAdi, UrunKodu))


            else:
                islem.execute("update kitablar set urunAdi = ?,birimFiyat = ?, stokMiktari = ?,urunAciklamasi = ?,kullanicii = ?, kategori = ? where urunkodu = ?",(UrunAdi,BirimFiyat,StokMiktari,UrunAciklama,Kullanici,Kategori,UrunKodu))
            baglanti.commit()
            kayit_listele()
            ui.statusbar.showMessage("kayıt başarıyla güncellendi ")
        except Exception as error:
            ui.statusbar.showMessage("kayıt güncellemede hata çıktı==="+str(error))
    else:
        ui.statusbar.showMessage("güncelleme iptal edildi")


def rapor_yaz():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(("Isbn NoRapor","Kitap adıR ","Birim SüreR","Stok MiktarR","Kitap YayıneviR","Dış BaskıR","Kullanıcı NOR","İçerik TürüR"))
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    sorgu = "SELECT * FROM kitablar"
    islem.execute(sorgu)
    kitaplar = islem.fetchall()
    
    ui.tableWidget.setRowCount(len(kitaplar))
    
    for index, kitap in enumerate(kitaplar):
        for col_index, deger in enumerate(kitap):
            item = QTableWidgetItem(str(deger))
            ui.tableWidget.setItem(index, col_index, item)

# QPushButton'e tıklama olayına bağlı olarak rapor_yaz fonksiyonunu çağırın
ui.pushButton.clicked.connect(rapor_yaz)



#butonlar
ui.btnekle.clicked.connect(kayit_ekle)
ui.btnlstl.clicked.connect(kayit_listele)
ui.btnktgrlistele.clicked.connect(kategoriye_göre_listele)
ui.btnsil.clicked.connect(kayit_sil)
ui.btngncll.clicked.connect(kayit_güncelle)




    

sys.exit(uygulama.exec_())
