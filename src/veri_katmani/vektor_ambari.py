"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Vektör Ambarı Arayüzü
Tanım: Vektör veritabanları için temel sözleşme.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class VektorAmbariTabani(ABC):
    """
    Vektör tabanlı bilgi havuzu için temel arayüz.
    Metinlerin vektör temsillerini saklar ve anlamsal arama yapar.
    """

    @abstractmethod
    def baslat(self) -> bool:
        """
        Vektör ambarına bağlantı kurar veya koleksiyonu hazırlar.
        
        Returns:
            bool: Başarılıysa True.
        """
        pass

    @abstractmethod
    def belge_ekle(self, belgeler: List[Dict[str, Any]]) -> bool:
        """
        Yeni belgeleri vektör uzayına ekler.
        
        Args:
            belgeler (list): Eklenmek istenen belge listesi.
                             Her belge { 'id': str, 'metin': str, 'metadata': dict } formatında olmalı.
                             
        Returns:
            bool: Başarılıysa True.
        """
        pass

    @abstractmethod
    def ara(self, sorgu: str, k_sayisi: int = 3) -> List[Dict[str, Any]]:
        """
        Sorguya en benzer belgeleri bulur.
        
        Args:
            sorgu (str): Arama yapılacak metin.
            k_sayisi (int): Dönecek en yakın sonuç sayısı.
            
        Returns:
            list: Bulunan belgeler ve benzerlik skorları.
        """
        pass

    @abstractmethod
    def kapat(self) -> None:
        """
        Bağlantıyı kapatır ve kaynakları temizler.
        """
        pass
