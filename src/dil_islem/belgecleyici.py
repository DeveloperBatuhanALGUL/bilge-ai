"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Belgeçleyici (Tokenizer)
Tanım: Metni anlamlı parçalara (belgeçlere) ayırır.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""

class Belgecleyici:
    @staticmethod
    def belgecle(metin: str) -> list:
        """
        Basit boşluk bazlı tokenize işlemi.
        Gerçek implementasyonda TDK veya Oflazer algoritması entegre edilecektir.
        """
        if not metin:
            return []
        return metin.split()
