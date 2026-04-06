"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Model Eğitim Motoru
Tanım: LoRA tekniği ile yerel dil modelini ince ayarlar (Fine-Tuning).
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import torch
import yaml
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_from_disk

logger = logging.getLogger("BilgeEgitimMotoru")

class BilgeEgitimMotoru:
    def __init__(self, config_yolu: str = "ayarlar/egitim_ayarlari.yaml"):
        self.config = self._config_yukle(config_yolu)
        self.model = None
        self.tokenizer = None
        self.trainer = None

    def _config_yukle(self, yol: str) -> dict:
        with open(yol, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def baslat(self):
        """Modeli ve Tokenizer'ı yükler."""
        model_adi = self.config['model']['temeli']
        logger.info(f"Temel model yükleniyor: {model_adi}")
        
        # 4-bit Quantization (Bellek Tasarrufu)
        from transformers import BitsAndBytesConfig
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_adi)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_adi,
            quantization_config=bnb_config,
            device_map="auto"
        )
        
        self.model = prepare_model_for_kbit_training(self.model)
        logger.info("Model başarıyla yüklendi ve 4-bit'e sıkıştırıldı.")

    def lo_ra_yapilandir(self):
        """LoRA adaptörlerini modele ekler."""
        lora_cfg = self.config['lo_ra_ayarlari']
        
        peft_config = LoraConfig(
            r=lora_cfg['r'],
            lora_alpha=lora_cfg['lora_alpha'],
            lora_dropout=lora_cfg['lora_dropout'],
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=lora_cfg['hedef_moduller']
        )
        
        self.model = get_peft_model(self.model, peft_config)
        logger.info("LoRA adaptörleri modele entegre edildi.")

    def egit(self):
        """Eğitim sürecini başlatır."""
        if not self.model:
            self.baslat()
            self.lo_ra_yapilandir()

        # Veri setini yükle
        veri_yolu = self.config['veri_seti']['yol'].replace('.jsonl', '_hazir') # Hazır klasör adı
        try:
            dataset = load_from_disk(veri_yolu)
        except:
            logger.error("Hazır veri seti bulunamadı. Önce 'scripts/veri_hazirla.py' çalıştırılmalı.")
            return

        train_data = dataset['train']

        # Eğitim Argümanları
        egitim_cfg = self.config['egitim_parametreleri']
        training_args = TrainingArguments(
            output_dir=egitim_cfg['cikti_dizini'],
            num_train_epochs=1, # Adım sayısı ile kontrol edilecek
            per_device_train_batch_size=egitim_cfg['batch_buyuklugu'],
            gradient_accumulation_steps=egitim_cfg['gradyan_toplama_adimlari'],
            learning_rate=egitim_cfg['ogrenme_hizi'],
            fp16=True,
            logging_steps=10,
            save_strategy="steps",
            save_steps=100,
            report_to="none" # Wandb kullanmıyorsan none
        )

        # Trainer Oluştur
        self.trainer = SFTTrainer(
            model=self.model,
            train_dataset=train_data,
            tokenizer=self.tokenizer,
            args=training_args,
            max_seq_length=egitim_cfg['kosullu_uretim_boyutu'],
            packing=False
        )

        logger.info("Eğitim başlıyor...")
        self.trainer.train()
        
        # Modeli Kaydet
        self.model.save_pretrained(egitim_cfg['cikti_dizini'])
        self.tokenizer.save_pretrained(egitim_cfg['cikti_dizini'])
        logger.info(f"✅ Eğitim tamamlandı. Model şuraya kaydedildi: {egitim_cfg['cikti_dizini']}")

if __name__ == "__main__":
    motor = BilgeEgitimMotoru()
    motor.egit()
