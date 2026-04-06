"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Web Sunucusu (FastAPI)
Tanım: RESTful API üzerinden Bilge'ye erişim sağlar.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import sys
import os

# Proje kök dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cekirdek.motor import BilgeMotoru
from cekirdek.yapilandirma import YapilandirmaYonetici
from modeller.yerel_llm import YerelLLM
from veri_katmani.iliskisel_ambar import IliskiselAmbar
from veri_katmani.onbellek import AnlikBellek
from veri_katmani.chroma_impl import ChromaAmbar
from cekirdek.baglam import BaglamYonetici
from cekirdek.gunlukcu import gunlukcu

app = FastAPI(title="Bilge AI API", version="0.1.0-alpha", description="Türkçe Ulusal Zeka Asistanı API Servisi")

# Global motor örneği
motor = None

@app.on_event("startup")
async def startup_event():
    """Sunucu başlarken motoru hazırlar."""
    global motor
    gunlukcu.bilgi("Web sunucusu başlatılıyor...")
    
    config_mgr = YapilandirmaYonetici("config.yaml")
    model_adi = config_mgr.getir('model.model_adi', 'google/flan-t5-base')
    
    # Bileşenleri başlat
    model = YerelLLM(model_adi=model_adi)
    kisa_hafiza = AnlikBellek()
    uzun_hafiza = IliskiselAmbar(db_yolu="data/hafiza.db")
    hafiza_yonetici = BaglamYonetici(kisa_hafiza, uzun_hafiza)
    vektor_ambari = ChromaAmbar(kalici_yol="data/vectores_db")
    
    motor = BilgeMotoru(model=model, hafiza=hafiza_yonetici, vektor_ambari=vektor_ambari)
    
    if not motor.baslat():
        raise RuntimeError("Motor başlatılamadı!")
    
    gunlukcu.bilgi("Web sunucusu hazır.")

class SoruIstek(BaseModel):
    soru: str
    oturum_id: str = "web_oturumu_1"

@app.post("/cevapla")
async def cevapla(istek: SoruIstek):
    """
    Kullanıcı sorusunu alır ve Bilge'den yanıt döndürür.
    """
    if not motor:
        raise HTTPException(status_code=503, detail="Motor henüz hazır değil.")
        
    sonuc = motor.dusun_ve_cevapla(istek.soru, istek.oturum_id)
    
    if not sonuc['basarili']:
        raise HTTPException(status_code=400, detail=sonuc.get('hata', 'Bilinmeyen hata'))
        
    return sonuc

@app.get("/durum")
async def durum():
    """API'nin ayakta olup olmadığını kontrol eder."""
    return {"durum": "aktif", "versiyon": "0.1.0-alpha", "mesaj": "Bilge hizmetinizde."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
