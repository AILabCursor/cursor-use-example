"""
Модульные тесты для шифрования
"""

import unittest
from src.cipher_engine import mask_value, get_range_threshold
from src.utils import is_numeric



class TestCipherEngine(unittest.TestCase):
    """Тесты для движка шифрования"""

    def test_mask_value_range_1(self):
        """Тест маскирования для диапазона до 10 000"""
        value = 5000
        result = mask_value(value)

        # Проверяем, что результат находится в допустимом диапазоне
        self.assertTrue(isinstance(result, (int, float)))
        self.assertGreaterEqual(result, 5000 * 0.70)
        self.assertLessEqual(result, 5000 * 1.30)

    def test_mask_value_range_2(self):
        """Тест маскирования для диапазона до 100 000"""
        value = 50000
        result = mask_value(value)

        # Проверяем, что результат находится в допустимом диапазоне
        self.assertTrue(isinstance(result, (int, float)))
        self.assertGreaterEqual(result, 50000 * 0.85)
        self.assertLessEqual(result, 50000 * 1.15)

    def test_mask_value_range_3(self):
        """Тест маскирования для диапазона более 100 000"""
        value = 150000
        result = mask_value(value)

        # Проверяем, что результат находится в допустимом диапазоне
        self.assertTrue(isinstance(result, (int, float)))
        self.assertGreaterEqual(result, 150000 * 0.90)
        self.assertLessEqual(result, 150000 * 1.10)

    def test_get_range_threshold(self):
        """Тест определения диапазона"""
        self.assertEqual(get_range_threshold(5000), "до 10 000")
        self.assertEqual(get_range_threshold(50000), "до 100 000")
        self.assertEqual(get_range_threshold(150000), "более 100 000")

    def test_is_numeric(self):
        """Тест проверки числовых значений"""
        self.assertTrue(is_numeric("123"))
        self.assertTrue(is_numeric("123.45"))
        self.assertTrue(is_numeric(123))
        self.assertTrue(is_numeric(123.45))
        self.assertFalse(is_numeric("abc"))
        self.assertFalse(is_numeric("123abc"))


if __name__ == '__main__':
    unittest.main()