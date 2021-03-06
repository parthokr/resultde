import os

import telegram.ext
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler

from fetch_result import get_result

load_dotenv()
TOKEN = os.environ.get("TOKEN")

cache = {}


def any_msg(update: Update, context: CallbackContext) -> None:
    global cache
    split_msg = update.message.text.split(' ')
    if split_msg[0] == 'retry' or split_msg[0] == 'abar':
        split_msg = cache[update.effective_user.id]
    board_dict = {
        'bar': 'barisal',
        'chi': 'chittagong',
        'com': 'comilla',
        'dha': 'dhaka',
        'din': 'dinajpur',
        'jes': 'jessore',
        'mym': 'mymensingh',
        'raj': 'rajshahi',
        'syl': 'sylhet',
        'mad': 'madrasah',
        'tec': 'Technical',
        'dib': 'DIBS'
    }
    if split_msg[0].lower() == "resultde":
        try:
            exam = split_msg[1].lower()
            if exam == 'sscvoc':
                exam = 'ssc_voc'
            elif exam == 'hscvoc':
                exam = 'hsc_voc'
            elif exam == 'hscdic':
                exam = 'hsc_dic'

            year = split_msg[2]
            board = board_dict[split_msg[3].lower()]
            roll = split_msg[4]
            reg = split_msg[5]
            _result = get_result(exam, year, board, roll, reg)
            result = f'Name: {_result[0][0]}\n'
            for i in range(len(_result[1]) // 3):
                result += _result[1][i * 3 + 1] + ": \t" + _result[1][i * 3 + 2] + "\n"
        except Exception as e:
            print(e)
            result = "Something went wrong..."

        cache[update.effective_user.id] = split_msg
        update.message.reply_text(result)
        return
    msg = f"""
Hello *{update.effective_user.first_name}*
To get result follow the message format
```resultde <EXAM> <YEAR> <BOARD> <ROLL> <REGISTRATION NO>```

example: 
*resultde hsc 2021 raj 654321 987654321*

Use first three letters of board, i.e.,
====Board list====
Barisal ➜ bar
Chittagong ➜ chi
Comilla ➜  com
Dhaka ➜  dha
Dinajpur ➜  din
Jessore ➜  jes
Mymensingh ➜  mym
Rajshahi ➜  raj
Sylhet ➜  syl
Madrasah ➜ mad
Technical ➜  tec
DIBS ➜  dib

====Exam list====
jsc, ssc, sscvoc, hsc, hscvoc, hscdic, hsc

Note: Case doesn't matter. You can use any case.

Send __abar__ or __retry__ to resend last message.
If you find any issue with this bot feel free to raise an issue at https://github.com/parthokr/resultde/issues
"""
    update.message.reply_text(msg, parse_mode=telegram.ParseMode.MARKDOWN)


updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(telegram.ext.Filters.text, any_msg))
updater.start_polling()
updater.idle()
