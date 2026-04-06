"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Canlı Veri Çekici
Tanım: Meclis, Haber Ajansları gibi kaynaklardan güncel verileri çeker ve işler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import requests
from bs4 import BeautifulSoup
import feedparser
import logging
from typing import List, Dict, Any
import re

logger = logging.getLogger("BilgeVeriCekici")

class CanliVeriCekici:
    """
    Dış kaynaklardan veri çeken ve yapılandıran sınıf.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Bilge-AI-Bot/1.0'
        }

    def rss_den_veri_cek(self, rss_url: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        RSS beslemesinden başlık ve özet çeker.
        
        Args:
            rss_url: RSS adresi.
            limit: Kaç haber çekileceği.
            
        Returns:
            list: Çekilen haberlerin listesi.
        """
        try:
            logger.info(f"RSS besleniyor: {rss_url}")
            feed = feedparser.parse(rss_url)
            belgeler = []
            
            for entry in feed.entries[:limit]:
                # Basit temizleme
                ozet = self._metni_temizle(entry.get('summary', ''))
                baslik = self._metni_temizle(entry.get('title', ''))
                
                if not ozet or not baslik:
                    continue
                    
                # Benzersiz ID oluştur
                doc_id = f"rss-{hash(baslik)}"
                
                belgeler.append({
                    'id': doc_id,
                    'metin': f"Başlık: {baslik}\nÖzet: {ozet}",
                    'metadata': {
                        'kaynak': 'RSS_Haber',
                        'link': entry.get('link', ''),
                        'tarih': entry.get('published', '')
                    }
                })
                
            logger.info(f"{len(belgeler)} adet RSS haberi çekildi.")
            return belgeler
            
        except Exception as e:
            logger.error(f"RSS çekilirken hata: {e}")
            return []

    def web_sayfasindan_metin_cek(self, url: str) -> List[Dict[str, Any]]:
        """
        Bir web sayfasındaki ana metin içeriğini çeker (Örn: Meclis Tutanakları).
        
        Args:
            url: Hedef URL.
            
        Returns:
            list: Çekilen metin parçaları.
        """
        try:
            logger.info(f"Web sayfası taranıyor: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8' # Türkçe karakter sorunu olmaması için
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # NOT: Her sitenin yapısı farklıdır. Burası genel bir yaklaşımdır.
            # Meclis veya haber siteleri için spesifik 'div' veya 'article' etiketleri hedeflenmelidir.
            # Şimdilik tüm paragrafları çekip birleştiriyoruz.
            
            paragraflar = soup.find_all('p')
            tam_metin = ""
            
            for p in paragraflar:
                text = p.get_text()
                if len(text) > 20: # Çok kısa paragrafları (reklam vs.) atla
                    tam_metin += text + "\n\n"
                    
            if not tam_metin.strip():
                return []
                
            # Metni parçalara böl (Chunking)
            parcalar = self._metni_parcala(tam_metin, parca_boyutu=500)
            
            belgeler = []
            for i, parca in enumerate(parcalar):
                belgeler.append({
                    'id': f"web-{hash(url)}-{i}",
                    'metin': parca,
                    'metadata': {
                        'kaynak': 'Web_Sayfasi',
                        'url': url
                    }
                })
                
            logger.info(f"{len(belgeler)} adet web parçası çekildi.")
            return belgeler
            
        except Exception as e:
            logger.error(f"Web sayfası çekilirken hata: {e}")
            return []

    def _metni_temizle(self, metin: str) -> str:
        """HTML etiketlerini ve gereksiz boşlukları temizler."""
        clean = re.sub('<[^<]+?>', '', metin) # HTML taglerini sil
        clean = re.sub(r'\s+', ' ', clean) # Fazla boşluk
        return clean.strip()

    def _metni_parcala(self, metin: str, parca_boyutu: int = 500) -> List[str]:
        """
        Uzun metinleri, anlamlı bütünlüğü koruyarak parçalara ayırır.
        Basitçe cümle sonlarından böler.
        """
        # Nokta, ünlem, soru işaretinden böl
        cumleler = re.split(r'(?<=[.!?])\s+', metin)
        
        parcalar = []
        mevcut_parca = ""
        
        for cumle in cumleler:
            if len(mevcut_parca) + len(cumle) < parca_boyutu:
                mevcut_parca += cumle + " "
            else:
                if mevcut_parca:
                    parcalar.append(mevcut_parca.strip())
                mevcut_parca = cumle + " "
                
        if mevcut_parca:
            parcalar.append(mevcut_parca.strip())
            
        return parcalar
