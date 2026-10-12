"""Every endpoint's summary, description and business error codes, in three
languages. Keys are operation ids: `<tag>_<function name>`.

Who may call an endpoint is *not* written here: it is read off the route's own
guard (see `app.docs.openapi._access`), so it cannot disagree with the code.
"""

from __future__ import annotations

from typing import NamedTuple

from app.docs.i18n.base import T


class Op(NamedTuple):
    summary: T
    description: T
    # HTTP status -> business error codes this endpoint can answer with.
    errors: dict[int, tuple[str, ...]] | None = None


OPERATIONS: dict[str, Op] = {
    # ------------------------------------------------------------------- auth
    "auth_signup": Op(
        T(
            "Register a new shop",
            "Yangi do'konni ro'yxatdan o'tkazish",
            "Регистрация нового магазина",
        ),
        T(
            "Creates the shop, its owner account, a first branch and a trial subscription on the chosen plan. The owner then signs in with `POST /auth/login`, using the chosen `slug` as `tenant_slug`.",
            "Do'kon, uning egasi hisobi, birinchi filial va tanlangan tarif bo'yicha sinov obunasini yaratadi. Keyin ega tanlangan `slug` ni `tenant_slug` sifatida ishlatib, `POST /auth/login` orqali kiradi.",
            "Создаёт магазин, учётную запись владельца, первый филиал и пробную подписку на выбранном тарифе. Затем владелец входит через `POST /auth/login`, указав выбранный `slug` как `tenant_slug`.",
        ),
        {404: ("plan_not_found",), 409: ("slug_taken",)},
    ),
    "auth_login": Op(
        T("Sign in", "Tizimga kirish", "Вход"),
        T(
            "Exchanges email and password for a token pair. Shop staff must send `tenant_slug`; platform staff leave it out. Five wrong passwords in a row lock the account for 15 minutes.",
            "Email va parolni token juftligiga almashtiradi. Do'kon xodimlari `tenant_slug` ni yuborishi shart; platforma xodimlari yubormaydi. Ketma-ket beshta noto'g'ri parol hisobni 15 daqiqaga bloklaydi.",
            "Обменивает email и пароль на пару токенов. Сотрудники магазина обязаны передать `tenant_slug`; сотрудники платформы его не передают. Пять неверных паролей подряд блокируют учётную запись на 15 минут.",
        ),
        {
            401: ("invalid_credentials", "account_locked"),
            403: ("tenant_inactive",),
            404: ("tenant_not_found",),
        },
    ),
    "auth_pin_login": Op(
        T("Switch cashier by PIN", "PIN orqali kassirni almashtirish", "Смена кассира по PIN"),
        T(
            "Signs a different member of staff in on a shared terminal with their PIN, without typing a password. Call it with the terminal's current session token and pick the person from `GET /auth/terminal/staff`. Wrong PINs count towards the same lockout as passwords.",
            "Umumiy terminalda boshqa xodimni parol yozmasdan, uning PIN'i bilan tizimga kiritadi. Terminalning joriy sessiya tokeni bilan chaqiring va xodimni `GET /auth/terminal/staff` dan tanlang. Noto'g'ri PIN'lar parol bilan bir xil bloklash hisobiga qo'shiladi.",
            "Входит другим сотрудником на общем терминале по его PIN, без ввода пароля. Вызывайте с токеном текущей сессии терминала, сотрудника выбирайте из `GET /auth/terminal/staff`. Неверные PIN учитываются в той же блокировке, что и пароли.",
        ),
        {401: ("invalid_credentials", "account_locked")},
    ),
    "auth_terminal_staff": Op(
        T("Staff for the PIN screen", "PIN ekrani uchun xodimlar", "Сотрудники для экрана PIN"),
        T(
            "Names, roles and avatars of the shop's active staff, for the terminal's who-are-you screen. Email addresses are deliberately left out.",
            "Terminalning kimligingizni tanlash ekrani uchun do'kondagi faol xodimlarning ismlari, rollari va avatarlari. Email manzillar ataylab qo'shilmagan.",
            "Имена, роли и аватары активных сотрудников магазина для экрана выбора на терминале. Email намеренно не включены.",
        ),
    ),
    "auth_refresh": Op(
        T("Renew the session", "Sessiyani yangilash", "Обновление сессии"),
        T(
            "Exchanges a refresh token for a new token pair; the old refresh token stops working. Presenting a refresh token that was already used is treated as theft, and every session of the account is revoked.",
            "Refresh tokenni yangi token juftligiga almashtiradi; eski refresh token ishlamay qoladi. Allaqachon ishlatilgan refresh token yuborilsa, bu o'g'irlik deb qaraladi va hisobning barcha sessiyalari bekor qilinadi.",
            "Обменивает refresh-токен на новую пару; старый перестаёт работать. Повторно использованный refresh-токен считается украденным, и все сессии учётной записи отзываются.",
        ),
        {401: ("invalid_credentials",), 403: ("tenant_inactive",)},
    ),
    "auth_logout": Op(
        T("Sign out", "Tizimdan chiqish", "Выход"),
        T(
            "Revokes the given refresh token. The access token stays valid until it expires, so the client should discard it too.",
            "Berilgan refresh tokenni bekor qiladi. Access token muddati tugaguncha amal qiladi, shuning uchun mijoz ilovasi uni ham o'chirishi kerak.",
            "Отзывает переданный refresh-токен. Access-токен действует до истечения срока, поэтому клиенту следует удалить и его.",
        ),
    ),
    "auth_me": Op(
        T("Current session", "Joriy sessiya", "Текущая сессия"),
        T(
            "The signed-in user, their shop, the shop's currency and the exact set of permissions they hold. Decide what to show from this — the API refuses exactly the same things.",
            "Tizimga kirgan foydalanuvchi, uning do'koni, do'kon valyutasi va aniq ruxsatlari. Nimani ko'rsatishni shunga qarab hal qiling — API ham aynan shularni rad etadi.",
            "Вошедший пользователь, его магазин, валюта магазина и точный набор прав. По нему решайте, что показывать, — API отказывает ровно в том же.",
        ),
    ),
    "auth_update_me": Op(
        T("Update your profile", "Profilingizni yangilash", "Изменение своего профиля"),
        T(
            "Changes your own name, phone and avatar. Role, branch and permissions cannot be changed here — they are granted by an owner, and any such fields sent are ignored.",
            "O'z ismingiz, telefoningiz va avataringizni o'zgartiradi. Rol, filial va ruxsatlarni bu yerda o'zgartirib bo'lmaydi — ularni ega beradi, bunday maydonlar yuborilsa e'tiborsiz qoldiriladi.",
            "Меняет ваше имя, телефон и аватар. Роль, филиал и права здесь изменить нельзя — их назначает владелец, и такие поля игнорируются.",
        ),
    ),
    "auth_change_password": Op(
        T("Change your password", "Parolni o'zgartirish", "Смена пароля"),
        T(
            "Sets a new password after checking the current one, and signs you out on every other device.",
            "Joriy parolni tekshirgandan so'ng yangi parol o'rnatadi va boshqa barcha qurilmalardan chiqaradi.",
            "Устанавливает новый пароль после проверки текущего и завершает сессии на всех остальных устройствах.",
        ),
        {401: ("invalid_credentials",)},
    ),
    "auth_set_pin": Op(
        T("Set your PIN", "PIN o'rnatish", "Установка PIN"),
        T(
            "Sets or replaces your terminal PIN, used to switch cashiers on a shared terminal without typing a password.",
            "Terminal PIN'ingizni o'rnatadi yoki almashtiradi; u umumiy terminalda parol yozmasdan kassirni almashtirish uchun ishlatiladi.",
            "Устанавливает или заменяет PIN-код терминала — им меняют кассира на общем терминале без ввода пароля.",
        ),
    ),
    "auth_forgot_password": Op(
        T("Request a password reset", "Parolni tiklashni so'rash", "Запрос сброса пароля"),
        T(
            "Emails a reset link valid for 60 minutes. The answer is the same whether or not the address has an account, so this cannot be used to find out who works at a shop.",
            "60 daqiqa amal qiladigan tiklash havolasini emailga yuboradi. Manzil ro'yxatda bormi-yo'qmi, javob bir xil — shuning uchun bu orqali do'konda kim ishlashini bilib bo'lmaydi.",
            "Отправляет ссылку для сброса, действующую 60 минут. Ответ одинаков, есть ли такой адрес или нет, — так нельзя узнать, кто работает в магазине.",
        ),
    ),
    "auth_reset_password": Op(
        T("Reset the password", "Parolni tiklash", "Сброс пароля"),
        T(
            "Sets a new password using the token from the emailed link. The token works once and expires 60 minutes after it was sent.",
            "Emaildagi havola tokeni yordamida yangi parol o'rnatadi. Token bir marta ishlaydi va yuborilganidan 60 daqiqa o'tgach eskiradi.",
            "Устанавливает новый пароль по токену из письма. Токен работает один раз и истекает через 60 минут после отправки.",
        ),
        {401: ("invalid_reset_token",)},
    ),
    # ---------------------------------------------------------------- catalog
    "catalog_list_categories": Op(
        T("List categories", "Kategoriyalar ro'yxati", "Список категорий"),
        T(
            "The shop's categories, in grid order.",
            "Do'kon kategoriyalari, paneldagi tartibda.",
            "Категории магазина в порядке отображения.",
        ),
    ),
    "catalog_create_category": Op(
        T("Create a category", "Kategoriya yaratish", "Создание категории"),
        T(
            "Adds a category. Names must be unique within the shop.",
            "Kategoriya qo'shadi. Nomlar do'kon ichida noyob bo'lishi kerak.",
            "Добавляет категорию. Названия должны быть уникальны в магазине.",
        ),
        {409: ("slug_taken",)},
    ),
    "catalog_update_category": Op(
        T("Update a category", "Kategoriyani yangilash", "Изменение категории"),
        T(
            "Changes a category; only the fields sent change. A category cannot be made its own parent.",
            "Kategoriyani o'zgartiradi; faqat yuborilgan maydonlar o'zgaradi. Kategoriya o'ziga o'zi ota bo'la olmaydi.",
            "Изменяет категорию; меняются только переданные поля. Категория не может быть родителем самой себя.",
        ),
        {409: ("cyclic_parent",)},
    ),
    "catalog_delete_category": Op(
        T("Delete a category", "Kategoriyani o'chirish", "Удаление категории"),
        T("Removes the category.", "Kategoriyani olib tashlaydi.", "Удаляет категорию."),
    ),
    "catalog_list_products": Op(
        T("List products", "Mahsulotlar ro'yxati", "Список товаров"),
        T(
            "The catalog, paginated and searchable by name, SKU or barcode. Stock figures are for `branch_id`, or your own branch. Cost prices appear only for callers holding `product.cost.read`.",
            "Sahifalangan katalog; nom, SKU yoki shtrix-kod bo'yicha qidiriladi. Qoldiq `branch_id` filiali yoki o'z filialingiz uchun. Tannarx faqat `product.cost.read` ruxsati borlarga ko'rinadi.",
            "Каталог с пагинацией и поиском по названию, артикулу или штрихкоду. Остатки — по `branch_id` или вашему филиалу. Себестоимость видна только при праве `product.cost.read`.",
        ),
    ),
    "catalog_create_product": Op(
        T("Create a product", "Mahsulot yaratish", "Создание товара"),
        T(
            "Adds a product. SKU and barcode must be unique within the shop. Send `opening_stock` to record what is already on the shelf at your branch in the same step. Limited by the plan.",
            "Mahsulot qo'shadi. SKU va shtrix-kod do'kon ichida noyob bo'lishi kerak. Filialingizda javonda turgan miqdorni shu qadamda yozish uchun `opening_stock` ni yuboring. Tarif bilan cheklangan.",
            "Добавляет товар. Артикул и штрихкод должны быть уникальны в магазине. Передайте `opening_stock`, чтобы сразу записать остаток на полке вашего филиала. Ограничено тарифом.",
        ),
        {402: ("quota_exceeded",), 409: ("sku_taken", "barcode_taken")},
    ),
    "catalog_lookup_by_code": Op(
        T("Look up a scanned code", "Skanerlangan kodni topish", "Поиск по отсканированному коду"),
        T(
            "Resolves a barcode, a carton barcode or a SKU to a product in one step — the call a scanner makes on every beep. A carton barcode returns its `pack_size`, so one scan can add a whole case.",
            "Shtrix-kod, quti kodi yoki SKU ni bir qadamda mahsulotga aylantiradi — skaner har bir signalida shu chaqiruvni qiladi. Quti kodi `pack_size` ni qaytaradi, shuning uchun bitta skan butun qutini qo'shishi mumkin.",
            "Сопоставляет штрихкод, код упаковки или артикул с товаром за один шаг — этот запрос сканер делает при каждом срабатывании. Код упаковки возвращает `pack_size`, поэтому одно сканирование может добавить целую коробку.",
        ),
        {404: ("product_not_found",)},
    ),
    "catalog_get_product": Op(
        T("Get a product", "Mahsulotni olish", "Получение товара"),
        T(
            "One product with everything needed to edit it.",
            "Tahrirlash uchun kerakli hamma ma'lumoti bilan bitta mahsulot.",
            "Один товар со всеми данными для редактирования.",
        ),
    ),
    "catalog_update_product": Op(
        T("Update a product", "Mahsulotni yangilash", "Изменение товара"),
        T(
            "Changes a product; only the fields sent change. A new price applies to future sales — receipts already issued keep the price they were sold at.",
            "Mahsulotni o'zgartiradi; faqat yuborilgan maydonlar o'zgaradi. Yangi narx kelgusi sotuvlarga qo'llanadi — berilgan cheklar sotilgan narxini saqlaydi.",
            "Изменяет товар; меняются только переданные поля. Новая цена действует для будущих продаж — уже выданные чеки сохраняют цену продажи.",
        ),
        {409: ("sku_taken", "barcode_taken")},
    ),
    "catalog_delete_product": Op(
        T("Delete a product", "Mahsulotni o'chirish", "Удаление товара"),
        T(
            "Takes a product off the catalog and the POS grid. Its sales history stays, so past receipts still print.",
            "Mahsulotni katalog va POS panelidan olib tashlaydi. Sotuvlar tarixi saqlanadi — o'tgan cheklar hamon chop etiladi.",
            "Убирает товар из каталога и с экрана кассы. История продаж сохраняется, поэтому прошлые чеки по-прежнему печатаются.",
        ),
    ),
    "catalog_list_tax_rates": Op(
        T("List tax rates", "Soliq stavkalari ro'yxati", "Список налоговых ставок"),
        T("The shop's tax rates.", "Do'konning soliq stavkalari.", "Налоговые ставки магазина."),
    ),
    "catalog_create_tax_rate": Op(
        T("Create a tax rate", "Soliq stavkasini yaratish", "Создание налоговой ставки"),
        T(
            "Adds a tax rate. `rate` is a fraction: `0.12` for 12%.",
            "Soliq stavkasini qo'shadi. `rate` — kasr: 12% uchun `0.12`.",
            "Добавляет налоговую ставку. `rate` — дробь: `0.12` для 12%.",
        ),
        {409: ("name_taken",)},
    ),
    # -------------------------------------------------------------- inventory
    "inventory_stock_levels": Op(
        T("Stock levels", "Qoldiqlar", "Остатки"),
        T(
            "On-hand, reserved and available quantities per product at a branch, with stock value. `low_only` narrows it to what needs reordering.",
            "Filialdagi har bir mahsulot bo'yicha mavjud, zaxiradagi va sotish mumkin bo'lgan miqdor hamda qoldiq qiymati. `low_only` faqat qayta buyurtma kerak bo'lganlarni qoldiradi.",
            "Количество в наличии, в резерве и доступное по каждому товару филиала, со стоимостью остатков. `low_only` оставляет только то, что пора дозаказать.",
        ),
    ),
    "inventory_adjust_stock": Op(
        T("Adjust stock", "Qoldiqni o'zgartirish", "Корректировка остатка"),
        T(
            "Records a delivery, a write-off or a correction as a signed quantity. Every change goes through the movement ledger; stock is never edited directly.",
            "Yetkazib berish, hisobdan chiqarish yoki tuzatishni ishorali miqdor sifatida yozadi. Har bir o'zgarish harakatlar daftari orqali o'tadi; qoldiq hech qachon to'g'ridan-to'g'ri tahrirlanmaydi.",
            "Записывает поставку, списание или корректировку как количество со знаком. Каждое изменение проходит через журнал движений; остаток никогда не правится напрямую.",
        ),
        {404: ("product_not_found",)},
    ),
    "inventory_record_count": Op(
        T("Record a stocktake", "Inventarizatsiyani yozish", "Запись инвентаризации"),
        T(
            "Sets stock to what was physically counted and records the difference as an adjustment — the shrinkage figure.",
            "Qoldiqni haqiqatda sanalgan miqdorga tenglashtiradi va farqni tuzatish sifatida yozadi — bu yo'qotish ko'rsatkichi.",
            "Устанавливает остаток по фактическому пересчёту и записывает разницу как корректировку — это показатель недостачи.",
        ),
        {404: ("product_not_found",)},
    ),
    "inventory_list_movements": Op(
        T("Stock movements", "Qoldiq harakatlari", "Движения товара"),
        T(
            "The append-only ledger of every stock change, with the balance after each one.",
            "Har bir qoldiq o'zgarishining faqat qo'shiladigan daftari, har biridan keyingi balans bilan.",
            "Журнал всех изменений остатка, куда только добавляют, с остатком после каждого.",
        ),
    ),
    # ----------------------------------------------------------------- orders
    "orders_create_order": Op(
        T("Complete a sale", "Sotuvni yakunlash", "Проведение продажи"),
        T(
            "Takes payment and completes a sale in one step: prices, discounts and tax are calculated on the server, stock is taken down and the receipt number is assigned. Requires an open shift and a current subscription. Discounts additionally need `order.discount`. Send an `idempotency_key` so that a retry after a timeout never charges twice.",
            "To'lovni qabul qiladi va sotuvni bitta qadamda yakunlaydi: narx, chegirma va soliq serverda hisoblanadi, qoldiq kamaytiriladi va chek raqami beriladi. Ochiq smena va amaldagi obuna talab qilinadi. Chegirmalar uchun qo'shimcha `order.discount` ruxsati kerak. Timeout'dan keyin qayta urinish ikki marta pul olmasligi uchun `idempotency_key` yuboring.",
            "Принимает оплату и проводит продажу за один шаг: цены, скидки и налог считаются на сервере, остаток уменьшается, присваивается номер чека. Нужны открытая смена и действующая подписка. Для скидок дополнительно требуется `order.discount`. Передавайте `idempotency_key`, чтобы повтор после таймаута не списал деньги дважды.",
        ),
        {
            400: ("payment_mismatch", "empty_cart"),
            402: ("subscription_required",),
            404: ("product_not_found",),
            409: ("insufficient_stock", "no_open_shift"),
        },
    ),
    "orders_list_orders": Op(
        T("List sales", "Sotuvlar ro'yxati", "Список продаж"),
        T(
            "Completed sales, newest first. Cashiers see only their own; `order.read_all` shows the whole shop.",
            "Yakunlangan sotuvlar, eng yangisi birinchi. Kassirlar faqat o'z sotuvlarini ko'radi; `order.read_all` butun do'konni ko'rsatadi.",
            "Проведённые продажи, новые первыми. Кассиры видят только свои; с `order.read_all` — все продажи магазина.",
        ),
    ),
    "orders_get_order": Op(
        T("Get a sale", "Sotuvni olish", "Получение продажи"),
        T(
            "One sale with its lines and payments.",
            "Qatorlari va to'lovlari bilan bitta sotuv.",
            "Одна продажа со строками и оплатами.",
        ),
    ),
    "orders_get_receipt": Op(
        T("Receipt for a sale", "Sotuv cheki", "Чек продажи"),
        T(
            "Everything the receipt shows, for reprinting on a thermal printer or as a PDF.",
            "Chekda ko'rinadigan hamma narsa — termoprinterda yoki PDF sifatida qayta chop etish uchun.",
            "Всё, что есть на чеке, — для повторной печати на термопринтере или в PDF.",
        ),
    ),
    "orders_refundable": Op(
        T("What can be refunded", "Nimani qaytarish mumkin", "Что можно вернуть"),
        T(
            "Each line of a sale with how much of it is still returnable, and the refunds already made. Show this before taking a refund.",
            "Sotuvning har bir qatori, undan yana qanchasini qaytarish mumkinligi va qilingan qaytarishlar. Qaytarishdan oldin shuni ko'rsating.",
            "Каждая строка продажи, сколько по ней ещё можно вернуть, и уже проведённые возвраты. Показывайте это перед оформлением возврата.",
        ),
    ),
    "orders_create_refund": Op(
        T("Refund a sale", "Sotuvni qaytarish", "Возврат по продаже"),
        T(
            "Returns money for some or all of a sale; leave `lines` empty to refund everything still refundable. Goods go back into stock unless `restock` is false. Requires an open shift, and cash refunds come out of that shift's drawer.",
            "Sotuvning bir qismi yoki hammasi uchun pulni qaytaradi; hali qaytarish mumkin bo'lgan hammasini qaytarish uchun `lines` ni bo'sh qoldiring. `restock` false bo'lmasa, tovar qoldiqqa qaytadi. Ochiq smena talab qilinadi; naqd qaytarishlar shu smena yashigidan chiqadi.",
            "Возвращает деньги за часть или всю продажу; оставьте `lines` пустым, чтобы вернуть всё, что ещё можно. Товар возвращается на склад, если `restock` не false. Нужна открытая смена; возвраты наличными выдаются из её ящика.",
        ),
        {
            400: ("refund_exceeds_order",),
            404: ("line_not_found",),
            409: ("order_not_refundable", "no_open_shift"),
        },
    ),
    # ----------------------------------------------------------------- shifts
    "shifts_current_shift": Op(
        T("Your open shift", "Ochiq smenangiz", "Ваша открытая смена"),
        T(
            "Your open shift at your branch, or `null` if you have none — the terminal uses this to choose between the till and the open-till screen.",
            "Filialingizdagi ochiq smenangiz yoki yo'q bo'lsa `null` — terminal shunga qarab kassani yoki kassani ochish ekranini ko'rsatadi.",
            "Ваша открытая смена в вашем филиале или `null`, если её нет, — по этому терминал решает, показать кассу или экран открытия.",
        ),
    ),
    "shifts_open_shift": Op(
        T("Open a shift", "Smenani ochish", "Открытие смены"),
        T(
            "Opens your till with the cash already in the drawer. Closing reconciles against this figure.",
            "Yashikdagi naqd pul bilan kassangizni ochadi. Yopishda hisob-kitob shu summaga nisbatan qilinadi.",
            "Открывает вашу кассу с наличными, уже лежащими в ящике. При закрытии сверка идёт от этой суммы.",
        ),
        {409: ("shift_already_open",)},
    ),
    "shifts_current_shift_summary": Op(
        T("Takings so far", "Hozirgacha tushum", "Выручка на данный момент"),
        T(
            "Sales, takings by method, refunds and the opening float of your open shift, for counting the drawer against before closing.",
            "Ochiq smenangizning sotuvlari, usullar bo'yicha tushumi, qaytarishlari va boshlang'ich puli — yopishdan oldin yashikni shunga qarab sanash uchun.",
            "Продажи, выручка по способам оплаты, возвраты и размен вашей открытой смены — для сверки ящика перед закрытием.",
        ),
        {404: ("no_open_shift",)},
    ),
    "shifts_close_current_shift": Op(
        T("Close your shift", "Smenani yopish", "Закрытие смены"),
        T(
            "Closes your till with the cash counted in the drawer. The response carries the difference: positive when the drawer holds more than expected, negative when it is short.",
            "Yashikda sanalgan naqd pul bilan kassangizni yopadi. Javobda farq bor: yashikda kutilgandan ko'p bo'lsa musbat, kam bo'lsa manfiy.",
            "Закрывает вашу кассу с пересчитанными наличными. В ответе — расхождение: плюс, если в ящике больше ожидаемого, минус — при недостаче.",
        ),
        {404: ("no_open_shift",)},
    ),
    "shifts_list_shifts": Op(
        T("Review shifts", "Smenalarni ko'rib chiqish", "Обзор смен"),
        T(
            "Every shift, newest first, with who worked it, what was taken and how the drawer reconciled. Filter by branch, cashier, status and dates; `date_to` includes that whole day.",
            "Har bir smena, eng yangisi birinchi: kim ishlagan, qancha tushum va yashik qanday hisob-kitob qilingan. Filial, kassir, holat va sana bo'yicha filtrlang; `date_to` o'sha kunni to'liq qamraydi.",
            "Все смены, новые первыми: кто работал, сколько принято и как сошлась касса. Фильтры по филиалу, кассиру, статусу и датам; `date_to` включает весь этот день.",
        ),
    ),
    # -------------------------------------------------------------- employees
    "employees_list_employees": Op(
        T("List staff", "Xodimlar ro'yxati", "Список сотрудников"),
        T(
            "Staff accounts, searchable by name or email. Deactivated accounts are hidden unless `include_inactive` is set.",
            "Xodim hisoblari; ism yoki email bo'yicha qidiriladi. `include_inactive` berilmasa, faolsizlantirilganlar yashiriladi.",
            "Учётные записи сотрудников с поиском по имени или email. Деактивированные скрыты, если не задан `include_inactive`.",
        ),
    ),
    "employees_create_employee": Op(
        T("Add a member of staff", "Xodim qo'shish", "Добавление сотрудника"),
        T(
            "Creates a staff account. Emails are unique within the shop, and only an owner can create another owner. Limited by the plan.",
            "Xodim hisobini yaratadi. Emaillar do'kon ichida noyob, boshqa egani faqat ega yarata oladi. Tarif bilan cheklangan.",
            "Создаёт учётную запись сотрудника. Email уникален в магазине, создать другого владельца может только владелец. Ограничено тарифом.",
        ),
        {402: ("quota_exceeded",), 409: ("email_taken",)},
    ),
    "employees_get_employee": Op(
        T("Get a member of staff", "Xodimni olish", "Получение сотрудника"),
        T(
            "One staff account with its effective permissions.",
            "Amaldagi ruxsatlari bilan bitta xodim hisobi.",
            "Одна учётная запись сотрудника с действующими правами.",
        ),
    ),
    "employees_update_employee": Op(
        T("Update a member of staff", "Xodimni yangilash", "Изменение сотрудника"),
        T(
            "Changes role, branch, phone, active status or permission overrides. Only an owner can manage an owner or promote someone to owner, and nobody can edit themselves here. Deactivating someone signs them out everywhere.",
            "Rol, filial, telefon, faollik holati yoki ruxsat o'zgartirishlarini o'zgartiradi. Egani boshqarish yoki ega darajasiga ko'tarish faqat egaga mumkin, bu yerda hech kim o'zini tahrirlay olmaydi. Faolsizlantirish xodimni hamma joydan chiqaradi.",
            "Меняет роль, филиал, телефон, активность или индивидуальные права. Управлять владельцем или повышать до владельца может только владелец, а себя здесь не редактирует никто. Деактивация завершает все сессии сотрудника.",
        ),
        {403: ("self_edit_blocked",)},
    ),
    "employees_delete_employee": Op(
        T("Remove a member of staff", "Xodimni o'chirish", "Удаление сотрудника"),
        T(
            "Removes a staff account. Sales they made stay in the history.",
            "Xodim hisobini o'chiradi. U qilgan sotuvlar tarixda qoladi.",
            "Удаляет учётную запись сотрудника. Проведённые им продажи остаются в истории.",
        ),
        {403: ("self_edit_blocked",)},
    ),
    "employees_reset_password": Op(
        T("Set a staff member's password", "Xodim parolini o'rnatish", "Смена пароля сотрудника"),
        T(
            "Sets a new password for a member of staff — for when they have forgotten theirs and an email reset is not an option.",
            "Xodim uchun yangi parol o'rnatadi — o'z parolini unutganda va email orqali tiklash imkoni bo'lmaganda.",
            "Задаёт сотруднику новый пароль — если он забыл свой, а сброс по email невозможен.",
        ),
        {403: ("self_edit_blocked",)},
    ),
    # ------------------------------------------------------------------- shop
    "shop_list_branches": Op(
        T("List branches", "Filiallar ro'yxati", "Список филиалов"),
        T(
            "The shop's branches, default first, with staff, product and 30-day sales counts.",
            "Do'kon filiallari, asosiysi birinchi, xodimlar, mahsulotlar va 30 kunlik sotuvlar soni bilan.",
            "Филиалы магазина, основной первым, с числом сотрудников, товаров и продаж за 30 дней.",
        ),
    ),
    "shop_create_branch": Op(
        T("Add a branch", "Filial qo'shish", "Добавление филиала"),
        T(
            "Adds a branch. Its code is normalised to upper case, prefixes every receipt number it issues, and cannot be changed later. Limited by the plan.",
            "Filial qo'shadi. Uning kodi katta harfga o'tkaziladi, har bir chek raqami boshida turadi va keyin o'zgartirilmaydi. Tarif bilan cheklangan.",
            "Добавляет филиал. Код приводится к верхнему регистру, начинает номер каждого чека и потом не меняется. Ограничено тарифом.",
        ),
        {402: ("quota_exceeded",), 409: ("code_taken",)},
    ),
    "shop_update_branch": Op(
        T("Update a branch", "Filialni yangilash", "Изменение филиала"),
        T(
            "Changes a branch's details, default flag or active status. Making a branch the default takes the flag from the previous one, and the default branch cannot be deactivated.",
            "Filial ma'lumotlari, asosiylik belgisi yoki faollik holatini o'zgartiradi. Filialni asosiy qilish bu belgini oldingisidan oladi, asosiy filialni esa faolsizlantirib bo'lmaydi.",
            "Меняет данные филиала, признак основного или активность. Назначение основным снимает признак с прежнего, а основной филиал деактивировать нельзя.",
        ),
        {409: ("default_branch",)},
    ),
    "shop_delete_branch": Op(
        T("Close a branch", "Filialni yopish", "Закрытие филиала"),
        T(
            "Closes a branch. It disappears from the till, but its sales, receipts and stock history are kept; staff assigned to it are unassigned. The last branch and the default branch cannot be closed.",
            "Filialni yopadi. U kassadan yo'qoladi, lekin sotuvlari, cheklari va qoldiq tarixi saqlanadi; unga biriktirilgan xodimlar bo'shatiladi. Oxirgi va asosiy filialni yopib bo'lmaydi.",
            "Закрывает филиал. Он пропадает с кассы, но продажи, чеки и история остатков сохраняются; закреплённые сотрудники открепляются. Последний и основной филиалы закрыть нельзя.",
        ),
        {409: ("last_branch", "default_branch")},
    ),
    "shop_get_shop": Op(
        T("Shop details", "Do'kon ma'lumotlari", "Данные магазина"),
        T(
            "The shop's details, receipt layout and settings.",
            "Do'kon ma'lumotlari, chek ko'rinishi va sozlamalari.",
            "Данные магазина, оформление чека и настройки.",
        ),
    ),
    "shop_update_shop": Op(
        T("Update shop details", "Do'kon ma'lumotlarini yangilash", "Изменение данных магазина"),
        T(
            "Changes the shop's details and receipt layout. Keys in `settings` are merged into the existing ones. Currency and shop address cannot be changed here — they are ignored if sent.",
            "Do'kon ma'lumotlari va chek ko'rinishini o'zgartiradi. `settings` dagi kalitlar mavjudlariga qo'shiladi. Valyuta va do'kon manzilini bu yerda o'zgartirib bo'lmaydi — yuborilsa e'tiborsiz qoldiriladi.",
            "Меняет данные магазина и оформление чека. Ключи `settings` объединяются с существующими. Валюту и адрес магазина здесь изменить нельзя — если их передать, они игнорируются.",
        ),
    ),
    "shop_update_tax_rate": Op(
        T("Update a tax rate", "Soliq stavkasini yangilash", "Изменение налоговой ставки"),
        T(
            "Changes a tax rate. Past sales are not affected: every order line stored the rate and tax at the time, so the figures for last quarter never change.",
            "Soliq stavkasini o'zgartiradi. O'tgan sotuvlarga ta'sir qilmaydi: har bir buyurtma qatori o'sha paytdagi stavka va soliqni saqlagan, shuning uchun o'tgan chorak raqamlari o'zgarmaydi.",
            "Изменяет налоговую ставку. Прошлые продажи не затрагиваются: каждая строка заказа хранит ставку и налог на момент продажи, поэтому цифры за прошлый квартал не меняются.",
        ),
    ),
    "shop_delete_tax_rate": Op(
        T("Delete a tax rate", "Soliq stavkasini o'chirish", "Удаление налоговой ставки"),
        T(
            "Removes a tax rate that no product uses. If products still use it, the answer says how many.",
            "Hech bir mahsulot ishlatmayotgan soliq stavkasini o'chiradi. Mahsulotlar hali ishlatayotgan bo'lsa, javob nechta ekanini aytadi.",
            "Удаляет ставку, которую не использует ни один товар. Если товары её ещё используют, ответ сообщает сколько.",
        ),
        {409: ("rate_in_use",)},
    ),
    # -------------------------------------------------------------- analytics
    "analytics_dashboard": Op(
        T("Dashboard", "Boshqaruv paneli", "Панель показателей"),
        T(
            "Today's revenue against yesterday, orders, average basket, margin, this month's revenue, stock warnings and open tills — for one branch or the whole shop.",
            "Bugungi tushum kechagiga nisbatan, buyurtmalar, o'rtacha chek, marja, oylik tushum, qoldiq ogohlantirishlari va ochiq kassalar — bitta filial yoki butun do'kon uchun.",
            "Выручка сегодня в сравнении со вчера, заказы, средний чек, маржа, выручка за месяц, предупреждения по остаткам и открытые кассы — по филиалу или всему магазину.",
        ),
    ),
    "analytics_revenue": Op(
        T("Revenue by day", "Kunlik tushum", "Выручка по дням"),
        T(
            "Revenue, orders and margin for each of the last `days` days.",
            "Oxirgi `days` kunning har biri uchun tushum, buyurtmalar va marja.",
            "Выручка, заказы и маржа за каждый из последних `days` дней.",
        ),
    ),
    "analytics_top_products": Op(
        T("Best sellers", "Eng ko'p sotilganlar", "Лидеры продаж"),
        T(
            "The best-selling products over the last `days` days.",
            "Oxirgi `days` kunda eng ko'p sotilgan mahsulotlar.",
            "Самые продаваемые товары за последние `days` дней.",
        ),
    ),
    "analytics_low_stock": Op(
        T("Low stock", "Kam qolgan mahsulotlar", "Заканчивающиеся товары"),
        T(
            "Products at or below their reorder threshold.",
            "Qayta buyurtma chegarasiga yetgan yoki undan kam qolgan mahsulotlar.",
            "Товары на пороге дозаказа или ниже.",
        ),
    ),
    "analytics_payments": Op(
        T(
            "Takings by payment method",
            "To'lov usullari bo'yicha tushum",
            "Выручка по способам оплаты",
        ),
        T(
            "How much was taken by each payment method over the last `days` days.",
            "Oxirgi `days` kunda har bir to'lov usuli bo'yicha qancha qabul qilingani.",
            "Сколько принято каждым способом оплаты за последние `days` дней.",
        ),
    ),
    "analytics_hourly": Op(
        T("Sales by hour", "Soatlar bo'yicha sotuvlar", "Продажи по часам"),
        T(
            "Sales for each hour of the day over the last `days` days — when the shop is busiest.",
            "Oxirgi `days` kunda kunning har bir soatidagi sotuvlar — do'kon qachon eng band ekani.",
            "Продажи по часам дня за последние `days` дней — когда в магазине больше всего покупателей.",
        ),
    ),
    "analytics_plan_usage": Op(
        T("Plan usage", "Tarifdan foydalanish", "Использование тарифа"),
        T(
            "Branches, staff and products the shop has, and sales this month, against its plan's limits — so a ceiling is visible before it is hit. Each entry has `used` and `limit`; a null limit means unlimited.",
            "Do'kondagi filiallar, xodimlar va mahsulotlar hamda shu oydagi sotuvlar tarif cheklovlariga nisbatan — chegara unga yetmasdan oldin ko'rinadi. Har bir yozuvda `used` va `limit` bor; null chegara — cheksiz.",
            "Филиалы, сотрудники и товары магазина и продажи в этом месяце в сравнении с лимитами тарифа — чтобы потолок был виден заранее. В каждой записи есть `used` и `limit`; null означает без ограничений.",
        ),
    ),
    # ---------------------------------------------------------------- reports
    "reports_request_report": Op(
        T("Request a report", "Hisobot so'rash", "Запрос отчёта"),
        T(
            "Queues a report for background generation and answers `202` straight away. Poll `GET /reports/{job_id}` until `status` is `completed`, then download it.",
            "Hisobotni fonda tayyorlash uchun navbatga qo'yadi va darhol `202` qaytaradi. `status` `completed` bo'lguncha `GET /reports/{job_id}` ni so'rab turing, keyin yuklab oling.",
            "Ставит отчёт в очередь на фоновое формирование и сразу отвечает `202`. Опрашивайте `GET /reports/{job_id}`, пока `status` не станет `completed`, затем скачайте.",
        ),
    ),
    "reports_list_reports": Op(
        T("List reports", "Hisobotlar ro'yxati", "Список отчётов"),
        T(
            "Reports requested in this shop and their status.",
            "Shu do'konda so'ralgan hisobotlar va ularning holati.",
            "Отчёты, запрошенные в магазине, и их статус.",
        ),
    ),
    "reports_get_report": Op(
        T("Report status", "Hisobot holati", "Статус отчёта"),
        T(
            "One report job — poll this while it is generated.",
            "Bitta hisobot vazifasi — tayyorlanayotganda shuni so'rab turing.",
            "Одна задача отчёта — опрашивайте её во время формирования.",
        ),
    ),
    "reports_download_report": Op(
        T("Download a report", "Hisobotni yuklab olish", "Скачивание отчёта"),
        T(
            "Streams the generated file. Available once the report is `completed`, until `expires_at`.",
            "Tayyorlangan faylni uzatadi. Hisobot `completed` bo'lgandan keyin `expires_at` gacha mavjud.",
            "Отдаёт сформированный файл. Доступен после статуса `completed` и до `expires_at`.",
        ),
        {400: ("report_not_ready",), 404: ("report_expired",)},
    ),
    # ---------------------------------------------------------------- billing
    "billing_overview": Op(
        T("Subscription and invoices", "Obuna va hisob-fakturalar", "Подписка и счета"),
        T(
            "The shop's plan and billing period, trial or grace days left, the invoice awaiting payment with links to pay it through Payme or Click, and recent invoices.",
            "Do'kon tarifi va to'lov davri, sinov yoki imtiyozli davrdan qolgan kunlar, to'lov kutayotgan hisob-faktura va uni Payme yoki Click orqali to'lash havolalari hamda so'nggi hisob-fakturalar.",
            "Тариф и период оплаты магазина, оставшиеся дни пробного или льготного периода, счёт к оплате со ссылками на Payme или Click и последние счета.",
        ),
    ),
    # --------------------------------------------------------------- platform
    "platform_metrics": Op(
        T("Platform metrics", "Platforma ko'rsatkichlari", "Показатели платформы"),
        T(
            "Shops by status, MRR and ARR, the trial pipeline, sign-ups and churn this month, and 30-day activity across every shop.",
            "Holat bo'yicha do'konlar, MRR va ARR, sinovdagilar salohiyati, shu oydagi yangi va ketgan do'konlar hamda barcha do'konlarning 30 kunlik faolligi.",
            "Магазины по статусам, MRR и ARR, потенциал пробных, регистрации и отток за месяц и активность всех магазинов за 30 дней.",
        ),
    ),
    "platform_mrr": Op(
        T("MRR history", "MRR tarixi", "История MRR"),
        T(
            "Monthly recurring revenue at the end of each of the last `months` months.",
            "Oxirgi `months` oyning har biri oxiridagi oylik takroriy daromad.",
            "Ежемесячная регулярная выручка на конец каждого из последних `months` месяцев.",
        ),
    ),
    "platform_list_tenants": Op(
        T("List shops", "Do'konlar ro'yxati", "Список магазинов"),
        T(
            "Every shop, searchable and filterable by status, with plan, revenue and activity.",
            "Har bir do'kon — qidiriladi va holat bo'yicha filtrlanadi — tarifi, daromadi va faolligi bilan.",
            "Все магазины с поиском и фильтром по статусу, с тарифом, выручкой и активностью.",
        ),
    ),
    "platform_create_tenant": Op(
        T("Create a shop", "Do'kon yaratish", "Создание магазина"),
        T(
            "Opens a shop on a customer's behalf, with its owner account — for sales-assisted onboarding.",
            "Mijoz nomidan, egasi hisobi bilan do'kon ochadi — sotuv bo'limi yordamida ulash uchun.",
            "Открывает магазин от имени клиента вместе с учётной записью владельца — для подключения через отдел продаж.",
        ),
        {404: ("plan_not_found",), 409: ("slug_taken",)},
    ),
    "platform_get_tenant": Op(
        T("Get a shop", "Do'konni olish", "Получение магазина"),
        T(
            "One shop's summary.",
            "Bitta do'kon haqida umumiy ma'lumot.",
            "Сводка по одному магазину.",
        ),
    ),
    "platform_delete_tenant": Op(
        T("Close a shop", "Do'konni yopish", "Закрытие магазина"),
        T(
            "Closes a shop: marks it cancelled, cancels its subscription and signs its staff out. Nothing is erased — its sales history is kept, as it is usually a record the operator must retain.",
            "Do'konni yopadi: uni bekor qilingan deb belgilaydi, obunasini bekor qiladi va xodimlarini tizimdan chiqaradi. Hech narsa o'chirilmaydi — sotuvlar tarixi saqlanadi, chunki odatda uni saqlash majburiy.",
            "Закрывает магазин: помечает его отменённым, отменяет подписку и завершает сессии сотрудников. Ничего не удаляется — история продаж сохраняется, так как её обычно обязаны хранить.",
        ),
    ),
    "platform_set_tenant_status": Op(
        T(
            "Block or unblock a shop",
            "Do'konni bloklash yoki ochish",
            "Блокировка и разблокировка магазина",
        ),
        T(
            "Sets a shop's status. A blocked shop's staff are refused from their very next request, and `reason` is shown to them.",
            "Do'kon holatini o'rnatadi. Bloklangan do'kon xodimlari keyingi so'rovidayoq rad etiladi va ularga `reason` ko'rsatiladi.",
            "Устанавливает статус магазина. Сотрудникам заблокированного магазина отказывают уже при следующем запросе и показывают `reason`.",
        ),
    ),
    "platform_change_tenant_plan": Op(
        T("Change a shop's plan", "Do'kon tarifini o'zgartirish", "Смена тарифа магазина"),
        T(
            "Moves a shop to another plan or billing cycle at the plan's current price. `activate` converts a trial to paid now. A downgrade never deletes data: the shop simply cannot add more until it is back under the new limits.",
            "Do'konni boshqa tarif yoki to'lov davriga tarifning joriy narxida o'tkazadi. `activate` sinovni hozir pullikka aylantiradi. Past tarifga o'tish hech qachon ma'lumotni o'chirmaydi: do'kon yangi cheklovlar ichiga qaytmaguncha shunchaki yangi narsa qo'sha olmaydi.",
            "Переводит магазин на другой тариф или период по текущей цене тарифа. `activate` сразу переводит пробный период в платный. Понижение тарифа никогда не удаляет данные: магазин просто не сможет добавлять новое, пока не вернётся в новые лимиты.",
        ),
        {404: ("plan_not_found",)},
    ),
    "platform_list_plans": Op(
        T("List plans", "Tariflar ro'yxati", "Список тарифов"),
        T(
            "Every plan, with how many shops are on it and the MRR it brings.",
            "Har bir tarif, unda nechta do'kon borligi va keltiradigan MRR bilan.",
            "Все тарифы с числом магазинов и приносимым MRR.",
        ),
    ),
    "platform_create_plan": Op(
        T("Create a plan", "Tarif yaratish", "Создание тарифа"),
        T("Adds a subscription plan.", "Obuna tarifini qo'shadi.", "Добавляет тариф подписки."),
        {409: ("code_taken",)},
    ),
    "platform_update_plan": Op(
        T("Update a plan", "Tarifni yangilash", "Изменение тарифа"),
        T(
            "Changes a plan. Shops already on it keep the price they signed up at until their plan is changed.",
            "Tarifni o'zgartiradi. Undagi do'konlar tarifi o'zgartirilmaguncha ulangan narxida qoladi.",
            "Изменяет тариф. Магазины на нём сохраняют цену подключения, пока им не сменят тариф.",
        ),
    ),
    "platform_retire_plan": Op(
        T("Retire a plan", "Tarifni to'xtatish", "Вывод тарифа из продажи"),
        T(
            "Stops offering a plan without deleting it; shops already on it are not moved.",
            "Tarifni o'chirmasdan taklif qilishni to'xtatadi; undagi do'konlar ko'chirilmaydi.",
            "Прекращает предлагать тариф, не удаляя его; магазины на нём не переводятся.",
        ),
    ),
    # -------------------------------------------------------------------- ops
    "ops_health": Op(
        T("Liveness", "Ishlayotganlik", "Живость"),
        T(
            "Answers as long as the process is running. Does not touch the database.",
            "Jarayon ishlab turgan ekan, javob beradi. Ma'lumotlar bazasiga murojaat qilmaydi.",
            "Отвечает, пока процесс запущен. К базе данных не обращается.",
        ),
    ),
    "ops_readiness": Op(
        T("Readiness", "Tayyorlik", "Готовность"),
        T(
            "Ready only when the database is reachable, `503` otherwise. Load balancers and Compose route traffic by this.",
            "Faqat ma'lumotlar bazasiga ulanish bo'lsa tayyor, aks holda `503`. Yuk taqsimlagichlar va Compose trafikni shunga qarab yo'naltiradi.",
            "Готов, только если доступна база данных, иначе `503`. Балансировщики и Compose направляют трафик по этому признаку.",
        ),
    ),
}
