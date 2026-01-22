## Cursor Use Example — Excel Clipboard Masker (мини‑проект)

Этот репозиторий — **учебный пример того, как можно работать с Cursor (и LLM) при разработке проекта**: от постановки задачи и промптов до реализации кода и тестов.

Проект реализует простой сценарий практики:
- пользователь копирует диапазон из Excel (в буфер обмена обычно попадает TSV: `\t` между колонками, `\n` между строками)
- фоновый процесс читает буфер, находит числа и **маскирует суммы по диапазонам**
- пользователь вставляет — вставляются уже “безопасные” значения

Важно: здесь используется **polling (опрос буфера)**, без системных хуков.

## Быстрые ссылки

- **Шаблон кейса/чата**: [`CHAT_USE_CASE_TEMPLATE.md`](CHAT_USE_CASE_TEMPLATE.md)
- **Папка с карточками‑скриншотами**: [`cards-screenshots/`](cards-screenshots/)

## Карточки правил (из `cards-screenshots/`)

Ниже — карточки, которые использовались в промптах в `CHAT_USE_CASE_TEMPLATE.md`:

- [01 — “Используй роль”](cards-screenshots/card01-role.png)
- [02 — “Сформулируй цель”](cards-screenshots/card02-goal.png)
- [03 — “Определи уровень детализации”](cards-screenshots/card03-detail-level.png)
- [04 — “Зафиксируй формат ответа”](cards-screenshots/card04-format-response.png)
- [05 — “Выбери файлы”](cards-screenshots/card05-select-files.png)
- [06 — “Ограничь область”](cards-screenshots/card06-limit-scope.png)
- [09 — “Пошаговое рассуждение”](cards-screenshots/card09-stepwise-reasoning.png)
- [10 — “Проверь гипотезы”](cards-screenshots/card10-check-hypotheses.png)
- [11 — “Сравни альтернативы”](cards-screenshots/card11-compare-alternatives.png)
- [12 — “Объясняй допущения”](cards-screenshots/card12-explain-assumptions.png)
- [15 — “Предложи решение”](cards-screenshots/card15-suggest-solution.png)
- [16 — “Напиши код”](cards-screenshots/card16-write-code.png)
- [18 — “Сгенерируй тесты”](cards-screenshots/card18-generate-tests.png)

## Что внутри (структура)

- `src/cipher_engine.py`: алгоритм маскирования чисел по диапазонам (до 10k / до 100k / >100k)
- `src/clipboard_handler.py`: polling буфера, эвристика “похоже на таблицу”, маскирование и **anti-loop по MD5**
- `src/daemon.py`: запуск “как демон” (лог + корректная остановка по Ctrl+C)
- `src/main.py`: CLI‑входная точка
- `tests/`: минимальные unit‑тесты

## Установка

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск

### Интерактивный режим (мониторинг буфера)

```bash
python src/main.py
```

Скопируйте диапазон в Excel (Ctrl+C) → вставьте куда‑нибудь (Ctrl+V) и проверьте, что числа подменились.

### Режим “демона” (лог + остановка Ctrl+C)

```bash
python src/main.py --daemon
```

Логи пишутся в `clipboard_daemon.log` (и в stdout).

## Тесты

Проект содержит тесты на `unittest`:

```bash
python -m unittest discover -s tests -v
```

Также в `src/main.py` есть флаг:

```bash
python src/main.py --test
```

## Как это использовать как пример работы с Cursor

Рекомендуемый сценарий:
- берёте **шаблон** [`CHAT_USE_CASE_TEMPLATE.md`](CHAT_USE_CASE_TEMPLATE.md)
- идёте **по этапам** (цель → разбиение → алгоритм → код → anti-loop → демон → тесты)
- в каждом этапе “подключаете” нужные **карточки** (см. список выше), чтобы промпты были короткими, точными и повторяемыми

Итог: вы получаете воспроизводимый процесс — **не просто “написать код”, а выстроить инженерный поток с LLM** (контекст, ограничения, выбор файлов, тесты, фиксация результата).

