# Документация Steam Gamification Research

> Согласованный комплект · 22.11.2026. Разместить содержимое этой папки в `<корень проекта>/docs/`.

## С чего начать

1. [`STEAM_GAMIFICATION_RESEARCH_1.0.md`](STEAM_GAMIFICATION_RESEARCH_1.0.md) — краткий паспорт и актуальное состояние.
2. [`RESEARCH_CONTEXT.md`](RESEARCH_CONTEXT.md) — научная постановка и принятые ограничения.
3. [`DATA_COLLECTION_METHODOLOGY.md`](DATA_COLLECTION_METHODOLOGY.md) — методология The Game Census, Steam Store API и DuckDB.
4. [`DATA_LINEAGE.md`](DATA_LINEAGE.md) — карта происхождения таблиц и 11 CSV.
5. [`DATABASE_PROFILE.md`](DATABASE_PROFILE.md) — полное описание схемы и SQL VIEW.
6. [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) — поля, метрики и формулы.
7. [`VISUALIZATION_CATALOG.md`](VISUALIZATION_CATALOG.md) — перечень 20 рисунков.

## Решение о переконфигурации старых материалов

- Старый **первоначальный паспорт** слишком подробно дублировал схему DuckDB, каталог CSV и графиков. Оригинал сохраняется в `archive/`, а одноимённый актуальный файл превращён в краткую точку входа с ссылками.
- **DATABASE_PROFILE** оставлен подробным: это единственное место для фактических SQL определений VIEW и полного списка колонок. Обновлён способ подключения через `project_config.py`.
- **RESEARCH_CONTEXT** отражает научную постановку, а не техническую инструкцию загрузки.
- **DATA_COLLECTION_METHODOLOGY** описывает исторически выполненные запросы и запись, отличая их от предлагаемых улучшений.
- **DATA_LINEAGE**, **DATA_DICTIONARY**, **VISUALIZATION_CATALOG** выделены отдельно, чтобы исключить повторение и облегчить обновления.

## Структура папки

```text
docs/
├── README.md
├── STEAM_GAMIFICATION_RESEARCH_1.0.md
├── RESEARCH_CONTEXT.md
├── DATA_COLLECTION_METHODOLOGY.md
├── DATA_LINEAGE.md
├── DATABASE_PROFILE.md
├── DATA_DICTIONARY.md
├── VISUALIZATION_CATALOG.md
└── archive/
    └── STEAM_GAMIFICATION_RESEARCH_1.0_original.md
```

Документы не заменяют исходные данные, `project_config.py`, Jupyter Notebook и скрипты преобразования. Бинарный DuckDB-файл не включён в архив документов.
