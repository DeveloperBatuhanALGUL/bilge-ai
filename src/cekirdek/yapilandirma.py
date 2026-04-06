"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Yapılandırma Yöneticisi
Tanım: YAML yapılandırma dosyasını yükler ve erişim sağlar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import yaml
import os
import logging

logger = logging.getLogger("BilgeYapilandirma")

class YapilandirmaYonetici:
    def __init__(self, config_yolu: str = "config.yaml"):
        self.config_yolu = config_yolu
        self.ayarlar = {}
        self.yukle()

    def yukle(self) -> bool:
        try:
            if not os.path.exists(self.config_yolu):
                logger.error(f"Yapılandırma dosyası bulunamadı: {self.config_yolu}")
                return False
            
            with open(self.config_yolu, 'r', encoding='utf-8') as f:
                self.ayarlar = yaml.safe_load(f)
            
            logger.info("Yapılandırma başarıyla yüklendi.")
            return True
        except Exception as e:
            logger.error(f"Yapılandırma yüklenirken hata: {e}")
            return False

    def getir(self, anahtar_yolu: str, varsayilan=None):
        keys = anahtar_yolu.split('.')
        deger = self.ayarlar
        
        for key in keys:
            if isinstance(deger, dict) and key in deger:
                deger = deger[key]
            else:
                return varsayilan
        
        return deger
