"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Niyet Tanıyıcı
Tanım: Kullanıcı girdisinin amacını sınıflandırır.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""

class NiyetTaniyici:
    @staticmethod
    def tespitet(metin: str) -> str:
        """
        Basit kural tabanlı niyet tespiti.
        Dönüş değerleri: 'selamlama', 'soru', 'komut', 'genel'
        """
        metin_alt = metin.lower()
        
        # Selamlama kontrolü
        selamlamalar = ['merhaba', 'selam', 'hayırlı sabahlar', 'iyi akşamlar', 'nasılsın']
        if any(kelime in metin_alt for kelime in selamlamalar):
            return 'selamlama'
        
        # Soru kontrolü
        if '?' in metin or metin_alt.startswith(('nedir', 'nasıl', 'kimdir', 'nerede', 'ne zaman')):
            return 'soru'
            
        # Komut kontrolü (basit örnekler)
        if metin_alt.startswith(('aç', 'kapat', 'listele', 'bul')):
            return 'komut'
            
        return 'genel'
