"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Bağlam Yöneticisi
Tanım: Kısa ve uzun vadeli hafızayı koordine eder.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from ..veri_katmani.ambar_tabani import VeriAmbariTabani

logger = logging.getLogger("BilgeBaglamYonetici")

class BaglamYonetici:
    """
    Çok katmanlı hafıza yöneticisi.
    Önce anlık belleğe, sonra kalıcı ambara yazar.
    """

    def __init__(self, kisa_vadeli: VeriAmbariTabani, uzun_vadeli: VeriAmbariTabani):
        self.kisa_vadeli = kisa_vadeli
        self.uzun_vadeli = uzun_vadeli

    def baslat(self) -> bool:
        return self.kisa_vadeli.baglan() and self.uzun_vadeli.baglan()

    def getir(self, oturum_id: str):
        # Önce kısa vadeli hafızadan kontrol et
        gecmis = self.kisa_vadeli.getir(oturum_id)
        if gecmis is not None:
            return gecmis
        
        # Yoksa uzun vadeli amardan çek
        gecmis = self.uzun_vadeli.getir(oturum_id)
        if gecmis:
            # Kısa vadeli hafızaya da yaz (cache)
            self.kisa_vadeli.kaydet(oturum_id, gecmis)
        return gecmis

    def kaydet(self, oturum_id: str, gecmis: list):
        # Her iki katmana da yaz
        self.kisa_vadeli.kaydet(oturum_id, gecmis)
        self.uzun_vadeli.kaydet(oturum_id, gecmis)

    def kapat(self):
        self.kisa_vadeli.kapat()
        self.uzun_vadeli.kapat()
