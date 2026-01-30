# TeamLabSofter

Краулер на Scrapy, который обходит страницы сайта и собирает с них email и телефоны. Результат выводится в JSON.

## Что делает проект

Паук `site` заходит на указанный URL и рекурсивно ходит по всем ссылкам в пределах того же домена (или схемы, для локальных файлов). На каждой странице он:

- достаёт адреса из ссылок `mailto:` и из текста страницы по регулярному выражению;
- достаёт номера из ссылок `tel:` и из текста по регулярному выражению;
- убирает дубликаты и отдаёт по странице один объект: `url`, `emails`, `phones`.

Ссылки вида `mailto:` и `tel:` не используются для перехода, только для извлечения контактов. Остальные ссылки обрабатываются через `response.follow`, то есть относительные пути и якоря разрешаются корректно.

## Структура

```
TeamLabSofter/
  crawler/                 # проект Scrapy
    crawler/
      spiders/
        site.py            # паук site
      items.py
      middlewares.py
      pipelines.py
      settings.py
    scrapy.cfg
  test.html                # тестовая страница
  page2.html               # вторая страница (ссылка из test.html)
  requirements.txt
```

## Установка

Нужен Python 3. Рекомендуется виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Основная зависимость — Scrapy 2.14.1.

## Запуск

Команды выполняются из каталога `crawler`, где лежит `scrapy.cfg`:

```bash
cd crawler
```

Обязательный аргумент паука — `start_url`. Без него паук выдаст ошибку.

**Тестовый запуск по локальному файлу:**

```bash
scrapy crawl site -a start_url=file:///C:/Work/TeamLabSofter/test.html -o output.json
```

Путь к `test.html` замени на свой абсолютный путь. Результат будет в `crawler/output.json`.

**Запуск по живому сайту:**

```bash
scrapy crawl site -a start_url=https://example.com -o output.json
```

**Другие форматы вывода:**

```bash
scrapy crawl site -a start_url=https://example.com -o result.jsonl
scrapy crawl site -a start_url=https://example.com -o result.csv
```

Имена файлов `output.json`, `result.jsonl` и т.п. — на выбор; расширение задаёт формат.

## Поведение и ограничения

- В `settings.py` включено соблюдение `robots.txt` (`ROBOTSTXT_OBEY = True`). Для файловых URL это не играет роли.
- На домен ограничен один одновременный запрос и задержка 1 секунда между запросами (`CONCURRENT_REQUESTS_PER_DOMAIN = 1`, `DOWNLOAD_DELAY = 1`), чтобы не нагружать сервер.
- Кодировка экспорта — UTF-8 (`FEED_EXPORT_ENCODING = "utf-8"`).
- Паук не использует кастомные Scrapy Item и pipeline: данные отдаются словарём в `parse`.

## Пример вывода

Для локального прогона по `test.html` и `page2.html` в `output.json` ожидается:

```json
[
  {"url": "file:///C:/Work/TeamLabSofter/test.html", "emails": ["support@example.com", "info@example.com"], "phones": ["+1234567890", "+1987654321"]},
  {"url": "file:///C:/Work/TeamLabSofter/page2.html", "emails": ["other@example.com"], "phones": ["+1122334455"]}
]
```

Фактический порядок полей внутри объектов и порядок элементов в массивах `emails`/`phones` может отличаться.

## Список пауков

```bash
cd crawler
scrapy list
```

Должен быть выведен один паук: `site`.
