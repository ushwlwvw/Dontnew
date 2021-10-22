from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

ERROR_MESSAGE = "عـذرا هـنالك خـطأ ما في الاستخراج \n\n**الخـطأ** : {} "


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "**اضغط في الاسفل لبدأ عملبة الاستخراج**",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("Telethon", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("بـدأ صنـع كـود تيرمكـس".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, '▾∮ اهلا بك مجددا في بوت استخراج كود تيرمكس \n الان عليك ارسال ايبي ايدي هنا', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('عـذرا الايبي ايدي يجـب ان يكـون ارقـام اعـد تشغيل البوت مجددا\n /start', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'حسـنا الان ارسـل الايبـي هـاش', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'حسنا الان ارسل رقم الحساب مع كود الدولة  ! \nمثـال  : `+96476543210`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("** يتم الان ارسال كود التحقق **")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('الايبي ايدي والايبي هاش خـطأ يرجى اعاة الاستخراج من جديد', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('** رقم الهاتف خطا يرجى التاكد من الرقم واعادة الاستخراج من جديد', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "- حسنا لقد تم ارسال كود التحقق اليك من قبل تليكرام  \n الان انسخ الكود وضع بين كل رقم مسافة مثل  : `1 2 3 4 5`", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('انتهى مدة كود التحقق استخرج من جديد', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('كـود التحقـق خطـأ يرجـى الاستخراج من جديد والتاكد من وصع مسافه بين كل رقم عند ارسال الكود.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('انتهت مده كود التحقق يرجى استخراج كود تيرمكس مره ثانيه من جديد', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, '**يبدو ان حسابك مفعـل رمز التحقـق بخطـوتين يرجى ارسال الرمز الان**', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('انتهت المـدة استخرج من جديد.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('عـذرا رمـز التحقـق غيـر صحيح يـرجى الاستـخراج من جديـد\n/start', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "** هذا هو كود تيرمكس الخاص بك ** \n\n`{}` \n\n ملاحظة  :  لا تقم بمشاركه هذا الكود الى اي شخص حتى لو انه من مطوريم السورس\n CH:  @Jmthon".format("TELETHON" if telethon else "PYROGRAM", string_session)
    await client.send_message("me", text)
    await client.disconnect()
    await phone_code_msg.reply("تم بنجاح استخـراج كـود تيرمكـس يـرجى التأكد من الرسـائل المحـفوظة \n\n CH:  @JMTHON".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("تم الغاء العملية بنجاح !", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("تم اعادة تشغيل البوت بنجاح !", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم الغاء الاستخراج بنجاح !", quote=True)
        return True
    else:
        return False


# @Client.on_message(filters.private & ~filters.forwarded & filters.command(['cancel', 'restart']))
# async def formalities(_, msg):
#     if "/cancel" in msg.text:
#         await msg.reply("Cancelled all the Processes!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     elif "/restart" in msg.text:
#         await msg.reply("Restarted the Bot!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
#         return True
#     else:
#         return False
