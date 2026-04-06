"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Çekirdek Motor (Core Engine) - GÜVENLİK ENTEGRELİ
Tanım: Girdi/çıktı güvenliği, bağlam yönetimi ve yanıt üretimini koordine eder.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

# Arayüzler ve Modüller
from ..modeller.tabani import DilModeliTabani
from ..veri_katmani.ambar_tabani import VeriAmbariTabani
from ..veri_katmani.vektor_ambari import VektorAmbariTabani
from .guvenlik_suzgeci import GuvenlikSuzgeci

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("BilgeMotor")

class BilgeMotoru:
    """
    Bilge'nin ana işlem motoru.
    """

    def __init__(self, model: DilModeliTabani, hafiza: VeriAmbariTabani, 
                 vektor_ambari: Optional[VektorAmbariTabani] = None):
        
        if not isinstance(model, DilModeliTabani):
            raise TypeError("Model, DilModeliTabani arayüzünü uygulamalıdır.")
            
        self.model = model
        self.hafiza = hafiza
        self.vektor_ambari = vektor_ambari
        
        # Güvenlik Süzgecini Başlat
        self.guvenlik_suzgeci = GuvenlikSuzgeci()
        
        self.aktif_mi = False
        logger.info("Bilge Motoru ve Güvenlik Katmanı başlatıldı.")

    def baslat(self) -> bool:
        try:
            self.model.baslat()
            self.hafiza.baglan()
            if self.vektor_ambari:
                self.vektor_ambari.baslat()
            self.aktif_mi = True
            return True
        except Exception as e:
            logger.error(f"Motor başlatılırken hata: {e}")
            return False

    def dusun_ve_cevapla(self, soru: str, oturum_id: str = "default") -> Dict[str, Any]:
        if not self.aktif_mi:
            return {"hata": "Motor aktif değil.", "basarili": False}

        zaman_damgasi = datetime.now().isoformat()
        
        try:
            # --- 1. KATMAN: GİRDİ GÜVENLİĞİ ---
            guvenli, hata_mesaji = self.guvenlik_suzgeci.girdiyi_denetle(soru)
            if not guvenli:
                logger.warning(f"Güvensiz girdi engellendi: {soru[:20]}...")
                return {
                    "yanit": hata_mesaji,
                    "basarili": False,
                    "guvenlik_uyarisi": True
                }

            # 2. Geçmiş Bağlamı Getir ve Temizle
            gecmis = self.hafiza.getir(oturum_id) or []
            # Geçmişteki kişisel verileri maskelle
            temiz_gecmis = self.guvenlik_suzgeci.baglam_temizle(gecmis)
            
            # 3. Vektör Ambarından İlgili Bilgi Ara (RAG)
            baglam_metinleri = []
            if self.vektor_ambari:
                ilgili_belgeler = self.vektor_ambari.ara(sorgu=soru, k_sayisi=3)
                for belge in ilgili_belgeler:
                    baglam_metinleri.append(belge['metin'])
            
            # 4. Model İçin Nihai Bağlamı Oluştur
            tam_baglam = {
                "gecmis": temiz_gecmis,
                "bilgi_parcalari": baglam_metinleri
            }
            
            # 5. Modelden Yanıt Al
            ham_yanit = self.model.tahmin_et(soru, baglam=tam_baglam)
            
            # --- 2. KATMAN: ÇIKTI GÜVENLİĞİ ---
            guvenli_cikti, islenmis_yanit = self.guvenlik_suzgeci.ciktiyi_denetle(ham_yanit)
            
            if not guvenli_cikti:
                return {
                    "yanit": "Üzgünüm, bu yanıt güvenlik politikaları nedeniyle görüntülenemiyor.",
                    "basarili": False,
                    "guvenlik_uyarisi": True
                }

            # 6. Geçmişi Güncelle (Maskelenmiş halini kaydet)
            yeni_gecmis = temiz_gecmis + [
                {"rol": "user", "icerik": soru}, 
                {"rol": "assistant", "icerik": islenmis_yanit}
            ]
            self.hafiza.kaydet(oturum_id, yeni_gecmis)
            
            sonuc = {
                "yanit": islenmis_yanit,
                "oturum_id": oturum_id,
                "zaman": zaman_damgasi,
                "basarili": True
            }
            
            return sonuc

        except Exception as e:
            logger.error(f"Yanıt üretilirken kritik hata: {e}")
            return {
                "hata": "Sistem hatası oluştu.",
                "basarili": False
            }

    def durdur(self) -> None:
        try:
            self.model.durdur()
            self.hafiza.kapat()
            if self.vektor_ambari:
                self.vektor_ambari.kapat()
            self.aktif_mi = False
        except Exception as e:
            logger.error(f"Motor durdurulurken hata: {e}")
