"""
Модульные тесты для обработчика буфера обмена
"""

import unittest
import sys
import os
import hashlib


from src.clipboard_handler import ClipboardHandler


class TestClipboardHandler(unittest.TestCase):
    """Тесты для обработчика буфера обмена"""

    def setUp(self):
        """Подготовка тестов"""
        self.handler = ClipboardHandler(polling_interval=100)

    def test_is_table_like(self):
        """Тест определения таблицы"""
        # Тест 1: Таблица с табуляциями
        table_text = "A\tB\tC\n1000\t2000\t3000\n4000\t5000\t6000"
        self.assertTrue(self.handler.is_table_like(table_text))

        # Тест 2: Не таблица (нет табуляций)
        non_table_text = "Просто текст без табуляций"
        self.assertFalse(self.handler.is_table_like(non_table_text))

        # Тест 3: Не таблица (одна строка)
        single_line = "A\tB\tC"
        self.assertFalse(self.handler.is_table_like(single_line))

        # Тест 4: Пустая строка
        self.assertFalse(self.handler.is_table_like(""))

    def test_extract_numbers_from_text(self):
        """Тест извлечения чисел"""
        table_text = "A\tB\tC\n1000\t2000\t3000\n4000\t5000\t6000"
        numbers = self.handler.extract_numbers_from_text(table_text)
        expected = [1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0]
        self.assertEqual(numbers, expected)

    def test_calculate_content_hash(self):
        """Тест вычисления хэша содержимого"""
        text1 = "Привет мир!"
        text2 = "Привет мир!"
        text3 = "Привет МИР!"

        hash1 = self.handler.calculate_content_hash(text1)
        hash2 = self.handler.calculate_content_hash(text2)
        hash3 = self.handler.calculate_content_hash(text3)

        # Хэши одинаковых строк должны совпадать
        self.assertEqual(hash1, hash2)
        # Хэши разных строк должны отличаться
        self.assertNotEqual(hash1, hash3)

    def test_should_process_content(self):
        """Тест проверки необходимости обработки содержимого"""
        content = "Тестовая строка для хэширования"

        # Первый вызов должен вернуть True (содержимое новое)
        result1 = self.handler.should_process_content(content)
        self.assertTrue(result1)

        # Второй вызов с тем же содержимым должен вернуть False (цикл)
        result2 = self.handler.should_process_content(content)
        self.assertFalse(result2)

        # Вызов с новым содержимым должен вернуть True
        new_content = "Новая строка"
        result3 = self.handler.should_process_content(new_content)
        self.assertTrue(result3)


if __name__ == '__main__':
    unittest.main()