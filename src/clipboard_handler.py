"""
Обработчик буфера обмена для автоматического шифрования данных
"""

import pyperclip
import time
import re
import logging
import sys
import os
import hashlib


from cipher_engine import mask_range_values, mask_value
from utils import is_numeric

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ClipboardHandler:
    """Класс для обработки буфера обмена с защитой от циклов"""

    def __init__(self, polling_interval=1000):
        """
        Инициализация обработчика буфера

        Args:
            polling_interval: интервал опроса буфера в миллисекундах
        """
        self.polling_interval = polling_interval
        self.last_clipboard_content = ""
        self.is_running = False
        self.last_clipboard_hash = None
        self.current_clipboard_hash = None

    def calculate_content_hash(self, content):
        """
        Вычисляет MD5 хэш содержимого для защиты от циклов

        Args:
            content: содержимое для хэширования

        Returns:
            MD5 хэш содержимого
        """
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def is_table_like(self, text):
        """
        Определяет, похож ли текст на таблицу

        Args:
            text: текст для анализа

        Returns:
            True если текст похож на таблицу, иначе False
        """
        if not text or not isinstance(text, str):
            return False

        # Проверяем наличие строк и табуляций
        lines = text.strip().split('\n')
        if len(lines) < 2:
            return False

        # Проверяем наличие табуляций в строках
        has_tabs = any('\t' in line for line in lines)
        if not has_tabs:
            return False

        # Проверяем наличие чисел
        has_numbers = any(is_numeric(word) for line in lines for word in line.split('\t'))
        if not has_numbers:
            return False

        return True

    def extract_numbers_from_text(self, text):
        """
        Извлекает числа из текста

        Args:
            text: текст для извлечения чисел

        Returns:
            список чисел
        """
        # Разбиваем текст на строки и потом на слова
        numbers = []
        lines = text.strip().split('\n')

        for line in lines:
            words = line.split('\t')
            for word in words:
                # Убираем пробелы и проверяем, является ли слово числом
                clean_word = word.strip()
                if is_numeric(clean_word):
                    try:
                        numbers.append(float(clean_word))
                    except ValueError:
                        continue

        return numbers

    def mask_table_data(self, text):
        """
        Маскирует числовые данные в таблице

        Args:
            text: текст таблицы

        Returns:
            маскированный текст таблицы
        """
        if not text or not isinstance(text, str):
            return text

        lines = text.strip().split('\n')
        masked_lines = []

        for line in lines:
            words = line.split('\t')
            masked_words = []

            for word in words:
                clean_word = word.strip()
                if is_numeric(clean_word):
                    try:
                        # Преобразуем в число и маскируем
                        number = float(clean_word)
                        # Здесь будет вызов функции маскирования
                        masked_number = mask_value(number)  # предполагаем, что есть такая функция
                        masked_words.append(str(masked_number))
                    except ValueError:
                        masked_words.append(word)
                else:
                    masked_words.append(word)

            masked_lines.append('\t'.join(masked_words))

        return '\n'.join(masked_lines)

    def should_process_content(self, current_content):
        """
        Проверяет, нужно ли обрабатывать содержимое с защитой от циклов

        Args:
            current_content: текущее содержимое

        Returns:
            True если содержимое нужно обрабатывать
        """
        # Вычисляем хэш текущего содержимого
        current_hash = self.calculate_content_hash(current_content)

        # Если хэши совпадают, содержимое не изменилось, пропускаем обработку
        if current_hash == self.last_clipboard_hash:
            logger.info("Содержимое буфера не изменилось, пропускаем обработку")
            return False

        # Обновляем хэш для следующей проверки
        self.last_clipboard_hash = current_hash
        return True

    def process_content(self, content):
        """
        Обрабатывает содержимое с защитой от циклов

        Args:
            content: содержимое для обработки

        Returns:
            обработанное содержимое
        """
        if not content:
            return content

        # Проверяем, нужно ли обрабатывать содержимое
        if not self.should_process_content(content):
            return content

        # Проверяем, похоже ли содержимое на таблицу
        if self.is_table_like(content):
            logger.info("Обнаружена таблица в буфере обмена")
            numbers = self.extract_numbers_from_text(content)

            if numbers:
                logger.info(f"Найдено чисел: {len(numbers)}")
                # Маскируем данные
                masked_content = self.mask_table_data(content)
                return masked_content
            else:
                logger.info("В таблице не найдено числовых значений")
        else:
            logger.info("Содержимое буфера не похоже на таблицу")

        return content

    def start_monitoring(self):
        """
        Запускает мониторинг буфера обмена
        """
        self.is_running = True
        logger.info("Запуск мониторинга буфера обмена...")

        try:
            while self.is_running:
                # Читаем содержимое буфера
                current_content = pyperclip.paste()

                # Проверяем, изменилось ли содержимое
                if current_content != self.last_clipboard_content:
                    logger.info("Обнаружено изменение в буфере обмена")
                    self.last_clipboard_content = current_content

                    # Обрабатываем содержимое с защитой от циклов
                    processed_content = self.process_content(current_content)

                    # Записываем обратно в буфер, если содержимое изменилось
                    if processed_content != current_content:
                        pyperclip.copy(processed_content)
                        logger.info("Содержимое буфера обновлено с маскированными данными")

                # Ждем перед следующей проверкой
                time.sleep(self.polling_interval / 1000.0)

        except KeyboardInterrupt:
            logger.info("Остановка мониторинга буфера обмена")
        except Exception as e:
            logger.error(f"Ошибка в мониторинге буфера: {e}")

    def stop_monitoring(self):
        """
        Останавливает мониторинг буфера обмена
        """
        self.is_running = False
        logger.info("Мониторинг буфера обмена остановлен")


def handle_clipboard_operations():
    """
    Обработка операций с буфером обмена
    """
    handler = ClipboardHandler()

    print("Запуск мониторинга буфера обмена...")
    print("Нажмите Ctrl+C для остановки")

    try:
        handler.start_monitoring()
    except KeyboardInterrupt:
        print("\nОстановка...")
        handler.stop_monitoring()

    print("Мониторинг завершен")


if __name__ == "__main__":
    # Запуск мониторинга
    handle_clipboard_operations()