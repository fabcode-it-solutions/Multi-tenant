"""What each schema in the API reference is, in three languages."""

from __future__ import annotations

from app.docs.i18n.base import T

SCHEMAS: dict[str, T] = {
    # ------------------------------------------------------------------ common
    "ErrorResponse": T(
        "The body of every error response. Branch on `code`, which is stable; `message` is written for people and may change.",
        "Har bir xato javobining tanasi. Dasturda `code` bo'yicha tarmoqlaning — u o'zgarmaydi; `message` odamlar uchun yozilgan va o'zgarishi mumkin.",
        "Тело любого ответа с ошибкой. Ветвитесь по `code` — он стабилен; `message` написан для людей и может меняться.",
    ),
    "Message": T(
        "A plain confirmation from an action that has nothing else to return.",
        "Boshqa qaytaradigan narsasi bo'lmagan amalning oddiy tasdig'i.",
        "Простое подтверждение действия, которому больше нечего вернуть.",
    ),
    # -------------------------------------------------------------------- auth
    "SignupRequest": T(
        "Everything needed to open a new shop: the shop, its address, its owner and the plan to trial.",
        "Yangi do'kon ochish uchun kerak bo'lgan hamma narsa: do'kon, uning manzili, egasi va sinab ko'riladigan tarif.",
        "Всё необходимое для открытия магазина: магазин, его адрес, владелец и тариф на пробный период.",
    ),
    "LoginRequest": T(
        "Sign in with email and password. Shop staff also send the shop address.",
        "Email va parol bilan kirish. Do'kon xodimlari do'kon manzilini ham yuboradi.",
        "Вход по email и паролю. Сотрудники магазина также передают адрес магазина.",
    ),
    "PinLoginRequest": T(
        "Switch the person at a terminal with their PIN instead of a password.",
        "Terminaldagi xodimni parol o'rniga PIN orqali almashtirish.",
        "Смена сотрудника на терминале по PIN-коду вместо пароля.",
    ),
    "TokenPair": T(
        "A new session: a short-lived access token for API calls and a single-use refresh token to renew it.",
        "Yangi sessiya: API chaqiruvlari uchun qisqa muddatli access token va uni yangilash uchun bir martalik refresh token.",
        "Новая сессия: короткоживущий access-токен для запросов и одноразовый refresh-токен для его обновления.",
    ),
    "RefreshRequest": T(
        "A refresh token to exchange for a new pair, or to revoke when signing out.",
        "Yangi juftlikka almashtiriladigan yoki chiqishda bekor qilinadigan refresh token.",
        "Refresh-токен для обмена на новую пару или для отзыва при выходе.",
    ),
    "SessionInfo": T(
        "The signed-in user, their shop and the exact permissions they hold — enough to render the app without asking again.",
        "Tizimga kirgan foydalanuvchi, uning do'koni va aniq ruxsatlari — ilovani qayta so'ramasdan ko'rsatish uchun yetarli.",
        "Вошедший пользователь, его магазин и точный набор прав — достаточно, чтобы отрисовать приложение без повторных запросов.",
    ),
    "UserPublic": T(
        "A user as they see themselves: identity and role, never credentials.",
        "Foydalanuvchining o'zi ko'radigan ma'lumoti: shaxsi va roli, hech qachon maxfiy ma'lumotlar emas.",
        "Пользователь так, как он видит себя: личность и роль, но никогда не учётные данные.",
    ),
    "ProfileUpdate": T(
        "Fields you may change on your own account. Role, branch and permissions are granted by an owner and cannot be set here — extra fields are ignored.",
        "O'z hisobingizda o'zgartira oladigan maydonlar. Rol, filial va ruxsatlarni egasi beradi, ularni bu yerda o'rnatib bo'lmaydi — ortiqcha maydonlar e'tiborsiz qoldiriladi.",
        "Поля, которые можно изменить в своей учётной записи. Роль, филиал и права назначает владелец, здесь их задать нельзя — лишние поля игнорируются.",
    ),
    "ChangePasswordRequest": T(
        "Change your own password. The current password is required.",
        "O'z parolingizni o'zgartirish. Joriy parol talab qilinadi.",
        "Смена собственного пароля. Требуется текущий пароль.",
    ),
    "SetPinRequest": T(
        "Set or replace your terminal PIN.",
        "Terminal PIN'ini o'rnatish yoki almashtirish.",
        "Установка или замена PIN-кода терминала.",
    ),
    "ForgotPasswordRequest": T(
        "Ask for a password-reset link by email.",
        "Parolni tiklash havolasini email orqali so'rash.",
        "Запрос ссылки для сброса пароля по email.",
    ),
    "ResetPasswordRequest": T(
        "Complete a reset: the token from the emailed link and the new password.",
        "Tiklashni yakunlash: emaildagi havoladagi token va yangi parol.",
        "Завершение сброса: токен из письма и новый пароль.",
    ),
    "TerminalStaff": T(
        "A person on the PIN-login screen. Deliberately without an email address, so a shop-floor tablet never shows login identifiers.",
        "PIN bilan kirish ekranidagi xodim. Ataylab emailsiz — savdo zalidagi planshet hech qachon login ma'lumotlarini ko'rsatmaydi.",
        "Сотрудник на экране входа по PIN. Намеренно без email — планшет в торговом зале никогда не показывает логины.",
    ),
    # ----------------------------------------------------------------- catalog
    "CategoryIn": T(
        "A new category. Categories group products and become tiles on the POS grid.",
        "Yangi kategoriya. Kategoriyalar mahsulotlarni guruhlaydi va POS panelida plitka bo'lib ko'rinadi.",
        "Новая категория. Категории группируют товары и становятся плитками на экране кассы.",
    ),
    "CategoryOut": T(
        "A product category.",
        "Mahsulot kategoriyasi.",
        "Категория товаров.",
    ),
    "CategoryUpdate": T(
        "Changes to a category. Only the fields sent are changed.",
        "Kategoriyaga o'zgartirishlar. Faqat yuborilgan maydonlar o'zgaradi.",
        "Изменения категории. Меняются только переданные поля.",
    ),
    "ProductIn": T(
        "A new product. Optionally with the quantity already on the shelf, which is recorded as opening stock.",
        "Yangi mahsulot. Ixtiyoriy ravishda javonda turgan miqdori bilan — u boshlang'ich qoldiq sifatida yoziladi.",
        "Новый товар. Можно сразу указать количество на полке — оно запишется как начальный остаток.",
    ),
    "ProductUpdate": T(
        "Changes to a product. Only the fields sent are changed. Price changes apply to future sales; past receipts keep the price they were sold at.",
        "Mahsulotga o'zgartirishlar. Faqat yuborilgan maydonlar o'zgaradi. Narx o'zgarishi kelgusi sotuvlarga ta'sir qiladi; o'tgan cheklar o'z narxida qoladi.",
        "Изменения товара. Меняются только переданные поля. Новая цена действует для будущих продаж; прошлые чеки сохраняют цену продажи.",
    ),
    "ProductOut": T(
        "A product as the till needs it: price, tax, stock and grid position.",
        "Kassa uchun kerakli mahsulot ma'lumoti: narx, soliq, qoldiq va paneldagi o'rni.",
        "Товар в том виде, в каком он нужен кассе: цена, налог, остаток и место на экране.",
    ),
    "ProductListItem": T(
        "A product row in the catalog list. Cost figures appear only for callers allowed to see them.",
        "Katalog ro'yxatidagi mahsulot qatori. Tannarx faqat uni ko'rishga ruxsati borlarga ko'rsatiladi.",
        "Строка товара в списке каталога. Себестоимость видна только тем, у кого есть на это право.",
    ),
    "ProductDetail": T(
        "A single product with everything needed to edit it.",
        "Tahrirlash uchun kerakli hamma ma'lumoti bilan bitta mahsulot.",
        "Один товар со всеми данными для редактирования.",
    ),
    "ProductLookupOut": T(
        "The product a scanned code resolved to, how it matched, and how many units one scan represents.",
        "Skanerlangan kod qaysi mahsulotga to'g'ri kelgani, qanday moslashgani va bitta skan nechta donaga teng ekani.",
        "Товар, найденный по отсканированному коду, способ совпадения и сколько единиц даёт одно сканирование.",
    ),
    "TaxRateIn": T(
        "A new tax rate.",
        "Yangi soliq stavkasi.",
        "Новая налоговая ставка.",
    ),
    "TaxRateOut": T(
        "A tax rate products can be assigned to.",
        "Mahsulotlarga biriktiriladigan soliq stavkasi.",
        "Налоговая ставка, которую можно назначить товарам.",
    ),
    "TaxRateUpdate": T(
        "Changes to a tax rate. They apply to future sales only — every past order line kept the rate it was sold at.",
        "Soliq stavkasiga o'zgartirishlar. Faqat kelgusi sotuvlarga ta'sir qiladi — har bir o'tgan buyurtma qatori sotilgan paytdagi stavkani saqlaydi.",
        "Изменения налоговой ставки. Действуют только для будущих продаж — каждая прошлая строка заказа сохранила свою ставку.",
    ),
    # --------------------------------------------------------------- inventory
    "StockLevelOut": T(
        "How much of one product a branch holds, and what it is worth.",
        "Filialda bitta mahsulotdan qancha borligi va uning qiymati.",
        "Сколько единиц товара есть в филиале и сколько они стоят.",
    ),
    "StockAdjustIn": T(
        "A change to stock: a delivery, a write-off or a correction. The quantity is signed.",
        "Qoldiqni o'zgartirish: yetkazib berish, hisobdan chiqarish yoki tuzatish. Miqdor ishorali.",
        "Изменение остатка: поставка, списание или корректировка. Количество со знаком.",
    ),
    "StockCountIn": T(
        "The result of counting a product on the shelf. The system records the difference from its own figure.",
        "Javondagi mahsulotni sanash natijasi. Tizim o'z hisobidan farqni yozib qo'yadi.",
        "Результат пересчёта товара на полке. Система записывает расхождение со своими данными.",
    ),
    "StockMovementOut": T(
        "One entry in the append-only stock ledger. On-hand quantity is the sum of these entries, so it can always be reconstructed.",
        "Faqat qo'shiladigan ombor daftaridagi bitta yozuv. Qoldiq shu yozuvlar yig'indisi, shuning uchun uni har doim qayta tiklash mumkin.",
        "Одна запись в журнале движения товара, куда только добавляют. Остаток — сумма этих записей, поэтому его всегда можно восстановить.",
    ),
    # ------------------------------------------------------------------ orders
    "OrderCreate": T(
        "A sale to complete: the lines, the payments that settle it, and an optional order-level discount.",
        "Yakunlanadigan sotuv: qatorlar, uni to'laydigan to'lovlar va ixtiyoriy buyurtma chegirmasi.",
        "Продажа к проведению: строки, оплаты, закрывающие её, и необязательная скидка на весь заказ.",
    ),
    "OrderItemIn": T(
        "One line of a sale: a product, a quantity and an optional line discount.",
        "Sotuvning bitta qatori: mahsulot, miqdor va ixtiyoriy qator chegirmasi.",
        "Одна строка продажи: товар, количество и необязательная скидка на строку.",
    ),
    "PaymentIn": T(
        "One payment towards a sale. A sale may be split across several methods.",
        "Sotuv uchun bitta to'lov. Bitta sotuvni bir necha usulda to'lash mumkin.",
        "Одна оплата по продаже. Продажу можно разделить на несколько способов оплаты.",
    ),
    "OrderOut": T(
        "A completed sale with its lines, payments and totals, as calculated by the server.",
        "Server hisoblagan qatorlari, to'lovlari va jami summalari bilan yakunlangan sotuv.",
        "Проведённая продажа со строками, оплатами и итогами, рассчитанными сервером.",
    ),
    "OrderItemOut": T(
        "A line as it was sold. Name, price and tax are snapshots, so later catalog changes never alter a past receipt.",
        "Sotilgan paytdagi qator. Nomi, narxi va solig'i o'sha paytdagi nusxa — keyingi katalog o'zgarishlari o'tgan chekni o'zgartirmaydi.",
        "Строка в момент продажи. Название, цена и налог — снимки, поэтому изменения каталога не меняют прошлые чеки.",
    ),
    "PaymentOut": T(
        "A payment taken on a sale.",
        "Sotuv bo'yicha qabul qilingan to'lov.",
        "Оплата, принятая по продаже.",
    ),
    "ReceiptOut": T(
        "Everything a receipt shows, in one payload used by both the thermal printer and the PDF renderer.",
        "Chekda ko'rinadigan hamma narsa — termoprinter ham, PDF ham foydalanadigan bitta javobda.",
        "Всё, что есть на чеке, одним ответом — его используют и термопринтер, и PDF.",
    ),
    "ReceiptShop": T(
        "The shop and branch details printed on a receipt.",
        "Chekda chop etiladigan do'kon va filial ma'lumotlari.",
        "Данные магазина и филиала, печатаемые на чеке.",
    ),
    "OrderRefundView": T(
        "What is still returnable on an order, line by line, and the refunds already made.",
        "Buyurtmada hali qaytarilishi mumkin bo'lgan narsalar, qatorma-qator, va allaqachon qilingan qaytarishlar.",
        "Что ещё можно вернуть по заказу, построчно, и уже проведённые возвраты.",
    ),
    "RefundableLine": T(
        "One order line and how much of it can still be returned.",
        "Buyurtmaning bitta qatori va undan yana qanchasini qaytarish mumkinligi.",
        "Одна строка заказа и сколько по ней ещё можно вернуть.",
    ),
    "RefundCreate": T(
        "A return: which lines and quantities, how the money goes back, and whether the goods go back on the shelf.",
        "Qaytarish: qaysi qatorlar va miqdorlar, pul qanday qaytariladi va tovar javonga qaytadimi.",
        "Возврат: какие строки и количества, как возвращаются деньги и возвращается ли товар на полку.",
    ),
    "RefundLineIn": T(
        "One order line to return, and how many units.",
        "Qaytariladigan bitta buyurtma qatori va nechta dona.",
        "Одна строка заказа к возврату и количество единиц.",
    ),
    "RefundOut": T(
        "A completed refund.",
        "Amalga oshirilgan qaytarish.",
        "Проведённый возврат.",
    ),
    "RefundLineOut": T(
        "One line of a refund and the money returned for it.",
        "Qaytarishning bitta qatori va u uchun qaytarilgan pul.",
        "Одна строка возврата и возвращённая по ней сумма.",
    ),
    # ------------------------------------------------------------------ shifts
    "ShiftOpenIn": T(
        "Open a till: the cash already in the drawer before trading starts.",
        "Kassani ochish: savdo boshlanishidan oldin yashikda turgan naqd pul.",
        "Открытие кассы: наличные в ящике до начала торговли.",
    ),
    "ShiftCloseIn": T(
        "Close a till: the cash counted in the drawer, and an optional note explaining any difference.",
        "Kassani yopish: yashikda sanalgan naqd pul va farqni tushuntiruvchi ixtiyoriy izoh.",
        "Закрытие кассы: пересчитанные наличные и необязательная заметка, объясняющая расхождение.",
    ),
    "ShiftOut": T(
        "A cashier's shift at a till and how its drawer reconciled.",
        "Kassirning kassadagi smenasi va uning yashigi qanday hisob-kitob qilingani.",
        "Смена кассира и то, как сошлась его касса.",
    ),
    "ShiftSummaryOut": T(
        "The takings of the open shift so far — what the cashier counts against before closing.",
        "Ochiq smenaning hozirgacha tushumi — kassir yopishdan oldin shunga qarab sanaydi.",
        "Выручка открытой смены на данный момент — с ней кассир сверяется перед закрытием.",
    ),
    "ShiftListItem": T(
        "A shift as the office reviews it: who, where, when, what was taken, and the cash difference.",
        "Ofis ko'rib chiqadigan smena: kim, qayerda, qachon, qancha tushum va naqd farq.",
        "Смена глазами офиса: кто, где, когда, сколько принято и расхождение по наличным.",
    ),
    # --------------------------------------------------------------- employees
    "EmployeeIn": T(
        "A new staff account. Only an owner may create another owner.",
        "Yangi xodim hisobi. Boshqa egani faqat ega yarata oladi.",
        "Новая учётная запись сотрудника. Создать другого владельца может только владелец.",
    ),
    "EmployeeOut": T(
        "A member of staff, with the permissions they actually hold.",
        "Xodim va uning haqiqiy ruxsatlari.",
        "Сотрудник и права, которые у него фактически есть.",
    ),
    "EmployeeUpdate": T(
        "Changes to a member of staff. Only the fields sent are changed. Deactivating someone signs them out everywhere.",
        "Xodimga o'zgartirishlar. Faqat yuborilgan maydonlar o'zgaradi. Xodimni o'chirish uni hamma qurilmalardan chiqaradi.",
        "Изменения сотрудника. Меняются только переданные поля. Деактивация завершает все его сессии.",
    ),
    "ResetPasswordIn": T(
        "A new password set for a member of staff by a manager or owner.",
        "Menejer yoki ega tomonidan xodimga o'rnatiladigan yangi parol.",
        "Новый пароль, который менеджер или владелец задаёт сотруднику.",
    ),
    # -------------------------------------------------------------------- shop
    "BranchIn": T(
        "A new branch (shop location). Stock is counted per branch.",
        "Yangi filial (do'kon joyi). Qoldiq har bir filial uchun alohida hisoblanadi.",
        "Новый филиал (точка магазина). Остатки ведутся по каждому филиалу отдельно.",
    ),
    "BranchOut": T(
        "A branch with its staff, product and recent sales counts.",
        "Xodimlar, mahsulotlar va so'nggi sotuvlar soni bilan filial.",
        "Филиал с количеством сотрудников, товаров и недавних продаж.",
    ),
    "BranchUpdate": T(
        "Changes to a branch. The code cannot change: it is part of every receipt number the branch has issued.",
        "Filialga o'zgartirishlar. Kodni o'zgartirib bo'lmaydi: u filial bergan har bir chek raqamining bir qismi.",
        "Изменения филиала. Код изменить нельзя: он входит в номер каждого выданного филиалом чека.",
    ),
    "ShopSettings": T(
        "The shop's details and receipt layout.",
        "Do'kon ma'lumotlari va chek ko'rinishi.",
        "Данные магазина и оформление чека.",
    ),
    "ShopSettingsUpdate": T(
        "Changes to the shop's details. Currency and shop address are not self-service: currency is stamped on every past order and the address is how staff sign in.",
        "Do'kon ma'lumotlariga o'zgartirishlar. Valyuta va do'kon manzilini o'zingiz o'zgartira olmaysiz: valyuta har bir o'tgan buyurtmaga yozilgan, manzil esa xodimlarning kirish manzili.",
        "Изменения данных магазина. Валюту и адрес магазина нельзя сменить самостоятельно: валюта записана в каждом прошлом заказе, а адрес — это то, по чему входят сотрудники.",
    ),
    # --------------------------------------------------------------- analytics
    "DashboardSummary": T(
        "Today at a glance: revenue, orders, margin, stock warnings and open tills.",
        "Bugungi holat bir qarashda: tushum, buyurtmalar, marja, qoldiq ogohlantirishlari va ochiq kassalar.",
        "Сегодняшний день одним взглядом: выручка, заказы, маржа, предупреждения по остаткам и открытые кассы.",
    ),
    "RevenuePoint": T(
        "Revenue, orders and margin for one day.",
        "Bir kunlik tushum, buyurtmalar va marja.",
        "Выручка, заказы и маржа за один день.",
    ),
    "TopProduct": T(
        "A best-selling product over the period.",
        "Davr mobaynida eng ko'p sotilgan mahsulot.",
        "Самый продаваемый товар за период.",
    ),
    "LowStockItem": T(
        "A product at or below its reorder threshold at a branch.",
        "Filialda qayta buyurtma chegarasiga yetgan yoki undan kam qolgan mahsulot.",
        "Товар, остаток которого в филиале достиг порога дозаказа или ниже.",
    ),
    "PaymentBreakdown": T(
        "How much was taken by one payment method over the period.",
        "Davr mobaynida bitta to'lov usuli bilan qancha qabul qilingani.",
        "Сколько принято одним способом оплаты за период.",
    ),
    "SalesByHour": T(
        "Sales in one hour of the day, summed across the period.",
        "Kunning bir soatidagi sotuvlar, davr bo'yicha yig'indi.",
        "Продажи за один час дня, суммарно за период.",
    ),
    # ----------------------------------------------------------------- reports
    "ReportRequest": T(
        "A report to generate in the background.",
        "Fonda tayyorlanadigan hisobot.",
        "Отчёт для формирования в фоне.",
    ),
    "ReportJobOut": T(
        "A report job and its progress. Poll until `status` is `completed`, then download the file.",
        "Hisobot vazifasi va uning holati. `status` `completed` bo'lguncha so'rab turing, keyin faylni yuklab oling.",
        "Задача отчёта и её ход. Опрашивайте, пока `status` не станет `completed`, затем скачайте файл.",
    ),
    # ----------------------------------------------------------------- billing
    "BillingOverview": T(
        "The shop's subscription: plan, period, what is owed and where to pay it.",
        "Do'kon obunasi: tarif, davr, qancha qarz va qayerda to'lash mumkin.",
        "Подписка магазина: тариф, период, задолженность и где её оплатить.",
    ),
    "InvoiceOut": T(
        "A subscription invoice.",
        "Obuna uchun hisob-faktura.",
        "Счёт за подписку.",
    ),
    "PayLink": T(
        "A link that opens a payment provider's checkout for the outstanding invoice.",
        "To'lanmagan hisob-faktura uchun to'lov tizimi sahifasini ochadigan havola.",
        "Ссылка, открывающая страницу оплаты платёжной системы для неоплаченного счёта.",
    ),
    # ---------------------------------------------------------------- platform
    "PlatformMetrics": T(
        "Platform-wide numbers: shops, recurring revenue and activity.",
        "Butun platforma ko'rsatkichlari: do'konlar, takroriy daromad va faollik.",
        "Показатели всей платформы: магазины, регулярная выручка и активность.",
    ),
    "MrrPoint": T(
        "Monthly recurring revenue at the end of one month.",
        "Bir oy oxiridagi oylik takroriy daromad.",
        "Ежемесячная регулярная выручка на конец одного месяца.",
    ),
    "TenantSummary": T(
        "A shop as platform staff see it: status, plan, revenue and activity.",
        "Platforma xodimlari ko'radigan do'kon: holati, tarifi, daromadi va faolligi.",
        "Магазин глазами сотрудников платформы: статус, тариф, выручка и активность.",
    ),
    "TenantCreate": T(
        "A shop created on a customer's behalf, with its owner account.",
        "Mijoz nomidan, egasi hisobi bilan birga yaratiladigan do'kon.",
        "Магазин, создаваемый от имени клиента вместе с учётной записью владельца.",
    ),
    "TenantStatusUpdate": T(
        "Block or unblock a shop. A blocked shop's staff are refused from their next request.",
        "Do'konni bloklash yoki blokdan chiqarish. Bloklangan do'kon xodimlari keyingi so'rovidayoq rad etiladi.",
        "Блокировка или разблокировка магазина. Сотрудникам заблокированного магазина отказывают со следующего запроса.",
    ),
    "TenantPlanUpdate": T(
        "Move a shop to another plan or billing cycle.",
        "Do'konni boshqa tarif yoki to'lov davriga o'tkazish.",
        "Перевод магазина на другой тариф или период оплаты.",
    ),
    "PlanIn": T(
        "A new subscription plan: price, limits and features.",
        "Yangi obuna tarifi: narx, cheklovlar va imkoniyatlar.",
        "Новый тариф подписки: цена, лимиты и возможности.",
    ),
    "PlanOut": T(
        "A subscription plan, with how many shops are on it and what it earns.",
        "Obuna tarifi, unda nechta do'kon borligi va qancha daromad keltirishi bilan.",
        "Тариф подписки с числом магазинов на нём и приносимой выручкой.",
    ),
    "PlanUpdate": T(
        "Changes to a plan. Only the fields sent are changed. The code cannot change.",
        "Tarifga o'zgartirishlar. Faqat yuborilgan maydonlar o'zgaradi. Kodni o'zgartirib bo'lmaydi.",
        "Изменения тарифа. Меняются только переданные поля. Код изменить нельзя.",
    ),
    # ------------------------------------------------------------------- enums
    "UserRole": T(
        "A person's role, which grants a default set of permissions.\n\n- `owner` — everything in the shop, including billing, branches and settings\n- `manager` — catalog, inventory, staff, refunds, shifts and reports; no billing or settings\n- `cashier` — the till: sell, and open and close their own shift\n- `super_admin` — platform staff; belongs to no shop",
        "Xodimning roli; har bir rol standart ruxsatlar to'plamini beradi.\n\n- `owner` — ega: do'kondagi hamma narsa, to'lov, filiallar va sozlamalar ham\n- `manager` — menejer: katalog, ombor, xodimlar, qaytarishlar, smenalar va hisobotlar; to'lov va sozlamalarsiz\n- `cashier` — kassir: sotish, o'z smenasini ochish va yopish\n- `super_admin` — platforma xodimi; hech bir do'konga tegishli emas",
        "Роль сотрудника; каждая роль даёт стандартный набор прав.\n\n- `owner` — владелец: всё в магазине, включая оплату, филиалы и настройки\n- `manager` — менеджер: каталог, склад, сотрудники, возвраты, смены и отчёты; без оплаты и настроек\n- `cashier` — кассир: продажи, открытие и закрытие своей смены\n- `super_admin` — сотрудник платформы; не принадлежит ни одному магазину",
    ),
    "OrderStatus": T(
        "Where a sale stands.\n\n- `draft` — a parked cart, not yet paid\n- `completed` — paid in full\n- `partially_refunded` — some lines returned\n- `refunded` — everything returned\n- `voided` — cancelled",
        "Sotuv holati.\n\n- `draft` — to'xtatib qo'yilgan savat, hali to'lanmagan\n- `completed` — to'liq to'langan\n- `partially_refunded` — ayrim qatorlar qaytarilgan\n- `refunded` — hammasi qaytarilgan\n- `voided` — bekor qilingan",
        "Состояние продажи.\n\n- `draft` — отложенная корзина, ещё не оплачена\n- `completed` — оплачена полностью\n- `partially_refunded` — часть строк возвращена\n- `refunded` — возвращено всё\n- `voided` — аннулирована",
    ),
    "PaymentMethod": T(
        "How money changed hands.\n\n- `cash` — notes and coins; counted in the drawer at close\n- `card` — bank card on a terminal\n- `mobile` — a payment app or QR code\n- `bank_transfer` — transfer to the shop's account\n- `store_credit` — credit held for a customer",
        "Pul qanday to'langani.\n\n- `cash` — naqd pul; smena yopilganda yashikda sanaladi\n- `card` — terminal orqali bank kartasi\n- `mobile` — to'lov ilovasi yoki QR kod\n- `bank_transfer` — do'kon hisobiga o'tkazma\n- `store_credit` — mijoz uchun saqlangan kredit",
        "Как были переданы деньги.\n\n- `cash` — наличные; пересчитываются в ящике при закрытии смены\n- `card` — банковская карта через терминал\n- `mobile` — платёжное приложение или QR-код\n- `bank_transfer` — перевод на счёт магазина\n- `store_credit` — кредит, хранящийся за клиентом",
    ),
    "DiscountType": T(
        "How a discount is expressed.\n\n- `none` — no discount\n- `percent` — `discount_value` is a percentage\n- `fixed` — `discount_value` is an amount in the shop currency",
        "Chegirma qanday ifodalanadi.\n\n- `none` — chegirma yo'q\n- `percent` — `discount_value` foiz\n- `fixed` — `discount_value` do'kon valyutasidagi summa",
        "Как задаётся скидка.\n\n- `none` — без скидки\n- `percent` — `discount_value` в процентах\n- `fixed` — `discount_value` — сумма в валюте магазина",
    ),
    "ProductUnit": T(
        "The unit a product is sold in. Weight and length units allow fractional quantities.\n\n`piece`, `kg`, `gram`, `liter`, `meter`, `pack`, `box`",
        "Mahsulot sotiladigan o'lchov birligi. Og'irlik va uzunlik birliklari kasr miqdorga ruxsat beradi.\n\n`piece` (dona), `kg`, `gram`, `liter`, `meter`, `pack` (qadoq), `box` (quti)",
        "Единица, в которой продаётся товар. Весовые и линейные единицы допускают дробное количество.\n\n`piece` (штука), `kg`, `gram`, `liter`, `meter`, `pack` (упаковка), `box` (коробка)",
    ),
    "StockMovementType": T(
        "Why stock changed.\n\n- `initial` — opening stock\n- `purchase` — a delivery\n- `sale` — sold at the till\n- `return` — put back after a refund\n- `adjustment` — a correction or stocktake difference\n- `transfer_in` / `transfer_out` — moved between branches\n- `waste` — damaged, expired or lost",
        "Qoldiq nima uchun o'zgargani.\n\n- `initial` — boshlang'ich qoldiq\n- `purchase` — yetkazib berish\n- `sale` — kassada sotilgan\n- `return` — qaytarishdan keyin javonga qaytarilgan\n- `adjustment` — tuzatish yoki inventarizatsiya farqi\n- `transfer_in` / `transfer_out` — filiallar orasida ko'chirilgan\n- `waste` — shikastlangan, muddati o'tgan yoki yo'qolgan",
        "Почему изменился остаток.\n\n- `initial` — начальный остаток\n- `purchase` — поставка\n- `sale` — продано на кассе\n- `return` — возвращено на полку после возврата\n- `adjustment` — корректировка или расхождение инвентаризации\n- `transfer_in` / `transfer_out` — перемещение между филиалами\n- `waste` — порча, истёк срок или потеря",
    ),
    "ShiftStatus": T(
        "- `open` — the till is taking money\n- `closed` — the drawer has been counted",
        "- `open` — kassa pul qabul qilmoqda\n- `closed` — yashik sanalgan",
        "- `open` — касса принимает деньги\n- `closed` — ящик пересчитан",
    ),
    "TenantStatus": T(
        "A shop's standing on the platform.\n\n- `trial` — in its free trial\n- `active` — paying\n- `suspended` — blocked by platform staff or for non-payment; staff cannot sign in\n- `cancelled` — closed; its history is kept",
        "Do'konning platformadagi holati.\n\n- `trial` — bepul sinov davrida\n- `active` — to'lov qilmoqda\n- `suspended` — platforma tomonidan yoki to'lov qilinmagani uchun bloklangan; xodimlar kira olmaydi\n- `cancelled` — yopilgan; tarixi saqlanadi",
        "Положение магазина на платформе.\n\n- `trial` — на бесплатном пробном периоде\n- `active` — платит\n- `suspended` — заблокирован платформой или за неуплату; сотрудники не могут войти\n- `cancelled` — закрыт; история сохраняется",
    ),
    "SubscriptionStatus": T(
        "- `trialing` — free trial\n- `active` — paid and current\n- `past_due` — payment overdue, in the grace period\n- `canceled` — will not renew\n- `expired` — ended",
        "- `trialing` — bepul sinov\n- `active` — to'langan va amalda\n- `past_due` — to'lov kechikkan, imtiyozli davrda\n- `canceled` — yangilanmaydi\n- `expired` — tugagan",
        "- `trialing` — бесплатный пробный период\n- `active` — оплачена и действует\n- `past_due` — оплата просрочена, льготный период\n- `canceled` — не будет продлена\n- `expired` — закончилась",
    ),
    "BillingCycle": T(
        "- `monthly` — billed every month\n- `yearly` — billed once a year",
        "- `monthly` — har oy to'lanadi\n- `yearly` — yiliga bir marta to'lanadi",
        "- `monthly` — оплата каждый месяц\n- `yearly` — оплата раз в год",
    ),
    "InvoiceStatus": T(
        "- `draft` — not yet issued\n- `open` — awaiting payment\n- `paid` — settled\n- `void` — cancelled\n- `uncollectible` — written off",
        "- `draft` — hali chiqarilmagan\n- `open` — to'lov kutilmoqda\n- `paid` — to'langan\n- `void` — bekor qilingan\n- `uncollectible` — hisobdan chiqarilgan",
        "- `draft` — ещё не выставлен\n- `open` — ожидает оплаты\n- `paid` — оплачен\n- `void` — аннулирован\n- `uncollectible` — списан",
    ),
    "ReportType": T(
        "- `sales_summary` — totals by day\n- `sales_detailed` — every sale and line\n- `tax` — tax collected, by rate\n- `inventory` — stock on hand and its value\n- `employee_performance` — sales by cashier",
        "- `sales_summary` — kunlar bo'yicha jami\n- `sales_detailed` — har bir sotuv va qator\n- `tax` — stavkalar bo'yicha yig'ilgan soliq\n- `inventory` — ombordagi qoldiq va uning qiymati\n- `employee_performance` — kassirlar bo'yicha sotuvlar",
        "- `sales_summary` — итоги по дням\n- `sales_detailed` — каждая продажа и строка\n- `tax` — собранный налог по ставкам\n- `inventory` — остатки и их стоимость\n- `employee_performance` — продажи по кассирам",
    ),
    "ReportFormat": T(
        "File format of a report: `csv`, `xlsx` or `pdf`.",
        "Hisobot fayli formati: `csv`, `xlsx` yoki `pdf`.",
        "Формат файла отчёта: `csv`, `xlsx` или `pdf`.",
    ),
    "ReportStatus": T(
        "- `pending` — queued\n- `running` — being generated\n- `completed` — ready to download\n- `failed` — see `error_message`",
        "- `pending` — navbatda\n- `running` — tayyorlanmoqda\n- `completed` — yuklab olishga tayyor\n- `failed` — `error_message` ga qarang",
        "- `pending` — в очереди\n- `running` — формируется\n- `completed` — готов к скачиванию\n- `failed` — см. `error_message`",
    ),
}
