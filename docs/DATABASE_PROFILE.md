# DATABASE_PROFILE — Steam Analytics

> Версия 1.1 · 22.11.2026. Структура и SQL — по экспорту DuckDB 21.11.2026; покрытие 2 000 игр и уникальность проверены дополнительными запросами, но физический файл базы не передавался.

## Назначение
Локальная DuckDB для исследования игр Steam, игровой активности, жанров, категорий и дальнейшей идентификации 120 игровых приёмов.

## Подключение
```python
from project_config import connect_db, DB_PATH
# В новом ядре без уже открытого соединения DuckDB:
con = connect_db(read_only=True)
# Если con уже существует в этом ядре, используйте его повторно.
```

> Если база уже открыта в том же ядре Jupyter с `read_only=False`, используйте имеющееся соединение `con` вместо повторного подключения с другой конфигурацией.

## Проверенное покрытие исследовательской выборки

Базовая таблица `steam_app_details`: 2 000 строк / 2 000 уникальных `app_id`. Все 2 000 представлены в `games`, `health` и `ccu_daily`; в жанрах — 1 990, в категориях — 1 997, в `sales` — 358. В основных таблицах `games` и `health` соответственно 84 843 и 84 844 уникальных идентификатора. См. `DATA_COLLECTION_METHODOLOGY.md` и `DATA_DICTIONARY.md`.

## Объём объектов
| Таблица | Строк |
|---|---:|
| `games` | 84 843 |
| `ccu_daily` | 189 405 |
| `health` | 84 844 |
| `sales` | 647 |
| `steam_app_details` | 2 000 |
| `steam_app_genres` | 5 677 |
| `steam_app_categories` | 20 689 |

## Словарь физических таблиц и представлений

### ccu_daily

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `date` | `TIMESTAMP` | YES |
| `max_players` | `BIGINT` | YES |

### games

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `name` | `VARCHAR` | YES |
| `slug` | `VARCHAR` | YES |
| `release_date` | `TIMESTAMP` | YES |
| `is_free` | `BOOLEAN` | YES |
| `total_positive` | `BIGINT` | YES |
| `total_negative` | `BIGINT` | YES |
| `health_tier` | `VARCHAR` | YES |

### health

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `slug` | `VARCHAR` | YES |
| `tier` | `VARCHAR` | YES |
| `current_players` | `DOUBLE` | YES |

### review_games

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `csv_name` | `VARCHAR` | YES |
| `api_name` | `VARCHAR` | YES |
| `status` | `VARCHAR` | YES |
| `final_name` | `VARCHAR` | YES |
| `decision` | `VARCHAR` | YES |
| `comment` | `VARCHAR` | YES |

### sales

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `name` | `VARCHAR` | YES |
| `slug` | `VARCHAR` | YES |
| `release_date` | `VARCHAR` | YES |
| `era` | `VARCHAR` | YES |
| `pc_only` | `BOOLEAN` | YES |
| `units` | `BIGINT` | YES |
| `units_sold_at` | `VARCHAR` | YES |
| `ref_url` | `VARCHAR` | YES |
| `reviews` | `BIGINT` | YES |
| `review_source` | `VARCHAR` | YES |
| `snap_date` | `VARCHAR` | YES |
| `rescale_factor` | `DOUBLE` | YES |
| `ratio` | `DOUBLE` | YES |
| `position` | `VARCHAR` | YES |

### steam_app_categories

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `INTEGER` | NO |
| `category_id` | `INTEGER` | NO |
| `category_name` | `VARCHAR` | YES |

### steam_app_details

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | NO |
| `api_name` | `VARCHAR` | YES |
| `app_type` | `VARCHAR` | YES |
| `genres` | `VARCHAR` | YES |
| `categories` | `VARCHAR` | YES |
| `short_description` | `VARCHAR` | YES |
| `final_name` | `VARCHAR` | YES |

### steam_app_genres

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `INTEGER` | NO |
| `genre_id` | `VARCHAR` | NO |
| `genre_name` | `VARCHAR` | YES |

### steam_games_analytics

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `final_name` | `VARCHAR` | YES |
| `app_type` | `VARCHAR` | YES |
| `peak_ccu` | `BIGINT` | YES |
| `avg_daily_peak` | `DOUBLE` | YES |
| `min_daily_peak` | `BIGINT` | YES |
| `days_observed` | `BIGINT` | YES |
| `total_days` | `BIGINT` | YES |
| `coverage_pct` | `DOUBLE` | YES |
| `genres_count` | `BIGINT` | YES |
| `categories_count` | `BIGINT` | YES |

### vw_game_activity

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `name` | `VARCHAR` | YES |
| `mean_ccu` | `DOUBLE` | YES |
| `median_ccu` | `DOUBLE` | YES |
| `peak_ccu` | `BIGINT` | YES |
| `observed_days` | `BIGINT` | YES |

### vw_game_analytics

| Поле | Тип | NULL разрешён |
|---|---|---|
| `app_id` | `BIGINT` | YES |
| `name` | `VARCHAR` | YES |
| `mean_ccu` | `DOUBLE` | YES |
| `median_ccu` | `DOUBLE` | YES |
| `peak_ccu` | `BIGINT` | YES |
| `observed_days` | `BIGINT` | YES |
| `app_type` | `VARCHAR` | YES |
| `genres` | `VARCHAR` | YES |
| `categories` | `VARCHAR` | YES |
| `short_description` | `VARCHAR` | YES |

## SQL аналитических представлений

### review_games

```sql
CREATE TEMP VIEW review_games AS SELECT * FROM pandas_scan() AS __duckdb_source_e20bbc22e146_6;
```

### steam_games_analytics

```sql
CREATE VIEW steam_games_analytics AS WITH activity AS (SELECT app_id, max(max_players) AS peak_ccu, round(avg(max_players), 2) AS avg_daily_peak, min(max_players) AS min_daily_peak, count(DISTINCT date) AS days_observed FROM ccu_daily GROUP BY app_id), period AS (SELECT count(DISTINCT date) AS total_days FROM ccu_daily), genre_stats AS (SELECT app_id, count_star() AS genres_count FROM steam_app_genres GROUP BY app_id), category_stats AS (SELECT app_id, count_star() AS categories_count FROM steam_app_categories GROUP BY app_id) SELECT d.app_id, d.final_name, d.app_type, a.peak_ccu, a.avg_daily_peak, a.min_daily_peak, a.days_observed, p.total_days, round(((100.0 * a.days_observed) / "nullif"(p.total_days, 0)), 2) AS coverage_pct, COALESCE(g.genres_count, 0) AS genres_count, COALESCE(c.categories_count, 0) AS categories_count FROM ((((steam_app_details AS d INNER JOIN activity AS a ON ((d.app_id = a.app_id))) CROSS JOIN period AS p) LEFT JOIN genre_stats AS g ON ((d.app_id = g.app_id))) LEFT JOIN category_stats AS c ON ((d.app_id = c.app_id)));
```

### vw_game_activity

```sql
CREATE VIEW vw_game_activity AS SELECT c.app_id, g."name", avg(c.max_players) AS mean_ccu, median(c.max_players) AS median_ccu, max(c.max_players) AS peak_ccu, count(DISTINCT c.date) AS observed_days FROM (ccu_daily AS c LEFT JOIN games AS g ON ((c.app_id = g.app_id))) GROUP BY c.app_id, g."name";
```

### vw_game_analytics

```sql
CREATE VIEW vw_game_analytics AS SELECT a.app_id, a."name", a.mean_ccu, a.median_ccu, a.peak_ccu, a.observed_days, d.app_type, d.genres, d.categories, d.short_description FROM (vw_game_activity AS a LEFT JOIN steam_app_details AS d ON ((a.app_id = d.app_id)));
```

## Подтверждённые SQL-зависимости

- `steam_games_analytics`: `steam_app_details` INNER JOIN агрегированной `ccu_daily` по `app_id`; LEFT JOIN числа жанров и категорий; глобальный `total_days`.
- `vw_game_activity`: `ccu_daily` LEFT JOIN `games` по `app_id`; группировка по `app_id` и имени.
- `vw_game_analytics`: `vw_game_activity` LEFT JOIN `steam_app_details` по `app_id`.
- `review_games`: TEMP VIEW, созданный из `pandas_scan()`, не является надёжным постоянным представлением.

## Оговорки

- 77 описаний колонок включают колонки 4 VIEW и 7 таблиц.
- Показатели количества строк не означают количество уникальных `app_id`.
- Проверена уникальность `app_id` во всех семи физических таблицах в пользовательских запросах: у `ccu_daily` множество строк на игру, у связующих таблиц жанров и категорий — несколько строк на игру. При этом полнота отдельных полей, фактические ограничения ключей, а также права на сторонние датасеты требуют дополнительного аудита.
- Для периода CCU в текущем материале зафиксированы 06.08–12.11.2026 (99 дат); при изменении источника период сверяется заново.
- На данном этапе нет доказанного наличия таблиц 120 игровых приёмов, оценок LLM, Game Profile 1.0.

## Проверки для следующего этапа

```python
for table in ["games", "health", "ccu_daily", "sales", "steam_app_details", "steam_app_genres", "steam_app_categories"]:
    sql = f'SELECT COUNT(*) n, COUNT(DISTINCT app_id) unique_games, COUNT(*)-COUNT(app_id) missing_app_id FROM "{table}"'
    print(table, con.execute(sql).df().to_dict("records")[0])
```

```sql
-- Временное покрытие активности
SELECT MIN(date) AS date_min, MAX(date) AS date_max, COUNT(DISTINCT date) AS days FROM ccu_daily;
-- Сопоставление набора из 2000 игр Steam с активностью
SELECT COUNT(*) AS games_without_activity FROM steam_app_details d WHERE NOT EXISTS (SELECT 1 FROM ccu_daily a WHERE a.app_id=d.app_id);
```

## Следующие документы

- `DATA_DICTIONARY.md`: смысл полей, единицы измерения, источник, метод расчёта, допустимые пропуски.
- `RESEARCH_CONTEXT.md`: цель, гипотезы, результаты выполненных этапов.
- `DATA_LINEAGE.md`: происхождение CSV и логика загрузки/преобразований.
- `database_schema/schema.sql`: воспроизводимые DDL таблиц и VIEW, кроме временных зависимостей.
- `requirements.txt` и скрипты загрузки данных.
