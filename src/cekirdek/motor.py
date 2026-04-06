"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Çekirdek Motor (Core Engine) - PERFORMANS ENTEGRE
Tanım: Girdi işleme, bağlam yönetimi ve yanıt üretimini asenkron koordine eder.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

# Yerel modüller
from ..modeller.tabani import DilModeliTabani
from ..veri_katmani.ambar_tabani import VeriAmbariTabani
from ..veri_katmani.vektor_ambari import VektorAmbariTabani
from .guvenlik_suzgeci import GuvenlikSuzgeci
from .gunlukcu import gunlukcu
from .yapilandirma import YapilandirmaYonetici
from .boru_hatti import GirdiIslemeHatti
from .performans_izleyici import PerformansOlcer

logger = logging.getLogger("BilgeMotor")

class BilgeMotoru:
    """
    Bilge'nin ana işlem motoru.
    Asenkron akış sağlar ve performans metriklerini toplar.
    """

    def __init__(self, model: DilModeliTabani, hafiza: VeriAmbariTabani, 
                 vektor_ambari: Optional[VektorAmbariTabani] = None):
        
        if not isinstance(model, DilModeliTabani):
            raise TypeError("Model, DilModeliTabani arayüzünü uygulamalıdır.")
            
        self.model = model
        self.hafiza = hafiza
        self.vektor_ambari = vektor_ambari
        
        # Güvenlik ve Araçlar
        self.guvenlik_suzgeci = GuvenlikSuzgeci()
        self.yapilandirma = YapilandirmaYonetici()
        self.boru_hatti = GirdiIslemeHatti()
        
        self.aktif_mi = False
        gunlukcu.bilgi("Bilge Motoru (Async + PerfMon) başlatıldı.")

    def baslat(self) -> bool:
        try:
            self.model.baslat()
            self.hafiza.baglan()
            if self.vektor_ambari:
                self.vektor_ambari.baslat()
            self.aktif_mi = True
            return True
        except Exception as e:
            gunlukcu.hata(f"Motor başlatılırken hata: {e}")
            return False

    @PerformansOlcer.asenkron_sure_olcer
    async def dusun_ve_cevapla(self, soru: str, oturum_id: str = "default") -> Dict[str, Any]:
        """
        Asenkron düşünme ve cevaplama süreci.
        Tüm adımlar performans izleyici tarafından loglanır.
        """
        if not self.aktif_mi:
            return {"hata": "Motor aktif değil.", "basarili": False}

        zaman_damgasi = datetime.now().isoformat()
        
        try:
            # --- 1. ADIM: GİRDİ İŞLEME BORU HATTI ---
            islenmis_veri = await self.boru_hatti.isle(soru)
            
            if islenmis_veri['hata']:
                return {"yanit": "Girdi işlenirken hata oluştu.", "basarili": False}

            temiz_soru = islenmis_veri['temiz']
            morfolojik_baglam = islenmis_veri['morfoloji']
            
            # --- 2. ADIM: GÜVENLİK KONTROLÜ ---
            guvenli, hata_mesaji = self.guvenlik_suzgeci.girdiyi_denetle(temiz_soru)
            if not guvenli:
                return {"yanit": hata_mesaji, "basarili": False, "guvenlik_uyarisi": True}

            # --- 3. ADIM: BAĞLAM TOPLAMA ---
            gecmis = self.hafiza.getir(oturum_id) or []
            temiz_gecmis = self.guvenlik_suzgeci.baglam_temizle(gecmis)
            
            baglam_metinleri = []
            if self.vektor_ambari:
                ilgili_belgeler = self.vektor_ambari.ara(sorgu=temiz_soru, k_sayisi=3)
                for belge in ilgili_belgeler:
                    baglam_metinleri.append(belge['metin'])

            # --- 4. ADIM: MODEL ÇIKARIMI (INFERENCE) ---
            loop = asyncio.get_event_loop()
            ham_yanit = await loop.run_in_executor(None, self.model.tahmin_et, temiz_soru, {
                "gecmis": temiz_gecmis,
                "bilgi_parcalari": baglam_metinleri,
                "morfoloji": morfolojik_baglam
            })
            
            # --- 5. ADIM: ÇIKTI GÜVENLİĞİ ---
            guvenli_cikti, islenmis_yanit = self.guvenlik_suzgeci.ciktiyi_denetle(ham_yanit)
            
            if not guvenli_cikti:
                return {"yanit": "Yanıt güvenlik nedeniyle engellendi.", "basarili": False}

            # --- 6. ADIM: HAFIZA GÜNCELLEME ---
            yeni_gecmis = temiz_gecmis + [
                {"rol": "user", "icerik": temiz_soru}, 
                {"rol": "assistant", "icerik": islenmis_yanit}
            ]
            self.hafiza.kaydet(oturum_id, yeni_gecmis)
            
            return {
                "yanit": islenmis_yanit,
                "oturum_id": oturum_id,
                "zaman": zaman_damgasi,
                "basarili": True,
                "morfolojik_detay": morfolojik_baglam
            }

        except Exception as e:
            gunlukcu.hata(f"Yanıt üretilirken kritik hata: {e}")
            return {"hata": "Sistem hatası.", "basarili": False}

    def durdur(self) -> None:
        self.model.durdur()
        self.hafiza.kapat()
        if self.vektor_ambari:
            self.vektor_ambari.kapat()
        self.aktif_mi = False
