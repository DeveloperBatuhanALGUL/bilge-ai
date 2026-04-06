"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Güvenlik Süzgeci (Security Guard)
Tanım: Girdi ve çıktıları etik ve güvenlik kurallarına göre denetler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import re
import yaml
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("BilgeGuvenlikSuzgeci")

class GuvenlikSuzgeci:
    """
    Çok katmanlı güvenlik ve etik denetim sistemi.
    """

    def __init__(self, config_yolu: str = "ayarlar/guvenlik_kurallari.yaml"):
        self.kurallar = self._kurallari_yukle(config_yolu)
        
        # Kişisel Veri Regex Desenleri
        self.pii_desenleri = {
            'tc_kimlik': r'\b\d{11}\b',
            'telefon': r'\b05\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'kredi_karti': r'\b(?:\d[ -]*?){13,16}\b'
        }

    def _kurallari_yukle(self, yol: str) -> dict:
        try:
            with open(yol, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Güvenlik kuralları yüklenemedi: {e}")
            return {}

    def girdiyi_denetle(self, metin: str) -> Tuple[bool, str]:
        """
        Kullanıcı girdisini denetler.
        
        Returns:
            Tuple[bool, str]: (Güvenli mi?, Hata Mesajı/Açıklama)
        """
        if not metin:
            return True, ""

        metin_alt = metin.lower()

        # 1. Prompt Injection / Sistem Saldırısı Kontrolü
        red_kelimeler = self.kurallar.get('sistem_koruma', {}).get('red_kelimeler', [])
        for kelime in red_kelimeler:
            if kelime.lower() in metin_alt:
                logger.warning(f"Sistem saldırısı tespit edildi: '{kelime}'")
                return False, "Bu tür bir talep güvenlik protokolleri gereği işleme alınamaz."

        # 2. Yasaklı İçerik Kontrolü (Basit Kelime Eşleşmesi - Geliştirilebilir)
        # Not: Gerçek projede burada bir NLP sınıflandırıcı modeli kullanılmalıdır.
        # Şimdilik temel kelimeler için örnek:
        yasakli_kelimeler = ['öldür', 'vur', 'nefret', 'aptal', 'salak'] # Örnek liste
        for kelime in yasakli_kelimeler:
            if kelime in metin_alt:
                return False, "Girdiniz uygun olmayan içerik barındırıyor."

        return True, ""

    def ciktiyi_denetle(self, metin: str) -> Tuple[bool, str]:
        """
        Modelden çıkan yanıtı denetler.
        """
        if not metin:
            return True, ""

        # 1. Kişisel Veri Maskeleme (PII Redaction)
        maskelenmis_metin = metin
        for tip, desen in self.pii_desenleri.items():
            if re.search(desen, maskelenmis_metin):
                # Bulunan veriyi *** ile değiştir
                maskelenmis_metin = re.sub(desen, '[MASKELANDI]', maskelenmis_metin)
                logger.info(f"Kişisel veri tespit edildi ve maskelendi: {tip}")
        
        # 2. Uzunluk ve Boşluk Kontrolü (Basit DoS önleme)
        if len(maskelenmis_metin) > 5000:
             return False, "Yanıt çok uzun, lütfen daha spesifik sorun."

        return True, maskelenmis_metin

    def baglam_temizle(self, gecmis: list) -> list:
        """
        Sohbet geçmişindeki kişisel verileri temizler/maskeler.
        """
        temiz_gecmis = []
        for mesaj in gecmis:
            icerik = mesaj.get('icerik', '')
            _, maskeli_icerik = self.ciktiyi_denetle(icerik)
            mesaj['icerik'] = maskeli_icerik
            temiz_gecmis.append(mesaj)
        return temiz_gecmis
