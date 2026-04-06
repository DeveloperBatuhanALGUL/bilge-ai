"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Metin Normalleştirici
Tanım: Girdi metnindeki gereksiz karakterleri temizler ve standart hale getirir.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import re
import unicodedata

class MetinNormallestirici:
    @staticmethod
    def normallestir(metin: str) -> str:
        if not metin:
            return ""
        
        # Unicode normalize (NFKC: uyumluluk ve bileşik karakterler için)
        metin = unicodedata.normalize('NFKC', metin)
        
        # Fazla boşlukları tek boşluğa indir
        metin = re.sub(r'\s+', ' ', metin)
        
        # Başlangıç ve bitiş boşluklarını kaldır
        metin = metin.strip()
        
        # Noktalama işaretlerinden önceki/sonraki boşluk düzeltmeleri
        metin = re.sub(r'\s+([.,!?;:])', r'\1', metin)
        metin = re.sub(r'([.,!?;:])\s+', r'\1 ', metin)
        
        return metin
