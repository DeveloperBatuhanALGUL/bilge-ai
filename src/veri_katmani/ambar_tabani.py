"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Veri Ambarı Tabanı (Base Storage Interface)
Tanım: Veri saklama ve erişim işlemleri için standart arayüz.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class VeriAmbariTabani(ABC):
    """
    Veri saklama işlemleri için soyut temel sınıf.
    İlişkisel DB, Vektör DB veya Cache implementasyonları bu sınıfı miras alır.
    """

    @abstractmethod
    def baglan(self) -> bool:
        """Veritabanına bağlantı kurar."""
        pass

    @abstractmethod
    def kaydet(self, anahtar: str, veri: Any) -> bool:
        """
        Veriyi saklar.
        
        Args:
            anahtar (str): Verinin benzersiz kimliği.
            veri (Any): Saklanacak veri objesi.
            
        Returns:
            bool: İşlem başarılıysa True.
        """
        pass

    @abstractmethod
    def getir(self, anahtar: str) -> Optional[Any]:
        """
        Anahtara karşılık gelen veriyi getirir.
        
        Args:
            anahtar (str): Aranacak veri kimliği.
            
        Returns:
            Any: Bulunan veri, yoksa None.
        """
        pass

    @abstractmethod
    def sil(self, anahtar: str) -> bool:
        """Veriyi siler."""
        pass

    @abstractmethod
    def kapat(self) -> None:
        """Bağlantıyı kapatır."""
        pass
