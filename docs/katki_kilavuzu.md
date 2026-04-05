Harika. İsteğin üzerine, **emoji kullanılmayan**, tamamen **ASCII tabanlı şemalarla** zenginleştirilmiş, **geçişlerin (flow)** net olduğu, **kurumsal ciddiyeti** koruyan ve sadece **Batuhan ALGÜL**'ün imzasını taşıyan `docs/katki_kilavuzu.md` dosyasını hazırladım.

Bu doküman, projeye gelecek her geliştiriciye "Burada kurallar vardır, süreç bellidir" mesajını verecek kadar detaylıdır.

GitHub'da `docs/katki_kilavuzu.md` dosyasının içeriğini aşağıdaki metinle değiştir:

```markdown
# BİLGE PROJESESİ KATKI SAĞLAMA VE GELİŞTİRME KILAVUZU

## 1. GİRİŞ VE AMAÇ

Bu kılavuz, **Bilge Ulusal Açık Kaynak Zekâ Çerçevesi** projesine kod, veri, dokümantasyon veya test desteği sağlamak isteyen geliştiriciler için resmi süreçleri tanımlar. Proje, merkezi bir yönetim anlayışıyla, **Batuhan ALGÜL** tarafından yürütülmekte olup, tüm katkılar proje liderinin onayından geçerek ana depoya entegre edilir.

Temel ilke: **Şeffaflık, Standartlaşma ve Kalite.**

---

## 2. KATKI SÜRECİ MİMARİSİ

Projeye katkı sağlama süreci, aşağıdaki diyagramda gösterildiği gibi doğrusal ve denetimli bir akışa sahiptir.

### 2.1. Genel Katkı Akış Diyagramı

```text
+---------------------------------------------------------------------------------------+
|                           KATKIDA BULUNAN GELİŞTİRİCİ                                 |
+---------------------------------------------------------------------------------------+
        |
        | 1. Fikri Oluştur / Hata Bul
        v
+---------------------+
| GITHUB ISSUE AÇ     |
| - Etiket Seç        |
| - Detaylandır       |
+----------+----------+
           |
           | 2. Proje Lideri Onayı (Batuhan ALGÜL)
           v
+---------------------+
| DEPOYU FORK ET      |
| - Kendi Hesabına    |
|   Kopyala           |
+----------+----------+
           |
           | 3. Yerel Ortam Kurulumu
           v
+---------------------+
| DAL (BRANCH) OLUŞTUR|
| - ozellik/...       |
| - duzeltme/...      |
+----------+----------+
           |
           | 4. Kodlama & Test
           v
+---------------------+
| GELİŞTİRME YAP      |
| - Kod Yaz           |
| - Birim Test Koş    |
| - Lint Kontrolü     |
+----------+----------+
           |
           | 5. Değişiklikleri Gönder
           v
+---------------------+
| COMMIT & PUSH       |
| - Conventional Commits|
|   Formatı           |
+----------+----------+
           |
           | 6. Pull Request (PR) Aç
           v
+---------------------+
| İNCELEME SÜRECİ     |
| - Otomatik Testler  |
| - Manuel Kod İnceleme|
|   (Batuhan ALGÜL)   |
+----------+----------+
           |
           | 7. Onay / Red
           v
+---------------------+       +---------------------+
| PR KABUL EDİLDİ     |       | PR REDDEDİLDİ       |
| - Main'e Merge      |       | - Geri Bildirim Ver |
| - Issue Kapat       |       | - Düzeltme İste     |
+---------------------+       +---------------------+
```

---

## 3. TEKNİK STANDARTLAR VE KURALLAR

Projede kod bütünlüğünü korumak için aşağıdaki teknik standartlara uyulması zorunludur.

### 3.1. Dizin Yapısı ve Sorumluluklar

Her modülün sorumluluk alanı keskindir. Yeni dosya eklerken aşağıdaki yapıyı referans alın:

```text
bilge-ai/
├── src/
│   ├── cekirdek/           # Ana iş mantığı (Motor, Orkestratör)
│   ├── dil_islem/          # NLP araçları (Tokenizer, Parser)
│   ├── modeller/           # AI Model arayüzleri ve implementasyonları
│   ├── veri_katmani/       # Veritabanı ve önbellek yönetimi
│   └── arayuz/             # Kullanıcı etkileşimi (CLI, API)
├── tests/                  # Birim ve entegrasyon testleri
├── docs/                   # Dokümantasyon
└── data/                   # Veri stratejisi ve örnek veriler
```

### 3.2. Kod Biçimlendirme Standartları

*   **Dil:** Python 3.9+
*   **Stil Rehberi:** PEP 8
*   **Tip Açıklamaları:** Tüm fonksiyonlar ve değişkenler tip belirtilmelidir (Type Hints).
*   **Belgelendirme:** Her public sınıf ve fonksiyon Google Style Docstrings ile belgelendirilmelidir.

**Örnek Kod Bloğu:**

```python
def metni_temizle(girdi: str, ozel_karakterleri_sil: bool = True) -> str:
    """
    Verilen metni temizler ve normalize eder.
    
    Args:
        girdi (str): Temizlenecek ham metin.
        ozel_karakterleri_sil (bool): Özel karakterlerin silinip silinmeyeceği.
        
    Returns:
        str: Temizlenmiş ve normalize edilmiş metin.
    """
    if not isinstance(girdi, str):
        raise TypeError("Girdi string olmalıdır.")
    
    # İşlem mantığı buraya yazılacak
    return girdi.strip()
```

### 3.3. Commit Mesajı Standartları

Değişiklik geçmişini okunabilir kılmak için **Conventional Commits** standardı uygulanır.

**Format:**
`<tip>: <konu>`

**Tip Listesi:**
*   `feat`: Yeni özellik ekleme
*   `fix`: Hata düzeltme
*   `docs`: Sadece dokümantasyon değişikliği
*   `style`: Kod biçimlendirme (boşluk, noktalı virgül vb.)
*   `refactor`: Kod yeniden yapılandırma (davranış değişikliği yok)
*   `test`: Test ekleme veya düzeltme
*   `chore`: Bakım görevleri (bağımlılık güncelleme vb.)

**Örnekler:**
*   `feat: turkce-morfoloji-cozumleyici-eklendi`
*   `fix: motor-baslatma-hatasi-duzeltildi`
*   `docs: katki-kilavuzu-guncellendi`

---

## 4. VERİ KATKISI SÜRECİ

Veri setleri projenin en hassas bileşenidir. Ham veri dosyaları (`.csv`, `.json`, `.parquet`) asla doğrudan Git deposuna yüklenmez.

### 4.1. Veri Akış Şeması

```text
[HAM VERİ KAYNAĞI]
(HuggingFace, TDK, Mevzuat vb.)
       |
       v
+---------------------+
| YEREL İNDİRME       |
| - scripts/download.py|
+----------+----------+
           |
           v
+---------------------+
| TEMİZLEME & DOĞRULAMA|
| - scripts/clean.py   |
| - İnsan Denetimi     |
+----------+----------+
           |
           v
+---------------------+
| FORMATLAMA          |
| - JSONL / Parquet   |
| - Metadata Ekleme   |
+----------+----------+
           |
           v
+---------------------+
| DEPOLAMA            |
| - data/raw/ (GitIgnore)|
| - data/processed/   |
+---------------------+
```

> **Not:** Sadece `data/ornek_veri.jsonl` gibi küçük şema dosyaları Git'te tutulur. Büyük veri setleri için harici depolama veya indirme scriptleri kullanılır.

---

## 5. İLETİŞİM VE ONAY MEKANİZMASI

Tüm Pull Request (PR) ve Issue'lar, proje lideri **Batuhan ALGÜL** tarafından incelenir.

### 5.1. İnceleme Kriterleri

Bir PR'ın kabul edilmesi için şu koşullar aranır:
1.  ✅ Kod PEP 8 standartlarına uyuyor mu?
2.  ✅ Tip açıklamaları eksiksiz mi?
3.  ✅ Yeni özellik için birim test yazıldı mı?
4.  ✅ Dokümantasyon güncellendi mi?
5.  ✅ Commit mesajı standartlara uygun mu?

### 5.2. İletişim Kanalları

*   **Resmi Talepler:** GitHub Issues üzerinden açılmalıdır.
*   **Teknik Tartışmalar:** GitHub Discussions kullanılmalıdır.
*   **Acil Durumlar / Resmi Yazışmalar:** `batuhanalgul@proton.me` adresi üzerinden yapılmalıdır.

---

## 6. YASAL UYARI VE LİSANSLAMA

Projeye yapılan her katkı, otomatik olarak **Apache License 2.0** kapsamında lisanslanır. Katkı sağlayan kişi, telif haklarını devretmez ancak projenin ticari ve ticari olmayan kullanımına izin verir.

**Telif Hakkı Bildirimi:**
Tüm kaynak kod dosyalarının başında aşağıdaki başlık bulunmalıdır:

```python
"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: loosely coupled
Tanım: Modül Sorumluluğu
Yazar: Batuhan ALGÜL
Tarih: 2026
Lisans: Apache 2.0
"""
```

---

© 2026 Batuhan ALGÜL
*Kıdemli Geliştirici & Sistem Mimarı*
```

---
