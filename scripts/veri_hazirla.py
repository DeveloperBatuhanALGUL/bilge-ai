"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Betik: Eğitim Verisi Hazırlama
Tanım: Ham JSONL verilerini, model eğitimi için uygun formata dönüştürür.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import json
import os
from datasets import load_dataset

def hazirla_ve_kaydet(giris_yolu: str, cikis_yolu: str):
    """
    JSONL dosyasını okur, temizler ve Arrow formatında kaydeder.
    """
    print(f"Veri yükleniyor: {giris_yolu}")
    
    # JSONL yükleme
    dataset = load_dataset('json', data_files=giris_yolu)
    
    def formatlama_fonksiyonu(examples):
        """
        Her bir örneği 'prompt' ve 'completion' çiftine dönüştürür.
        Chat template kullanımı için hazırlık.
        """
        prompts = []
        completions = []
        
        for i in range(len(examples['content'])):
            content = examples['content'][i]
            prompt_text = content.get('prompt', '')
            completion_text = content.get('completion', '')
            
            # Boş verileri atla
            if not prompt_text or not completion_text:
                continue
                
            prompts.append(prompt_text)
            completions.append(completion_text)
            
        return {"prompt": prompts, "completion": completions}

    # Veriyi uygula
    formatted_dataset = dataset.map(formatlama_fonksiyonu, batched=True, remove_columns=dataset['train'].column_names)
    
    # Train/Test split
    split_dataset = formatted_dataset['train'].train_test_split(test_size=0.1)
    
    print(f"Eğitim seti boyutu: {len(split_dataset['train'])}")
    print(f"Test seti boyutu: {len(split_dataset['test'])}")
    
    # Disk'e kaydet
    os.makedirs(os.path.dirname(cikis_yolu), exist_ok=True)
    split_dataset.save_to_disk(cikis_yolu)
    print(f"✅ Veri seti hazırlandı ve şuraya kaydedildi: {cikis_yolu}")

if __name__ == "__main__":
    # Örnek kullanım
    hazirla_ve_kaydet(
        giris_yolu="data/ornek_veri.jsonl", 
        cikis_yolu="data/hazir_egitim_verisi"
    )
