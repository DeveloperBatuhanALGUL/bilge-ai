"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Web Sunucusu (FastAPI) - WEB ARAYÜZ ENTEGRE
Tanım: RESTful API ve Web Arayüzünü sunan servis.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
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
from cekirdek.gunlukcu import gunlukcu

app = FastAPI(title="Bilge AI API", version="0.1.0-alpha")

# Statik dosyalar ve şablonlar için ayarlar
static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Global motor örneği
motor = None

@app.on_event("startup")
async def startup_event():
    global motor
    gunlukcu.bilgi("Web sunucusu başlatılıyor...")
    
    config_mgr = YapilandirmaYonetici("config.yaml")
    model_adi = config_mgr.getir('model.model_adi', 'google/flan-t5-base')
    
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

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Ana sayfayı (Web Arayüzü) döndürür."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/cevapla")
async def cevapla(istek: SoruIstek):
    """API endpoint'i: Soruyu alır ve yanıtı döndürür."""
    if not motor:
        raise HTTPException(status_code=503, detail="Motor hazır değil.")
        
    sonuc = await motor.dusun_ve_cevapla(istek.soru, istek.oturum_id)
    
    if not sonuc['basarili']:
        raise HTTPException(status_code=400, detail=sonuc.get('hata', 'Hata'))
        
    return sonuc

@app.get("/durum")
async def durum():
    return {"durum": "aktif", "versiyon": "0.1.0-alpha"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
