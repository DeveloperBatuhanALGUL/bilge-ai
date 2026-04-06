"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Eğitilmiş Yerel LLM Wrapper
Tanım: Fine-tune edilmiş Bilge modelini yükler ve çalıştırır.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from .tabani import DilModeliTabani
import logging

logger = logging.getLogger("BilgeEgitimliLLM")

class EgitimliLLM(DilModeliTabani):
    def __init__(self, model_yolu: str = "ciktilar/bilge-finetuned", cihaz: str = "cuda"):
        self.model_yolu = model_yolu
        self.cihaz = cihaz
        self.model = None
        self.tokenizer = None
        self.yuklendi_mi = False

    def baslat(self) -> bool:
        try:
            logger.info(f"Eğitilmiş model yükleniyor: {self.model_yolu}")
            
            # Temel model konfigürasyonu (Burada temel modelin ne olduğunu bilmemiz lazım, 
            # genelde config.json içinde yazar ama manuel de belirtebiliriz)
            # Basitlik adına, temel modelin aynı olduğunu varsayıyoruz.
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
            )

            self.tokenizer = AutoTokenizer.from_pretrained(self.model_yolu)
            
            # Önce temel modeli yükle
            base_model = AutoModelForCausalLM.from_pretrained(
                "meta-llama/Llama-3-8b", # Temel model burada belirtilmeli
                quantization_config=bnb_config,
                device_map="auto"
            )
            
            # Üzerine LoRA adaptörlerini yükle
            self.model = PeftModel.from_pretrained(base_model, self.model_yolu)
            
            self.yuklendi_mi = True
            logger.info("Eğitilmiş Bilge modeli başarıyla yüklendi.")
            return True
            
        except Exception as e:
            logger.error(f"Model yüklenirken hata: {e}")
            return False

    def tahmin_et(self, girdi: str, baglam: dict = None) -> str:
        if not self.yuklendi_mi:
            raise RuntimeError("Model yüklenmedi.")
            
        # Basit inference mantığı (YerelLLM ile benzer)
        inputs = self.tokenizer(girdi, return_tensors="pt").to(self.cihaz)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def durdur(self) -> None:
        if self.model:
            del self.model
        self.yuklendi_mi = False
