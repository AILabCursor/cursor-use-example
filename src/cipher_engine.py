"""
Движок шифрования для Excel файлов
Содержит алгоритмы маскирования данных в зависимости от суммы
"""

import random
import math


def mask_value(value, threshold=10000):
    """
    Маскирует значение в зависимости от порога

    Args:
        value: исходное числовое значение
        threshold: порог для определения диапазона

    Returns:
        замаскированное значение
    """
    if not isinstance(value, (int, float)) or value <= 0:
        return value

    # Определяем диапазон и соответствующий коэффициент
    if value <= 10000:
        k_min, k_max, round_digits = 0.70, 1.30, 1
    elif value <= 100000:
        k_min, k_max, round_digits = 0.85, 1.15, 10
    else:
        k_min, k_max, round_digits = 0.90, 1.10, 100

    # Генерируем случайный коэффициент
    k = random.uniform(k_min, k_max)

    # Применяем коэффициент и округляем
    masked_value = value * k

    # Округляем до нужного числа знаков
    if round_digits == 1:
        return round(masked_value, 0)
    elif round_digits == 10:
        return round(masked_value / 10) * 10
    else:  # round_digits == 100
        return round(masked_value / 100) * 100


def mask_range_values(values):
    """
    Маскирует диапазон значений

    Args:
        values: список числовых значений

    Returns:
        список замаскированных значений
    """
    return [mask_value(value) for value in values]


def get_range_threshold(value):
    """
    Определяет порог для значения

    Args:
        value: числовое значение

    Returns:
        порог (строка)
    """
    if value <= 10000:
        return "до 10 000"
    elif value <= 100000:
        return "до 100 000"
    else:
        return "более 100 000"


# Тестовые функции
def test_mask_value():
    """Тестирование функции маскирования"""
    test_values = [5000, 50000, 150000]

    print("Тест маскирования значений:")
    for value in test_values:
        masked = mask_value(value)
        threshold = get_range_threshold(value)
        print(f"Исходное: {value:>8} -> Маскированное: {masked:>8} (диапазон: {threshold})")


if __name__ == "__main__":
    test_mask_value()