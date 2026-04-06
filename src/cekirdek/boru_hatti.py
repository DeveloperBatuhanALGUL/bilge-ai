"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Girdi İşleme Boru Hattı (Async)
Tanım: Ham girdiyi alır, temizler, morfolojik olarak çözümler ve niyetini belirler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import asyncio
import logging
from ..dil_islem.normallestirici import MetinNormallestirici
from ..dil_islem.cozumleyici import MorfolojikCozumleyici
from ..dil_islem.niyet_taniyici import NiyetTaniyici
from .gunlukcu import gunlukcu

logger = logging.getLogger("BilgeBoruHatti")

class GirdiIslemeHatti:
    """
    Asenkron girdi işleme hattı.
    Tüm adımları non-blocking şekilde yürütür.
    """

    def __init__(self):
        self.normallestirici = MetinNormallestirici()
        self.cozumleyici = MorfolojikCozumleyici()
        self.niyet_taniyici = NiyetTaniyici()

    async def isle(self, ham_girdi: str) -> dict:
        """
        Ana işleme fonksiyonu.
        
        Args:
            ham_girdi (str): Kullanıcıdan gelen ham veri.
            
        Returns:
            dict: İşlenmiş ve zenginleştirilmiş veri paketi.
        """
        try:
            gunlukcu.ayikla(f"Girdi işleme başlatıldı: {ham_girdi[:30]}...")
            
            # 1. Temizle (Senkron - Hızlı)
            temiz_metin = self.normallestirici.normallestir(ham_girdi)
            
            # 2. Niyet Tespiti (Senkron - Hızlı)
            niyet = self.niyet_taniyici.tespitet(temiz_metin)
            
            # 3. Morfolojik Çözümleme (Asenkron - Yoğun İşlem)
            morfolojik_agac = await self.cozumleyici.cumleyi_cozumle(temiz_metin)
            
            # 4. Sonucu Paketle
            sonuc = {
                'ham': ham_girdi,
                'temiz': temiz_metin,
                'niyet': niyet,
                'morfoloji': morfolojik_agac, # Detaylı kök-ek analizi
                'hata': None
            }
            
            gunlukcu.ayikla("Girdi işleme tamamlandı.")
            return sonuc
            
        except Exception as e:
            logger.error(f"Boru hattında kritik hata: {e}")
            return {
                'ham': ham_girdi,
                'temiz': '',
                'niyet': 'bilinmeyen',
                'morfoloji': [],
                'hata': str(e)
            }
