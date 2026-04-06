"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Yapılandırma Yöneticisi
Tanım: YAML yapılandırma dosyalarını okur ve yönetir.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import yaml
import os
from .gunlukcu import gunlukcu

class YapilandirmaYonetici:
    """
    Uygulama ayarlarını merkezi olarak yöneten sınıf.
    Hiyerarşik YAML yapısını düz anahtarlarla sorgulamaya izin verir.
    """

    def __init__(self, dosya_yolu: str = "config.yaml"):
        self.dosya_yolu = dosya_yolu
        self.ayarlar = {}
        self.yukle()

    def yukle(self):
        try:
            if not os.path.exists(self.dosya_yolu):
                gunlukcu.hata(f"Yapılandırma dosyası bulunamadı: {self.dosya_yolu}")
                raise FileNotFoundError(f"{self.dosya_yolu} dosyası eksik.")
            
            with open(self.dosya_yolu, 'r', encoding='utf-8') as f:
                self.ayarlar = yaml.safe_load(f)
            
            gunlukcu.bilgi("Yapılandırma başarıyla yüklendi.")
            
        except Exception as e:
            gunlukcu.hata(f"Yapılandırma yüklenirken hata: {e}")
            raise e

    def getir(self, anahtar_yolu: str, varsayilan=None):
        """
        Nokta notasyonu ile iç içe geçmiş ayarlara erişir.
        Örnek: getir('model.model_adi') -> "bilge-small-7b"
        
        Args:
            anahtar_yolu (str): Ayarın yolu (nokta ile ayrılmış).
            varsayilan: Anahtar bulunamazsa dönecek değer.
            
        Returns:
            Any: Ayar değeri.
        """
        keys = anahtar_yolu.split('.')
        deger = self.ayarlar
        
        for key in keys:
            if isinstance(deger, dict) and key in deger:
                deger = deger[key]
            else:
                return varsayilan
        
        return deger
