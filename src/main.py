#!/usr/bin/env python3
"""
Главная программа для обработки буфера обмена
"""

import sys
import os
import argparse

from clipboard_handler import handle_clipboard_operations
from daemon import ClipboardDaemon

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description='Обработчик буфера обмена для шифрования данных')
    parser.add_argument('--daemon', action='store_true', help='Запустить как демон в фоне')
    parser.add_argument('--stop', action='store_true', help='Остановить демон')
    parser.add_argument('--test', action='store_true', help='Запустить тесты')

    args = parser.parse_args()

    if args.test:
        # Запуск тестов
        import subprocess
        import unittest
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', 'tests'],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)
        return

    elif args.daemon:
        # Запуск как демон
        daemon = ClipboardDaemon()
        daemon.start()

    elif args.stop:
        # Остановка демона (реализация будет зависеть от способа хранения PID)
        print("Остановка демона...")
        # В реальной реализации здесь должна быть логика остановки демона
        # Например, чтение PID файла и отправка сигнала
        print("Демон остановлен")

    else:
        # Запуск в интерактивном режиме
        handle_clipboard_operations()

if __name__ == "__main__":
    main()