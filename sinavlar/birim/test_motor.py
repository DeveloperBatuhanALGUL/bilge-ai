import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.cekrdek.motor import BilgeMotoru
from src.modeller.yerel_llm import YerelLLM
from src.veri_katmani.onbellek import AnlikBellek

class TestBilgeMotoru(unittest.TestCase):
    def setUp(self):
        self.model = YerelLLM(model_adi="test-model")
        self.hafiza = AnlikBellek()
        self.motor = BilgeMotoru(model=self.model, hafiza=self.hafiza)

    def test_baslat(self):
        self.assertTrue(self.motor.baslat())
        self.assertTrue(self.motor.aktif_mi)

    def test_dusun_ve_cevapla(self):
        self.motor.baslat()
        sonuc = self.motor.dusun_ve_cevapla("Merhaba", oturum_id="test")
        self.assertIn('yanit', sonuc)
        self.assertTrue(sonuc['basarili'])

if __name__ == '__main__':
    unittest.main()
