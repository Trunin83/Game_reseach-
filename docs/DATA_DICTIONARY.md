# DATA DICTIONARY — словарь показателей и полей

> Версия 1.0 · 22.11.2026. Источник структуры: `database_columns.csv` и `DATABASE_PROFILE.md`. Значения терминов — по SQL и ноутбуку; неподтверждённая семантика явно отмечена.

## 1. Общие правила

- Каждая строка профиля игры соответствует одному `app_id`; каждая строка активности — одному (`app_id`, `date`).
- `NULL` и отсутствие строки — не ноль. `NULL`-допустимость из схемы не означает фактические пропуски.
- `AVG(max_players)` означает среднее дневных **максимумов** CCU. `mean_ccu` — историческое имя той же логики.
- Единица Lift — коэффициент без размерности, рассчитываемый для пар признаков в выборке N=2000.

## 2. Поля всех объектов DuckDB

### `ccu_daily`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `date` | `TIMESTAMP` | Дата наблюдения дневного максимума CCU. Проверять временную зону и зерно дат | дата |
| `max_players` | `BIGINT` | Максимальное одновременно активное число игроков за дату. Не DAU и не среднесуточный CCU | игроки |

### `games`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `name` | `VARCHAR` | Название в исходном каталоге или производном VIEW. Происхождение зависит от таблицы | текст |
| `slug` | `VARCHAR` | Человекочитаемый идентификатор в The Game Census. Не заменять app_id | текст |
| `release_date` | `TIMESTAMP` | Дата релиза по источнику. Тип отличается между games и sales | дата/текст |
| `is_free` | `BOOLEAN` | Признак бесплатной игры в The Game Census. Источник, не Steam API | логический |
| `total_positive` | `BIGINT` | Количество положительных отзывов источника. Момент измерения требует фиксации | отзывы |
| `total_negative` | `BIGINT` | Количество отрицательных отзывов источника. Момент измерения требует фиксации | отзывы |
| `health_tier` | `VARCHAR` | Исходная категория состояния игры. Значения задаёт источник | категория |

### `health`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `slug` | `VARCHAR` | Человекочитаемый идентификатор в The Game Census. Не заменять app_id | текст |
| `tier` | `VARCHAR` | Категория состояния игры в health. Не обязательно равна health_tier | категория |
| `current_players` | `DOUBLE` | Текущий онлайн по срезу health. Дата/время снимка не установлены | игроки |

### `review_games`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `csv_name` | `VARCHAR` | Название игры в исходном каталоге. Только журнал ревизии | текст |
| `api_name` | `VARCHAR` | Название приложения из Steam Store API. Может отличаться от исходного каталога | текст |
| `status` | `VARCHAR` | Статус запроса/проверки API. Только журнал ревизии | категория |
| `final_name` | `VARCHAR` | Итоговое название для отчёта. Обычно API, исключение ParanormalHK | текст |
| `decision` | `VARCHAR` | Решение о дальнейшей загрузке. В итоговом Excel — load | категория |
| `comment` | `VARCHAR` | Комментарий ручной проверки. Может быть пустым | текст |

### `sales`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `name` | `VARCHAR` | Название в исходном каталоге или производном VIEW. Происхождение зависит от таблицы | текст |
| `slug` | `VARCHAR` | Человекочитаемый идентификатор в The Game Census. Не заменять app_id | текст |
| `release_date` | `VARCHAR` | Дата релиза по источнику. Тип отличается между games и sales | дата/текст |
| `era` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `pc_only` | `BOOLEAN` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `units` | `BIGINT` | Проданные единицы по калибровочному источнику. Не для всей выборки | единицы |
| `units_sold_at` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `ref_url` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `reviews` | `BIGINT` | Число отзывов в калибровочном источнике. Не для всей выборки | отзывы |
| `review_source` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `snap_date` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |
| `rescale_factor` | `DOUBLE` | Коэффициент пересчёта из источника продаж. Семантика поставщика требует проверки | коэффициент |
| `ratio` | `DOUBLE` | Показатель отношения из источника продаж. Точная методика требует внешнего описания | коэффициент |
| `position` | `VARCHAR` | Поле исходного источника; точное значение проверить по документации поставщика. Не выдумывать определение | требует проверки |

### `steam_app_categories`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `INTEGER` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `category_id` | `INTEGER` | Идентификатор категории Steam. Часть пары (app_id, category_id) | ID |
| `category_name` | `VARCHAR` | Название категории Steam. Категория Steam не равно приём Codebook | текст |

### `steam_app_details`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `api_name` | `VARCHAR` | Название приложения из Steam Store API. Может отличаться от исходного каталога | текст |
| `app_type` | `VARCHAR` | Тип приложения по Steam Store API. Использовать для контроля видеоигр | категория |
| `genres` | `VARCHAR` | JSON-подобный массив жанров API, сохранённый текстом. SQL тип VARCHAR | текст JSON |
| `categories` | `VARCHAR` | JSON-подобный массив категорий API, сохранённый текстом. SQL тип VARCHAR | текст JSON |
| `short_description` | `VARCHAR` | Краткое описание приложения по Steam API. Не достаточно для всех 120 оценок | текст |
| `final_name` | `VARCHAR` | Итоговое название для отчёта. Обычно API, исключение ParanormalHK | текст |

### `steam_app_genres`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `INTEGER` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `genre_id` | `VARCHAR` | Идентификатор жанра Steam. Часть пары (app_id, genre_id) | ID |
| `genre_name` | `VARCHAR` | Название жанра Steam. Название — не первичный ключ | текст |

### `steam_games_analytics`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `final_name` | `VARCHAR` | Итоговое название для отчёта. Обычно API, исключение ParanormalHK | текст |
| `app_type` | `VARCHAR` | Тип приложения по Steam Store API. Использовать для контроля видеоигр | категория |
| `peak_ccu` | `BIGINT` | MAX(max_players) за доступный период. Зависит от периода и покрытия | игроки |
| `avg_daily_peak` | `DOUBLE` | AVG(max_players) по имеющимся датам. Средний дневной максимум; НЕ средний онлайн за сутки | игроки |
| `min_daily_peak` | `BIGINT` | MIN(max_players) по доступным датам. Минимум дневных пиков | игроки |
| `days_observed` | `BIGINT` | COUNT(DISTINCT date) для игры. Отличать от общего окна | дни |
| `total_days` | `BIGINT` | COUNT(DISTINCT date) по всей таблице ccu_daily. Общий горизонт наблюдений | дни |
| `coverage_pct` | `DOUBLE` | 100 × days_observed / total_days. Округление до 2 знаков | % |
| `genres_count` | `BIGINT` | Число записей жанров на app_id. Пустая связь не всегда ошибка | шт. |
| `categories_count` | `BIGINT` | Число записей категорий на app_id. Не путать с 120 механиками | шт. |

### `vw_game_activity`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `name` | `VARCHAR` | Название в исходном каталоге или производном VIEW. Происхождение зависит от таблицы | текст |
| `mean_ccu` | `DOUBLE` | AVG(max_players) по имеющимся датам. Имя историческое; означает среднее дневных максимумов | игроки |
| `median_ccu` | `DOUBLE` | MEDIAN(max_players) по доступным датам. Медиана дневных максимумов | игроки |
| `peak_ccu` | `BIGINT` | MAX(max_players) за доступный период. Зависит от периода и покрытия | игроки |
| `observed_days` | `BIGINT` | COUNT(DISTINCT date) для игры. Отличать от общего окна | дни |

### `vw_game_analytics`

| Поле | SQL-тип | Операциональное определение | Единица / статус |
|---|---|---|---|
| `app_id` | `BIGINT` | Идентификатор приложения Steam. Исходный ключ для сопоставления | ID |
| `name` | `VARCHAR` | Название в исходном каталоге или производном VIEW. Происхождение зависит от таблицы | текст |
| `mean_ccu` | `DOUBLE` | AVG(max_players) по имеющимся датам. Имя историческое; означает среднее дневных максимумов | игроки |
| `median_ccu` | `DOUBLE` | MEDIAN(max_players) по доступным датам. Медиана дневных максимумов | игроки |
| `peak_ccu` | `BIGINT` | MAX(max_players) за доступный период. Зависит от периода и покрытия | игроки |
| `observed_days` | `BIGINT` | COUNT(DISTINCT date) для игры. Отличать от общего окна | дни |
| `app_type` | `VARCHAR` | Тип приложения по Steam Store API. Использовать для контроля видеоигр | категория |
| `genres` | `VARCHAR` | JSON-подобный массив жанров API, сохранённый текстом. SQL тип VARCHAR | текст JSON |
| `categories` | `VARCHAR` | JSON-подобный массив категорий API, сохранённый текстом. SQL тип VARCHAR | текст JSON |
| `short_description` | `VARCHAR` | Краткое описание приложения по Steam API. Не достаточно для всех 120 оценок | текст |

## 3. Основные производные показатели

| Метрика | Формула / алгоритм | Оговорка |
|---|---|---|
| `peak_ccu` | `MAX(max_players)` на игру | Не retention |
| `avg_daily_peak`, `mean_ccu` | `AVG(max_players)` на игру | Среднее пиков, не всех измерений в течение дня |
| `median_ccu` | `MEDIAN(max_players)` | Медиана дневных пиков |
| `coverage_pct` | `100 × days_observed / total_days` | Окно дат задаётся содержимым всей `ccu_daily` |
| `rank_peak` | `ROW_NUMBER() OVER (ORDER BY peak_ccu DESC, app_id)` | Упорядочивание по пику |
| `rank_avg_daily_peak` | `ROW_NUMBER() OVER (ORDER BY avg_daily_peak DESC, app_id)` | Упорядочивание по среднему дневному пику |
| `rank_stable` | Только `coverage_pct >= 90`, ранг по среднему дневному пику среди игр с таким покрытием | Для остальных `NULL` |
| Частота жанра/категории | Количество уникальных игр с признаком | Делитель 2 000 при расчёте доли в выборке |
| `share_pct` | `100 × games_count / 2000` (для соответствующего файла частот) | Проверять знаменатель в каждой версии анализа |
| `expected_count` | `count(A) × count(B) / 2000` | Гипотеза независимости |
| `lift` | `count(A∩B) × 2000 / (count(A) × count(B))` | Не причинность; учитывать размер пары |
| `excess_count` | `games_count - expected_count` | Разность с ожидаемой частотой |

## 4. Поля CSV `data/processed`

- **`steam_category_frequency.csv`** (63 строк): `category_name`, `games_count`, `share_pct`.
- **`steam_category_pairs_frequency.csv`** (1704 строк): `category_name_1`, `category_name_2`, `games_count`, `share_pct`, `category_pair`.
- **`steam_category_pairs_lift.csv`** (1704 строк): `category_name_1`, `category_name_2`, `games_count`, `share_pct`, `category_pair`, `count_1`, `count_2`, `lift`.
- **`steam_games_ranking.csv`** (2000 строк): `app_id`, `final_name`, `app_type`, `peak_ccu`, `avg_daily_peak`, `min_daily_peak`, `days_observed`, `total_days`, `coverage_pct`, `genres_count`, `categories_count`, `rank_peak`, `rank_avg_daily_peak`, `rank_stable`.
- **`steam_genre_lift_all.csv`** (92 строк): `genre_1`, `genre_2`, `games_count`, `share_pct`, `genre_1_count`, `genre_2_count`, `expected_count`, `lift`, `excess_count`.
- **`steam_genre_lift_filtered.csv`** (51 строк): `genre_1`, `genre_2`, `games_count`, `share_pct`, `genre_1_count`, `genre_2_count`, `expected_count`, `lift`, `excess_count`.
- **`steam_genre_lift_matrix.csv`** (12 строк): ``, `Action`, `Indie`, `Adventure`, `Simulation`, `Strategy`, `RPG`, `Casual`, `Free To Play`, `Massively Multiplayer`, `Early Access`, `Sports`, `Racing`.
- **`steam_genre_pairs.csv`** (92 строк): `genre_1`, `genre_2`, `games_count`, `share_pct`.
- **`steam_genre_pairs_popularity.csv`** (92 строк): `genre_1`, `genre_2`, `games_count`, `median_peak_ccu`, `mean_peak_ccu`, `median_avg_daily_peak`, `top100_games`, `top100_share_pct`.
- **`steam_genre_popularity.csv`** (19 строк): `genre_name`, `games_count`, `share_pct`, `median_peak_ccu`, `mean_peak_ccu`, `median_avg_daily_peak`, `top100_games`, `top100_share_pct`.
- **`steam_top100.csv`** (100 строк): `app_id`, `final_name`, `app_type`, `peak_ccu`, `avg_daily_peak`, `min_daily_peak`, `days_observed`, `total_days`, `coverage_pct`, `genres_count`, `categories_count`, `rank_peak`, `rank_avg_daily_peak`, `rank_stable`.

## 5. Пропуски и границы измеримости

- `sales`: пересечение с 2 000 играми — 358. Не интерпретировать незаполненность как 0 продаж.
- `steam_app_genres`: есть хотя бы одна связь у 1 990 игр; `steam_app_categories` — у 1 997.
- `current_players` в `health` относится к отдельному моментному снимку поставщика и не заменяет исторические пики.
- Жанры и категории Steam — метаданные платформы, а не результаты полноценной диагностики 120 игровых приёмов.
- Поля из калибровочного набора (`units_sold_at`, `era`, `position`, `ratio` и пр.) не интерпретировать без документации первоисточника.
