import os
from dotenv import load_dotenv
from weather import get_weather
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


load_dotenv()

Bot = Client(
    "Weather-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """Hello {},

I am a weather information finding bot. \
Give me a country/city/place name, \
I will send the weather informations about the place."""

HELP_TEXT = """**More Help**

- Just send me a country/city/place name
- Then I will check and send you the informations

**Informations :-**
Location details, current weather conditions \
(includes air quality details)"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Weather Bot`
- **Creator :**
  - [Telegram](https://telegram.me/FayasNoushad)
  - [GitHub](https://github.com/FayasNoushad)
- **Source :** [Click here](https://github.com/FayasNoushad/Weather-Bot/tree/main)
- **Language :** [Python3](https://python.org)
- **Framework :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Send Feedback', url='https://telegram.me/FayasNoushad')
        ],
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)
ERROR_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    
    else:
        await update.message.delete()


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.text)
async def weatherinfo(bot, update):
    
    try:
        details = get_weather(update.text)
    except KeyError:
        await update.reply_text(
            text="Key error.\nCan you check the name again."
        )
        return
    
    reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Send Feedback', url='https://telegram.me/FayasNoushad')]
    ])
    
    try:
        for i in details:
            await update.reply_text(
                text=i,
                disable_web_page_preview=True
            )
        await update.reply_text(
            text="Thanks for using me.",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as error:
        print(error)


Bot.run()
