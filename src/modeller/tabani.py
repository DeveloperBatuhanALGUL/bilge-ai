"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Model Tabanı (Base Model Interface)
Tanım: Tüm dil modellerinin uyması zorunlu olan arayüz.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class DilModeliTabani(ABC):
    """
    Tüm dil modelleri için soyut temel sınıf.
    Yeni bir model entegre edilirken bu sınıf miras alınmalıdır.
    """

    @abstractmethod
    def baslat(self) -> None:
        """Modeli belleğe yükler ve hazır hale getirir."""
        pass

    @abstractmethod
    def tahmin_et(self, girdi: str, baglam: Optional[Dict[str, Any]] = None) -> str:
        """
        Verilen girdiye göre metin üretir.
        
        Args:
            girdi (str): Kullanıcı sorusu veya yönerge.
            baglam (dict, optional): Önceki konuşma geçmişi veya meta veriler.
            
        Returns:
            str: Modelin ürettiği yanıt.
        """
        pass

    @abstractmethod
    def durdur(self) -> None:
        """Model kaynaklarını serbest bırakır."""
        pass
