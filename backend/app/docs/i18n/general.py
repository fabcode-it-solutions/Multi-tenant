"""The reference's framing text: introduction, sections, access lines, HTTP
statuses, error codes and query/path parameters -- in three languages."""

from __future__ import annotations

from app.docs.i18n.base import T

INFO_TITLE = T("JoinPay POS API", "JoinPay POS API", "JoinPay POS API")

_EN = """
The backend of JoinPay, a multi-tenant point-of-sale system: the till, each shop's back office, and the platform's own administration.

**Language.** This reference exists in English, Uzbek and Russian — switch with *Select a definition* at the top of the page, or fetch `/api/v1/openapi.json?lang=en|uz|ru`.

## Signing in
1. Call `POST /api/v1/auth/login` with `email`, `password` and the shop address in `tenant_slug` (for example `demo`).
2. Copy `access_token` from the response, press **Authorize** and paste it. Every request is then sent with `Authorization: Bearer <token>`.
3. Access tokens last 30 minutes — 12 hours for cashiers, so a till is not signed out mid-shift. Exchange `refresh_token` at `POST /api/v1/auth/refresh` for a new pair. Each refresh token works once; presenting one twice signs the account out everywhere.

Five wrong passwords lock an account for 15 minutes.

## Shops
Every account except platform staff belongs to exactly one shop, and every request is confined to the shop in its token. Passing another shop's IDs finds nothing — the database enforces the same boundary with row-level security, independently of the API.

## Permissions
Each endpoint states the permission it checks and which roles hold it by default. **Owner** has everything in the shop. **Manager** runs the floor — catalog, stock, staff, refunds, shifts and reports — but not billing, branches or shop settings. **Cashier** has the till. A request without the permission gets `403 permission_denied`.

## Money and quantities
Amounts are decimal **strings** such as `"12500.00"` in the shop's currency — never floating-point numbers. Quantities have up to three decimals (`"1.250"` kg). Tax rates are fractions: `"0.12"` is 12%. Totals are always calculated by the server; totals sent by a client are never trusted.

## Lists
Paginated lists take `page` (from 1) and `size`, and return `items`, `total`, `page` and `size`.

## Errors
Every error has the same body:

    {"code": "sku_taken", "message": "SKU DRK-001 is already in use.", "details": {}, "request_id": "…"}

Branch on `code` — it is stable. `message` is written for people and may change. Each endpoint lists the codes it can return.

## Limits
Sign-in, sign-up and password reset allow 5 requests per minute per IP address; the rest of the API allows 30 per second. Going over returns `429`.
"""

_UZ = """
JoinPay — ko'p do'konli (multi-tenant) savdo nuqtasi tizimining backend'i: kassa, har bir do'konning boshqaruv paneli va platformaning o'z boshqaruvi.

**Til.** Bu hujjat ingliz, o'zbek va rus tillarida mavjud — sahifa tepasidagi *Select a definition* orqali almashtiring yoki `/api/v1/openapi.json?lang=en|uz|ru` ni oling.

## Tizimga kirish
1. `POST /api/v1/auth/login` ga `email`, `password` va `tenant_slug` da do'kon manzilini (masalan, `demo`) yuboring.
2. Javobdagi `access_token` ni nusxalang, **Authorize** tugmasini bosing va joylashtiring. Shundan keyin har bir so'rov `Authorization: Bearer <token>` bilan yuboriladi.
3. Access token 30 daqiqa amal qiladi — kassirlar uchun 12 soat, toki kassa smena o'rtasida chiqib ketmasin. `refresh_token` ni `POST /api/v1/auth/refresh` da yangi juftlikka almashtiring. Har bir refresh token bir marta ishlaydi; ikkinchi marta yuborilsa, hisob hamma qurilmalardan chiqariladi.

Beshta noto'g'ri parol hisobni 15 daqiqaga bloklaydi.

## Do'konlar
Platforma xodimlaridan tashqari har bir hisob faqat bitta do'konga tegishli va har bir so'rov tokendagi do'kon doirasida bajariladi. Boshqa do'konning ID'larini yuborish hech narsa topmaydi — ma'lumotlar bazasi xuddi shu chegarani API'dan mustaqil ravishda row-level security bilan ta'minlaydi.

## Ruxsatlar
Har bir endpoint qaysi ruxsatni tekshirishini va u standart bo'yicha qaysi rollarda borligini ko'rsatadi. **Ega** — do'kondagi hamma narsa. **Menejer** savdo zalini boshqaradi — katalog, ombor, xodimlar, qaytarishlar, smenalar va hisobotlar — lekin to'lov, filiallar va do'kon sozlamalarisiz. **Kassir** — kassa. Ruxsat bo'lmasa `403 permission_denied` qaytadi.

## Pul va miqdor
Summalar do'kon valyutasidagi o'nlik **satrlar**, masalan `"12500.00"` — hech qachon suzuvchi nuqtali son emas. Miqdorlar uch xonagacha kasrli (`"1.250"` kg). Soliq stavkalari kasr: `"0.12"` — 12%. Jami summalarni har doim server hisoblaydi; mijoz yuborgan jamiga ishonilmaydi.

## Ro'yxatlar
Sahifalangan ro'yxatlar `page` (1 dan) va `size` qabul qiladi hamda `items`, `total`, `page` va `size` qaytaradi.

## Xatolar
Har bir xato bir xil ko'rinishda:

    {"code": "sku_taken", "message": "SKU DRK-001 is already in use.", "details": {}, "request_id": "…"}

Dasturda `code` bo'yicha tarmoqlaning — u o'zgarmaydi. `message` odamlar uchun yozilgan va o'zgarishi mumkin. Har bir endpoint qaytarishi mumkin bo'lgan kodlarni sanab o'tadi.

## Cheklovlar
Kirish, ro'yxatdan o'tish va parolni tiklash bitta IP manzildan daqiqasiga 5 ta so'rovga ruxsat beradi; qolgan API — soniyasiga 30 ta. Oshib ketsa `429` qaytadi.
"""

_RU = """
Бэкенд JoinPay — мультитенантной системы для точек продаж: касса, панель управления каждого магазина и администрирование самой платформы.

**Язык.** Документация доступна на английском, узбекском и русском — переключайтесь через *Select a definition* вверху страницы или запрашивайте `/api/v1/openapi.json?lang=en|uz|ru`.

## Вход
1. Вызовите `POST /api/v1/auth/login` с `email`, `password` и адресом магазина в `tenant_slug` (например, `demo`).
2. Скопируйте `access_token` из ответа, нажмите **Authorize** и вставьте его. Дальше каждый запрос отправляется с `Authorization: Bearer <token>`.
3. Access-токен действует 30 минут — для кассиров 12 часов, чтобы касса не разлогинивалась посреди смены. Обменяйте `refresh_token` на новую пару в `POST /api/v1/auth/refresh`. Каждый refresh-токен работает один раз; повторное использование завершает все сессии учётной записи.

Пять неверных паролей блокируют учётную запись на 15 минут.

## Магазины
Каждая учётная запись, кроме сотрудников платформы, принадлежит ровно одному магазину, и каждый запрос ограничен магазином из токена. Передача ID другого магазина ничего не найдёт — база данных обеспечивает ту же границу через row-level security независимо от API.

## Права
Каждый эндпоинт указывает проверяемое право и роли, у которых оно есть по умолчанию. **Владелец** — всё в магазине. **Менеджер** ведёт торговый зал — каталог, склад, сотрудники, возвраты, смены и отчёты, — но без оплаты, филиалов и настроек магазина. **Кассир** — касса. Без нужного права ответ — `403 permission_denied`.

## Деньги и количества
Суммы — десятичные **строки** вида `"12500.00"` в валюте магазина, никогда не числа с плавающей точкой. Количества — до трёх знаков после запятой (`"1.250"` кг). Налоговые ставки — дроби: `"0.12"` — это 12%. Итоги всегда считает сервер; присланным клиентом итогам не доверяют.

## Списки
Постраничные списки принимают `page` (с 1) и `size` и возвращают `items`, `total`, `page` и `size`.

## Ошибки
У каждой ошибки одинаковое тело:

    {"code": "sku_taken", "message": "SKU DRK-001 is already in use.", "details": {}, "request_id": "…"}

Ветвитесь по `code` — он стабилен. `message` написан для людей и может меняться. Каждый эндпоинт перечисляет коды, которые может вернуть.

## Лимиты
Вход, регистрация и сброс пароля — 5 запросов в минуту с одного IP-адреса; остальной API — 30 в секунду. При превышении возвращается `429`.
"""

INFO_DESCRIPTION = T(_EN.strip(), _UZ.strip(), _RU.strip())

# Section order in the reference follows this dict.
TAGS: dict[str, tuple[T, T]] = {
    "auth": (
        T("Authentication", "Autentifikatsiya", "Аутентификация"),
        T(
            "Sign-up, sign-in, sessions, and your own profile, password and PIN.",
            "Ro'yxatdan o'tish, kirish, sessiyalar hamda o'z profilingiz, parolingiz va PIN'ingiz.",
            "Регистрация, вход, сессии, а также свой профиль, пароль и PIN.",
        ),
    ),
    "catalog": (
        T("Catalog", "Katalog", "Каталог"),
        T(
            "Products, categories, tax rates and barcode lookup.",
            "Mahsulotlar, kategoriyalar, soliq stavkalari va shtrix-kod bo'yicha qidiruv.",
            "Товары, категории, налоговые ставки и поиск по штрихкоду.",
        ),
    ),
    "inventory": (
        T("Inventory", "Ombor", "Склад"),
        T(
            "Stock per branch: deliveries, write-offs, stocktakes and the movement ledger.",
            "Filiallar bo'yicha qoldiq: yetkazib berish, hisobdan chiqarish, inventarizatsiya va harakatlar daftari.",
            "Остатки по филиалам: поставки, списания, инвентаризация и журнал движений.",
        ),
    ),
    "orders": (
        T("Sales", "Sotuvlar", "Продажи"),
        T(
            "Taking payment, receipts and refunds.",
            "To'lov qabul qilish, cheklar va qaytarishlar.",
            "Приём оплаты, чеки и возвраты.",
        ),
    ),
    "shifts": (
        T("Shifts", "Smenalar", "Смены"),
        T(
            "Opening and closing tills, and reviewing how each drawer reconciled.",
            "Kassalarni ochish va yopish hamda har bir yashik qanday hisob-kitob qilinganini ko'rib chiqish.",
            "Открытие и закрытие касс и обзор того, как сошёлся каждый ящик.",
        ),
    ),
    "employees": (
        T("Staff", "Xodimlar", "Сотрудники"),
        T(
            "Staff accounts, roles and permissions.",
            "Xodim hisoblari, rollar va ruxsatlar.",
            "Учётные записи сотрудников, роли и права.",
        ),
    ),
    "shop": (
        T("Shop", "Do'kon", "Магазин"),
        T(
            "Branches, shop details, receipt layout and tax-rate changes.",
            "Filiallar, do'kon ma'lumotlari, chek ko'rinishi va soliq stavkalarini o'zgartirish.",
            "Филиалы, данные магазина, оформление чека и изменение налоговых ставок.",
        ),
    ),
    "analytics": (
        T("Analytics", "Tahlil", "Аналитика"),
        T(
            "Dashboard figures and charts.",
            "Boshqaruv paneli ko'rsatkichlari va grafiklar.",
            "Показатели панели и графики.",
        ),
    ),
    "reports": (
        T("Reports", "Hisobotlar", "Отчёты"),
        T(
            "Exports generated in the background as CSV, XLSX or PDF.",
            "Fonda CSV, XLSX yoki PDF sifatida tayyorlanadigan eksportlar.",
            "Выгрузки, формируемые в фоне в CSV, XLSX или PDF.",
        ),
    ),
    "billing": (
        T("Billing", "To'lov", "Оплата"),
        T(
            "The shop's own subscription to JoinPay.",
            "Do'konning JoinPay'ga o'z obunasi.",
            "Собственная подписка магазина на JoinPay.",
        ),
    ),
    "platform": (
        T("Platform", "Platforma", "Платформа"),
        T(
            "Platform staff only: every shop, plans and revenue.",
            "Faqat platforma xodimlari uchun: barcha do'konlar, tariflar va daromad.",
            "Только для сотрудников платформы: все магазины, тарифы и выручка.",
        ),
    ),
    "ops": (
        T("Service", "Xizmat", "Служебное"),
        T(
            "Health checks for load balancers and monitoring.",
            "Yuk taqsimlagichlar va monitoring uchun holat tekshiruvlari.",
            "Проверки состояния для балансировщиков и мониторинга.",
        ),
    ),
}

SECURITY = T(
    "Paste the `access_token` from `POST /api/v1/auth/login` — without the word Bearer.",
    "`POST /api/v1/auth/login` javobidagi `access_token` ni joylashtiring — Bearer so'zisiz.",
    "Вставьте `access_token` из ответа `POST /api/v1/auth/login` — без слова Bearer.",
)

ACCESS: dict[str, T] = {
    "public": T(
        "**Access:** public — no token needed.",
        "**Kirish:** ochiq — token kerak emas.",
        "**Доступ:** открытый — токен не нужен.",
    ),
    "authenticated": T(
        "**Access:** any signed-in user.",
        "**Kirish:** tizimga kirgan har qanday foydalanuvchi.",
        "**Доступ:** любой вошедший пользователь.",
    ),
    "permission": T(
        "**Requires:** {permissions}. **Held by default by:** {roles}.",
        "**Talab qilinadi:** {permissions}. **Standart bo'yicha kimda bor:** {roles}.",
        "**Требуется:** {permissions}. **По умолчанию есть у:** {roles}.",
    ),
    "no_role": T(
        "no shop role — grant it per user",
        "hech bir do'kon rolida yo'q — foydalanuvchiga alohida beriladi",
        "ни у одной роли магазина — выдаётся индивидуально",
    ),
    "platform": T(
        "**Access:** platform staff (`super_admin`) only.",
        "**Kirish:** faqat platforma xodimlari (`super_admin`).",
        "**Доступ:** только сотрудники платформы (`super_admin`).",
    ),
}

ROLE_NAMES: dict[str, T] = {
    "cashier": T("cashier", "kassir", "кассир"),
    "manager": T("manager", "menejer", "менеджер"),
    "owner": T("owner", "ega", "владелец"),
}

STATUS: dict[str, T] = {
    "200": T("Success.", "Muvaffaqiyatli.", "Успешно."),
    "201": T("Created.", "Yaratildi.", "Создано."),
    "202": T(
        "Accepted — the work continues in the background.",
        "Qabul qilindi — ish fonda davom etadi.",
        "Принято — работа продолжается в фоне.",
    ),
    "400": T(
        "The request cannot be carried out as given.",
        "So'rovni bu ko'rinishda bajarib bo'lmaydi.",
        "Запрос в таком виде выполнить нельзя.",
    ),
    "401": T(
        "Not signed in, or the session is no longer valid — sign in again.",
        "Tizimga kirilmagan yoki sessiya endi amal qilmaydi — qayta kiring.",
        "Вход не выполнен или сессия больше не действительна — войдите снова.",
    ),
    "402": T(
        "The shop's plan or subscription does not allow this.",
        "Do'kon tarifi yoki obunasi bunga ruxsat bermaydi.",
        "Тариф или подписка магазина этого не позволяют.",
    ),
    "403": T(
        "Signed in, but not allowed: a permission is missing (`permission_denied`) or the shop is blocked (`tenant_inactive`).",
        "Tizimga kirilgan, lekin ruxsat yo'q: ruxsat yetishmaydi (`permission_denied`) yoki do'kon bloklangan (`tenant_inactive`).",
        "Вход выполнен, но действие запрещено: нет права (`permission_denied`) или магазин заблокирован (`tenant_inactive`).",
    ),
    "404": T("Not found in your shop.", "Do'koningizda topilmadi.", "Не найдено в вашем магазине."),
    "409": T(
        "Conflicts with the current state.", "Joriy holatga zid.", "Конфликт с текущим состоянием."
    ),
    "422": T(
        "Some fields are invalid — `details.errors` lists each field and why.",
        "Ayrim maydonlar noto'g'ri — `details.errors` har bir maydon va sababni ko'rsatadi.",
        "Некоторые поля неверны — `details.errors` перечисляет каждое поле и причину.",
    ),
}

ERROR_CODES: dict[str, T] = {
    # generic
    "bad_request": T(
        "The request cannot be processed.",
        "So'rovni qayta ishlab bo'lmaydi.",
        "Запрос не может быть обработан.",
    ),
    "validation_error": T(
        "Some fields are invalid.", "Ayrim maydonlar noto'g'ri.", "Некоторые поля неверны."
    ),
    "not_found": T("Not found.", "Topilmadi.", "Не найдено."),
    "conflict": T(
        "Conflicts with existing data.",
        "Mavjud ma'lumotlarga zid.",
        "Конфликт с существующими данными.",
    ),
    "internal_error": T(
        "Something went wrong on the server.",
        "Serverda xatolik yuz berdi.",
        "На сервере произошла ошибка.",
    ),
    # access
    "unauthenticated": T(
        "Not signed in, or the session is no longer valid.",
        "Tizimga kirilmagan yoki sessiya endi amal qilmaydi.",
        "Вход не выполнен или сессия больше не действительна.",
    ),
    "invalid_credentials": T(
        "Wrong email, password, PIN or token.",
        "Email, parol, PIN yoki token noto'g'ri.",
        "Неверный email, пароль, PIN или токен.",
    ),
    "account_locked": T(
        "Too many failed attempts — try again in 15 minutes.",
        "Juda ko'p muvaffaqiyatsiz urinish — 15 daqiqadan keyin qayta urining.",
        "Слишком много неудачных попыток — повторите через 15 минут.",
    ),
    "invalid_reset_token": T(
        "The reset link is invalid, already used or expired.",
        "Tiklash havolasi noto'g'ri, ishlatilgan yoki muddati o'tgan.",
        "Ссылка для сброса неверна, уже использована или истекла.",
    ),
    "permission_denied": T(
        "A required permission is missing; `details.missing` lists it.",
        "Kerakli ruxsat yo'q; `details.missing` uni ko'rsatadi.",
        "Нет нужного права; `details.missing` его перечисляет.",
    ),
    "self_edit_blocked": T(
        "Staff endpoints cannot change your own account — use `/auth/me`.",
        "Xodimlar endpointlari o'z hisobingizni o'zgartira olmaydi — `/auth/me` dan foydalaning.",
        "Через эндпоинты сотрудников нельзя менять свою учётную запись — используйте `/auth/me`.",
    ),
    "tenant_inactive": T(
        "The shop is blocked or closed.",
        "Do'kon bloklangan yoki yopilgan.",
        "Магазин заблокирован или закрыт.",
    ),
    "tenant_not_found": T(
        "No shop has that address.", "Bunday manzilli do'kon yo'q.", "Магазина с таким адресом нет."
    ),
    # plan
    "subscription_required": T(
        "The shop's subscription has ended — pay the outstanding invoice to keep selling.",
        "Do'kon obunasi tugagan — sotishni davom ettirish uchun hisobni to'lang.",
        "Подписка магазина закончилась — оплатите счёт, чтобы продолжить продажи.",
    ),
    "quota_exceeded": T(
        "The plan's limit is reached; `details` has the limit and the current count.",
        "Tarif chegarasiga yetildi; `details` da chegara va joriy son bor.",
        "Достигнут лимит тарифа; в `details` — лимит и текущее количество.",
    ),
    "plan_not_found": T("No such plan.", "Bunday tarif yo'q.", "Такого тарифа нет."),
    # catalog
    "sku_taken": T(
        "Another product in this shop already uses this SKU.",
        "Bu SKU ni do'kondagi boshqa mahsulot ishlatmoqda.",
        "Этот артикул уже использует другой товар магазина.",
    ),
    "barcode_taken": T(
        "Another product in this shop already uses this barcode.",
        "Bu shtrix-kodni do'kondagi boshqa mahsulot ishlatmoqda.",
        "Этот штрихкод уже использует другой товар магазина.",
    ),
    "slug_taken": T(
        "That address or name is already taken.",
        "Bu manzil yoki nom allaqachon band.",
        "Этот адрес или название уже занят.",
    ),
    "name_taken": T(
        "Something with that name already exists.",
        "Bu nomdagi yozuv allaqachon mavjud.",
        "Запись с таким названием уже существует.",
    ),
    "code_taken": T(
        "That code is already in use.", "Bu kod allaqachon band.", "Этот код уже занят."
    ),
    "cyclic_parent": T(
        "A category cannot be its own parent.",
        "Kategoriya o'ziga o'zi ota bo'la olmaydi.",
        "Категория не может быть родителем самой себя.",
    ),
    "product_not_found": T(
        "No product matches.", "Mos mahsulot topilmadi.", "Подходящий товар не найден."
    ),
    "rate_in_use": T(
        "Products still use this rate; `details.products` says how many.",
        "Bu stavkani hali mahsulotlar ishlatmoqda; `details.products` nechta ekanini ko'rsatadi.",
        "Ставку ещё используют товары; `details.products` показывает сколько.",
    ),
    # sales
    "empty_cart": T(
        "A sale needs at least one line.",
        "Sotuvda kamida bitta qator bo'lishi kerak.",
        "В продаже должна быть хотя бы одна строка.",
    ),
    "insufficient_stock": T(
        "Not enough stock to sell that quantity.",
        "Bu miqdorni sotish uchun qoldiq yetarli emas.",
        "Недостаточно остатка для продажи такого количества.",
    ),
    "payment_mismatch": T(
        "Payments do not cover the order total; `details` has both figures.",
        "To'lovlar buyurtma jamisini qoplamaydi; `details` da ikkala summa bor.",
        "Оплаты не покрывают итог заказа; в `details` обе суммы.",
    ),
    "no_open_shift": T(
        "There is no open shift — open one first.",
        "Ochiq smena yo'q — avval smena oching.",
        "Нет открытой смены — сначала откройте её.",
    ),
    "shift_already_open": T(
        "You already have an open shift.",
        "Sizda allaqachon ochiq smena bor.",
        "У вас уже есть открытая смена.",
    ),
    "order_not_refundable": T(
        "The order cannot be refunded in its current state.",
        "Buyurtmani hozirgi holatida qaytarib bo'lmaydi.",
        "Заказ нельзя вернуть в текущем состоянии.",
    ),
    "refund_exceeds_order": T(
        "More than is still refundable was requested.",
        "Hali qaytarish mumkin bo'lganidan ko'proq so'raldi.",
        "Запрошено больше, чем ещё можно вернуть.",
    ),
    "line_not_found": T(
        "That line is not part of this order.",
        "Bu qator ushbu buyurtmaga tegishli emas.",
        "Эта строка не относится к заказу.",
    ),
    # shop
    "last_branch": T(
        "A shop needs at least one branch.",
        "Do'konda kamida bitta filial bo'lishi kerak.",
        "У магазина должен быть хотя бы один филиал.",
    ),
    "default_branch": T(
        "This is the default branch — make another branch the default first.",
        "Bu asosiy filial — avval boshqa filialni asosiy qiling.",
        "Это основной филиал — сначала сделайте основным другой.",
    ),
    "email_taken": T(
        "Someone at this shop already uses that email.",
        "Bu emailni do'kondagi boshqa xodim ishlatmoqda.",
        "Этот email уже использует другой сотрудник магазина.",
    ),
    # reports
    "report_not_ready": T(
        "The report is still being generated.",
        "Hisobot hali tayyorlanmoqda.",
        "Отчёт ещё формируется.",
    ),
    "report_expired": T(
        "The file has expired — request the report again.",
        "Fayl muddati tugagan — hisobotni qayta so'rang.",
        "Срок файла истёк — запросите отчёт заново.",
    ),
    # billing (payment-provider callbacks)
    "invoice_not_payable": T(
        "The invoice cannot be paid in its current state.",
        "Hisob-fakturani hozirgi holatida to'lab bo'lmaydi.",
        "Счёт нельзя оплатить в текущем состоянии.",
    ),
    "already_paid": T(
        "The invoice is already paid.", "Hisob-faktura allaqachon to'langan.", "Счёт уже оплачен."
    ),
    "void": T("The invoice was cancelled.", "Hisob-faktura bekor qilingan.", "Счёт аннулирован."),
    "wrong_amount": T(
        "The amount does not match the invoice.",
        "Summa hisob-fakturaga mos emas.",
        "Сумма не совпадает со счётом.",
    ),
}

PARAMS: dict[str, T] = {
    "query:page": T(
        "Page number, from 1.", "Sahifa raqami, 1 dan boshlab.", "Номер страницы, начиная с 1."
    ),
    "query:size": T("Records per page.", "Sahifadagi yozuvlar soni.", "Записей на странице."),
    "query:search": T("Text to search for.", "Qidiriladigan matn.", "Текст для поиска."),
    "query:branch_id": T(
        "Only this branch. Defaults to your own; cashiers always see theirs.",
        "Faqat shu filial. Standart — o'z filialingiz; kassirlar har doim o'z filialini ko'radi.",
        "Только этот филиал. По умолчанию — ваш; кассиры всегда видят свой.",
    ),
    "query:category_id": T(
        "Only products in this category.",
        "Faqat shu kategoriyadagi mahsulotlar.",
        "Только товары этой категории.",
    ),
    "query:favorites_only": T(
        "Only products pinned to the front of the grid.",
        "Faqat panel boshiga qadalgan mahsulotlar.",
        "Только товары, закреплённые в начале экрана.",
    ),
    "query:code": T(
        "The scanned barcode, carton barcode or SKU.",
        "Skanerlangan shtrix-kod, quti kodi yoki SKU.",
        "Отсканированный штрихкод, код упаковки или артикул.",
    ),
    "query:low_only": T(
        "Only products at or below their reorder threshold.",
        "Faqat qayta buyurtma chegarasiga yetgan yoki undan kam mahsulotlar.",
        "Только товары на пороге дозаказа или ниже.",
    ),
    "query:product_id": T("Only this product.", "Faqat shu mahsulot.", "Только этот товар."),
    "query:shift_id": T(
        "Only sales from this shift.", "Faqat shu smenadagi sotuvlar.", "Только продажи этой смены."
    ),
    "query:user_id": T(
        "Only this cashier's shifts.",
        "Faqat shu kassirning smenalari.",
        "Только смены этого кассира.",
    ),
    "query:status": T(
        "Only shifts in this status.",
        "Faqat shu holatdagi smenalar.",
        "Только смены в этом статусе.",
    ),
    "query:date_from": T(
        "Opened on or after this day, in the shop's time zone.",
        "Do'kon vaqt mintaqasi bo'yicha shu kuni yoki undan keyin ochilgan.",
        "Открыты в этот день или позже — по часовому поясу магазина.",
    ),
    "query:date_to": T(
        "Opened on or before this day, in the shop's time zone — the whole day is included.",
        "Do'kon vaqt mintaqasi bo'yicha shu kuni yoki undan oldin ochilgan — kun to'liq kiradi.",
        "Открыты в этот день или раньше — по часовому поясу магазина; день включается целиком.",
    ),
    "query:role": T(
        "Only staff with this role.",
        "Faqat shu roldagi xodimlar.",
        "Только сотрудники с этой ролью.",
    ),
    "query:include_inactive": T(
        "Include deactivated accounts.",
        "Faolsizlantirilgan hisoblarni ham qo'shish.",
        "Включить деактивированные учётные записи.",
    ),
    "query:days": T(
        "How many days back, counting today.",
        "Bugunni ham hisoblab, necha kun orqaga.",
        "Сколько дней назад, включая сегодня.",
    ),
    "query:limit": T(
        "Maximum number of rows.", "Qatorlarning eng ko'p soni.", "Максимальное число строк."
    ),
    "query:months": T("How many months back.", "Necha oy orqaga.", "Сколько месяцев назад."),
    "query:tenant_status": T(
        "Only shops in this status.",
        "Faqat shu holatdagi do'konlar.",
        "Только магазины в этом статусе.",
    ),
    "path:category_id": T("Category ID.", "Kategoriya ID.", "ID категории."),
    "path:product_id": T("Product ID.", "Mahsulot ID.", "ID товара."),
    "path:order_id": T("Order ID.", "Buyurtma ID.", "ID заказа."),
    "path:user_id": T("Staff member ID.", "Xodim ID.", "ID сотрудника."),
    "path:branch_id": T("Branch ID.", "Filial ID.", "ID филиала."),
    "path:rate_id": T("Tax rate ID.", "Soliq stavkasi ID.", "ID налоговой ставки."),
    "path:job_id": T("Report job ID.", "Hisobot vazifasi ID.", "ID задачи отчёта."),
    "path:tenant_id": T("Shop ID.", "Do'kon ID.", "ID магазина."),
    "path:plan_id": T("Plan ID.", "Tarif ID.", "ID тарифа."),
}

PAGE_SCHEMA = T(
    "A page of `{item}` records.",
    "`{item}` yozuvlarining bitta sahifasi.",
    "Страница записей `{item}`.",
)
