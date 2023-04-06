from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
- مرحبا بك في بوت الخليفه 

من هذا البوت يمكنك استخراج كود تيرمكس بسهولة وبسرعة و بدون مشاكل اختر امر الاستخراج في الاسفل واكمل العملية  ، 

@aaaalqp
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(" • بدء الاستخراج  •", callback_data="generate")],
        [InlineKeyboardButton(text="• الواجهة الرئيسية •", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("• بدء الاستخراج  •", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("• بدء الاستخراج •", callback_data="generate")],
        [InlineKeyboardButton("• قناة الخليفه •", url="https://t.me/aaaalqp")],
        [
            InlineKeyboardButton("• اوامر البوت •", callback_data="help"),
            InlineKeyboardButton("• حول البوت •", callback_data="about")
        ],
    ]


    # Help Message
    HELP = """ 
✨ الاوامر المتوفرة التي يمكنك مساعدة استخدام البوت بسلاسة هي : ✨

/about 
لعـرض معلومـات البـوت
/help 
 لعـرض اوامـر البوت
/start 
 لتشغـيل البـوت
/generate 
لبـدء استخـراج كود تيرمكس
"""

    # About Message
    ABOUT = """
بوت استخراج كود تيرمكس 

وهـو عبـارة عن بوت بسيط للمساعـدة في استخـراج كـود تيرمكس بسهولة وبأمان تام  ومساعدك في عمليه تنصيب سورس جمثون 

قناة السورس  : 
@Jmthon
>    """
