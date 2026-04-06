"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Anlık Bellek (Memory Cache)
Tanım: Hızlı erişim için bellekte geçen oturumları saklar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from typing import List, Dict, Any, Optional
from .ambar_tabani import VeriAmbariTabani

logger = logging.getLogger("BilgeAnlikBellek")

class AnlikBellek(VeriAmbariTabani):
    """
    Bellek içi önbellek.
    Performans için kısa vadeli hafıza sağlar.
    """

    def __init__(self):
        self.hafiza = {}

    def baglan(self) -> bool:
        logger.info("Anlık bellek başlatıldı.")
        return True

    def getir(self, oturum_id: str) -> Optional[List[Dict[str, Any]]]:
        return self.hafiza.get(oturum_id)

    def kaydet(self, oturum_id: str, gecmis: List[Dict[str, Any]]) -> bool:
        self.hafiza[oturum_id] = gecmis
        return True

    def kapat(self) -> None:
        self.hafiza.clear()
        logger.info("Anlık bellek temizlendi.")
