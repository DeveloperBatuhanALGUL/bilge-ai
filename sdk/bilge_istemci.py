"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi - Python SDK
Modül: Bilge İstemcisi (Client)
Tanım: Uygulamaların Bilge AI API'sine kolayca bağlanmasını sağlayan kütüphane.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import requests
import json
import logging
from typing import Optional, Dict, Any

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BilgeSDK")

class BilgeBaglantisi:
    """
    Bilge AI sunucusuna bağlantı kuran ve sorgu gönderen sınıf.
    Tüm HTTP detaylarını soyutlayarak geliştiriciye basit bir arayüz sunar.
    """

    def __init__(self, api_url: str = "http://localhost:8000", api_anahtari: Optional[str] = None):
        """
        Args:
            api_url (str): Bilge Web Sunucusunun adresi.
            api_anahtari (str, optional): Eğer API korumalıysa kullanılacak anahtar.
        """
        self.api_url = api_url.rstrip('/')
        self.api_anahtari = api_anahtari
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_anahtari:
            self.headers['Authorization'] = f'Bearer {api_anahtari}'
            
        logger.info(f"Bilge SDK başlatıldı. Hedef sunucu: {self.api_url}")

    def _istek_gonder(self, endpoint: str, veri: dict) -> Dict[str, Any]:
        """
        Dahili HTTP isteği gönderme metodu.
        Hata durumlarını yakalar ve uygun exception fırlatır.
        """
        url = f"{self.api_url}{endpoint}"
        
        try:
            response = requests.post(url, headers=self.headers, json=veri, timeout=30)
            response.raise_for_status() # 4xx veya 5xx hatası varsa exception fırlat
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("İstek zaman aşımına uğradı.")
            raise ConnectionError("Sunucu yanıt vermedi (Zaman Aşımı).")
        except requests.exceptions.RequestException as e:
            logger.error(f"API isteği başarısız oldu: {e}")
            raise ConnectionError(f"Bilge sunucusuna bağlanılamadı: {e}")

    def sor(self, soru_metni: str, oturum_id: str = "sdk_oturumu") -> str:
        """
        Bilge'ye soru sorar ve yanıtı döndürür.
        
        Args:
            soru_metni (str): Kullanıcının sorusu.
            oturum_id (str): Sohbet bağlamını korumak için benzersiz kimlik.
            
        Returns:
            str: Bilge'nin verdiği yanıt metni.
        """
        payload = {
            "soru": soru_metni,
            "oturum_id": oturum_id
        }
        
        logger.debug(f"Soru gönderiliyor: {soru_metni[:50]}...")
        
        try:
            sonuc = self._istek_gonder("/cevapla", payload)
            
            if sonuc.get('basarili'):
                return sonuc.get('yanit', 'Yanıt alınamadı.')
            else:
                hata_msg = sonuc.get('hata', 'Bilinmeyen hata')
                logger.warning(f"Sunucu tarafından döndürülen hata: {hata_msg}")
                return f"Hata: {hata_msg}"
                
        except Exception as e:
            return f"Bağlantı Hatası: {str(e)}"

    def durum_kontrol(self) -> bool:
        """
        Sunucunun ayakta olup olmadığını kontrol eder.
        
        Returns:
            bool: Sunucu aktifse True, değilse False.
        """
        try:
            response = requests.get(f"{self.api_url}/durum", timeout=5)
            return response.status_code == 200
        except:
            return False

# --- ÖRNEK KULLANIM VE TEST ---
if __name__ == "__main__":
    # 1. Bağlantıyı başlat
    bilge = BilgeBaglantisi(api_url="http://localhost:8000")
    
    # 2. Sunucu durumunu kontrol et
    if bilge.durum_kontrol():
        print("Durum: Bilge Sunucusu Aktif.")
        
        # 3. Soru Sor
        yanit = bilge.sor("Türkçe'nin en önemli morfolojik özelliği nedir?")
        print(f"\nYanıt: {yanit}")
        
        # 4. Bağlamlı Soru Sor (Önceki soruyu hatırlaması için aynı oturum_id kullanılır)
        yanit2 = bilge.sor("Bunu biraz daha detaylandırır mısın?", oturum_id="sdk_oturumu")
        print(f"\nDetaylı Yanıt: {yanit2}")
        
    else:
        print("Hata: Bilge Sunucusu Yanıt Vermiyor. Lütfen 'web_sunucu.py'yi çalıştırın.")
