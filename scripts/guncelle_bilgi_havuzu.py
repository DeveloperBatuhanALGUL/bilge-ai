"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Betik: Bilgi Havuzu Güncelleme
Tanım: Canlı kaynaklardan veri çekip Vektör Ambarına ekler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from veri_katmani.chroma_impl import ChromaAmbar
from veri_katmani.veri_cekici import CanliVeriCekici
import logging

# Loglama
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GuncellemeBetigi")

def main():
    logger.info("--- BİLGE BİLGİ HAVUZU GÜNCELLENİYOR ---")
    
    # 1. Bileşenleri Başlat
    ambar = ChromaAmbar(kalici_yol="data/vectores_db")
    cekici = CanliVeriCekici()
    
    if not ambar.baslat():
        logger.error("Vektör ambarı başlatılamadı!")
        return

    tum_belgeler = []

    # 2. Kaynak 1: TBMM Genel Kurul Tutanakları (Örnek RSS veya Link)
    # Not: TBMM'nin resmi RSS adresi değişebilir, güncel linki kontrol etmelisin.
    # Burada örnek olarak genel bir haber RSS'si kullanıyoruz, sen TBMM linkini buraya koyabilirsin.
    tbmm_rss = "https://www.tbmm.gov.tr/rss/genelkurul.xml" 
    # Eğer bu link çalışmazsa, alternatif bir haber kaynağı deneyelim:
    alternatif_haber = "https://www.trthaber.com/manset_articles.rss"
    
    logger.info("Haber/RSS verileri çekiliyor...")
    rss_belgeleri = cekici.rss_den_veri_cek(alternatif_haber, limit=10)
    tum_belgeler.extend(rss_belgeleri)

    # 3. Kaynak 2: Örnek Bir Meclis Konuşması veya Makale (Web Scraping)
    # Örnek: Wikipedia'dan Türkçe Dil Tarihi sayfası (Eğitim amaçlı)
    wiki_url = "https://tr.wikipedia.org/wiki/T%C3%BCrk%C3%A7e"
    logger.info("Web sayfası taranıyor...")
    web_belgeleri = cekici.web_sayfasindan_metin_cek(wiki_url)
    tum_belgeler.extend(web_belgeleri)

    # 4. Verileri Ambara Ekle
    if tum_belgeler:
        logger.info(f"Toplam {len(tum_belgeler)} belge eklenecek.")
        if ambar.belge_ekle(tum_belgeler):
            logger.info("✅ Bilgi havuzu başarıyla güncellendi!")
        else:
            logger.error("❌ Belgeler eklenirken hata oluştu.")
    else:
        logger.warning("Hiç yeni veri bulunamadı.")

    ambar.kapat()
    logger.info("--- GÜNCELLEME TAMAMLANDI ---")

if __name__ == "__main__":
    main()
