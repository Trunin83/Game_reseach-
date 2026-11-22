# DATA LINEAGE — происхождение и преобразования данных

> Версия 1.0 · 22.11.2026. Карта основана на фактических именах файлов, SQL VIEW и ячейках `Attestation - Trunin(1).ipynb`. Связи отражают логику вычислений, а не формальные ограничения FOREIGN KEY.

## 1. Поток данных

```text
The Game Census (четыре CSV в data/raw)
    ├─ games-index.csv ───────────────► games ──────────┐
    ├─ ccu-daily-top2000.csv ─────────► ccu_daily ──────┼──► VIEW активности
    ├─ health-tiers.csv ──────────────► health          │
    └─ sales-calibration.csv ─────────► sales           │
                                                        │
Steam Store API appdetails (appids, l=english, cc=us)   │
    └─ проверка + транзакционная запись                 │
         ├─ steam_app_details ──────────────────────────┤
         ├─ steam_app_genres ───────────────────────────┤
         └─ steam_app_categories ───────────────────────┘
                         │
                         ▼
            steam_games_analytics / vw_*
                         │
           ├─ рейтинг 2000 / TOP-100
           ├─ жанровые частоты, пары, Lift
           └─ категории: частоты, пары, Lift
                         │
                         ▼
          11 CSV в data/processed → 20 PNG reports/figures
```

## 2. Физические источники

| Физическая таблица | Источник | Количество строк в срезе | Гранулярность |
|---|---|---:|---|
| `games` | `games-index.csv` | 84 843 | приложение |
| `ccu_daily` | `ccu-daily-top2000.csv` | 189 405 | приложение-дата |
| `health` | `health-tiers.csv` | 84 844 | приложение |
| `sales` | `sales-calibration.csv` | 647 | приложение |
| `steam_app_details` | `appdetails` | 2 000 | приложение |
| `steam_app_genres` | массив `genres` API | 5 677 | приложение-жанр |
| `steam_app_categories` | массив `categories` API | 20 689 | приложение-категория |

Числа описывают конкретный экспорт, не «вечные» размеры БД.

## 3. Представления и SQL-источники

| VIEW | Зависит от | Оговорка |
|---|---|---|
| `vw_game_activity` | `ccu_daily` LEFT JOIN `games` | Среднее и медиана дневных максимумов |
| `vw_game_analytics` | `vw_game_activity` LEFT JOIN `steam_app_details` | Берёт часть метаданных API |
| `steam_games_analytics` | `steam_app_details` INNER JOIN агрегация `ccu_daily`; LEFT JOIN агрегаты жанров/категорий | Пропускает приложения без CCU |
| `review_games` | временный Python DataFrame через `pandas_scan()` | Не считать переносимым VIEW |

Определения SQL в полном виде находятся в `DATABASE_PROFILE.md` и исходном `database_views.csv`.

## 4. Выходные CSV

| Выход `data/processed` | Единица записи | Основные предшественники |
|---|---|---|
| `steam_games_ranking.csv` | игра | `steam_games_analytics`, оконные ранги |
| `steam_top100.csv` | игра из TOP-100 | рейтинг, правило сортировки ноутбука |
| `steam_genre_popularity.csv` | жанр | `steam_app_genres`, активность, TOP-100 |
| `steam_genre_pairs.csv` | жанровая пара | `steam_app_genres` |
| `steam_genre_pairs_popularity.csv` | жанровая пара | жанровые пары + аналитика CCU |
| `steam_genre_lift_all.csv` | жанровая пара | парные частоты + частоты отдельных жанров, N=2000 |
| `steam_genre_lift_filtered.csv` | жанровая пара | предыдущий файл, пороги n>=20 |
| `steam_genre_lift_matrix.csv` | жанровая пара в формате матрицы | Lift по основным жанрам |
| `steam_category_frequency.csv` | категория | `steam_app_categories` |
| `steam_category_pairs_frequency.csv` | категория-категория | `steam_app_categories` |
| `steam_category_pairs_lift.csv` | категория-категория | частоты отдельных категорий и пар, N=2000 |

Каждый CSV должен пересчитываться из одного зафиксированного снимка DuckDB. Даты генерации каждого файла и Git-хеш конкретного варианта ноутбука пока не документированы.

## 5. Единая схема контроля происхождения новых данных

Для будущих таблиц `Game Profile 1.0` и разметки 120 приёмов рекомендуемые поля происхождения: `source_system`, `source_url`, `source_app_id`, `retrieved_at_utc`, `data_snapshot_id`, `transformation_version`, `codebook_version`, `assessor_type`, `evidence_id` (последние три — для оценок приёмов). Это **проектное решение**, а не существующие столбцы DuckDB.

## 6. Контрольные точки

- До агрегации пар проверять уникальность (`app_id`, `genre_id`) и (`app_id`, `category_id`).
- До построения Game Profile агрегировать многозначные жанры и категории, исключая размножение строк.
- После построения профиля проверять 2 000 строк = 2 000 уникальных `app_id`.
- Перед сравнением CCU фиксировать дату начала/конца, `days_observed` и `coverage_pct`.
- `sales` присоединять опционально, не отбрасывая 1 642 игры без пересечения.
