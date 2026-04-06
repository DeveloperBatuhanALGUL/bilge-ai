"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Performans İzleyici
Tanım: Sistem bileşenlerinin çalışma sürelerini ve kaynak kullanımını ölçer.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import time
import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger("BilgePerformans")

class PerformansOlcer:
    """
    Fonksiyonların veya kod bloklarının çalışma süresini ölçen yardımcı sınıf.
    Decorator pattern kullanılarak kolayca entegre edilebilir.
    """

    @staticmethod
    def sure_olcer(fonksiyon: Callable) -> Callable:
        """
        Bir fonksiyonun çalışma süresini ölçen decorator.
        
        Args:
            fonksiyon (Callable): Ölçülecek fonksiyon.
            
        Returns:
            Callable: Süre ölçümü eklenmiş sarmalanmış fonksiyon.
        """
        @wraps(fonksiyon)
        def wrapper(*args, **kwargs):
            baslangic_zamani = time.perf_counter()
            
            try:
                sonuc = fonksiyon(*args, **kwargs)
                return sonuc
            finally:
                bitis_zamani = time.perf_counter()
                gecen_sure = (bitis_zamani - baslangic_zamani) * 1000 # Milisaniye
                
                # Loglama seviyesine göre yazdırma
                if gecen_sure > 1000: # 1 saniyeden uzun sürerse uyarı ver
                    logger.warning(f"{fonksiyon.__name__} fonksiyonu {gecen_sure:.2f} ms sürdü (YAVAŞ).")
                else:
                    logger.debug(f"{fonksiyon.__name__} fonksiyonu {gecen_sure:.2f} ms sürdü.")
                    
        return wrapper

    @staticmethod
    def asenkron_sure_olcer(fonksiyon: Callable) -> Callable:
        """
        Asenkron fonksiyonlar için süre ölçüm decorator'u.
        """
        import asyncio
        
        @wraps(fonksiyon)
        async def wrapper(*args, **kwargs):
            baslangic_zamani = time.perf_counter()
            
            try:
                sonuc = await fonksiyon(*args, **kwargs)
                return sonuc
            finally:
                bitis_zamani = time.perf_counter()
                gecen_sure = (bitis_zamani - baslangic_zamani) * 1000
                
                if gecen_sure > 1000:
                    logger.warning(f"[ASYNC] {fonksiyon.__name__} fonksiyonu {gecen_sure:.2f} ms sürdü (YAVAŞ).")
                else:
                    logger.debug(f"[ASYNC] {fonksiyon.__name__} fonksiyonu {gecen_sure:.2f} ms sürdü.")
                    
        return wrapper
