"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Uçbirim Arayüzü (CLI) - ASYNC
Tanım: Terminal üzerinden kullanıcı ile etkileşim sağlar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cekirdek.motor import BilgeMotoru
from cekirdek.yapilandirma import YapilandirmaYonetici
from modeller.yerel_llm import YerelLLM
from veri_katmani.iliskisel_ambar import IliskiselAmbar
from veri_katmani.onbellek import AnlikBellek
from veri_katmani.chroma_impl import ChromaAmbar
from cekirdek.baglam import BaglamYonetici

async def main_async():
    print("=" * 60)
    print("BİLGE ULUSAL AÇIK KAYNAK ZEKÂ ÇERÇEVESİ v0.1.0-alpha (ASYNC)")
    print("=" * 60)
    
    config_mgr = YapilandirmaYonetici("config.yaml")
    model_adi = config_mgr.getir('model.model_adi', 'google/flan-t5-base')
    
    model = YerelLLM(model_adi=model_adi)
    kisa_hafiza = AnlikBellek()
    uzun_hafiza = IliskiselAmbar(db_yolu="data/hafiza.db")
    hafiza_yonetici = BaglamYonetici(kisa_hafiza, uzun_hafiza)
    vektor_ambari = ChromaAmbar(kalici_yol="data/vectores_db")
    
    motor = BilgeMotoru(model=model, hafiza=hafiza_yonetici, vektor_ambari=vektor_ambari)
    
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
                
            # Asenkron motor çağrısı
            sonuc = await motor.dusun_ve_cevapla(ham_soru, oturum_id=oturum_id)
            
            if sonuc['basarili']:
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
    asyncio.run(main_async())
