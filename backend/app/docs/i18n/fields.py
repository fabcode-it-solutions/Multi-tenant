"""What each field means, in three languages.

`FIELDS` is keyed by field name and used wherever that name means the same
thing. `FIELD_OVERRIDES` is keyed `Schema.field` for the names that mean
different things in different places -- `code` is a branch's receipt prefix in
one schema and a plan identifier in another. `PAGE_FIELDS` describes the
envelope every paginated list shares.

Constraints (lengths, ranges, patterns) are deliberately left out: Swagger
renders them from the schema, and restating them here is how the two drift.
"""

from __future__ import annotations

from app.docs.i18n.base import T

PAGE_FIELDS: dict[str, T] = {
    "items": T("The records on this page.", "Shu sahifadagi yozuvlar.", "Записи на этой странице."),
    "total": T(
        "How many records match across all pages.",
        "Barcha sahifalar bo'yicha mos keladigan yozuvlar soni.",
        "Сколько записей подходит по всем страницам.",
    ),
    "page": T(
        "This page's number, from 1.",
        "Sahifa raqami, 1 dan boshlab.",
        "Номер страницы, начиная с 1.",
    ),
    "size": T("Records per page.", "Sahifadagi yozuvlar soni.", "Записей на странице."),
}

FIELDS: dict[str, T] = {
    # ------------------------------------------------------ identity & records
    "id": T(
        "Unique identifier (UUID).",
        "Noyob identifikator (UUID).",
        "Уникальный идентификатор (UUID).",
    ),
    "created_at": T(
        "When the record was created (UTC).",
        "Yozuv yaratilgan vaqt (UTC).",
        "Когда создана запись (UTC).",
    ),
    "created_by_id": T(
        "Who created it (user ID).",
        "Kim yaratgani (foydalanuvchi ID).",
        "Кто создал (ID пользователя).",
    ),
    "name": T("Display name.", "Ko'rsatiladigan nom.", "Отображаемое название."),
    "description": T(
        "Longer free-text description.",
        "Batafsil erkin matnli tavsif.",
        "Подробное описание в свободной форме.",
    ),
    "note": T("Free-text note.", "Erkin matnli izoh.", "Заметка в свободной форме."),
    "reason": T("Reason, in free text.", "Sabab, erkin matnda.", "Причина в свободной форме."),
    "is_active": T(
        "Inactive records are hidden from everyday use but kept for history.",
        "Faol bo'lmagan yozuvlar kundalik ishda ko'rinmaydi, lekin tarix uchun saqlanadi.",
        "Неактивные записи скрыты из повседневной работы, но сохраняются для истории.",
    ),
    "status": T(
        "Current status. The allowed values are explained on the enum.",
        "Joriy holat. Ruxsat etilgan qiymatlar enum'da tushuntirilgan.",
        "Текущий статус. Допустимые значения описаны в перечислении.",
    ),
    "sort_order": T(
        "Lower numbers are shown first.",
        "Kichik raqamlilar birinchi ko'rsatiladi.",
        "Меньшие значения показываются первыми.",
    ),
    "message": T(
        "A human-readable message.", "Odam o'qishi uchun xabar.", "Сообщение для человека."
    ),
    "details": T(
        "Machine-readable context — for example the missing permission or the invalid fields. Its shape depends on `code`.",
        "Dastur uchun qo'shimcha ma'lumot — masalan, yetishmayotgan ruxsat yoki noto'g'ri maydonlar. Shakli `code` ga bog'liq.",
        "Машиночитаемый контекст — например, недостающее право или неверные поля. Структура зависит от `code`.",
    ),
    "request_id": T(
        "Identifies this request in the server logs. Quote it when reporting a problem.",
        "Server loglarida shu so'rovni aniqlaydi. Muammo haqida xabar berganda uni ko'rsating.",
        "Идентифицирует запрос в логах сервера. Укажите его, сообщая о проблеме.",
    ),
    # --------------------------------------------------------- people & access
    "email": T("Email address.", "Email manzil.", "Адрес электронной почты."),
    "password": T("Password.", "Parol.", "Пароль."),
    "current_password": T("Your current password.", "Joriy parolingiz.", "Текущий пароль."),
    "new_password": T("The new password.", "Yangi parol.", "Новый пароль."),
    "pin": T(
        "Terminal PIN, digits only, for switching cashiers quickly.",
        "Kassirlarni tez almashtirish uchun terminal PIN'i, faqat raqamlar.",
        "PIN-код терминала, только цифры, для быстрой смены кассира.",
    ),
    "has_pin": T(
        "Whether a terminal PIN is set.",
        "Terminal PIN'i o'rnatilganmi.",
        "Задан ли PIN-код терминала.",
    ),
    "full_name": T("Full name.", "To'liq ism.", "Полное имя."),
    "owner_name": T("The owner's full name.", "Egasining to'liq ismi.", "Полное имя владельца."),
    "phone": T("Phone number.", "Telefon raqami.", "Номер телефона."),
    "avatar_url": T(
        "Link to a profile picture, shown on the PIN-login screen.",
        "Profil rasmi havolasi, PIN bilan kirish ekranida ko'rsatiladi.",
        "Ссылка на фото профиля, показывается на экране входа по PIN.",
    ),
    "role": T(
        "Role; see the enum for what each grants.",
        "Rol; har biri nima berishini enum'da ko'ring.",
        "Роль; что даёт каждая — см. перечисление.",
    ),
    "permissions": T(
        "Effective permissions: the role's defaults with per-user overrides applied.",
        "Amaldagi ruxsatlar: rolning standart ruxsatlari va foydalanuvchiga xos o'zgartirishlar.",
        "Действующие права: права роли с учётом индивидуальных изменений.",
    ),
    "permission_overrides": T(
        'Per-user changes to the role\'s permissions, as `{"allow": [...], "deny": [...]}`. A deny always wins over an allow.',
        'Rol ruxsatlariga foydalanuvchiga xos o\'zgartirishlar: `{"allow": [...], "deny": [...]}`. `deny` har doim `allow` dan ustun.',
        'Индивидуальные изменения прав роли в виде `{"allow": [...], "deny": [...]}`. Запрет всегда сильнее разрешения.',
    ),
    "last_login_at": T(
        "Last successful sign-in (UTC).",
        "Oxirgi muvaffaqiyatli kirish (UTC).",
        "Последний успешный вход (UTC).",
    ),
    "user": T("The signed-in user.", "Tizimga kirgan foydalanuvchi.", "Вошедший пользователь."),
    "user_id": T("User ID.", "Foydalanuvchi ID.", "ID пользователя."),
    "user_count": T(
        "Number of staff accounts.",
        "Xodim hisoblari soni.",
        "Количество учётных записей сотрудников.",
    ),
    # ----------------------------------------------------------------- tokens
    "access_token": T(
        "Send as `Authorization: Bearer <token>`. Short-lived: see `expires_in`.",
        "`Authorization: Bearer <token>` sifatida yuboring. Qisqa muddatli: `expires_in` ga qarang.",
        "Передавайте как `Authorization: Bearer <token>`. Короткоживущий: см. `expires_in`.",
    ),
    "refresh_token": T(
        "Exchange at `/auth/refresh` for a new pair. Each refresh token works once; presenting a used one revokes every session of the account.",
        "`/auth/refresh` da yangi juftlikka almashtiring. Har bir refresh token bir marta ishlaydi; ishlatilganini qayta yuborish hisobning barcha sessiyalarini bekor qiladi.",
        "Обменивайте на новую пару в `/auth/refresh`. Каждый refresh-токен работает один раз; повторное использование отзывает все сессии учётной записи.",
    ),
    "token_type": T("Always `bearer`.", "Har doim `bearer`.", "Всегда `bearer`."),
    "expires_in": T(
        "Seconds until the access token expires.",
        "Access token muddati tugashigacha qolgan soniyalar.",
        "Секунд до истечения access-токена.",
    ),
    "token": T(
        "The token from the password-reset link. Works once and expires.",
        "Parolni tiklash havolasidagi token. Bir marta ishlaydi va muddati tugaydi.",
        "Токен из ссылки для сброса пароля. Работает один раз и имеет срок действия.",
    ),
    # ------------------------------------------------------------------ shops
    "tenant_id": T(
        "Shop ID; null for platform staff.",
        "Do'kon ID; platforma xodimlari uchun null.",
        "ID магазина; null для сотрудников платформы.",
    ),
    "tenant_slug": T(
        "Shop address used to sign in, e.g. `demo`. Omit for platform staff.",
        "Kirish uchun do'kon manzili, masalan `demo`. Platforma xodimlari yubormaydi.",
        "Адрес магазина для входа, например `demo`. Сотрудники платформы не передают.",
    ),
    "slug": T(
        "Shop address (subdomain), e.g. `demo`. Staff type it to sign in; it cannot be changed self-service.",
        "Do'kon manzili (subdomen), masalan `demo`. Xodimlar kirishda shuni yozadi; uni o'zingiz o'zgartira olmaysiz.",
        "Адрес магазина (поддомен), например `demo`. Сотрудники вводят его при входе; самостоятельно изменить нельзя.",
    ),
    "shop_name": T(
        "The shop's trading name.", "Do'konning savdo nomi.", "Торговое название магазина."
    ),
    "legal_name": T(
        "Registered legal name, if different from the trading name.",
        "Ro'yxatdan o'tgan yuridik nom, agar savdo nomidan farq qilsa.",
        "Зарегистрированное юридическое название, если отличается от торгового.",
    ),
    "tax_number": T(
        "Tax identification number (INN / STIR).",
        "Soliq to'lovchining identifikatsiya raqami (STIR).",
        "Идентификационный номер налогоплательщика (ИНН).",
    ),
    "address": T("Street address.", "Manzil.", "Адрес."),
    "currency": T(
        "ISO 4217 currency code, e.g. `UZS`.",
        "ISO 4217 valyuta kodi, masalan `UZS`.",
        "Код валюты ISO 4217, например `UZS`.",
    ),
    "country_code": T(
        "ISO 3166-1 alpha-2 country code, e.g. `UZ`.",
        "ISO 3166-1 alpha-2 davlat kodi, masalan `UZ`.",
        "Код страны ISO 3166-1 alpha-2, например `UZ`.",
    ),
    "timezone": T(
        "IANA time zone, e.g. `Asia/Tashkent`. Decides where a business day starts for reports and receipt numbers.",
        "IANA vaqt mintaqasi, masalan `Asia/Tashkent`. Hisobotlar va chek raqamlari uchun ish kuni qachon boshlanishini belgilaydi.",
        "Часовой пояс IANA, например `Asia/Tashkent`. Определяет начало рабочего дня для отчётов и номеров чеков.",
    ),
    "locale": T(
        "Language and region for receipts, e.g. `uz`.",
        "Cheklar uchun til va mintaqa, masalan `uz`.",
        "Язык и регион для чеков, например `uz`.",
    ),
    "logo_url": T(
        "Link to the shop's logo.", "Do'kon logotipi havolasi.", "Ссылка на логотип магазина."
    ),
    "receipt_header": T(
        "Text printed above the items on every receipt.",
        "Har bir chekda mahsulotlar ustida chop etiladigan matn.",
        "Текст над товарами на каждом чеке.",
    ),
    "receipt_footer": T(
        "Text printed below the totals on every receipt — returns policy, opening hours, a thank-you.",
        "Har bir chekda jami summadan pastda chop etiladigan matn — qaytarish qoidasi, ish vaqti, minnatdorchilik.",
        "Текст под итогами на каждом чеке — правила возврата, часы работы, благодарность.",
    ),
    "settings": T(
        "Free-form shop switches such as `allow_negative_stock`, `cash_rounding` and `receipt_width_mm`. On update the keys sent are merged in; keys not sent are kept.",
        "`allow_negative_stock`, `cash_rounding`, `receipt_width_mm` kabi erkin do'kon sozlamalari. Yangilashda yuborilgan kalitlar qo'shiladi; yuborilmaganlari saqlanadi.",
        "Произвольные настройки магазина, например `allow_negative_stock`, `cash_rounding`, `receipt_width_mm`. При обновлении переданные ключи объединяются с существующими; непереданные сохраняются.",
    ),
    "tenant_status": T("The shop's status.", "Do'kon holati.", "Статус магазина."),
    "blocked_reason": T(
        "Why the shop is blocked; shown to its staff when they try to sign in.",
        "Do'kon nima uchun bloklangani; xodimlar kirishga uringanda ko'rsatiladi.",
        "Почему магазин заблокирован; показывается сотрудникам при попытке входа.",
    ),
    "last_activity_at": T(
        "Most recent sale or sign-in.",
        "Eng so'nggi sotuv yoki kirish.",
        "Последняя продажа или вход.",
    ),
    # ---------------------------------------------------------------- branches
    "branch_id": T(
        "Branch. Where it is optional on input, the signed-in user's own branch is used; cashiers are always held to theirs.",
        "Filial. Kiritishda ixtiyoriy bo'lsa, tizimga kirgan foydalanuvchining filiali olinadi; kassirlar har doim o'z filialiga bog'langan.",
        "Филиал. Если на входе не указан, берётся филиал вошедшего пользователя; кассиры всегда привязаны к своему.",
    ),
    "branch_name": T("Branch name.", "Filial nomi.", "Название филиала."),
    "is_default": T(
        "The default branch: new staff and anything without a branch fall back to it. Exactly one branch is the default.",
        "Asosiy filial: yangi xodimlar va filiali ko'rsatilmagan hamma narsa unga tushadi. Faqat bitta filial asosiy bo'ladi.",
        "Филиал по умолчанию: к нему относятся новые сотрудники и всё без филиала. Ровно один филиал — по умолчанию.",
    ),
    "staff_count": T(
        "Staff assigned to this branch.",
        "Shu filialga biriktirilgan xodimlar.",
        "Сотрудники, закреплённые за филиалом.",
    ),
    "product_count": T(
        "Number of products in the catalog.",
        "Katalogdagi mahsulotlar soni.",
        "Количество товаров в каталоге.",
    ),
    "orders_last_30_days": T(
        "Completed sales in the last 30 days.",
        "Oxirgi 30 kundagi yakunlangan sotuvlar.",
        "Проведённые продажи за последние 30 дней.",
    ),
    # ----------------------------------------------------------------- catalog
    "category_id": T("Category ID.", "Kategoriya ID.", "ID категории."),
    "category_name": T("Category name.", "Kategoriya nomi.", "Название категории."),
    "parent_id": T(
        "Parent category, for nesting; null for a top-level category.",
        "Ichma-ich joylash uchun ota kategoriya; yuqori darajadagi kategoriya uchun null.",
        "Родительская категория для вложенности; null для категории верхнего уровня.",
    ),
    "color": T(
        "Tile colour on the POS grid, as hex, e.g. `#0f766e`.",
        "POS panelidagi plitka rangi, hex ko'rinishida, masalan `#0f766e`.",
        "Цвет плитки на экране кассы в hex, например `#0f766e`.",
    ),
    "image_url": T("Link to an image.", "Rasm havolasi.", "Ссылка на изображение."),
    "product": T("The product.", "Mahsulot.", "Товар."),
    "product_id": T("Product ID.", "Mahsulot ID.", "ID товара."),
    "product_name": T("Product name.", "Mahsulot nomi.", "Название товара."),
    "sku": T(
        "Stock-keeping unit: the shop's own product code, unique within the shop.",
        "SKU: do'konning o'z mahsulot kodi, do'kon ichida noyob.",
        "Артикул (SKU): собственный код товара, уникальный в магазине.",
    ),
    "barcode": T(
        "Barcode (EAN/UPC), unique within the shop.",
        "Shtrix-kod (EAN/UPC), do'kon ichida noyob.",
        "Штрихкод (EAN/UPC), уникальный в магазине.",
    ),
    "unit": T("Unit of sale.", "Sotuv birligi.", "Единица продажи."),
    "price": T(
        "Selling price per unit.", "Bir birlikning sotuv narxi.", "Цена продажи за единицу."
    ),
    "cost_price": T(
        "Purchase cost per unit, used for margin and stock value.",
        "Bir birlikning xarid narxi; marja va qoldiq qiymati uchun ishlatiladi.",
        "Закупочная цена за единицу; используется для маржи и стоимости остатков.",
    ),
    "track_stock": T(
        "Whether sales take stock down. Turn off for services and made-to-order items.",
        "Sotuvlar qoldiqni kamaytiradimi. Xizmatlar va buyurtma asosida tayyorlanadigan narsalar uchun o'chiring.",
        "Уменьшают ли продажи остаток. Отключите для услуг и товаров под заказ.",
    ),
    "is_favorite": T(
        "Pinned to the front of the POS grid.",
        "POS panelining boshiga qadalgan.",
        "Закреплён в начале экрана кассы.",
    ),
    "low_stock_threshold": T(
        "Reorder point: at or below this quantity the product is flagged as low.",
        "Qayta buyurtma chegarasi: miqdor shunga teng yoki kam bo'lsa, mahsulot kam qolgan deb belgilanadi.",
        "Точка дозаказа: при остатке на этом уровне или ниже товар помечается как заканчивающийся.",
    ),
    "low_stock": T(
        "True when on-hand stock is at or below the threshold.",
        "Qoldiq chegaraga teng yoki undan kam bo'lsa true.",
        "true, если остаток на пороге или ниже.",
    ),
    "stock_quantity": T(
        "Quantity on hand at the branch the request is about; null when it is not tracked.",
        "So'rov tegishli filialdagi qoldiq; hisob yuritilmasa null.",
        "Остаток в филиале, к которому относится запрос; null, если учёт не ведётся.",
    ),
    "opening_stock": T(
        "Quantity already on the shelf at your branch, recorded as an `initial` stock movement.",
        "Filialingizda javonda turgan miqdor; `initial` harakati sifatida yoziladi.",
        "Количество, уже лежащее на полке в вашем филиале; записывается как движение `initial`.",
    ),
    "tax_rate_id": T(
        "Tax rate applied to this product.",
        "Shu mahsulotga qo'llaniladigan soliq stavkasi.",
        "Налоговая ставка, применяемая к товару.",
    ),
    "tax_rate_name": T(
        "Name of the tax rate.", "Soliq stavkasi nomi.", "Название налоговой ставки."
    ),
    "tax_rate": T(
        "Tax rate as a fraction: `0.12` is 12%.",
        "Soliq stavkasi kasr ko'rinishida: `0.12` — 12%.",
        "Налоговая ставка дробью: `0.12` — это 12%.",
    ),
    "rate": T(
        "The rate as a fraction: `0.12` is 12%.",
        "Stavka kasr ko'rinishida: `0.12` — 12%.",
        "Ставка дробью: `0.12` — это 12%.",
    ),
    "tax_inclusive": T(
        "True when the price already includes the tax.",
        "Narx soliqni allaqachon o'z ichiga olsa true.",
        "true, если цена уже включает налог.",
    ),
    "is_inclusive": T(
        "Whether shelf prices already include this tax (as VAT usually does) or it is added at the till.",
        "Javondagi narxlar bu soliqni allaqachon o'z ichiga oladimi (QQS odatda shunday) yoki u kassada qo'shiladimi.",
        "Включён ли налог в цену на полке (как обычно НДС) или добавляется на кассе.",
    ),
    "matched_on": T(
        "What the code matched: `barcode`, `pack_barcode` (a carton code) or `sku`.",
        "Kod nimaga mos keldi: `barcode`, `pack_barcode` (quti kodi) yoki `sku`.",
        "С чем совпал код: `barcode`, `pack_barcode` (код упаковки) или `sku`.",
    ),
    "pack_size": T(
        "Units one scan represents: `1` for the product's own barcode, the case size for a carton barcode.",
        "Bitta skan nechta donaga teng: mahsulotning o'z shtrix-kodi uchun `1`, quti kodi uchun qutidagi soni.",
        "Сколько единиц даёт одно сканирование: `1` для штрихкода товара, размер упаковки — для кода упаковки.",
    ),
    # --------------------------------------------------------------- inventory
    "quantity": T(
        "Quantity; up to three decimals for weight and length units.",
        "Miqdor; og'irlik va uzunlik birliklari uchun uch xonagacha kasr.",
        "Количество; до трёх знаков после запятой для весовых и линейных единиц.",
    ),
    "reserved_quantity": T(
        "Set aside and not available to sell.",
        "Ajratib qo'yilgan va sotib bo'lmaydigan miqdor.",
        "Зарезервировано и недоступно для продажи.",
    ),
    "available": T(
        "On hand minus reserved: what can be sold now.",
        "Qoldiq minus zaxira: hozir sotish mumkin bo'lgan miqdor.",
        "Остаток минус резерв: что можно продать сейчас.",
    ),
    "is_low": T(
        "At or below the reorder threshold.",
        "Qayta buyurtma chegarasiga teng yoki kam.",
        "На пороге дозаказа или ниже.",
    ),
    "threshold": T(
        "The product's reorder threshold.",
        "Mahsulotning qayta buyurtma chegarasi.",
        "Порог дозаказа товара.",
    ),
    "stock_value": T(
        "Quantity on hand × cost price.", "Qoldiq × xarid narxi.", "Остаток × закупочная цена."
    ),
    "movement_type": T(
        "Why stock changed.", "Qoldiq nima uchun o'zgargani.", "Почему изменился остаток."
    ),
    "quantity_after": T(
        "On-hand quantity right after this movement — the running balance.",
        "Shu harakatdan keyingi qoldiq — joriy balans.",
        "Остаток сразу после этого движения — нарастающий итог.",
    ),
    "unit_cost": T(
        "Cost per unit recorded with this movement.",
        "Shu harakat bilan yozilgan bir birlik narxi.",
        "Себестоимость единицы, записанная с этим движением.",
    ),
    "supplier_id": T("Supplier of a delivery.", "Yetkazib beruvchi.", "Поставщик поставки."),
    "reference_type": T(
        "What caused the movement: `order` or `refund`; null for manual changes.",
        "Harakatga nima sabab bo'lgan: `order` yoki `refund`; qo'lda kiritilganlar uchun null.",
        "Что вызвало движение: `order` или `refund`; null для ручных изменений.",
    ),
    "reference_id": T(
        "ID of the order or refund that caused it.",
        "Unga sabab bo'lgan buyurtma yoki qaytarish ID'si.",
        "ID заказа или возврата, вызвавшего движение.",
    ),
    "counted_quantity": T(
        "Quantity physically counted. The difference from the system figure is recorded as an adjustment.",
        "Haqiqatda sanalgan miqdor. Tizimdagi raqamdan farqi tuzatish sifatida yoziladi.",
        "Фактически пересчитанное количество. Расхождение с учётом записывается как корректировка.",
    ),
    # ------------------------------------------------------------------ orders
    "order": T("The order.", "Buyurtma.", "Заказ."),
    "order_id": T("Order ID.", "Buyurtma ID.", "ID заказа."),
    "order_number": T(
        "Receipt number: branch code, local date and a daily sequence, e.g. `CHL-20260908-0012`.",
        "Chek raqami: filial kodi, mahalliy sana va kunlik tartib raqami, masalan `CHL-20260908-0012`.",
        "Номер чека: код филиала, местная дата и порядковый номер за день, например `CHL-20260908-0012`.",
    ),
    "items": T("The order lines.", "Buyurtma qatorlari.", "Строки заказа."),
    "payments": T(
        "Payments settling the order.",
        "Buyurtmani to'laydigan to'lovlar.",
        "Оплаты, закрывающие заказ.",
    ),
    "cashier_id": T(
        "Cashier who rang up the sale.",
        "Sotuvni amalga oshirgan kassir.",
        "Кассир, проведший продажу.",
    ),
    "cashier_name": T("Cashier's name.", "Kassir ismi.", "Имя кассира."),
    "customer_id": T(
        "Customer, if one was attached to the sale.",
        "Sotuvga biriktirilgan mijoz (bo'lsa).",
        "Покупатель, если он указан в продаже.",
    ),
    "customer_name": T("Customer's name.", "Mijoz ismi.", "Имя покупателя."),
    "discount_type": T(
        "How the discount is expressed.", "Chegirma qanday ifodalanadi.", "Как задана скидка."
    ),
    "discount_value": T(
        "Discount size: a percentage or an amount, depending on `discount_type`.",
        "Chegirma miqdori: `discount_type` ga qarab foiz yoki summa.",
        "Размер скидки: процент или сумма в зависимости от `discount_type`.",
    ),
    "discount_amount": T(
        "Total discount on this line, including its share of any order-level discount.",
        "Shu qatordagi umumiy chegirma, buyurtma chegirmasidan tushgan ulushi bilan.",
        "Общая скидка по строке, включая её долю скидки на заказ.",
    ),
    "subtotal": T(
        "Sum of the lines before discounts.",
        "Chegirmalardan oldingi qatorlar yig'indisi.",
        "Сумма строк до скидок.",
    ),
    "discount_total": T(
        "All discounts on the order.", "Buyurtmadagi barcha chegirmalar.", "Все скидки по заказу."
    ),
    "tax_total": T("Tax on the order.", "Buyurtma solig'i.", "Налог по заказу."),
    "tax_amount": T("Tax on this line.", "Shu qator solig'i.", "Налог по строке."),
    "rounding_adjustment": T(
        "Cash rounding applied to the total; zero unless the shop rounds cash.",
        "Jami summaga qo'llangan naqd yaxlitlash; do'kon yaxlitlamasa nol.",
        "Округление наличных в итоге; ноль, если магазин не округляет.",
    ),
    "total": T("Total amount.", "Jami summa.", "Итоговая сумма."),
    "paid_total": T("Sum of all payments.", "Barcha to'lovlar yig'indisi.", "Сумма всех оплат."),
    "change_due": T(
        "Change handed back for cash.",
        "Naqd pul uchun qaytarilgan qaytim.",
        "Сдача, выданная с наличных.",
    ),
    "refunded_total": T(
        "Money already returned on this order.",
        "Shu buyurtma bo'yicha allaqachon qaytarilgan pul.",
        "Уже возвращённые по заказу деньги.",
    ),
    "completed_at": T(
        "When the sale was completed (UTC).",
        "Sotuv yakunlangan vaqt (UTC).",
        "Когда продажа проведена (UTC).",
    ),
    "unit_price": T(
        "Price per unit at the time of sale — kept even if the product's price changes later.",
        "Sotuv paytidagi bir birlik narxi — mahsulot narxi keyin o'zgarsa ham saqlanadi.",
        "Цена за единицу на момент продажи — сохраняется, даже если цена товара потом изменится.",
    ),
    "line_total": T(
        "What the customer pays for this line after discounts.",
        "Chegirmalardan keyin mijoz shu qator uchun to'laydigan summa.",
        "Сколько покупатель платит за строку после скидок.",
    ),
    "idempotency_key": T(
        "A key unique to this attempt, generated by the client. Resending the same key returns the original result instead of doing it twice — safe to retry after a timeout.",
        "Mijoz ilovasi yaratgan, shu urinish uchun noyob kalit. Xuddi shu kalit qayta yuborilsa, amal ikki marta bajarilmaydi, dastlabki natija qaytadi — timeout'dan keyin qayta urinish xavfsiz.",
        "Уникальный для попытки ключ, генерируемый клиентом. Повтор с тем же ключом возвращает исходный результат вместо повторного действия — повтор после таймаута безопасен.",
    ),
    "method": T("Payment method.", "To'lov usuli.", "Способ оплаты."),
    "amount": T("Amount of money.", "Pul summasi.", "Сумма денег."),
    "tendered_amount": T(
        "Cash the customer handed over. Change is calculated from it.",
        "Mijoz bergan naqd pul. Qaytim shundan hisoblanadi.",
        "Наличные, переданные покупателем. Из них рассчитывается сдача.",
    ),
    "card_last4": T(
        "Last four digits of the card, from the terminal slip.",
        "Kartaning oxirgi to'rt raqami, terminal chekidan.",
        "Последние четыре цифры карты с чека терминала.",
    ),
    "reference": T(
        "Reference from the payment provider or terminal, for reconciliation.",
        "To'lov tizimi yoki terminaldan olingan havola raqami, solishtirish uchun.",
        "Референс платёжной системы или терминала для сверки.",
    ),
    "printed_at": T(
        "When this receipt was generated (UTC).",
        "Chek yaratilgan vaqt (UTC).",
        "Когда сформирован чек (UTC).",
    ),
    "shop": T(
        "Shop and branch details for the receipt.",
        "Chek uchun do'kon va filial ma'lumotlari.",
        "Данные магазина и филиала для чека.",
    ),
    "header": T(
        "Text printed above the items.",
        "Mahsulotlar ustida chop etiladigan matn.",
        "Текст над товарами.",
    ),
    "footer": T(
        "Text printed below the totals.",
        "Jami summadan pastda chop etiladigan matn.",
        "Текст под итогами.",
    ),
    # ---------------------------------------------------------------- refunds
    "order_item_id": T("The order line.", "Buyurtma qatori.", "Строка заказа."),
    "refunded_quantity": T(
        "Units of this line already returned.",
        "Shu qatordan allaqachon qaytarilgan dona.",
        "Уже возвращённые единицы по строке.",
    ),
    "refundable_quantity": T(
        "Units that can still be returned.",
        "Hali qaytarish mumkin bo'lgan dona.",
        "Единицы, которые ещё можно вернуть.",
    ),
    "refundable_amount": T(
        "Money that can still be returned for this line.",
        "Shu qator uchun hali qaytarish mumkin bo'lgan pul.",
        "Сумма, которую ещё можно вернуть по строке.",
    ),
    "refundable_total": T(
        "Money that can still be returned on the order.",
        "Buyurtma bo'yicha hali qaytarish mumkin bo'lgan pul.",
        "Сумма, которую ещё можно вернуть по заказу.",
    ),
    "refunds": T(
        "Refunds already made on this order.",
        "Shu buyurtma bo'yicha qilingan qaytarishlar.",
        "Уже проведённые по заказу возвраты.",
    ),
    "restock": T(
        "Put returned goods back into stock. Turn off for damaged goods.",
        "Qaytarilgan tovarni qoldiqqa qaytarish. Shikastlangan tovar uchun o'chiring.",
        "Вернуть товар на склад. Отключите для повреждённого товара.",
    ),
    "restocked": T(
        "Whether the goods went back into stock.",
        "Tovar qoldiqqa qaytarildimi.",
        "Вернулся ли товар на склад.",
    ),
    # ------------------------------------------------------------------ shifts
    "shift": T("The shift.", "Smena.", "Смена."),
    "opened_at": T(
        "When the shift was opened (UTC).",
        "Smena ochilgan vaqt (UTC).",
        "Когда открыта смена (UTC).",
    ),
    "closed_at": T(
        "When the shift was closed (UTC); null while open.",
        "Smena yopilgan vaqt (UTC); ochiq bo'lsa null.",
        "Когда закрыта смена (UTC); null, пока открыта.",
    ),
    "opening_float": T(
        "Cash in the drawer before trading, kept for giving change. Not revenue.",
        "Savdodan oldin yashikdagi naqd pul, qaytim berish uchun. Tushum emas.",
        "Наличные в ящике до начала торговли, для сдачи. Это не выручка.",
    ),
    "expected_cash": T(
        "What the drawer should hold: opening float + cash taken − change − cash refunds.",
        "Yashikda bo'lishi kerak bo'lgan summa: boshlang'ich pul + naqd tushum − qaytim − naqd qaytarishlar.",
        "Сколько должно быть в ящике: размен + принятые наличные − сдача − возвраты наличными.",
    ),
    "counted_cash": T(
        "Cash counted in the drawer at close; null while open.",
        "Yopishda yashikda sanalgan naqd pul; ochiq bo'lsa null.",
        "Пересчитанные при закрытии наличные; null, пока смена открыта.",
    ),
    "cash_difference": T(
        "Counted minus expected. Positive: more cash than expected; negative: short. Null until the drawer is counted.",
        "Sanalgan minus kutilgan. Musbat — kutilgandan ko'p; manfiy — kam. Yashik sanalmaguncha null.",
        "Пересчитано минус ожидалось. Плюс — больше ожидаемого, минус — недостача. null до пересчёта.",
    ),
    "order_count": T("Completed sales.", "Yakunlangan sotuvlar.", "Проведённые продажи."),
    "gross_sales": T(
        "Everything taken, all payment methods.",
        "Barcha to'lov usullari bo'yicha umumiy tushum.",
        "Всё принятое, всеми способами оплаты.",
    ),
    "cash_sales": T("Taken in cash.", "Naqd pul bilan qabul qilingan.", "Принято наличными."),
    "card_sales": T("Taken by card.", "Karta bilan qabul qilingan.", "Принято картой."),
    "refund_total": T(
        "Refunded during the shift.", "Smena davomida qaytarilgan.", "Возвращено за смену."
    ),
    # --------------------------------------------------------------- analytics
    "revenue_today": T("Sales today.", "Bugungi sotuvlar.", "Продажи сегодня."),
    "revenue_yesterday": T(
        "Sales yesterday, for comparison.",
        "Kechagi sotuvlar, taqqoslash uchun.",
        "Продажи вчера, для сравнения.",
    ),
    "revenue_month": T("Sales this month.", "Shu oydagi sotuvlar.", "Продажи за этот месяц."),
    "orders_today": T(
        "Completed sales today.", "Bugungi yakunlangan sotuvlar.", "Проведённые продажи сегодня."
    ),
    "average_basket": T(
        "Average sale value today.", "Bugungi o'rtacha chek.", "Средний чек сегодня."
    ),
    "gross_margin_today": T(
        "Today's sales minus the cost of the goods sold.",
        "Bugungi sotuvlar minus sotilgan tovar tannarxi.",
        "Продажи сегодня минус себестоимость проданного.",
    ),
    "low_stock_count": T(
        "Products at or below their threshold.",
        "Chegarasiga yetgan yoki undan kam mahsulotlar.",
        "Товары на пороге дозаказа или ниже.",
    ),
    "out_of_stock_count": T(
        "Products with nothing left.",
        "Butunlay tugagan mahsulotlar.",
        "Товары, которых не осталось.",
    ),
    "active_shifts": T("Tills open right now.", "Hozir ochiq kassalar.", "Открытые сейчас кассы."),
    "day": T("The day.", "Kun.", "День."),
    "hour": T(
        "Hour of the day, 0–23, in the shop's time zone.",
        "Kun soati, 0–23, do'kon vaqt mintaqasida.",
        "Час дня, 0–23, в часовом поясе магазина.",
    ),
    "month": T("The month.", "Oy.", "Месяц."),
    "revenue": T("Sales revenue.", "Sotuv tushumi.", "Выручка от продаж."),
    "orders": T("Completed sales.", "Yakunlangan sotuvlar.", "Проведённые продажи."),
    "margin": T(
        "Revenue minus the cost of the goods sold.",
        "Tushum minus sotilgan tovar tannarxi.",
        "Выручка минус себестоимость проданного.",
    ),
    "quantity_sold": T("Units sold.", "Sotilgan dona.", "Продано единиц."),
    "count": T("Number of payments.", "To'lovlar soni.", "Количество оплат."),
    # ----------------------------------------------------------------- reports
    "report_type": T("Which report.", "Qaysi hisobot.", "Какой отчёт."),
    "export_format": T("File format.", "Fayl formati.", "Формат файла."),
    "date_from": T("First day included.", "Kiritiladigan birinchi kun.", "Первый включаемый день."),
    "date_to": T("Last day included.", "Kiritiladigan oxirgi kun.", "Последний включаемый день."),
    "params": T(
        "The parameters the report was requested with.",
        "Hisobot so'ralgan parametrlar.",
        "Параметры, с которыми запрошен отчёт.",
    ),
    "file_size_bytes": T(
        "Size of the generated file.", "Tayyorlangan fayl hajmi.", "Размер сформированного файла."
    ),
    "error_message": T(
        "Why generation failed.",
        "Tayyorlash nima uchun muvaffaqiyatsiz bo'lgani.",
        "Почему формирование не удалось.",
    ),
    "started_at": T(
        "When the worker started on it.",
        "Ishlov berish boshlangan vaqt.",
        "Когда началась обработка.",
    ),
    "expires_at": T(
        "After this the file is deleted and the report must be requested again.",
        "Shundan keyin fayl o'chiriladi va hisobotni qayta so'rash kerak.",
        "После этого файл удаляется и отчёт нужно запросить заново.",
    ),
    "is_downloadable": T(
        "Ready and not yet expired.", "Tayyor va muddati tugamagan.", "Готов и ещё не истёк."
    ),
    # ----------------------------------------------------------------- billing
    "plan_id": T("Plan ID.", "Tarif ID.", "ID тарифа."),
    "plan_code": T(
        "Plan code, e.g. `basic`.", "Tarif kodi, masalan `basic`.", "Код тарифа, например `basic`."
    ),
    "plan_name": T("Plan name.", "Tarif nomi.", "Название тарифа."),
    "billing_cycle": T(
        "Billed monthly or yearly.", "Oylik yoki yillik to'lov.", "Оплата помесячно или за год."
    ),
    "subscription_status": T("Subscription status.", "Obuna holati.", "Статус подписки."),
    "current_period_end": T(
        "When the paid period ends.",
        "To'langan davr tugaydigan vaqt.",
        "Когда заканчивается оплаченный период.",
    ),
    "trial_ends_at": T(
        "When the free trial ends.",
        "Bepul sinov tugaydigan vaqt.",
        "Когда заканчивается пробный период.",
    ),
    "cancel_at_period_end": T(
        "The subscription will not renew.", "Obuna yangilanmaydi.", "Подписка не будет продлена."
    ),
    "grace_days_remaining": T(
        "Days left to pay an overdue invoice before the shop is suspended.",
        "Do'kon bloklanishidan oldin kechikkan hisobni to'lash uchun qolgan kunlar.",
        "Сколько дней осталось оплатить просроченный счёт до блокировки магазина.",
    ),
    "outstanding": T(
        "The invoice currently awaiting payment, if any.",
        "Hozir to'lov kutayotgan hisob-faktura (bo'lsa).",
        "Счёт, ожидающий оплаты, если есть.",
    ),
    "pay_links": T(
        "Where the outstanding invoice can be paid.",
        "To'lanmagan hisobni qayerda to'lash mumkin.",
        "Где можно оплатить неоплаченный счёт.",
    ),
    "invoices": T(
        "Recent invoices, newest first.",
        "So'nggi hisob-fakturalar, eng yangisi birinchi.",
        "Последние счета, новые первыми.",
    ),
    "number": T("Invoice number.", "Hisob-faktura raqami.", "Номер счёта."),
    "amount_due": T("Amount to pay.", "To'lanishi kerak bo'lgan summa.", "Сумма к оплате."),
    "amount_paid": T(
        "Amount paid so far.", "Hozirgacha to'langan summa.", "Оплачено на данный момент."
    ),
    "period_start": T(
        "Start of the billed period.", "Hisoblangan davr boshi.", "Начало оплачиваемого периода."
    ),
    "period_end": T(
        "End of the billed period.", "Hisoblangan davr oxiri.", "Конец оплачиваемого периода."
    ),
    "issued_at": T(
        "When the invoice was issued.", "Hisob-faktura chiqarilgan vaqt.", "Когда выставлен счёт."
    ),
    "paid_at": T(
        "When it was paid; null if unpaid.",
        "To'langan vaqt; to'lanmagan bo'lsa null.",
        "Когда оплачен; null, если не оплачен.",
    ),
    "provider": T(
        "Payment provider: `payme` or `click`.",
        "To'lov tizimi: `payme` yoki `click`.",
        "Платёжная система: `payme` или `click`.",
    ),
    "label": T("Button text.", "Tugma matni.", "Текст кнопки."),
    "url": T("Checkout link.", "To'lov sahifasi havolasi.", "Ссылка на страницу оплаты."),
    # ---------------------------------------------------------------- platform
    "total_tenants": T("All shops.", "Barcha do'konlar.", "Все магазины."),
    "active_tenants": T("Paying shops.", "To'lov qilayotgan do'konlar.", "Платящие магазины."),
    "trialing_tenants": T(
        "Shops in their free trial.", "Bepul sinovdagi do'konlar.", "Магазины на пробном периоде."
    ),
    "suspended_tenants": T("Blocked shops.", "Bloklangan do'konlar.", "Заблокированные магазины."),
    "mrr": T(
        "Monthly recurring revenue.",
        "Oylik takroriy daromad (MRR).",
        "Ежемесячная регулярная выручка (MRR).",
    ),
    "arr": T(
        "Annual recurring revenue: MRR × 12.",
        "Yillik takroriy daromad: MRR × 12.",
        "Годовая регулярная выручка: MRR × 12.",
    ),
    "trial_pipeline_mrr": T(
        "MRR if every shop now in trial converted to paid.",
        "Hozir sinovdagi barcha do'konlar pullik bo'lsa, qo'shiladigan MRR.",
        "MRR, если все магазины на пробном периоде перейдут на оплату.",
    ),
    "new_tenants_this_month": T(
        "Shops signed up this month.",
        "Shu oy ro'yxatdan o'tgan do'konlar.",
        "Магазины, зарегистрированные в этом месяце.",
    ),
    "churned_this_month": T(
        "Shops that left this month.",
        "Shu oy ketgan do'konlar.",
        "Магазины, ушедшие в этом месяце.",
    ),
    "total_users": T(
        "Staff accounts across all shops.",
        "Barcha do'konlardagi xodim hisoblari.",
        "Учётные записи сотрудников во всех магазинах.",
    ),
    "gmv_last_30_days": T(
        "Gross merchandise value: sales across all shops in the last 30 days.",
        "Umumiy savdo hajmi (GMV): oxirgi 30 kunda barcha do'konlardagi sotuvlar.",
        "Валовой объём продаж (GMV): продажи всех магазинов за последние 30 дней.",
    ),
    "tenants": T(
        "Paying shops at the end of the month.",
        "Oy oxiridagi to'lov qiluvchi do'konlar.",
        "Платящие магазины на конец месяца.",
    ),
    "activate": T(
        "Start the paid plan now instead of continuing the trial.",
        "Sinovni davom ettirish o'rniga pullik tarifni hozir boshlash.",
        "Начать платный тариф сейчас, не продолжая пробный период.",
    ),
    "price_monthly": T("Price per month.", "Oylik narx.", "Цена в месяц."),
    "price_yearly": T("Price per year.", "Yillik narx.", "Цена в год."),
    "trial_days": T(
        "Length of the free trial.",
        "Bepul sinov davomiyligi (kun).",
        "Длительность пробного периода (дней).",
    ),
    "max_branches": T(
        "Branch limit; null means unlimited.",
        "Filiallar chegarasi; null — cheksiz.",
        "Лимит филиалов; null — без ограничений.",
    ),
    "max_users": T(
        "Staff limit; null means unlimited.",
        "Xodimlar chegarasi; null — cheksiz.",
        "Лимит сотрудников; null — без ограничений.",
    ),
    "max_products": T(
        "Product limit; null means unlimited.",
        "Mahsulotlar chegarasi; null — cheksiz.",
        "Лимит товаров; null — без ограничений.",
    ),
    "max_orders_per_month": T(
        "Monthly sales limit; null means unlimited.",
        "Oylik sotuvlar chegarasi; null — cheksiz.",
        "Лимит продаж в месяц; null — без ограничений.",
    ),
    "features": T(
        "Feature switches, e.g. `pdf_reports`, `multi_branch`, `api_access`.",
        "Imkoniyat kalitlari, masalan `pdf_reports`, `multi_branch`, `api_access`.",
        "Переключатели возможностей, например `pdf_reports`, `multi_branch`, `api_access`.",
    ),
    "is_public": T(
        "Offered on the public sign-up page.",
        "Ochiq ro'yxatdan o'tish sahifasida taklif qilinadi.",
        "Предлагается на публичной странице регистрации.",
    ),
    "subscriber_count": T(
        "Shops on this plan.", "Shu tarifdagi do'konlar.", "Магазины на этом тарифе."
    ),
}

FIELD_OVERRIDES: dict[str, T] = {
    "ErrorResponse.code": T(
        "Stable machine-readable error code, e.g. `sku_taken`. Branch on this.",
        "O'zgarmas xato kodi, masalan `sku_taken`. Dasturda shu bo'yicha tarmoqlaning.",
        "Стабильный машиночитаемый код ошибки, например `sku_taken`. Ветвитесь по нему.",
    ),
    "ErrorResponse.message": T(
        "Explanation for people. May change; do not branch on it.",
        "Odamlar uchun tushuntirish. O'zgarishi mumkin; dasturda unga tayanmang.",
        "Пояснение для людей. Может меняться; не ветвитесь по нему.",
    ),
    "BranchIn.code": T(
        "Short branch code, e.g. `CHL`. Normalised to upper case, prefixes every receipt number, and cannot change later.",
        "Qisqa filial kodi, masalan `CHL`. Katta harfga o'tkaziladi, har bir chek raqami boshida turadi va keyin o'zgarmaydi.",
        "Короткий код филиала, например `CHL`. Приводится к верхнему регистру, начинает каждый номер чека и не меняется.",
    ),
    "BranchOut.code": T(
        "Short branch code that prefixes every receipt number.",
        "Har bir chek raqami boshida turadigan qisqa filial kodi.",
        "Короткий код филиала, с которого начинается каждый номер чека.",
    ),
    "PlanIn.code": T(
        "Unique plan code shops sign up with, e.g. `basic`. Cannot change later.",
        "Do'konlar ro'yxatdan o'tadigan noyob tarif kodi, masalan `basic`. Keyin o'zgarmaydi.",
        "Уникальный код тарифа для регистрации, например `basic`. Не меняется.",
    ),
    "PlanOut.code": T(
        "Unique plan code shops sign up with.",
        "Do'konlar ro'yxatdan o'tadigan noyob tarif kodi.",
        "Уникальный код тарифа для регистрации.",
    ),
    "PlanOut.mrr": T(
        "Monthly recurring revenue from this plan's paying shops.",
        "Shu tarifdagi to'lov qiluvchi do'konlardan oylik takroriy daromad.",
        "Ежемесячная регулярная выручка от платящих магазинов на тарифе.",
    ),
    "TenantSummary.mrr": T(
        "What this shop pays per month on its current plan.",
        "Bu do'kon joriy tarifi bo'yicha oyiga to'laydigan summa.",
        "Сколько магазин платит в месяц по текущему тарифу.",
    ),
    "TenantSummary.status": T("The shop's status.", "Do'kon holati.", "Статус магазина."),
    "ShopSettings.status": T(
        "The shop's status on the platform.",
        "Do'konning platformadagi holati.",
        "Статус магазина на платформе.",
    ),
    "TenantStatusUpdate.status": T(
        "The status to set.", "O'rnatiladigan holat.", "Устанавливаемый статус."
    ),
    "TenantStatusUpdate.reason": T(
        "Why the shop is blocked; shown to its staff when they try to sign in.",
        "Do'kon nima uchun bloklangani; xodimlar kirishga uringanda ko'rsatiladi.",
        "Почему магазин заблокирован; показывается сотрудникам при попытке входа.",
    ),
    "BillingOverview.status": T("Subscription status.", "Obuna holati.", "Статус подписки."),
    "BillingOverview.amount": T(
        "Plan price for one billing cycle.",
        "Bir to'lov davri uchun tarif narxi.",
        "Цена тарифа за один период оплаты.",
    ),
    "PaymentIn.amount": T(
        "Amount paid by this method. Payments together must cover the order total; for cash, the excess is returned as change.",
        "Shu usulda to'langan summa. To'lovlar birgalikda buyurtma jamisini qoplashi kerak; naqd pulda ortig'i qaytim sifatida qaytariladi.",
        "Сумма, оплаченная этим способом. Вместе оплаты должны покрыть итог заказа; излишек наличными возвращается сдачей.",
    ),
    "StockAdjustIn.quantity": T(
        "Signed change: positive adds stock (a delivery), negative removes it (waste, a correction).",
        "Ishorali o'zgarish: musbat qoldiq qo'shadi (yetkazib berish), manfiy ayiradi (chiqim, tuzatish).",
        "Изменение со знаком: плюс добавляет (поставка), минус убирает (списание, корректировка).",
    ),
    "StockMovementOut.quantity": T(
        "Signed change: positive in, negative out.",
        "Ishorali o'zgarish: musbat — kirim, manfiy — chiqim.",
        "Изменение со знаком: плюс — приход, минус — расход.",
    ),
    "StockLevelOut.quantity": T("Quantity on hand.", "Mavjud qoldiq.", "Количество в наличии."),
    "ProductListItem.cost_price": T(
        "Purchase cost per unit. Null unless the caller holds `product.cost.read`.",
        "Bir birlik xarid narxi. Chaqiruvchida `product.cost.read` ruxsati bo'lmasa null.",
        "Закупочная цена за единицу. null, если у вызывающего нет права `product.cost.read`.",
    ),
    "TaxRateIn.is_default": T(
        "The rate new products get unless another is chosen. Only one rate is the default.",
        "Boshqasi tanlanmasa, yangi mahsulotlarga beriladigan stavka. Faqat bitta stavka asosiy bo'ladi.",
        "Ставка для новых товаров, если не выбрана другая. По умолчанию — только одна ставка.",
    ),
    "TaxRateOut.is_default": T(
        "The rate new products get unless another is chosen.",
        "Boshqasi tanlanmasa, yangi mahsulotlarga beriladigan stavka.",
        "Ставка для новых товаров, если не выбрана другая.",
    ),
    "TaxRateUpdate.is_default": T(
        "Make this the default rate; the previous default stops being one.",
        "Buni asosiy stavka qilish; oldingi asosiy stavka asosiy bo'lmay qoladi.",
        "Сделать ставкой по умолчанию; прежняя перестаёт ею быть.",
    ),
    "SessionInfo.tenant_slug": T(
        "The shop this session belongs to; null for platform staff.",
        "Shu sessiya tegishli do'kon; platforma xodimlari uchun null.",
        "Магазин, к которому относится сессия; null для сотрудников платформы.",
    ),
    "SessionInfo.currency": T(
        "The shop's currency; null for platform staff.",
        "Do'kon valyutasi; platforma xodimlari uchun null.",
        "Валюта магазина; null для сотрудников платформы.",
    ),
    "CategoryOut.slug": T(
        "URL-safe form of the name, unique within the shop.",
        "Nomning URL uchun xavfsiz shakli, do'kon ichida noyob.",
        "Безопасная для URL форма названия, уникальная в магазине.",
    ),
    "OrderItemOut.product_name": T(
        "Product name as sold — a snapshot, so renaming the product later does not change past receipts.",
        "Sotilgan paytdagi mahsulot nomi — nusxa, mahsulot keyin qayta nomlansa ham o'tgan cheklar o'zgarmaydi.",
        "Название товара на момент продажи — снимок, поэтому переименование не меняет прошлые чеки.",
    ),
    "EmployeeIn.password": T(
        "The password they first sign in with. They can change it afterwards.",
        "Birinchi kirish uchun parol. Keyin uni o'zgartirishi mumkin.",
        "Пароль для первого входа. Потом его можно сменить.",
    ),
    "RefundCreate.lines": T(
        "Lines and quantities to return. Leave empty to refund everything still refundable.",
        "Qaytariladigan qatorlar va miqdorlar. Hali qaytarish mumkin bo'lgan hammasini qaytarish uchun bo'sh qoldiring.",
        "Строки и количества к возврату. Оставьте пустым, чтобы вернуть всё, что ещё можно.",
    ),
    "RefundOut.lines": T(
        "What was returned, line by line.",
        "Nima qaytarilgani, qatorma-qator.",
        "Что возвращено, построчно.",
    ),
    "OrderRefundView.lines": T(
        "Every line of the order and what is still returnable on it.",
        "Buyurtmaning har bir qatori va undan hali qaytarish mumkin bo'lgan qismi.",
        "Каждая строка заказа и что по ней ещё можно вернуть.",
    ),
    "BranchUpdate.is_active": T(
        "Deactivate a branch without closing it. The default branch cannot be deactivated.",
        "Filialni yopmasdan faolsizlantirish. Asosiy filialni faolsizlantirib bo'lmaydi.",
        "Деактивировать филиал, не закрывая его. Филиал по умолчанию деактивировать нельзя.",
    ),
    "EmployeeUpdate.is_active": T(
        "Deactivating someone signs them out everywhere immediately.",
        "Xodimni faolsizlantirish uni darhol barcha qurilmalardan chiqaradi.",
        "Деактивация сразу завершает все сессии сотрудника.",
    ),
}
