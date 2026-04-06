"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Yerel Dil Modeli Wrapper
Tanım: HuggingFace Transformers ile yerel çalışan LLM entegrasyonu.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from .tabani import DilModeliTabani

logger = logging.getLogger("BilgeYerelLLM")

class YerelLLM(DilModeliTabani):
    """
    Yerel çalışan büyük dil modeli wrapper'ı.
    HuggingFace formatındaki modelleri destekler.
    """

    def __init__(self, model_adi: str = "bilge-small-7b", cihaz: str = "cpu"):
        self.model_adi = model_adi
        self.cihaz = cihaz
        self.tokenizer = None
        self.model = None
        self.yuklendi_mi = False

    def baslat(self) -> bool:
        try:
            logger.info(f"Model yükleniyor: {self.model_adi}")
            # Geçici olarak flan-t5-base kullanıyoruz (Türkçe desteği var)
            if self.model_adi == "bilge-small-7b":
                self.model_adi = "google/flan-t5-base"  # Gerçek model indirilecek
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_adi)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_adi).to(self.cihaz)
            self.yuklendi_mi = True
            logger.info("Model başarıyla yüklendi.")
            return True
        except Exception as e:
            logger.error(f"Model yüklenirken hata: {e}")
            return False

    def tahmin_et(self, girdi: str, baglam: dict = None) -> str:
        if not self.yuklendi_mi:
            raise RuntimeError("Model henüz yüklenmedi. 'baslat()' çağrılmalı.")

        # Basit prompt oluşturma (ileride daha gelişmiş olacak)
        if baglam and baglam.get("gecmis"):
            gecmis_metin = "\n".join([f"{msg['rol']}: {msg['icerik']}" for msg in baglam["gecmis"]])
            tam_girdi = f"{gecmis_metin}\nuser: {girdi}\nasistant:"
        else:
            tam_girdi = f"user: {girdi}\nasistant:"

        # Tokenize et
        inputs = self.tokenizer(tam_girdi, return_tensors="pt").to(self.cihaz)

        # Tahmin üret
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=2048,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Yanıtı decode et
        yanit = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Sadece asistan kısmını al
        if "asistant:" in yanit:
            yanit = yanit.split("asistant:")[-1].strip()
        else:
            yanit = yanit.strip()

        return yanit

    def durdur(self) -> None:
        if self.model:
            del self.model
        if self.tokenizer:
            del self.tokenizer
        self.yuklendi_mi = False
        logger.info("Model kaynakları serbest bırakıldı.")
