"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Girdi İşleme Boru Hattı
Tanım: Kullanıcı girdisini temizler, analiz eder ve modele hazır hale getirir.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import re
import logging

logger = logging.getLogger("BilgeBoruHatti")

class GirdiIsleyici:
    """
    Ham metni işleyen ve yapılandıran sınıf.
    """

    @staticmethod
    def metni_temizle(metin: str) -> str:
        """
        Metindeki gereksiz boşlukları ve karakterleri temizler.
        
        Args:
            metin (str): Ham kullanıcı girdisi.
            
        Returns:
            str: Temizlenmiş metin.
        """
        if not metin:
            return ""
        
        # Fazla boşlukları tek boşluğa indir
        metin = re.sub(r'\s+', ' ', metin)
        # Başlangıç ve bitiş boşluklarını kaldır
        metin = metin.strip()
        
        return metin

    @staticmethod
    def niyeti_tespit_et(metin: str) -> str:
        """
        Basit kural tabanlı niyet tespiti.
        Gerçek implementasyonda ML modeli kullanılacak.
        
        Args:
            metin (str): Temizlenmiş metin.
            
        Returns:
            str: Tespit edilen niyet (örn: 'selamlama', 'soru', 'komut').
        """
        metin_alt = metin.lower()
        
        selamlamalar = ['merhaba', 'selam', 'hayırlı sabahlar', 'iyi akşamlar']
        if any(kelime in metin_alt for kelime in selamlamalar):
            return 'selamlama'
        
        if '?' in metin or metin_alt.startswith('nedir') or metin_alt.startswith('nasıl'):
            return 'soru'
            
        return 'genel'

    def isle(self, ham_girdi: str) -> dict:
        """
        Tüm işleme adımlarını uygular.
        
        Args:
            ham_girdi (str): Kullanıcıdan gelen ham veri.
            
        Returns:
            dict: İşlenmiş veri ve meta bilgiler.
        """
        temiz_metin = self.metni_temizle(ham_girdi)
        niyet = self.niyeti_tespit_et(temiz_metin)
        
        return {
            'ham': ham_girdi,
            'temiz': temiz_metin,
            'niyet': niyet,
            'uzunluk': len(temiz_metin)
        }
