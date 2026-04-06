"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: İlişkisel Veri Ambarı (SQLite)
Tanım: Oturum geçmişini kalıcı olarak saklar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from .ambar_tabani import VeriAmbariTabani

logger = logging.getLogger("BilgeIliskiselAmbar")

class IliskiselAmbar(VeriAmbariTabani):
    """
    SQLite tabanlı ilişkisel veri ambarı.
    """

    def __init__(self, db_yolu: str = "data/hafiza.db"):
        self.db_yolu = db_yolu
        self.baglanti = None

    def baglan(self) -> bool:
        try:
            # data klasörünün var olduğundan emin ol
            import os
            os.makedirs(os.path.dirname(self.db_yolu), exist_ok=True)
            
            self.baglanti = sqlite3.connect(self.db_yolu)
            self._tablo_olustur()
            logger.info("SQLite ambarına bağlanıldı.")
            return True
        except Exception as e:
            logger.error(f"SQLite bağlantısında hata: {e}")
            return False

    def _tablo_olustur(self):
        cursor = self.baglanti.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS oturum_gecmisi (
                oturum_id TEXT PRIMARY KEY,
                gecmis_json TEXT NOT NULL,
                son_guncelleme TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.baglanti.commit()

    def getir(self, oturum_id: str) -> Optional[List[Dict[str, Any]]]:
        if not self.baglanti:
            return None
            
        cursor = self.baglanti.cursor()
        cursor.execute('SELECT gecmis_json FROM oturum_gecmisi WHERE oturum_id = ?', (oturum_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None

    def kaydet(self, oturum_id: str, gecmis: List[Dict[str, Any]]) -> bool:
        if not self.baglanti:
            return False
            
        try:
            cursor = self.baglanti.cursor()
            gecmis_json = json.dumps(gecmis, ensure_ascii=False)
            cursor.execute('''
                INSERT OR REPLACE INTO oturum_gecmisi (oturum_id, gecmis_json)
                VALUES (?, ?)
            ''', (oturum_id, gecmis_json))
            self.baglanti.commit()
            return True
        except Exception as e:
            logger.error(f"Geçmiş kaydedilirken hata: {e}")
            return False

    def kapat(self) -> None:
        if self.baglanti:
            self.baglanti.close()
            logger.info("SQLite bağlantısı kapatıldı.")
