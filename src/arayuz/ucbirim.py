"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Uçbirim Arayüzü (CLI) - GÜNCELLENMİŞ
Tanım: Terminal üzerinden kullanıcı ile etkileşim sağlar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cekirdek.motor import BilgeMotoru
from cekirdek.yapilandirma import YapilandirmaYonetici
from cekirdek.baglam import BaglamYonetici
from cekirdek.boru_hatti import GirdiIslemeHatti
from modeller.yerel_llm import YerelLLM
from veri_katmani.iliskisel_ambar import IliskiselAmbar
from veri_katmani.onbellek import AnlikBellek
from veri_katmani.chroma_impl import ChromaAmbar

def main():
    print("=" * 60)
    print("BİLGE ULUSAL AÇIK KAYNAK ZEKÂ ÇERÇEVESİ v0.1.0-alpha")
    print("=" * 60)
    
    # 1. Yapılandırma
    config_mgr = YapilandirmaYonetici("config.yaml")
    if not config_mgr.ayarlar:
        print("HATA: config.yaml yüklenemedi.")
        return

    # 2. Bileşenler
    model_adi = config_mgr.getir('model.model_adi', 'google/flan-t5-base')
    model = YerelLLM(model_adi=model_adi)
    
    # Hafıza Katmanı
    kisa_hafiza = AnlikBellek()
    uzun_hafiza = IliskiselAmbar(db_yolu="data/hafiza.db")
    hafiza_yonetici = BaglamYonetici(kisa_hafiza, uzun_hafiza)
    
    # Vektör Ambarı Katmanı (ChromaDB)
    vektor_ambari = ChromaAmbar(kalici_yol="data/vectores_db")
    
    # Motor
    motor = BilgeMotoru(model=model, hafiza=hafiza_yonetici, vektor_ambari=vektor_ambari)
    boru_hatti = GirdiIslemeHatti()
    
    if not motor.baslat():
        print("HATA: Motor başlatılamadı.")
        return

    print("\nBilge hazır. ('cikis' yazarak çıkabilirsiniz.)\n")
    
    oturum_id = "terminal_oturumu_1"
    
    while True:
        try:
            ham_soru = input("Siz: ")
            
            if ham_soru.lower() in ['cikis', 'quit', 'exit', 'q']:
                break
            
            if not ham_soru.strip():
                continue
                
            # Girdiyi işle
            islenmis_veri = boru_hatti.isle(ham_soru)
            
            if islenmis_veri['hata']:
                print(f"Hata (İşleme): {islenmis_veri['hata']}")
                continue
                
            # Motoru çalıştır
            sonuc = motor.dusun_ve_cevapla(islenmis_veri['temiz'], oturum_id=oturum_id)
            
            if sonuc['basarili']:
                # Kullanıcıya kaç belge kullanıldığını göster (opsiyonel debug bilgisi)
                # print(f"[{sonuc.get('kullanilan_belge_sayisi', 0)} belge tarandı]")
                print(f"\nBilge: {sonuc['yanit']}\n")
            else:
                print(f"\nHata: {sonuc.get('hata', 'Bilinmeyen hata')}\n")
                
        except KeyboardInterrupt:
            print("\n\nGörüşürüz!")
            break
        except EOFError:
            break
    
    motor.durdur()

if __name__ == "__main__":
    main()
