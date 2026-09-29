# SEL Center — Ecoverde (Django 6.1 + PostgreSQL)

**Автор:** Жахангир (9-А, 88-мактаб, Ташкент) — `Django-learn` → `sel`  
**Учитель:** Rahmet97/ecoverde (https://github.com/Rahmet97/ecoverde) — ветка `master` (`96b0093`)  
**Цель этого коммита:** довести `sel` **до уровня учителя и выше** (фикс багов учителя + polish).

## Что уже было у учителя (96b0093)
- Проект `home_market` / apps `base` + `auth`
- Модели `City` (name, img, created_at/updated_at) + `House` (img, type, price, address, description, room_count, floor, floor_count, area, title, city FK, broker FK)
- 5 миграций: `0001_initial` → `0005_house_broker` (city img, city options, broker)
- Views: `home` (annotate house_count, agents), `about`, `agent`, `services`, `contacts`, `add_house` (create без проверки)
- Auth: `AgentPhoneNumbers`, `AgentImage`, `RegisterForm` (UserCreationForm), `login_view`, `register_view`, `logout_view`
- Templates: Ecoverde theme (bg_1, ftco, carousel, search, cities, agents), `house_form.css` + `auth.css`
- Static: 171 файл, settings `Asia/Tashkent`, PostgreSQL `psycopg2`, `Pillow`

## Что в `sel` теперь (уровень учителя + фиксы)
### Фиксы багов учителя (честно, почему хрень)
1. **`Count('house')` → `Count('houses')`** — у учителя `City.objects.annotate(house_count=Count('house'))` падает, т.к. `related_name='houses'` (или `house_set`). Исправлено на `Count('houses')` с `houses` related_name + `order_by('-house_count','name')`.
2. **`is_staff = CheckboxInput()` → `BooleanField`** — у учителя поле формы объявлено как виджет, а не поле → не валидируется. Исправлено: `forms.BooleanField(required=False, label="Men agentman")`.
3. **`refresh_from_db()` лишний + `form.save()` без `commit=False`** — учитель не сохраняет `is_staff/first_name/last_name/email` правильно. Исправлено через `commit=False` + явное присваивание.
4. **`ALLOWED_HOSTS` краш** — у учителя `os.getenv('ALLOWED_HOSTS').split(',')` падает если env пуст. Исправлено: `os.getenv('ALLOWED_HOSTS','').split(',') if ... else []`.
5. **`add_house` без `login_required` и без `try/except`** — прямой `request.FILES['img']` / `request.POST['price']` даёт `KeyError`. Исправлено: `@login_required`, `request.FILES.get('img')`, `request.POST.get(...)`, `strip()`, `broker=request.user`, `try/except` → `error` в шаблон.
6. **`select_related` + `ordering`** — добавлено для скорости и детерминизма.
7. **Шаблоны: `city.img.url` / `house.img.url` без проверки** — падает если img пуст. Добавлены `{% if city.img %}` / `{% if house.img %}` с fallback на `place-1.jpg` / `work-1.jpg`.
8. **`broker` nullable** — `{{ house.broker.first_name }}` падает если `broker=None`. Исправлено: `{% if house.broker %}` → initials + fallback "No broker".

### Что сохранено на уровне учителя
- Все 5 миграций → у нас 3 (склеены, но эквивалентны): `0001_initial` (city+house), `0002_house_broker`, `0003_alter_city_options...` (verbose, related_name, broker_houses)
- Все routes: `/` (home), `/about`, `/agent`, `/services`, `/contact`, `/add-house`, `/auth/login`, `/auth/register`, `/auth/logout`, `/admin/`
- Все templates: `base.html`, `index.html` (Ecoverde hero + search + properties carousel + cities + workflow + about + counters + testimonials + agents + blog), `about.html`, `agent.html` (динамический цикл), `add_house.html` (hf-card), `login.html`/`register.html` (auth-card)
- Static: скопирован 1-в-1 из `ecoverde/static` (171 файл, `auth.css`, `house_form.css`, `style.css` и т.д.)
- DB: `ecoverde_db` (PostgreSQL, `Asia/Tashkent`)

### Улучшения сверх учителя (developer-подход)
- `agent.html` динамический с `{% for agent in agents %}` + empty-сообщением (учитель — статичные 4 карточки)
- `City`/`House` verbose_name на узбекском (`Shahar`, `Uy`, `Narxi ($)`) + `related_name='houses'` / `'broker_houses'`
- `index.html` — цена `floatformat:"0"` + `/month` для Rent, `date:"d.m.Y"` для created_at

## Запуск (как у учителя)
```bash
cd sel
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # заполни SECRET_KEY и DB_*
# создай БД ecoverde_db в psql:
#   CREATE DATABASE ecoverde_db OWNER postgres;
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver   # http://127.0.0.1:8000
```
`.env` пример (`sel/.env` уже есть для локалки):
```
SECRET_KEY=django-insecure-ay*x@_ib%69y)ze2+test-key-for-learn
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,testserver
DB_NAME=ecoverde_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

## Структура (как у учителя)
```
sel/
  config/        # settings (Asia/Tashkent, .env, media, static)
  main/          # = ecoverde/base (City, House, home/about/agent/services/contacts/add_house)
  auth/          # AgentPhoneNumbers, AgentImage, RegisterForm, login/register/logout
  templates/     # base, index, about, agent, add_house, login, register, services, contact
  static/        # css, js, images, scss, fonts (из ecoverde)
  media/         # houses/, cities/, agents/ (upload)
  manage.py
```

## Проверка
```bash
venv\Scripts\python manage.py check
venv\Scripts\python manage.py showmigrations
venv\Scripts\python manage.py test  # если добавишь tests
```

## Дальше (что учитель будет делать следующим)
- Поиск/фильтр на `index` (Keyword, Property Type, Location, Price Limit)
- `properties` список + `properties-single` детальная
- Пагинация, избранное, сравнение
- Админ полировка (list_filter, search_fields уже есть)
