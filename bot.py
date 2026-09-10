# -*- coding: utf-8 -*-
"""
SORCE-Shop | ربات ساده فروش سورس در تلگرام
اجرا روی گوشی با Pydroid 3

نصب پیش‌نیاز (فقط یک‌بار) داخل Pydroid 3:
    pip install aiogram

قبل از اجرا، بخش CONFIG پایین همین فایل رو پر کن (توکن ربات، آیدی عددی ادمین، شماره کارت).
سپس فایل رو با دکمه Run در Pydroid 3 اجرا کن.
"""

import asyncio
import logging
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ============================ CONFIG ============================
BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"          # توکن ربات از @BotFather
ADMIN_IDS = [111111111]                        # آیدی عددی خودت (از @userinfobot بگیر) - میشه چندتا گذاشت
CARD_NUMBER = "6037-XXXX-XXXX-XXXX"            # شماره کارت برای واریز
CARD_HOLDER = "نام و نام خانوادگی صاحب کارت"    # نام صاحب کارت
DB_PATH = "sorce_shop.db"
# ==================================================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


# ---------------------------- Database ----------------------------
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            available INTEGER DEFAULT 1,
            delivery_content TEXT
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            product_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            receipt_file_id TEXT,
            created_at TEXT
        )"""
    )
    conn.commit()
    conn.close()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


# ---------------------------- Keyboards ----------------------------
def main_menu_kb(user_id: int) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text="🛒 سورس‌ها"), KeyboardButton(text="📦 سورس‌های من")],
    ]
    if is_admin(user_id):
        rows.append([KeyboardButton(text="⚙️ پنل ادمین")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def admin_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ افزودن سورس", callback_data="admin_add")],
            [InlineKeyboardButton(text="📋 لیست سورس‌ها", callback_data="admin_list")],
            [InlineKeyboardButton(text="🕓 سفارش‌های در انتظار", callback_data="admin_pending")],
        ]
    )


# ---------------------------- FSM States ----------------------------
class AddProduct(StatesGroup):
    title = State()
    description = State()
    price = State()
    delivery = State()


class BuyFlow(StatesGroup):
    waiting_receipt = State()


# ============================ USER SIDE ============================
@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "به SORCE-Shop خوش اومدی 👋\nاز دکمه‌های پایین استفاده کن:",
        reply_markup=main_menu_kb(message.from_user.id),
    )


@router.message(F.text == "🛒 سورس‌ها")
async def list_products(message: Message):
    conn = db()
    rows = conn.execute("SELECT * FROM products WHERE available=1").fetchall()
    conn.close()
    if not rows:
        await message.answer("فعلاً هیچ سورسی موجود نیست.")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{r['title']} - {r['price']:,} تومان", callback_data=f"show:{r['id']}")]
            for r in rows
        ]
    )
    await message.answer("سورس‌های موجود:", reply_markup=kb)


@router.callback_query(F.data.startswith("show:"))
async def show_product(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    conn = db()
    p = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    conn.close()
    if not p or not p["available"]:
        await callback.answer("این سورس دیگه موجود نیست.", show_alert=True)
        return
    text = f"📦 {p['title']}\n\n{p['description'] or '-'}\n\n💰 قیمت: {p['price']:,} تومان"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 خرید", callback_data=f"buy:{p['id']}")],
            [InlineKeyboardButton(text="🔙 بازگشت", callback_data="back_list")],
        ]
    )
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "back_list")
async def back_to_list(callback: CallbackQuery):
    conn = db()
    rows = conn.execute("SELECT * FROM products WHERE available=1").fetchall()
    conn.close()
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{r['title']} - {r['price']:,} تومان", callback_data=f"show:{r['id']}")]
            for r in rows
        ]
    )
    await callback.message.edit_text("سورس‌های موجود:", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("buy:"))
async def buy_product(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    conn = db()
    p = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    already = conn.execute(
        "SELECT * FROM orders WHERE user_id=? AND product_id=? AND status IN ('pending','approved')",
        (callback.from_user.id, product_id),
    ).fetchone()
    conn.close()
    if not p or not p["available"]:
        await callback.answer("این سورس دیگه موجود نیست.", show_alert=True)
        return
    if already:
        await callback.answer("شما قبلاً برای این سورس سفارش ثبت کردید.", show_alert=True)
        return

    await state.update_data(product_id=product_id)
    await state.set_state(BuyFlow.waiting_receipt)
    await callback.message.answer(
        f"مبلغ {p['price']:,} تومان رو به کارت زیر واریز کن و عکس رسید رو همینجا بفرست:\n\n"
        f"💳 {CARD_NUMBER}\n👤 به نام: {CARD_HOLDER}\n\n"
        f"⚠️ بعد از ارسال رسید، ادمین بررسی و تایید می‌کنه."
    )
    await callback.answer()


@router.message(BuyFlow.waiting_receipt, F.photo)
async def receive_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data["product_id"]
    file_id = message.photo[-1].file_id

    conn = db()
    p = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    cur = conn.execute(
        "INSERT INTO orders (user_id, username, product_id, status, receipt_file_id, created_at) "
        "VALUES (?, ?, ?, 'pending', ?, ?)",
        (message.from_user.id, message.from_user.username or "-", product_id, file_id, datetime.now().isoformat()),
    )
    order_id = cur.lastrowid
    conn.commit()
    conn.close()

    await state.clear()
    await message.answer("رسید دریافت شد ✅ منتظر تایید ادمین باش.")

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ تایید", callback_data=f"approve:{order_id}"),
                InlineKeyboardButton(text="❌ رد", callback_data=f"reject:{order_id}"),
            ]
        ]
    )
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_photo(
                admin_id,
                file_id,
                caption=f"سفارش جدید #{order_id}\nسورس: {p['title']}\nکاربر: @{message.from_user.username or message.from_user.id}",
                reply_markup=kb,
            )
        except Exception as e:
            logging.warning(f"failed to notify admin {admin_id}: {e}")


@router.message(BuyFlow.waiting_receipt)
async def receipt_wrong_type(message: Message):
    await message.answer("لطفاً عکس رسید پرداخت رو ارسال کن.")


@router.message(F.text == "📦 سورس‌های من")
async def my_products(message: Message):
    conn = db()
    rows = conn.execute(
        """SELECT products.title, products.description, products.delivery_content, orders.status
           FROM orders JOIN products ON orders.product_id = products.id
           WHERE orders.user_id=?""",
        (message.from_user.id,),
    ).fetchall()
    conn.close()
    if not rows:
        await message.answer("هنوز هیچ سورسی نخریدی.")
        return
    lines = []
    for r in rows:
        if r["status"] == "approved":
            lines.append(f"✅ {r['title']}\n📎 تحویل: {r['delivery_content'] or 'با ادمین هماهنگ کن'}")
        elif r["status"] == "pending":
            lines.append(f"🕓 {r['title']} - در انتظار تایید")
        else:
            lines.append(f"❌ {r['title']} - رد شده")
    await message.answer("\n\n".join(lines))


# ============================ ADMIN SIDE ============================
@router.message(F.text == "⚙️ پنل ادمین")
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("پنل ادمین:", reply_markup=admin_panel_kb())


@router.callback_query(F.data == "admin_add")
async def admin_add_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return
    await state.set_state(AddProduct.title)
    await callback.message.answer("عنوان سورس رو بفرست:")
    await callback.answer()


@router.message(AddProduct.title)
async def admin_add_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddProduct.description)
    await message.answer("توضیحات سورس رو بفرست:")


@router.message(AddProduct.description)
async def admin_add_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("قیمت سورس رو به تومان بفرست (فقط عدد):")


@router.message(AddProduct.price)
async def admin_add_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("لطفاً فقط عدد بفرست. دوباره قیمت رو وارد کن:")
        return
    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.delivery)
    await message.answer(
        "لینک دانلود یا توضیح تحویل سورس رو بفرست (مثلاً لینک گیت‌هاب یا فایل).\n"
        "اگه فعلاً نداری بنویس: -"
    )


@router.message(AddProduct.delivery)
async def admin_add_delivery(message: Message, state: FSMContext):
    data = await state.get_data()
    conn = db()
    conn.execute(
        "INSERT INTO products (title, description, price, available, delivery_content) VALUES (?, ?, ?, 1, ?)",
        (data["title"], data["description"], data["price"], message.text),
    )
    conn.commit()
    conn.close()
    await state.clear()
    await message.answer(f"✅ سورس «{data['title']}» با قیمت {data['price']:,} تومان اضافه شد.")


@router.callback_query(F.data == "admin_list")
async def admin_list_products(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    conn = db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    if not rows:
        await callback.message.answer("هیچ سورسی ثبت نشده.")
        await callback.answer()
        return
    for r in rows:
        status = "✅ موجود" if r["available"] else "❌ ناموجود"
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="تغییر وضعیت موجودی", callback_data=f"toggle:{r['id']}"),
                    InlineKeyboardButton(text="🗑 حذف", callback_data=f"delete:{r['id']}"),
                ]
            ]
        )
        await callback.message.answer(
            f"#{r['id']} {r['title']} - {r['price']:,} تومان\n{status}", reply_markup=kb
        )
    await callback.answer()


@router.callback_query(F.data.startswith("toggle:"))
async def admin_toggle_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    product_id = int(callback.data.split(":")[1])
    conn = db()
    p = conn.execute("SELECT available FROM products WHERE id=?", (product_id,)).fetchone()
    new_status = 0 if p["available"] else 1
    conn.execute("UPDATE products SET available=? WHERE id=?", (new_status, product_id))
    conn.commit()
    conn.close()
    await callback.answer("وضعیت موجودی تغییر کرد ✅")


@router.callback_query(F.data.startswith("delete:"))
async def admin_delete_product(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    product_id = int(callback.data.split(":")[1])
    conn = db()
    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    await callback.message.edit_text("🗑 سورس حذف شد.")
    await callback.answer()


@router.callback_query(F.data == "admin_pending")
async def admin_pending_orders(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    conn = db()
    rows = conn.execute(
        """SELECT orders.id, orders.receipt_file_id, products.title, orders.user_id
           FROM orders JOIN products ON orders.product_id = products.id
           WHERE orders.status='pending'"""
    ).fetchall()
    conn.close()
    if not rows:
        await callback.message.answer("سفارش در انتظاری وجود نداره.")
        await callback.answer()
        return
    for r in rows:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ تایید", callback_data=f"approve:{r['id']}"),
                    InlineKeyboardButton(text="❌ رد", callback_data=f"reject:{r['id']}"),
                ]
            ]
        )
        await callback.message.answer_photo(
            r["receipt_file_id"], caption=f"سفارش #{r['id']} - {r['title']}", reply_markup=kb
        )
    await callback.answer()


@router.callback_query(F.data.startswith("approve:"))
async def admin_approve_order(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    order_id = int(callback.data.split(":")[1])
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    product = conn.execute("SELECT * FROM products WHERE id=?", (order["product_id"],)).fetchone()
    conn.execute("UPDATE orders SET status='approved' WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

    await bot.send_message(
        order["user_id"],
        f"✅ خرید «{product['title']}» تایید شد.\n📎 تحویل: {product['delivery_content'] or 'با ادمین هماهنگ کن'}",
    )
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n✅ تایید شد")
    await callback.answer("تایید شد")


@router.callback_query(F.data.startswith("reject:"))
async def admin_reject_order(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    order_id = int(callback.data.split(":")[1])
    conn = db()
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.execute("UPDATE orders SET status='rejected' WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

    await bot.send_message(order["user_id"], "❌ متاسفانه رسید پرداخت شما تایید نشد. با ادمین در ارتباط باش.")
    await callback.message.edit_caption(caption=callback.message.caption + "\n\n❌ رد شد")
    await callback.answer("رد شد")


# ============================ RUN ============================
async def main():
    init_db()
    print("ربات روشن شد...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
