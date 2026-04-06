"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Morfolojik Çözümleyici (Parser)
Tanım: Kelimeleri kök ve eklerine ayırır, gramer yapısını çıkarır.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from .morfoloji_tabani import MorfolojiTabani, KelimeKoku, EkBilgisi
from typing import List, Dict, Any

logger = logging.getLogger("BilgeCozumleyici")

class MorfolojikCozumleyici:
    """
    Türkçe kelimelerin derin morfolojik analizini yapan sınıf.
    Async uyumlu tasarlanmıştır.
    """

    def __init__(self):
        self.taban = MorfolojiTabani()

    async def cumleyi_cozumle(self, cumle: str) -> List[Dict[str, Any]]:
        """
        Bir cümleyi kelimelere böler ve her kelimeyi morfolojik olarak çözümler.
        
        Args:
            cumle (str): Analiz edilecek cümle.
            
        Returns:
            list: Her kelime için kök, ekler ve gramer bilgisi içeren liste.
        """
        kelimeler = cumle.split()
        sonuc_listesi = []

        for kelime in kelimeler:
            # Noktalama işaretlerini temizle (basitçe)
            temiz_kelime = ''.join(e for e in kelime if e.isalnum())
            if not temiz_kelime:
                continue
                
            analiz = await self._kelime_analiz_et(temiz_kelime)
            sonuc_listesi.append(analiz)
            
        return sonuc_listesi

    async def _kelime_analiz_et(self, kelime: str) -> Dict[str, Any]:
        """
        Tek bir kelimeyi geriye doğru iz sürerek (backtracking) çözümler.
        """
        kelime_lower = kelime.lower()
        
        # 1. Doğrudan kök mü?
        kok_bilgisi = self.taban.kok_bul(kelime_lower)
        if kok_bilgisi:
            return {
                "yuzey": kelime,
                "kok": kok_bilgisi.kok,
                "tip": kok_bilgisi.tip,
                "ekler": [],
                "analiz_str": f"[{kok_bilgisi.kok}+Isim]"
            }

        # 2. Ekleri sondan sökerek ilerle
        kalan = kelime_lower
        bulunan_ekler = []
        found_root = False
        root_candidate = ""

        # Maksimum 5 ek denemesi (performans için sınır)
        for _ in range(5):
            if len(kalan) < 3: break
            
            # Kalan kısmın kök olup olmadığını kontrol et
            potential_root = self.taban.kok_bul(kalan)
            if potential_root:
                root_candidate = kalan
                found_root = True
                break

            # Son 2-4 karakteri ek olarak dene
            for ek_len in range(2, 5):
                if len(kalan) <= ek_len: continue
                
                potential_ek_str = kalan[-ek_len:]
                ek_bilgisi = self.taban.ek_bul(potential_ek_str)
                
                if ek_bilgisi:
                    # Ünlü uyumu kontrolü (Basit versiyon)
                    bulunan_ekler.insert(0, ek_bilgisi.yuzey) # Başa ekle
                    kalan = kalan[:-ek_len]
                    break # Bir ek bulundu, döngüyü kır ve kalanla devam et
        
        if found_root:
            kok_bilgisi = self.taban.kok_bul(root_candidate)
            return {
                "yuzey": kelime,
                "kok": kok_bilgisi.kok,
                "tip": kok_bilgisi.tip,
                "ekler": bulunan_ekler,
                "analiz_str": f"[{kok_bilgisi.kok}+{''.join(['+'+e for e in bulunan_ekler])}]"
            }
        else:
            # Kök bulunamazsa, kelimeyi olduğu gibi döndür (Bilinmeyen Kelime)
            return {
                "yuzey": kelime,
                "kok": kelime_lower,
                "tip": "bilinmeyen",
                "ekler": [],
                "analiz_str": f"[{kelime_lower}?]"
            }
