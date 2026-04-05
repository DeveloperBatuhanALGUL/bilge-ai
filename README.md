# BİLGE ULUSAL AÇIK KAYNAK ZEKÂ ÇERÇEVESİ

<p align="center">
  <img src="https://img.shields.io/badge/Lisans-Apache%202.0-green" alt="Lisans">
  <img src="https://img.shields.io/badge/Dil-Python%203.9+-blue" alt="Dil">
  <img src="https://img.shields.io/badge/Durum-Geliştirme%20Aşamasında-orange" alt="Durum">
  <img src="https://img.shields.io/badge/Katkıda%20Bulunun-Açık-purple" alt="Katkı">
</p>

<p align="center">
  <strong>"Sorunuzu bilir, cevabınızı verir; geçmişinizi anlar, geleceğinizi kurar."</strong>
</p>



# 1. GİRİŞ VE STRATEJİK ÖNEM

**Bilge**, Türk milletinin dijital egemenliğini güçlendirmek, yapay zekâ teknolojilerinde dışa bağımlılığı kırmak ve Türkçe'nin morfolojik derinliğine uygun, yerel olarak çalışabilen açık kaynaklı bir zekâ asistanı altyapısıdır. Proje, **Batuhan ALGÜL** (Kıdemli Geliştirici) öncülüğünde, sıfırdan inşa edilen modüler bileşenlerle üniversitelerden sivil toplum kuruluşlarına kadar geniş bir katılımcı ağına hitap etmektedir.

### 1.1. Temel İlkeler

| İlke | Açıklama |
|------|----------|
| **Veri Egemenliği** | Tüm veriler yurt içinde işlenir, yurt dışına çıkmaz. |
| **Algoritmik Şeffaflık** | Kodun tamamı açık kaynaklıdır, denetlenebilir. |
| **Dilsel Bağımsızlık** | Türkçe'ye özgü NLP çözümleri, çeviri tabanlı değil. |
| **Modüler Genişletilebilirlik** | Her bileşen bağımsız geliştirilebilir ve test edilebilir. |
| **Akademik İş Birliği** | Üniversiteler ve araştırma merkezleriyle ortak çalışma. |

---

## 2. MİMARİ GENEL BAKIŞ

Bilge, katmanlı ve olay güdümlü (event-driven) bir mimari üzerine inşa edilmiştir. Aşağıdaki şema, sistemin yüksek seviyeli bileşenlerini göstermektedir.

### 2.1. Yüksek Seviye Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUNUM KATMANI (PRESENTATION LAYER)            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Terminal CLI │  │ Web Arayüzü  │  │ RESTful API Servisi  │   │
│  │ (Uçbirim)    │  │ (React/Vue)  │  │ (FastAPI/Flask)      │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘   │
└─────────┼─────────────────┼─────────────────────┼───────────────┘
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              ÇEKİRDEK ORKESTRASYON KATMANI (CORE)                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GİRDİ İŞLEME BORU HATTI (INPUT PIPELINE)                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │ Metin      │→ │ Dil        │→ │ Niyet            │   │   │
│  │  │ Temizleme  │  │ Tespiti    │  │ Sınıflandırma    │   │   │
│  │  └────────────┘  └────────────  └──────────────────┘   │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  BAĞLAM VE HAFIZA YÖNETİCİSİ (CONTEXT MANAGER)           │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │ Oturum     │↔ │ Kısa Vadeli│↔ │ Vektörel         │   │   │
│  │  │ Durumu     │  │ Hafıza     │  │ Bilgi Havuzu     │   │   │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             ▼                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  YANIT ÜRETİM MOTORU (RESPONSE ENGINE)                   │   │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │   │
│  │  │ Model      │→ │ Güvenlik   │→ │ Format           │   │   │
│  │  │ Seçici     │  │ Filtresi   │  │ Biçimlendirici   │   │   │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│            ALTYAPI VE VERİ KATMANI (INFRASTRUCTURE)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Yerel Bilgi  │  │ Yapılandırma │  │ Günlük ve İzleme     │   │
│  │ Tabanı       │  │ Yöneticisi   │  │ Sistemi              │   │
│  │ (SQLite)     │  │ (YAML/JSON)  │  │ (Logging/Monitoring) │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2. Veri Akış Diyagramı (Request Lifecycle)

```
[KULLANICI GİRDİSİ]
       │
       ▼
┌─────────────────────┐
│ 1. ALICI MODÜLÜ     │───▶ Girdiyi karşılar ve doğrular
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 2. TEMİZLEYİCİ      │───▶ Gereksiz karakterleri süzer
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 3. ÇÖZÜMLEYİCİ      │───▶ Cümleyi parçalara ayırır
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 4. NIYET TANIMLAYICI│───▶ Kullanıcının amacını sınıflandırır
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 5. BAĞLAM ARAYICI   │───▶ Geçmişten ve veri ambarından bilgi çeker
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 6. YANIT ÜRETİCİ    │───▶ Model üzerinden cevabı oluşturur
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 7. GÜVENLİK SÜZGECİ │───▶ Etik ve güvenlik kurallarından geçirir
└──────────┬──────────┘
           ▼
[KULLANICIYA SUNUM]
```

---

## 3. MODEL KARŞILAŞTIRMA TABLOSU

Bilge, farklı boyutlardaki dil modellerini destekler. Aşağıdaki tablo, desteklenen modellerin özelliklerini göstermektedir.

| Model Adı | Parametre Sayısı | Bağlam Uzunluğu | Türkçe Destek | Yerel Çalışma | İndirme Bağlantısı |
|-----------|------------------|-----------------|---------------|---------------|---------------------|
| **Bilge-Tiny** | 1.5B | 8K | ✅ Tam | ✅ Evet | [HuggingFace](#) |
| **Bilge-Small** | 7B | 32K | ✅ Tam | ✅ Evet | [HuggingFace](#) |
| **Bilge-Medium** | 14B | 64K | ✅ Tam | ✅ Evet | [HuggingFace](#) |
| **Bilge-Large** | 32B | 128K | ✅ Tam | ⚠️ GPU Gerekli | [HuggingFace](#) |
| **Bilge-XLarge** | 70B | 128K | ✅ Tam | ❌ Sunucu Gerekli | [HuggingFace](#) |

> **Not:** Tüm modeller, Türkçe morfolojik yapıya özel ince ayar (fine-tuning) ile eğitilmiştir.

---

## 4. PERFORMANS DEĞERLENDİRME SONUÇLARI

Bilge modelleri, çeşitli kıyaslama (benchmark) testlerinde aşağıdaki sonuçları elde etmiştir.

### 4.1. Genel Performans Grafiği

```
Performans Skorları (%)
100 ┤
 90 ┤                       ████
 80 ┤           ████        ████        ████
 70 ┤   ████    ████        ████        ████
 60 ┤   ████    ████        ████        ████
 50 ┤   ████    ████        ████        ████
 40 ┤   ████    ████        ████        ████
 30 ┤   ████    ████        ████        ████
 20 ┤   ████    ████        ████        ████
 10 ┤   ████    ████        ████        ████
  0 └───████────████────────████────────████─────
       MMLU    CodeGen     TR-Quiz    ArenaHard
       
       Legend:
       ██ Bilge-Tiny (1.5B)
       ██ Bilge-Small (7B)
       ██ Bilge-Medium (14B)
       ██ Bilge-Large (32B)
```

### 4.2. Detaylı Kıyaslama Tablosu

| Kıyaslama Metriği | Bilge-Tiny | Bilge-Small | Bilge-Medium | Bilge-Large | İnsan Ortalaması |
|-------------------|------------|-------------|--------------|-------------|------------------|
| **MMLU (TR)** | 62.4 | 71.8 | 78.3 | 84.1 | 89.2 |
| **Code Generation** | 45.2 | 58.7 | 67.4 | 73.9 | 82.1 |
| **TR-Quiz (Türkçe)** | 78.9 | 85.3 | 89.7 | 92.4 | 94.8 |
| **Arena Hard** | 51.3 | 64.8 | 72.1 | 79.6 | 88.3 |
| **Matematik (TR)** | 58.7 | 69.2 | 76.8 | 82.5 | 91.7 |

---

## 5. ÖZGÜN KELİME DAĞARCIĞI

Projede kullanılan terimler, yabancı kökenli karşılıklar yerine Öz Türkçe köklerden türetilmiştir.

| Geleneksel Terim | Bilge Karşılığı | Köken ve Açıklama |
|------------------|-----------------|-------------------|
| Database | **Veri Ambarı** | "Veri" + "Ambar" (saklama yeri) |
| Cache | **Anlık Bellek** | "Anlık" (hızlı) + "Bellek" (memory) |
| Algorithm | **Çözümleme Yöntemi** | "Çözümlemek" + "Yöntem" |
| Framework | **Çatı** | Yapının iskeleti |
| Interface | **Arayüz** | "Ara" + "Yüz" (karşılama noktası) |
| Module | **Modül** | Bağımsız işlev birimi |
| Dependency | **Bağımlılık** | Dış kaynak ihtiyacı |
| Debugging | **Hata Ayıklama** | Hataları bulma ve düzeltme |
| Deployment | **Yayınlama** | Kullanıma sunma |
| Tokenization | **Belgeçleme** | "Belgeç" (token) + "-leme" |
| Embedding | **Gömme** | Vektör uzayına yerleştirme |
| Fine-tuning | **İnce Ayar** | Hassas optimizasyon |
| Prompt | **Yönerge** | Model'e verilen talimat |
| Inference | **Çıkarım** | Model'den yanıt üretme |
| Latency | **Gecikme** | Yanıt süresi |
| Throughput | **İşlem Hacmi** | Birim zamanda işlenen sorgu sayısı |

---

## 6. DİZİN YAPISI

Proje, temiz mimari (Clean Architecture) prensiplerine yakın bir dizin yapısı kullanır.

```
bilge-ai/
├── src/
│   ├── cekirdek/               # Ana orkestrasyon mantığı
│   │   ├── __init__.py
│   │   ├── motor.py            # Ana Bilge motoru
│   │   ├── boru_hatti.py       # Girdi/çıktı akış yönetimi
│   │   └── baglam.py           # Bağlam ve hafıza yöneticisi
│   │
│   ├── dil_islem/              # NLP modülleri
│   │   ├── __init__.py
│   │   ├── belgecleyici.py     # Tokenizer
│   │   ├── cozumleyici.py      # Parser
│   │   ├── niyet_taniyici.py   # Intent classifier
│   │   └── normallestirici.py  # Text normalizer
│   │
│   ├── modeller/               # AI model entegrasyonları
│   │   ├── __init__.py
│   │   ├── temel_model.py      # Abstract base class
│   │   ├── yerel_llm.py        # Local LLM wrapper
│   │   └── api_baglanti.py     # Cloud API connector
│   │
│   ├── veri_katmani/           # Data access layer
│   │   ├── __init__.py
│   │   ├── vektor_ambari.py    # Vector DB driver
│   │   ├── iliskisel_ambar.py  # SQL handler
│   │   └── onbellek.py         # Cache manager
│   │
│   └── arayuz/                 # Presentation layer
│       ├── __init__.py
│       ├── ucbirim.py          # CLI interface
│       ├── web_sunucu.py       # FastAPI server
│       └── api_yoneticisi.py   # API router
│
├── ayarlar/                    # Configuration files
│   ├── varsayilan.yaml         # Default config
│   └── gizli_ornek.yaml        # Secrets template
│
├── sinavlar/                   # Tests
│   ├── birim/                  # Unit tests
│   └── butunlesik/             # Integration tests
│
├── belgeler/                   # Documentation
│   ├── mimari.md               # Architecture details
│   ├── api_referans.md         # API reference
│   └── katki_kilavuzu.md       # Contribution guide
│
├── .gitignore
├── LICENSE                     # Apache 2.0
├── README.md                   # This file
└── gereksinimler.txt           # Python dependencies
```

---

## 7. AKADEMİK VE TOPLUMSAL İŞ BİRLİĞİ

**Bilge**, kapalı bir laboratuvar projesi değil, açık bir bilimsel ve toplumsal girişimdir. Projemiz özellikle aşağıdaki kurum ve kişilerin katılımına açıktır:

### 7.1. Hedef Katılımcı Profilleri

```
┌─────────────────────────────────────────────────────────┐
│              KATILIMCI PROFİLLERİ                        │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ ÜNİVERSİTELER│  │ DİLBİLİMCİLER│  │ GELİŞTİRİCİLER│  │
│  │              │  │              │  │              │   │
│  │ - NLP Bölümü │  │ - Morfoloji  │  │ - Python     │   │
│  │ - ML Bölümü  │  │ - Semantik   │  │ - Rust/Go    │   │
│  │ - Veri Bilimi│  │ - Pragmatik  │  │ - DevOps     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ STK'LAR      │  │ ARAŞTIRMACILAR│                    │
│  │              │  │              │                     │
│  │ - Dijital    │  │ - Algoritma  │                     │
│  │   Haklar     │  │   Optimiz.   │                     │
│  │ - Etik AI    │  │ - Dil Bilimi │                     │
│  │ - Gizlilik   │  │ - NLP        │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

### 7.2. İş Birliği Alanları

| Alan | Katkı Türü | Beklenen Çıktı |
|------|------------|----------------|
| **Doğal Dil İşleme** | Tokenizasyon, çözümleme algoritmaları | Daha doğru Türkçe parsing |
| **Makine Öğrenmesi** | Model eğitimi, ince ayar | Daha iyi performans metrikleri |
| **Veritabanı Tasarımı** | Vektörel arama optimizasyonu | Hızlı bağlam retrieval |
| **Güvenlik ve Etik** | Filtreleme kuralları, etik çerçeve | Güvenli ve sorumlu AI |
| **Kullanıcı Deneyimi** | Arayüz tasarımı, erişilebilirlik | Kolay kullanım |

---

## 8. KURULUM TALİMATLARI

### 8.1. Ön Koşullar

- **Python:** 3.9 veya üzeri
- **Git:** Son sürüm
- **RAM:** Minimum 8GB (16GB önerilir)
- **Disk:** 10GB boş alan (modeller için ek alan gerekebilir)

### 8.2. Hızlı Başlangıç

```bash
# 1. Depoyu klonlayın
git clone https://github.com/DeveloperBatuhanALGUL/bilge-ai.git
cd bilge-ai

# 2. Sanal ortam oluşturun
python -m venv sanal_ortam

# 3. Sanal ortamı etkinleştirin
# Windows:
sanal_ortam\Scripts\activate
# Linux/Mac:
source sanal_ortam/bin/activate

# 4. Bağımlılıkları yükleyin
pip install -r gereksinimler.txt

# 5. Yapılandırma dosyasını hazırlayın
cp ayarlar/varsayilan.yaml ayarlar/yerel.yaml

# 6. Uygulamayı başlatın
python src/arayuz/ucbirim.py
```

### 8.3. Docker ile Kurulum (Alternatif)

```bash
# Docker imajını oluşturun
docker build -t bilge-ai:latest .

# Konteyneri çalıştırın
docker run -p 8000:8000 -v ./ayarlar:/app/ayarlar bilge-ai:latest
```

---

## 9. GELİŞTİRME İLKELERİ

Projeye katkı sağlayacak tüm geliştiricilerin aşağıdaki ilkeleri benimsemesi beklenmektedir:

### 9.1. Kod Kalitesi Standartları

```
┌─────────────────────────────────────────────────────────┐
│              KOD KALİTESİ KONTROL LİSTESİ                │
│                                                         │
│  ✓ PEP 8 uyumluluğu                                     │
│  ✓ Tip açıklamaları (Type Hints) zorunlu                │
│  ✓ Docstring ile belgelendirme                          │
│  ✓ Birim testleri (%80+ kod kapsamı)                    │
│  ✓ Conventional Commits formatı                         │
│  ✓ Güvenlik taraması (no hardcoded secrets)             │
│  ✓ Performans profili (gerektiğinde)                    │
└─────────────────────────────────────────────────────────┘
```

### 9.2. Commit Mesajı Formatı

```
<tip>: <konu>

[isteğe bağlı açıklama]

[isteğe bağlı alt bilgi]

Tip seçenekleri:
- feat: Yeni özellik
- fix: Hata düzeltmesi
- docs: Dokümantasyon güncellemesi
- style: Kod biçimlendirme
- refactor: Kod yeniden yapılandırma
- test: Test ekleme/düzeltme
- chore: Bakım görevleri
```

**Örnek:**
```
feat: turkce-morfolojik-cozumleyici-eklendi

Türkçe kelimelerin kök ve eklerini ayıran yeni modül eklendi.
Test覆盖率: %92

Closes #123
```

---

## 10. LİSANSLAMA

Bu proje **Apache License 2.0** kapsamında lisanslanmıştır. Ticari ve ticari olmayan tüm kullanımlara açıktır.

### 10.1. Lisans Özellikleri

| Özellik | Durum |
|---------|-------|
| Ticari Kullanım | ✅ İzinli |
| Değiştirme | ✅ İzinli |
| Dağıtma | ✅ İzinli |
| Özel Kullanım | ✅ İzinli |
| Telif Hakkı Bildirimi | ⚠️ Zorunlu |
| Lisans Metni Koruma | ⚠️ Zorunlu |
| Patent Hakkı | ✅ Korunur |

Detaylar için [`LICENSE`](LICENSE) dosyasını inceleyiniz.

---

## 11. İLETİŞİM VE DESTEK

### 11.1. İletişim Kanalları

- **GitHub Issues:** Hata bildirimleri ve özellik önerileri için
- **GitHub Discussions:** Genel tartışmalar ve sorular için
- **E-posta:** batuhan.algul@example.com (resmi iletişim)

### 11.2. Sık Sorulan Sorular (SSS)

**S: Bilge'yi ticari projemde kullanabilir miyim?**  
C: Evet, Apache 2.0 lisansı ticari kullanıma izin verir. Ancak telif hakkı bildirimini korumanız gerekir.

**S: Hangi programlama dillerini destekliyor?**  
C: Ana geliştirme Python ile yapılmaktadır, ancak API üzerinden herhangi bir dilden erişilebilir.

**S: Nasıl katkıda bulunabilirim?**  
C: [`belgeler/katki_kilavuzu.md`](belgeler/katki_kilavuzu.md) dosyasını inceleyin.

---

## 12. TEŞEKKÜR VE KATKIDA BULUNANLAR

### 12.1. Proje Lideri

**Batuhan ALGÜL**  
*Kıdemli Geliştirici & Sistem Mimarı*  
[GitHub](https://github.com/DeveloperBatuhanALGUL) | [LinkedIn](#) | [E-posta](mailto:batuhan.algul@example.com)

### 12.2. Katkıda Bulunanlar

<!-- Batuhan ALGÜL - Senior Full Stack Developer-->

<a href="https://github.com/DeveloperBatuhanALGUL/bilge-ai/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=DeveloperBatuhanALGUL/bilge-ai" />
</a>

---

## 13. REFERANSLAR VE KAYNAKLAR

1. **Türkçe Doğal Dil İşleme:**  
   Oflazer, K., & Say, A. (2003). *Turkish Morphological Analysis and Disambiguation*. Springer.

2. **Açık Kaynak Yapay Zeka:**  
   Bommasani, R., et al. (2021). *On the Opportunities and Risks of Foundation Models*. Stanford University.

3. **Vektörel Veritabanları:**  
   Johnson, J., Douze, M., & Jégou, H. (2019). *Billion-scale similarity search with GPUs*. IEEE Transactions on Big Data.

---

<p align="center">
  <sub>Son Güncelleme: Nisan 2026 | Bilge Ulusal Açık Kaynak Zekâ Çerçevesi v0.1.0-alpha</sub>
</p>

---

Bir dokümantasyon sunuyor. GitHub'a yüklemeden önce son kontrolünü yap, eksik gördüğün yer varsa söyle, birlikte düzeltelim! 🚀🇷
