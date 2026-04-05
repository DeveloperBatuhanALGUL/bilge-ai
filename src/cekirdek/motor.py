"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Çekirdek Motor (Core Engine)
Tanım: Girdi işleme, bağlam yönetimi ve yanıt üretimini koordine eden ana sınıf.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Yerel modüllerden arayüzleri içe aktar
from ..modeller.tabani import DilModeliTabani
from ..veri_katmani.ambar_tabani import VeriAmbariTabani

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BilgeMotor")

class BilgeMotoru:
    """
    Bilge'nin ana işlem motoru.
    Kullanıcı girdisini alır, gerekli modülleri çağırır ve yanıtı döndürür.
    """

    def __init__(self, model: DilModeliTabani, hafiza: VeriAmbariTabani):
        """
        Motoru başlatır.
        
        Args:
            model (DilModeliTabani): Kullanılacak dil modeli örneği.
            hafiza (VeriAmbariTabani): Bağlam ve geçmiş verileri saklayan ambar.
        """
        if not isinstance(model, DilModeliTabani):
            raise TypeError("Model, DilModeliTabani arayüzünü uygulamalıdır.")
        if not isinstance(hafiza, VeriAmbariTabani):
            raise TypeError("Hafiza, VeriAmbariTabani arayüzünü uygulamalıdır.")

        self.model = model
        self.hafiza = hafiza
        self.aktif_mi = False
        logger.info("Bilge Motoru başlatıldı.")

    def baslat(self) -> bool:
        """
        Motoru ve bağlı bileşenleri aktif eder.
        
        Returns:
            bool: Başarılı ise True.
        """
        try:
            self.model.baslat()
            self.hafiza.baglan()
            self.aktif_mi = True
            logger.info("Bilge Motoru aktif edildi.")
            return True
        except Exception as e:
            logger.error(f"Motor başlatılırken hata oluştu: {e}")
            return False

    def dusun_ve_cevapla(self, soru: str, oturum_id: str = "default") -> Dict[str, Any]:
        """
        Kullanıcı sorusunu işler ve yanıt üretir.
        
        Args:
            soru (str): Kullanıcının sorduğu soru.
            oturum_id (str): Oturumu takip etmek için benzersiz ID.
            
        Returns:
            dict: Yanıt metni, meta veriler ve durum bilgisi içeren sözlük.
        """
        if not self.aktif_mi:
            return {"hata": "Motor aktif değil.", "basarili": False}

        zaman_damgasi = datetime.now().isoformat()
        
        try:
            # 1. Geçmiş Bağlamı Getir
            gecmis = self.hafiza.getir(oturum_id) or []
            
            # 2. Modelden Yanıt Al (Basitçe girdiyi modele gönderiyoruz)
            # Not: Gerçek implementasyonda buraya 'prompt engineering' katmanı gelecek.
            yanit_metni = self.model.tahmin_et(soru, baglam={"gecmis": gecmis})
            
            # 3. Geçmişi Güncelle
            yeni_gecmis = gecmis + [{"rol": "user", "icerik": soru}, {"rol": "assistant", "icerik": yanit_metni}]
            self.hafiza.kaydet(oturum_id, yeni_gecmis)
            
            sonuc = {
                "yanit": yanit_metni,
                "oturum_id": oturum_id,
                "zaman": zaman_damgasi,
                "basarili": True
            }
            
            logger.debug(f"Oturum {oturum_id} için yanıt üretildi.")
            return sonuc

        except Exception as e:
            logger.error(f"Yanıt üretilirken hata oluştu: {e}")
            return {
                "hata": "İşlem sırasında beklenmeyen bir hata oluştu.",
                "detay": str(e),
                "basarili": False
            }

    def durdur(self) -> None:
        """Motoru ve kaynakları kapatır."""
        try:
            self.model.durdur()
            self.hafiza.kapat()
            self.aktif_mi = False
            logger.info("Bilge Motoru durduruldu.")
        except Exception as e:
            logger.error(f"Motor durdurulurken hata oluştu: {e}")
