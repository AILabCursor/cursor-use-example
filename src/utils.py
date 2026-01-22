"""
Вспомогательные функции для проекта шифратора
"""

import re
import pandas as pd
from typing import List, Union


def is_numeric(value) -> bool:
    """
    Проверяет, является ли значение числовым

    Args:
        value: значение для проверки

    Returns:
        True если значение числовое, иначе False
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def extract_numbers_from_string(text: str) -> List[float]:
    """
    Извлекает числа из строки

    Args:
        text: строка для извлечения чисел

    Returns:
        список чисел
    """
    numbers = re.findall(r'-?\d+\.?\d*', text)
    return [float(num) for num in numbers if num]


def clean_numeric_string(value: str) -> str:
    """
    Очищает строку от ненужных символов для чисел

    Args:
        value: строка для очистки

    Returns:
        очищенная строка
    """
    # Удаляем все символы кроме цифр, точек и минуса
    cleaned = re.sub(r'[^\d\.\-]', '', value)
    # Убираем лишние точки
    if cleaned.count('.') > 1:
        parts = cleaned.split('.')
        cleaned = parts[0] + '.' + ''.join(parts[1:])
    return cleaned


def convert_to_numeric(value: Union[str, float, int]) -> Union[float, int]:
    """
    Преобразует значение в числовое

    Args:
        value: значение для преобразования

    Returns:
        числовое значение или исходное значение
    """
    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        # Пытаемся преобразовать строку в число
        try:
            # Сначала пробуем целое число
            if '.' not in value:
                return int(value)
            else:
                return float(value)
        except ValueError:
            # Если не получилось, возвращаем исходное значение
            return value

    return value


def validate_excel_data(data):
    """
    Валидация данных Excel

    Args:
        data: данные для валидации

    Returns:
        True если данные валидны, иначе False
    """
    if data is None:
        return False

    if isinstance(data, pd.DataFrame):
        # Проверяем, что DataFrame не пустой
        return not data.empty

    return True