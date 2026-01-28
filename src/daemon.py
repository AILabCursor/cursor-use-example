"""
Демон для мониторинга буфера обмена в фоне
"""

import sys
import os
import time
import signal
import logging
from clipboard_handler import ClipboardHandler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clipboard_daemon.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ClipboardDaemon:
    """Демон для мониторинга буфера обмена"""

    def __init__(self):
        self.handler = ClipboardHandler()
        self.running = False

    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректной остановки"""
        logger.info(f"Получен сигнал {signum}, остановка демона...")
        self.running = False
        self.handler.stop_monitoring()
        logger.info("Демон остановлен")
        sys.exit(0)

    def start(self):
        """Запуск демона"""
        # Регистрируем обработчики сигналов
        signal.signal(signal.SIGINT, self.signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, self.signal_handler)  # Завершение системы

        self.running = True
        logger.info("Daemon started")

        try:
            self.handler.start_monitoring()
        except KeyboardInterrupt:
            logger.info("Демон остановлен пользователем")
            self.handler.stop_monitoring()
        except Exception as e:
            logger.error(f"Ошибка в демоне: {e}")
            self.handler.stop_monitoring()


if __name__ == "__main__":
    daemon = ClipboardDaemon()
    daemon.start()