"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Girdi İşleme Boru Hattı
Tanım: Ham girdiyi alır, temizler, parçalar ve niyetini belirler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
from ..dil_islem.normallestirici import MetinNormallestirici
from ..dil_islem.belgecleyici import Belgecleyici
from ..dil_islem.niyet_taniyici import NiyetTaniyici
import logging

logger = logging.getLogger("BilgeBoruHatti")

class GirdiIslemeHatti:
    def __init__(self):
        self.normallestirici = MetinNormallestirici()
        self.belgecleyici = Belgecleyici()
        self.niyet_taniyici = NiyetTaniyici()

    def isle(self, ham_girdi: str) -> dict:
        """
        Tüm işleme adımlarını sırayla uygular.
        
        Returns:
            dict: İşlenmiş veri paketi.
        """
        try:
            # 1. Temizle
            temiz_metin = self.normallestirici.normallestir(ham_girdi)
            
            # 2. Parçala (Belgeçle)
            belgecler = self.belgecleyici.belgecle(temiz_metin)
            
            # 3. Niyeti Bul
            niyet = self.niyet_taniyici.tespitet(temiz_metin)
            
            return {
                'ham': ham_girdi,
                'temiz': temiz_metin,
                'belgecler': belgecler,
                'niyet': niyet,
                'hata': None
            }
            
        except Exception as e:
            logger.error(f"Boru hattında hata: {e}")
            return {
                'ham': ham_girdi,
                'temiz': '',
                'belgecler': [],
                'niyet': 'bilinmeyen',
                'hata': str(e)
            }
