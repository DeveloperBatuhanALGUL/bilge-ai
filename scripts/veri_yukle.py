"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Betik: Örnek Veri Yükleme
Tanım: Örnek belgeleri Vektör Ambarına (ChromaDB) ekler.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from veri_katmani.chroma_impl import ChromaAmbar

def ornek_verileri_yukle():
    ambar = ChromaAmbar()
    
    if not ambar.baslat():
        print("Ambar başlatılamadı.")
        return

    # Örnek Belgeler (veri_stratejisi.md'den esinlenilmiştir)
    belgeler = [
        {
            "id": "doc-001",
            "metin": "Tevekkül, bir işi yaptıktan sonra sonucunu Allah'a bırakmak, güvenmek demektir.",
            "metadata": {"kategori": "CAT-01", "kaynak": "TDK"}
        },
        {
            "id": "doc-002",
            "metin": "Bir taşla iki kuş vurmak deyimi, tek bir hareketle iki farklı fayda sağlamak anlamında kullanılır.",
            "metadata": {"kategori": "CAT-02", "kaynak": "Halk_Edebiyati"}
        },
        {
            "id": "doc-003",
            "metin": "Türkiye Cumhuriyeti, toplumun huzuru, milli dayanışma ve adalet anlayışı içinde, insan haklarına saygılı, Atatürk milliyetçiliğine bağlı, demokratik, laik ve sosyal bir hukuk Devletidir.",
            "metadata": {"kategori": "CAT-04", "kaynak": "Anayasa"}
        }
    ]

    if ambar.belge_ekle(belgeler):
        print("✅ Örnek veriler başarıyla vektör ambarına eklendi.")
    else:
        print("❌ Veri eklenirken hata oluştu.")
        
    ambar.kapat()

if __name__ == "__main__":
    ornek_verileri_yukle()
