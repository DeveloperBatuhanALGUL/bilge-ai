"""
Bilge Ulusal Açık Kaynak Zekâ Çerçevesi
Modül: Morfolojik Taban ve Kurallar
Tanım: Türkçe ünlü uyumu, ünsüz benzeşmesi ve kök-ek ilişkilerini yönetir.
Yazar: Batuhan ALGÜL
Tarih: 2026
"""
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class KelimeKoku:
    """Bir kelimenin kök temsilini tutar."""
    yuzey: str      # Görünen form (örn: "ev")
    kok: str        # Gerçek kök (örn: "ev")
    tip: str        # "isim", "fiil", "sifat" vb.
    ozellikler: List[str] # ["ozel_isim", "yabanci_kokenli"] vb.

@dataclass
class EkBilgisi:
    """Eklerin özelliklerini tutar."""
    yuzey: str      # Görünen ek (örn: "ler")
    tur: str        # "cogul", "tamlayan", "simdiki_zaman" vb.
    on_ek_mi: bool  # Kökten önce mi geliyor? (Genelde hayır)
    ses_olayi: str  # "yumsama", "dusmesi", "kaynastirma" vb.

class MorfolojiTabani:
    """
    Türkçe morfolojik kuralları ve sözlük verisini sağlayan singleton sınıf.
    """
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MorfolojiTabani, cls).__new__(cls)
            cls._instance._init_data()
        return cls._instance

    def _init_data(self):
        # --- TEMEL KÖKLER (Örnek Veri Seti - Genişletilebilir) ---
        self.kokler = {
            "ev": KelimeKoku(yuzey="ev", kok="ev", tip="isim", ozellikler=[]),
            "araba": KelimeKoku(yuzey="araba", kok="araba", tip="isim", ozellikler=[]),
            "git": KelimeKoku(yuzey="git", kok="git", tip="fiil", ozellikler=[]),
            "gel": KelimeKoku(yuzey="gel", kok="gel", tip="fiil", ozellikler=[]),
            "Türk": KelimeKoku(yuzey="Türk", kok="türk", tip="isim", ozellikler=["ozel"]),
            "bilgisayar": KelimeKoku(yuzey="bilgisayar", kok="bilgisayar", tip="isim", ozellikler=["bilesik"]),
        }

        # --- EKLER VE BAĞLANMA KURALLARI ---
        self.ekler = {
            # İsim Çekim Ekleri
            "lar": EkBilgisi(yuzey="lar", tur="cogul", on_ek_mi=False, ses_olayi="none"),
            "ler": EkBilgisi(yuzey="ler", tur="cogul", on_ek_mi=False, ses_olayi="none"),
            "ın": EkBilgisi(yuzey="ın", tur="tamlayan", on_ek_mi=False, ses_olayi="unlu_uyumu"),
            "in": EkBilgisi(yuzey="in", tur="tamlayan", on_ek_mi=False, ses_olayi="unlu_uyumu"),
            "un": EkBilgisi(yuzey="un", tur="tamlayan", on_ek_mi=False, ses_olayi="unlu_uyumu"),
            "ün": EkBilgisi(yuzey="ün", tur="tamlayan", on_ek_mi=False, ses_olayi="unlu_uyumu"),
            
            # Fiil Çekim Ekleri
            "iyor": EkBilgisi(yuzey="iyor", tur="simdiki_zaman", on_ek_mi=False, ses_olayi="kaynastirma"),
            "di": EkBilgisi(yuzey="di", tur="gecmis_zaman", on_ek_mi=False, ses_olayi="unlu_uyumu"),
            
            # Kişi Ekleri
            "im": EkBilgisi(yuzey="im", tur="benlik", on_ek_mi=False, ses_olayi="unlu_uyumu"),
        }

    @staticmethod
    def son_unlu(kelime: str) -> Optional[str]:
        """Kelimenin son ünlüsünü bulur."""
        unluler = "aeıioöuü"
        for harf in reversed(kelime.lower()):
            if harf in unluler:
                return harf
        return None

    @staticmethod
    def unlu_uyumu_4_lu(son_unlu: str) -> Dict[str, str]:
        """
        Büyük Ünlü Uyumu'na göre ek varyantlarını belirler.
        a, ı -> kalın düz (a, ı)
        o, u -> kalın yuvarlak (o, u) -> Genellikle 'a' veya 'u' alır
        e, i -> ince düz (e, i)
        ö, ü -> ince yuvarlak (ö, ü) -> Genellikle 'e' veya 'ü' alır
        """
        if not son_unlu:
            return {}
        
        # Basitleştirilmiş 4'lü uyum haritası (Tamlayan, Çokluk vb. için)
        uyum_map = {
            'a': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
            'ı': {'kalin_duz': 'ı', 'kalin_yuvarlak': 'u', 'ince_duz': 'i', 'ince_yuvarlak': 'ü'},
            'o': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
            'u': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
            'e': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
            'i': {'kalin_duz': 'ı', 'kalin_yuvarlak': 'u', 'ince_duz': 'i', 'ince_yuvarlak': 'ü'},
            'ö': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
            'ü': {'kalin_duz': 'a', 'kalin_yuvarlak': 'u', 'ince_duz': 'e', 'ince_yuvarlak': 'ü'},
        }
        return uyum_map.get(son_unlu, {})

    def kok_bul(self, yuzey_kok: str) -> Optional[KelimeKoku]:
        """Sözlükten kök bilgilerini getirir."""
        return self.kokler.get(yuzey_kok.lower())

    def ek_bul(self, yuzey_ek: str) -> Optional[EkBilgisi]:
        """Sözlükten ek bilgilerini getirir."""
        return self.ekler.get(yuzey_ek.lower())
