"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Merkezi Günlükçü (Logger)
Tanım: Uygulama genelindeki loglama işlemlerini yönetir.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
import os
from logging.handlers import RotatingFileHandler

class BilgeGunlukcu:
    """
    Mercezi loglama sınıfı.
    Hem konsola hem de dosyaya yazar.
    """
    
    _ornek = None # Singleton pattern için

    def __new__(cls):
        if cls._ornek is None:
            cls._ornek = super(BilgeGunlukcu, cls).__new__(cls)
            cls._ornek._baslat()
        return cls._ornek

    def _baslat(self):
        # Log klasörünü oluştur
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        self.logger = logging.getLogger("BilgeAI")
        self.logger.setLevel(logging.DEBUG)
        
        # Formatlayıcı
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Konsol İşleyicisi
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Dosya İşleyicisi (Rotating: Eski logları siler/yeni açar)
        file_handler = RotatingFileHandler(
            'logs/bilge.log', 
            maxBytes=5*1024*1024, # 5 MB
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def bilgi(self, mesaj: str):
        self.logger.info(mesaj)

    def uyari(self, mesaj: str):
        self.logger.warning(mesaj)

    def hata(self, mesaj: str):
        self.logger.error(mesaj)

    def ayikla(self, mesaj: str):
        self.logger.debug(mesaj)

# Global erişim için
gunlukcu = BilgeGunlukcu()
