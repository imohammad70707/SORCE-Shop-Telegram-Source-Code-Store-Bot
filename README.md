# 🛒 SORCE-Shop — Telegram Source Code Store Bot

[🇬🇧 English](#-english) | [🇮🇷 فارسی](#-فارسی)

---

# 🇬🇧 English

## 📌 About

**SORCE-Shop** is a simple single-file Telegram bot for selling source-code products.

Built with **Python and Aiogram**, the bot provides a complete basic workflow for browsing products, placing orders, submitting payment receipts, admin verification, and source delivery after approval.

The project is designed to be easy to configure and can be run directly on **Pydroid 3**.

## ✨ Features

### 👤 User

* 🛒 Browse available source codes
* 💰 View prices
* 📖 View source descriptions and details
* 🧾 Place an order
* 💳 View payment information
* 📸 Submit a payment receipt
* 📦 View **My Sources / My Orders**
* 🕓 Track order status
* 🔗 Receive the delivery link after approval

### 👑 Admin

* ➕ Add new source products
* 📝 Set title, description, and price
* 🔗 Add delivery link or content
* 📋 View source list
* 🟢 Change product availability
* 🔴 Mark products as unavailable
* 🗑️ Delete products
* 🕓 Manage pending orders
* ✅ Approve orders
* ❌ Reject orders
* 📸 Receive payment receipts automatically
* 🔔 Get notified when a new order is submitted

## 💳 Payment System

SORCE-Shop uses a **manual card-to-card payment workflow**.

The general process is:

1. The user selects a source.
2. The bot displays the payment information.
3. The user completes the payment.
4. The user sends a payment receipt.
5. The receipt is forwarded to the administrator.
6. The administrator approves or rejects the order.
7. If approved, the source delivery information is provided to the user.

> ⚠️ Payment information should be configured securely and should not be hard-coded into public repositories.

## 🗄️ Database

The bot uses **SQLite** for data storage.

The database is created automatically when the bot starts, so no separate database server is required.

Example database file:

```text
sorce_shop.db
```

## 🧩 Single-File Structure

The project is designed as a **single-file bot**, making it convenient for beginners and simple deployments.

Example:

```text
SORCE-Shop/
└── bot.py
```

The database file is generated automatically next to the bot.

## 🛠️ Technologies

* 🐍 Python
* 🤖 Aiogram
* 🗄️ SQLite
* 📱 Pydroid 3
* 📦 Telegram Bot API

## 🚀 Installation

Install the required dependency:

```bash
pip install aiogram
```

Then open `bot.py` and configure:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_IDS = [YOUR_ADMIN_ID]

CARD_NUMBER = "YOUR_CARD_NUMBER"
CARD_HOLDER = "YOUR_CARD_HOLDER"
```

After configuration, run:

```bash
python bot.py
```

The bot will automatically create the SQLite database.

## 📱 Running on Pydroid 3

SORCE-Shop can be run on Android using **Pydroid 3**.

Basic setup:

1. Install Pydroid 3.
2. Install `aiogram` using Pydroid's Pip section.
3. Copy `bot.py` to your device.
4. Configure the bot token and administrator settings.
5. Run the file.
6. Open the bot in Telegram and send `/start`.

## 🔐 Security

Never publish the following information in a public GitHub repository:

* Bot Token
* Private credentials
* Real payment credentials
* Sensitive administrator information

Use a private configuration or environment variables when deploying the bot publicly.

## 🔮 Future Improvements

Possible future additions:

* 🌐 Online payment gateway
* 👥 Multiple administrators
* 🔐 Admin permission levels
* 🗂️ Source categories
* 📊 Sales statistics
* 📈 Advanced reports
* 🔎 Source search
* 🧾 Order history
* ⚙️ Advanced store settings

---

# 🇮🇷 فارسی

## 📌 درباره پروژه

**SORCE-Shop** یک ربات ساده و تک‌فایلی تلگرام برای فروش سورس‌کد است.

این ربات با **Python و Aiogram** ساخته شده و یک سیستم کامل و ساده برای مشاهده محصولات، ثبت سفارش، ارسال رسید پرداخت، بررسی سفارش توسط ادمین و تحویل سورس پس از تأیید فراهم می‌کند.

پروژه به‌گونه‌ای طراحی شده که تنظیم و اجرای آن ساده باشد و بتوان آن را مستقیماً روی **Pydroid 3** اجرا کرد.

## ✨ قابلیت‌ها

### 👤 بخش کاربر

* 🛒 مشاهده لیست سورس‌ها
* 💰 نمایش قیمت
* 📖 مشاهده توضیحات و جزئیات سورس
* 🧾 ثبت سفارش
* 💳 نمایش اطلاعات پرداخت
* 📸 ارسال عکس رسید
* 📦 بخش **سورس‌های من / سفارش‌های من**
* 🕓 مشاهده وضعیت سفارش
* 🔗 دریافت لینک تحویل پس از تأیید

### 👑 بخش ادمین

* ➕ افزودن سورس جدید
* 📝 تعیین عنوان، توضیحات و قیمت
* 🔗 تعیین لینک یا محتوای تحویل
* 📋 مشاهده لیست سورس‌ها
* 🟢 تغییر وضعیت موجود بودن
* 🔴 ناموجود کردن سورس
* 🗑️ حذف سورس
* 🕓 مدیریت سفارش‌های در انتظار
* ✅ تأیید سفارش
* ❌ رد سفارش
* 📸 دریافت خودکار رسید پرداخت
* 🔔 اطلاع‌رسانی ثبت سفارش جدید برای ادمین

## 💳 سیستم پرداخت

SORCE-Shop از سیستم **کارت‌به‌کارت** استفاده می‌کند.

روند کلی خرید:

1. کاربر سورس موردنظر را انتخاب می‌کند.
2. اطلاعات پرداخت نمایش داده می‌شود.
3. کاربر پرداخت را انجام می‌دهد.
4. عکس رسید را برای ربات ارسال می‌کند.
5. رسید برای ادمین ارسال می‌شود.
6. ادمین سفارش را تأیید یا رد می‌کند.
7. در صورت تأیید، اطلاعات تحویل سورس برای کاربر ارسال می‌شود.

> ⚠️ اطلاعات پرداخت را به‌صورت امن نگهداری کنید و اطلاعات واقعی را داخل Repository عمومی GitHub قرار ندهید.

## 🗄️ دیتابیس

ربات از **SQLite** برای ذخیره اطلاعات استفاده می‌کند.

دیتابیس به‌صورت خودکار هنگام اجرای ربات ساخته می‌شود و نیازی به نصب یا تنظیم یک Database Server جداگانه نیست.

نمونه فایل دیتابیس:

```text
sorce_shop.db
```

## 🧩 ساختار تک‌فایلی

این پروژه به‌صورت **Single-File** طراحی شده و برای افراد مبتدی و اجراهای ساده مناسب است.

ساختار نمونه:

```text
SORCE-Shop/
└── bot.py
```

فایل دیتابیس نیز به‌صورت خودکار در کنار فایل ربات ایجاد می‌شود.

## 🛠️ تکنولوژی‌های استفاده‌شده

* 🐍 Python
* 🤖 Aiogram
* 🗄️ SQLite
* 📱 Pydroid 3
* 📦 Telegram Bot API

## 🚀 نصب

ابتدا کتابخانه موردنیاز را نصب کنید:

```bash
pip install aiogram
```

سپس فایل `bot.py` را باز کرده و تنظیمات زیر را وارد کنید:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_IDS = [YOUR_ADMIN_ID]

CARD_NUMBER = "YOUR_CARD_NUMBER"
CARD_HOLDER = "YOUR_CARD_HOLDER"
```

سپس ربات را اجرا کنید:

```bash
python bot.py
```

دیتابیس SQLite به‌صورت خودکار ساخته خواهد شد.

## 📱 اجرا روی Pydroid 3

SORCE-Shop قابلیت اجرا روی اندروید با استفاده از **Pydroid 3** را دارد.

مراحل کلی:

1. Pydroid 3 را نصب کنید.
2. از بخش Pip کتابخانه `aiogram` را نصب کنید.
3. فایل `bot.py` را به گوشی منتقل کنید.
4. Token و تنظیمات ادمین را وارد کنید.
5. فایل را اجرا کنید.
6. داخل تلگرام به ربات دستور `/start` بدهید.

## 🔐 امنیت

اطلاعات زیر را داخل Repository عمومی GitHub قرار ندهید:

* Bot Token
* اطلاعات محرمانه ورود
* اطلاعات واقعی پرداخت
* اطلاعات حساس ادمین

برای انتشار عمومی پروژه بهتر است تنظیمات محرمانه را در فایل خصوصی یا متغیرهای محیطی نگهداری کنید.

## 🔮 قابلیت‌های آینده

امکان اضافه‌کردن قابلیت‌های زیر در نسخه‌های بعدی وجود دارد:

* 🌐 درگاه پرداخت آنلاین
* 👥 پشتیبانی از چند ادمین
* 🔐 سطح دسترسی مختلف برای ادمین‌ها
* 🗂️ دسته‌بندی سورس‌ها
* 📊 آمار فروش
* 📈 گزارش‌های پیشرفته
* 🔎 جستجوی سورس
* 🧾 تاریخچه سفارش‌ها
* ⚙️ تنظیمات پیشرفته فروشگاه

---

## 👨‍💻 Developer

**Mohammad**

⭐ اگر پروژه برایتان مفید بود، به Repository ستاره بدهید.
