"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Uçbirim Arayüzü (CLI)
Tanım: Terminal üzerinden kullanıcı ile etkileşim sağlar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cekirdek.motor import BilgeMotoru
from modeller.yerel_llm import YerelLLM
from veri_katmani.iliskisel_ambar import IliskiselAmbar
from veri_katmani.onbellek import AnlikBellek
from cekirdek.baglam import BaglamYonetici
import yaml

def main():
    # Yapılandırma yükle
    with open('ayarlar/varsayilan.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Bileşenleri başlat
    model = YerelLLM(model_adi=config['model']['model_adi'])
    
    kisa_hafiza = AnlikBellek()
    uzun_hafiza = IliskiselAmbar(db_yolu="data/hafiza.db")
    hafiza_yonetici = BaglamYonetici(kisa_hafiza, uzun_hafiza)
    
    motor = BilgeMotoru(model=model, hafiza=hafiza_yonetici)
    
    if not motor.baslat():
        print("❌ Motor başlatılamadı.")
        return

    print("🧠 Bilge hazır. Sorularınızı sorun. ('cikis' yazarak çıkabilirsiniz.)")
    
    oturum_id = "terminal_oturumu_1"
    
    while True:
        try:
            soru = input("\n➡️ Siz: ").strip()
            if soru.lower() in ['cikis', 'quit', 'exit']:
                break
            
            if not soru:
                continue
                
            sonuc = motor.dusun_ve_cevapla(soru, oturum_id=oturum_id)
            
            if sonuc['basarili']:
                print(f"\n🤖 Bilge: {sonuc['yanit']}")
            else:
                print(f"\n⚠️ Hata: {sonuc.get('hata', 'Bilinmeyen hata')}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Görüşürüz!")
            break
        except EOFError:
            break
    
    motor.durdur()

if __name__ == "__main__":
    main()
