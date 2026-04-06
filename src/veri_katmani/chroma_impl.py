"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: ChromaDB Vektör Ambarı Implementasyonu
Tanım: ChromaDB kullanarak yerel vektör depolama ve arama işlemleri.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
import os
from typing import List, Dict, Any
from .vektor_ambari import VektorAmbariTabani

# ChromaDB import
try:
    import chromadb
    from chromadb.config import Settings
except ImportError:
    raise ImportError("ChromaDB kütüphanesi bulunamadı. Lütfen 'pip install chromadb' komutunu çalıştırın.")

logger = logging.getLogger("BilgeChromaAmbar")

class ChromaAmbar(VektorAmbariTabani):
    """
    ChromaDB tabanlı vektör ambarı.
    Yerel diskte kalıcı depolama sağlar.
    """

    def __init__(self, kalici_yol: str = "data/vectores_db", koleksiyon_adi: str = "bilge_bilgi_havuzu"):
        self.kalici_yol = kalici_yol
        self.koleksiyon_adi = koleksiyon_adi
        self.client = None
        self.koleksiyon = None

    def baslat(self) -> bool:
        try:
            # Veri klasörünün var olduğundan emin ol
            os.makedirs(self.kalici_yol, exist_ok=True)
            
            # ChromaDB istemcisini başlat (Kalıcı mod)
            self.client = chromadb.PersistentClient(path=self.kalici_yol)
            
            # Koleksiyonu oluştur veya getir
            # Embedding fonksiyonu olarak varsayılanı kullanıyoruz (all-MiniLM-L6-v2 benzeri)
            self.koleksiyon = self.client.get_or_create_collection(name=self.koleksiyon_adi)
            
            logger.info(f"ChromaDB ambarı başlatıldı. Koleksiyon: {self.koleksiyon_adi}")
            return True
            
        except Exception as e:
            logger.error(f"ChromaDB başlatılırken hata: {e}")
            return False

    def belge_ekle(self, belgeler: List[Dict[str, Any]]) -> bool:
        if not self.koleksiyon:
            logger.error("Koleksiyon henüz oluşturulmadı. 'baslat()' çağrılmalı.")
            return False

        try:
            ids = []
            documents = []
            metadatas = []

            for belge in belgeler:
                # ChromaDB gereksinimleri: ID, Metin, Metadata
                ids.append(str(belge['id']))
                documents.append(belge['metin'])
                metadatas.append(belge.get('metadata', {}))

            self.koleksiyon.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"{len(belgeler)} adet belge vektör ambarına eklendi.")
            return True
            
        except Exception as e:
            logger.error(f"Belge eklenirken hata: {e}")
            return False

    def ara(self, sorgu: str, k_sayisi: int = 3) -> List[Dict[str, Any]]:
        if not self.koleksiyon:
            logger.error("Koleksiyon henüz oluşturulmadı.")
            return []

        try:
            # ChromaDB'de semantic search
            sonuclar = self.koleksiyon.query(
                query_texts=[sorgu],
                n_results=k_sayisi
            )
            
            # Sonuçları formatla
            bulunan_belgeler = []
            if sonuclar['ids'] and sonuclar['ids'][0]:
                for i in range(len(sonuclar['ids'][0])):
                    bulunan_belgeler.append({
                        'id': sonuclar['ids'][0][i],
                        'metin': sonuclar['documents'][0][i],
                        'metadata': sonuclar['metadatas'][0][i] if sonuclar['metadatas'] else {},
                        'mesafe': sonuclar['distances'][0][i] if sonuclar['distances'] else None
                    })
                    
            return bulunan_belgeler
            
        except Exception as e:
            logger.error(f"Arama yapılırken hata: {e}")
            return []

    def kapat(self) -> None:
        # ChromaDB PersistentClient otomatik yönetilir, özel kapatma gerekmez
        # Ancak referansları temizleyebiliriz
        self.koleksiyon = None
        self.client = None
        logger.info("ChromaDB bağlantısı temizlendi.")
