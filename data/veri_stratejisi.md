```markdown
# BİLGE ULUSAL EĞİTİM VERİ SETİ STRATEJİSİ VE ŞARTNAMESİ

## 1. GİRİŞ VE AMAÇ

Bu doküman, **Bilge Ulusal Açık Kaynak Zekâ Çerçevesi** projesi kapsamında kullanılacak eğitim veri setinin toplanması, işlenmesi, sınıflandırılması ve kalite kontrol süreçlerini tanımlar. Proje, Türkçe doğal dil işleme (NLP) alanında dışa bağımlılığı kırmak amacıyla, **yüksek kaliteli, doğrulanmış ve etik** bir veri havuzu oluşturmayı hedefler.

**Proje Lideri:** Batuhan ALGÜL  
**Tarih:** Nisan 2026  
**Versiyon:** 0.1.0-alpha

---

## 2. VERİ TOPLAMA STRATEJİSİ

Bilge'nin eğitimi için kullanılacak veri setleri üç ana kaynaktan sağlanacaktır:

### 2.1. Birincil Kaynaklar (Akademik & Kurumsal İş Birlikleri)
*   **Üniversiteler:** Boğaziçi Üniversitesi, ODTÜ, İTÜ gibi kurumların NLP laboratuvarları ile iş birliği yapılarak;
    *   Akademik makale özetleri (Türkçe)
    *   Tarihi belgeler ve arşiv kayıtları
    *   Bilimsel tez veritabanları
*   **Devlet Kurumları:** TDK (Türk Dil Kurumu), TÜİK, Diyanet İşleri Başkanlığı gibi kurumlardan edinilecek resmi sözlükler, ansiklopediler ve kültürel miras verileri.

### 2.2. İkincil Kaynaklar (Açık Veri & Kamu Malı)
*   Wikipedia (Türkçe) dökümleri
*   Project Gutenberg Türkiye koleksiyonu
*   Açık erişimli hukuk metinleri (Mevzuat, Yargıtay kararları - anonimleştirilmiş)
*   Haber arşivleri (Telif hakkı süresi dolmuş veya açık lisanslı)

### 2.3. Üçüncül Kaynaklar (Topluluk Katkısı & Sentez Veri)
*   "Bilge Topluluğu" tarafından doğrulanan diyalog veri setleri
*   Büyük dil modelleri tarafından üretilip insan denetiminden geçen sentetik veri (Self-Instruct yöntemi)

---

## 3. VERİ KATEGORİZASYONU VE ETİKETLEME STANDARTLARI

Veri seti, aşağıdaki kategorilere ayrılarak etiketlenecektir. Her veri parçası için **güvenilirlik skoru (0.0 - 1.0)** atanacaktır.

| Kategori ID | Kategori Adı | Açıklama | Örnek İçerik |
| :--- | :--- | :--- | :--- |
| `CAT-01` | **Dilsel Yapı** | Gramer, imla, noktalama, morfoloji | Cümle çözümlemeleri, eş anlamlılar |
| `CAT-02` | **Kültürel Miras** | Tarih, edebiyat, folklor, mitoloji | Dede Korkut hikayeleri, Osmanlı tarihi |
| `CAT-03` | **Bilim & Teknoloji** | Fizik, kimya, biyoloji, mühendislik | Ders kitapları, bilimsel makaleler |
| `CAT-04` | **Hukuk & Mevzuat** | Anayasa, kanunlar, yönetmelikler | Resmi Gazete yayınları |
| `CAT-05` | **Sağlık & Tıp** | Anatomi, hastalıklar, tedavi yöntemleri | Tıbbi terimler sözlüğü, hasta broşürleri |
| `CAT-06` | **Etik & Felsefe** | Ahlak, değerler, düşünce okulları | Tasavvuf metinleri, felsefe eserleri |
| `CAT-07` | **Günlük Diyalog** | Sosyal etkileşim, nezaket, deyimler | Günlük konuşma kalıpları, atasözleri |

---

## 4. VERİ FORMATI VE TEKNİK ŞARTLAR

Tüm eğitim verileri, makine öğrenimi modellerine uygun standart formatlarda saklanacaktır.

### 4.1. Dosya Formatları
*   **JSONL (JSON Lines):** Her satırda bir JSON objesi içeren metin dosyası. Büyük veri setleri için önerilir.
*   **Parquet:** Sütun tabanlı depolama formatı. Hızlı okuma/yazma için kullanılır.
*   **CSV:** Basit tablolar için yedek format.

### 4.2. JSONL Şeması Örneği

```json
{
  "id": "unique-hash-123",
  "category": "CAT-02",
  "source": "TDK_Sozluk_2025",
  "content": {
    "prompt": "Merhaba Bilge, 'tevekkül' nedir?",
    "completion": "Tevekkül, bir işi yaptıktan sonra sonucunu Allah'a bırakmak, güvenmek demektir.",
    "metadata": {
      "author": "TDK",
      "year": 2025,
      "license": "CC-BY-4.0"
    }
  },
  "quality_score": 0.98,
  "language": "tr",
  "tags": ["din", "kavram", "sozluk"]
}
```

### 4.3. Kalite Kontrol Kriterleri
1.  **Dil Doğruluğu:** Türkçe imla ve gramer kurallarına %100 uyum.
2.  **Tarafsızlık:** Siyasi, dini veya ideolojik önyargı içermeyen nötr dil.
3.  **Güncellik:** Bilimsel ve hukuki verilerin güncel mevzuata/makalelere göre doğrulanması.
4.  **Tekrarsızlık:** Deduplication (tekrar eden verilerin) temizlenmesi.

---

## 5. VERİ GİZLİLİĞİ VE ETİK İLKELER

*   **Kişisel Veri Yok:** Eğitim setinde hiçbir şekilde TCKN, adres, telefon numarası gibi kişisel veriler bulunmamalıdır.
*   **Telif Hakkı:** Sadece açık kaynak, kamu malı veya izin alınmış içerikler kullanılacaktır.
*   **Şeffaflık:** Veri setinin kaynağı her zaman `metadata` alanında belirtilecektir.

---

## 6. AKADEMİK İŞ BİRLİĞİ TALEBİ (BOĞAZİÇİ ÜNİVERSİTESİ VB.)

Bu proje kapsamında, aşağıdaki konularda akademik destek ve veri paylaşımı talebimiz bulunmaktadır:

1.  **Türkçe Morfolojik Analiz Veri Setleri:** Kök-ek ayrımı için doğrulanmış veri havuzları.
2.  **Anlamsal Benzerlik (Semantic Similarity) Kıyaslama Setleri:** Türkçe cümle çiftleri için insan tarafından etiketlenmiş veri.
3.  **Zehirli İçerik Tespiti (Toxicity Detection):** Nefret söylemi ve zararlı içerik örnekleri (güvenlik filtreleri için).
4.  **Hesaplama Kaynağı:** Büyük ölçekli model eğitimi için GPU kümesi erişimi (opsiyonel).

**İletişim:**  
Batuhan ALGÜL  
Kıdemli Geliştirici & Proje Mimarı  
batuhanalgul@proton.me 
https://github.com/DeveloperBatuhanALGUL/bilge-ai

---

© 2026 Batuhan ALGÜL
```

Commit message:
```
data: veri_stratejisi.md eklendi | data: Add data strategy and specification document
```

Extended description:
```
Eğitim veri setinin nasıl toplanacağı, kategorize edileceği ve formatlanacağı detaylıca açıklandı. Akademik iş birlikleri için resmi şartname niteliğindedir.

Detailed specification for training dataset collection, categorization, and formatting. Serves as an official requirement document for academic collaborations.
```

---

# 🔹 ADIM 2: `.gitignore` Dosyasını Güncelle (Veri Güvenliği İçin)

Ham veri dosyaları (özellikle büyük CSV/JSON dosyaları) GitHub'a yüklenmemelidir. Hem depo şişer hem de hassas veri sızabilir.

`.gitignore` dosyasını düzenle modunda aç ve en altına şunu ekle:

```text
# ========================================================================
# VERİ DOSYALARI (DATA FILES)
# Ham veri setleri GitHub'a yüklenmez. Sadece şema ve örnekler kalır.
# ========================================================================
data/raw/
data/processed/large_*
*.parquet
*.csv
*.jsonl
!data/veri_stratejisi.md
!data/ornek_veri.jsonl
```

> **Not:** `!data/veri_stratejisi.md` ve `!data/ornek_veri.jsonl` satırları, bu iki dosyanın Git'e eklenmesine izin verir (istisna). Diğer tüm büyük veri dosyaları engellenir.

Commit message:
```
chore: .gitignore güncellendi, veri dosyaları hariç tutuldu | chore: Update .gitignore to exclude raw data files
```

---

# 🔹 ADIM 3: Örnek Veri Dosyası Oluştur (`data/ornek_veri.jsonl`)

Akademisyenlere veya geliştiricilere "Veriniz bu formatta olmalı" demek için küçük bir örnek dosya oluşturalım.

Dosya adı: `data/ornek_veri.jsonl`

İçerik:

```json
{"id": "ex-001", "category": "CAT-01", "source": "Manuel", "content": {"prompt": "Elma kelimesinin çoğulu nedir?", "completion": "Elmalar."}, "quality_score": 1.0, "language": "tr", "tags": ["dilbilgisi", "cogul"]}
{"id": "ex-002", "category": "CAT-02", "source": "Halk_Edebiyati", "content": {"prompt": "Bir taşla iki kuş vurmak ne demek?", "completion": "Tek bir hareketle iki farklı fayda sağlamak anlamında kullanılan bir deyimdir."}, "quality_score": 0.95, "language": "tr", "tags": ["deyim", "folklor"]}
{"id": "ex-003", "category": "CAT-04", "source": "Resmi_Gazete", "content": {"prompt": "Anayasa'nın 2. maddesi nedir?", "completion": "Türkiye Cumhuriyeti, toplumun huzuru, milli dayanışma ve adalet anlayışı içinde, insan haklarına saygılı, Atatürk milliyetçiliğine bağlı, başlangıçta belirtilen temel ilkelere dayanan, demokratik, laik ve sosyal bir hukuk Devletidir."}, "quality_score": 1.0, "language": "tr", "tags": ["hukuk", "anayasa"]}
```

Commit message:
```
data: ornek_veri.jsonl eklendi | data: Add sample training data file
```

---
