"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Çekirdek Motor (Core Engine) - GÜNCELLENMİŞ
Tanım: Girdi işleme, bağlam yönetimi, vektör arama ve yanıt üretimini koordine eder.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

# Arayüzler
from ..modeller.tabani import DilModeliTabani
from ..veri_katmani.ambar_tabani import VeriAmbariTabani
from ..veri_katmani.vektor_ambari import VektorAmbariTabani

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BilgeMotor")

class BilgeMotoru:
    """
    Bilge'nin ana işlem motoru.
    """

    def __init__(self, model: DilModeliTabani, hafiza: VeriAmbariTabani, vektor_ambari: Optional[VektorAmbariTabani] = None):
        """
        Args:
            model: Dil modeli örneği.
            hafiza: Sohbet geçmişi ambarı.
            vektor_ambari: Bilgi havuzu (Opsiyonel).
        """
        if not isinstance(model, DilModeliTabani):
            raise TypeError("Model, DilModeliTabani arayüzünü uygulamalıdır.")
        if not isinstance(hafiza, VeriAmbariTabani):
            raise TypeError("Hafiza, VeriAmbariTabani arayüzünü uygulamalıdır.")
            
        self.model = model
        self.hafiza = hafiza
        self.vektor_ambari = vektor_ambari
        self.aktif_mi = False
        
        logger.info("Bilge Motoru başlatıldı.")

    def baslat(self) -> bool:
        try:
            self.model.baslat()
            self.hafiza.baglan()
            
            if self.vektor_ambari:
                self.vektor_ambari.baslat()
                
            self.aktif_mi = True
            logger.info("Bilge Motoru aktif edildi.")
            return True
        except Exception as e:
            logger.error(f"Motor başlatılırken hata oluştu: {e}")
            return False

    def dusun_ve_cevapla(self, soru: str, oturum_id: str = "default") -> Dict[str, Any]:
        if not self.aktif_mi:
            return {"hata": "Motor aktif değil.", "basarili": False}

        zaman_damgasi = datetime.now().isoformat()
        
        try:
            # 1. Geçmiş Bağlamı Getir (Sohbet Geçmişi)
            gecmis = self.hafiza.getir(oturum_id) or []
            
            # 2. Vektör Ambarından İlgili Bilgi Ara (RAG - Retrieval Augmented Generation)
            baglam_metinleri = []
            if self.vektor_ambari:
                # Soruyla en alakalı 3 belgeyi bul
                ilgili_belgeler = self.vektor_ambari.ara(sorgu=soru, k_sayisi=3)
                
                for belge in ilgili_belgeler:
                    # Sadece metni alıp bağlama ekle
                    baglam_metinleri.append(belge['metin'])
            
            # 3. Model İçin Nihai Bağlamı Oluştur
            # Eğer vektör aramasından sonuç geldiyse, bunları sisteme dahil et
            tam_baglam = {
                "gecmis": gecmis,
                "bilgi_parcalari": baglam_metinleri # Yeni eklenen kısım
            }
            
            # 4. Modelden Yanıt Al
            yanit_metni = self.model.tahmin_et(soru, baglam=tam_baglam)
            
            # 5. Geçmişi Güncelle
            yeni_gecmis = gecmis + [
                {"rol": "user", "icerik": soru}, 
                {"rol": "assistant", "icerik": yanit_metni}
            ]
            self.hafiza.kaydet(oturum_id, yeni_gecmis)
            
            sonuc = {
                "yanit": yanit_metni,
                "oturum_id": oturum_id,
                "zaman": zaman_damgasi,
                "kullanilan_belge_sayisi": len(baglam_metinleri),
                "basarili": True
            }
            
            return sonuc

        except Exception as e:
            logger.error(f"Yanıt üretilirken hata oluştu: {e}")
            return {
                "hata": "İşlem sırasında beklenmeyen bir hata oluştu.",
                "detay": str(e),
                "basarili": False
            }

    def durdur(self) -> None:
        try:
            self.model.durdur()
            self.hafiza.kapat()
            if self.vektor_ambari:
                self.vektor_ambari.kapat()
            self.aktif_mi = False
            logger.info("Bilge Motoru durduruldu.")
        except Exception as e:
            logger.error(f"Motor durdurulurken hata oluştu: {e}")
