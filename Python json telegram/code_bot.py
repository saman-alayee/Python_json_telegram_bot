from telegram.ext import MessageHandler, CommandHandler, Updater, Filters
from telegram import ReplyKeyboardMarkup
import json


#########################################################################

# MAKE YOUR BOT IN @BOTFATHER AND SAVE TOKEN
# INSTALL pip install python-telegram-bot
# REPLACE TOKEN IN LINE 355
## REPLACE YOUR ID ADMIN CODE IN LINE 17 


#########################################################################


ID_ADMIN = ID admin


def read_db():
    data_file = open('db.json', 'r')
    json_object = json.load(data_file)
    data_file.close()
    return json_object


def write_db(json_object):
    data_file = open('db.json', 'w')
    json.dump(json_object, data_file)
    data_file.close()


def start(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()

    if str(chat_id) in db.keys():
        update.bot.sendMessage(chat_id=chat_id,
                               text='خوش برگشتی')
        update.bot.sendMessage(chat_id=chat_id, text='چه کاری می خواهید انجام دهید؟',
                               reply_markup=ReplyKeyboardMarkup(
                                   [['کیف پول'], ['سبد خرید'], ['مشاهده محصولات', 'کدهای تخفیف'], ['راهنما', 'درباره ما']]))
    else:
        db[str(chat_id)] = {'pool': 0, 'sabad': []}
        update.bot.sendMessage(chat_id=chat_id,
                               text='خوش اومدی')
        update.bot.sendMessage(chat_id=chat_id, text='چه کاری می خواهید انجام دهید؟',
                               reply_markup=ReplyKeyboardMarkup(
                                   [['کیف پول'], ['سبد خرید'], ['مشاهده محصولات', 'کدهای تخفیف'], ['راهنما', 'درباره ما']]))
        write_db(db)


def kif_pool(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    user_data = db[str(chat_id)]
    mojodi = str(user_data['pool'])
    text = ' برای افزایش موجودی متنی مشابه متن زیر با مبلغ دلخواه برای ربات ارسال کنید \n\n افزایش 1000'
    update.bot.sendMessage(
        chat_id=chat_id, text='موجودی شما \n '+mojodi + '\n\n' + text)


def afzayesh_mojoodi(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    try:
        mablagh = bot.message.text.split(' ')
        mablagh = int(mablagh[1])
        if mablagh > 0:
            user_data = db[str(chat_id)]
            user_data['pool'] += mablagh
            db[str(chat_id)] = user_data
            write_db(db)
            update.bot.sendMessage(chat_id=chat_id, text='موجودی افزایش یافت')
        else:
            update.bot.sendMessage(
                chat_id=chat_id, text='برای افزایش موجودی عددی مثبت وارد کنید')
    except:
        update.bot.sendMessage(chat_id=chat_id, text='خطا در دریافت مبلغ')


def sabad_kharid(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    user_data = db[str(chat_id)]
    if not user_data['sabad']:
        update.bot.sendMessage(chat_id=chat_id, text='سبد شما خالی است')
    else:
        tedad = str(len(user_data['sabad']))
        set_sabad = set(user_data['sabad'])
        text = 'پیش فاکتور :\n'
        for mahsool in set_sabad:
            tedad_mahsool = user_data['sabad'].count(mahsool)
            text += '\nکد محصول : ' + str(mahsool)
            text += '\n قیمت محصول : ' + \
                str(db['mahsoolat'][mahsool]['gheymat'])
            text += '\n تعداد محصول در سبد : ' + str(tedad_mahsool)
        jam_kol = 0
        for code in user_data['sabad']:
            jam_kol += float(db['mahsoolat'][code]['gheymat'])
        text += '\n قیمت کل : ' + str(jam_kol)
        update.bot.sendMessage(chat_id=chat_id, text=text)
        text = 'شما ' + tedad + ' محصول آماده ی پرداخت دارید \n برای تسویه حساب کلمه ی پرداخت را ارسال کنید\nو برای استفاده از کد تخفیف ، کد را بعد از کلمه پرداخت بنویسید'
        update.bot.sendMessage(chat_id=chat_id, text=text)


def afzoodan_mahsool(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    code_mahsool = bot.message.text.split(' ')
    code_mahsool = str(code_mahsool[1])
    if code_mahsool in db['mahsoolat'].keys():
        if db['mahsoolat'][code_mahsool]['tedad'] > 0:
            user_data = db[str(chat_id)]
            user_data['sabad'].append(code_mahsool)
            update.bot.sendMessage(
                chat_id=chat_id, text='محصول مورد نظر به سبد شما اضافه شد')
            db[str(chat_id)] = user_data
            db['mahsoolat'][code_mahsool]['tedad'] -= 1
            write_db(db)
        else:
            update.bot.sendMessage(
                chat_id=chat_id, text='تعداد محصول مورد نظر تمام شده است')
    else:
        update.bot.sendMessage(
            chat_id=chat_id, text='محصولی با این کد پیدا نشد')


def afzoodan_code(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    if chat_id != ID_ADMIN:
        update.bot.sendMessage(
            chat_id=chat_id, text='فقط ادمین می تواند کد تخفیف جدید اضافه کند')
        return

    update.bot.sendMessage(
        chat_id=chat_id, text='در حال تلاش برای ثبت کد تخفیف جدید')
    try:
        data = bot.message.text.split('\n')
        tedad = int(data[-1])
        darasd = int(data[-2])
        code = str(data[-3])
        db['codeha'][code] = {'darsad': darasd, 'tedad': tedad}
        write_db(db)
        update.bot.sendMessage(chat_id=chat_id, text='کد با موفقیت افزوده شد')
    except:
        update.bot.sendMessage(
            chat_id=chat_id, text='لطفا مشابه الگو اطلاعات را وارد کنید')


def pardakht(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    user_data = db[str(chat_id)]
    jam_kol = 0
    if not user_data['sabad']:
        update.bot.sendMessage(chat_id=chat_id, text='سبد شما خالی است')
        return
    text = 'فاکتور :\n'
    set_sabad = set(user_data['sabad'])
    for mahsool in set_sabad:
        tedad_mahsool = user_data['sabad'].count(mahsool)
        text += '\nکد محصول : ' + str(mahsool)
        text += '\n قیمت محصول : ' + str(db['mahsoolat'][mahsool]['gheymat'])
        text += '\n تعداد محصول در سبد : ' + str(tedad_mahsool)
    jam_kol = 0
    for code in user_data['sabad']:
        jam_kol += float(db['mahsoolat'][code]['gheymat'])
    text += '\n قیمت کل : ' + str(jam_kol)
    update.bot.sendMessage(chat_id=chat_id, text=text)
    if len(bot.message.text) == 6:
        if jam_kol <= float(user_data['pool']):
            user_data['pool'] -= jam_kol
            db[str(chat_id)] = user_data
            user_data['sabad'] = []
            write_db(db)
            update.bot.sendMessage(
                chat_id=chat_id, text='محصولات با موفقیت خریداری شد')
            update.bot.sendMessage(
                chat_id=chat_id, text='\n مبلغ پرداخت شده : ' + str(jam_kol))
        else:
            text = 'موجودی برای پرداخت کافی نیست \n لطفا حساب خود را شارژ کنید'
            update.bot.sendMessage(chat_id=chat_id, text=text)
    else:  # ba code takhfif
        code_takhfif = bot.message.text.split(' ')
        code_takhfif = str(code_takhfif[1])
        if code_takhfif not in db['codeha'].keys():
            update.bot.sendMessage(
                chat_id=chat_id, text='کد وارد شده معتبر نیست')
            return
        # else :
        if db['codeha'][code_takhfif]['tedad'] == 0:
            update.bot.sendMessage(
                chat_id=chat_id, text='کد مورد نظر منقضی شده است')
            return
        jam_kol -= jam_kol * \
            (float(db['codeha'][code_takhfif]['darsad']) / 100)
        if jam_kol <= float(user_data['pool']):
            user_data['pool'] -= jam_kol
            user_data['sabad'] = []
            db[str(chat_id)] = user_data
            db['codeha'][code_takhfif]['tedad'] -= 1
            write_db(db)
            update.bot.sendMessage(
                chat_id=chat_id, text='محصولات با موفقیت خریداری شد')
            update.bot.sendMessage(
                chat_id=chat_id, text='\n مبلغ پرداخت شده با تخفیف : ' + str(jam_kol))
        else:
            text = 'موجودی برای پرداخت کافی نیست \n لطفا حساب خود را شارژ کنید'
            update.bot.sendMessage(chat_id=chat_id, text=text)


def moshahede_mahsoolat(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    list_keyboard = []
    for code in db['mahsoolat'].keys():
        list_keyboard.append([])
        list_keyboard[-1].append('افزودن '+str(code)+' به سبد خرید')
        text = 'کد محصول  \n' + str(code)
        text += '\n نام محصول  \n' + str(db['mahsoolat'][code]['nam'])
        text += '\n قیمت محصول  \n ' + str(db['mahsoolat'][code]['gheymat'])
        text += '\n تعداد باقی مانده  \n ' + \
            str(db['mahsoolat'][code]['tedad'])
        text += '\n برند محصول  \n ' + str(db['mahsoolat'][code]['berand'])
        update.bot.sendMessage(chat_id=chat_id, text=text)
    list_keyboard.append(['منوی اصلی'])
    update.bot.sendMessage(chat_id=chat_id, text='پایان نمایش محصولات',
                           reply_markup=ReplyKeyboardMarkup(list_keyboard))


def moshahede_takhfif(bot, update):
    chat_id = bot.message.chat_id
    db = read_db()
    if not db['codeha'].keys():
        update.bot.sendMessage(
            chat_id=chat_id, text='فعلا کد تخفیفی وجود ندارد')
        return
    msg = 'کدهای تخفیف موجود : \n'
    for code in db['codeha'].keys():
        if db['codeha'][code]['tedad'] != 0:
            msg += '\nکد : ' + str(code) + '\n درصد تخفیف : ' + str(
                db['codeha'][code]['darsad']) + '\n تعداد : ' + str(db['codeha'][code]['tedad'])
    update.bot.sendMessage(chat_id=chat_id, text=msg)


def msg_handler(bot, update):
    if bot.message is not None:
        chat_id = bot.message.chat_id

        if bot.message.text == 'کیف پول':
            kif_pool(bot, update)

        elif bot.message.text == 'منوی اصلی':
            update.bot.sendMessage(chat_id=chat_id, text='چه کاری می خواهید انجام دهید؟',
                                   reply_markup=ReplyKeyboardMarkup(
                                       [['کیف پول'], ['سبد خرید'], ['مشاهده محصولات', 'کدهای تخفیف'], ['راهنما', 'درباره ما']]))
        elif bot.message.text[:6] == 'افزایش':
            afzayesh_mojoodi(bot, update)

        elif bot.message.text == 'درباره ما':
            text = 'Made by Saman Alayee \n suppot : @Saamaannnn'
            update.bot.sendMessage(chat_id=chat_id, text=text)

        elif bot.message.text == 'راهنما':
            text = 'برای افزودن محصولات به سبد خرید متنی مشابه زیر برای ربات ارسال کنید \n'
            text += 'افزودن 1 \n\n'
            text += 'برای پرداخت سبد خرید «پرداخت» را برای ربات ارسال کنید و اگر کد تخفیف دارید مانند زیر عمل کنید \n'
            text += 'پرداخت qwe'
            # text += '\n\n ----ویژه ادمین---- \n\n'
            # text += 'برای افزدون محصول مشابه زیر عمل کنید\n'
            # text += 'محصول\n'
            # text += 'نام محصول\n'
            # text += 'قیمت محصول \n'
            # text += 'تعداد محصول \n'
            # text += 'برند محصول \n'
            # text += 'آیدی محصول(غیر تکراری) \n'
            # text += ' برای افزودن کد تخفیف مانند زیر عمل کنید \n'
            # text += 'کد\n'
            # text += 'کد تخفیف\n'
            # text += 'درصد تخفیف \n'
            # text += 'تعداد مصرفی (برای نامحدود -1 وارد کنید)\n'
            update.bot.sendMessage(chat_id=chat_id, text=text)

        elif bot.message.text == 'سبد خرید':
            sabad_kharid(bot, update)

        elif bot.message.text[:6] == 'افزودن':
            afzoodan_mahsool(bot, update)

        elif bot.message.text[:6] == 'پرداخت':
            pardakht(bot, update)

        elif bot.message.text == 'مشاهده محصولات':
            moshahede_mahsoolat(bot, update)

        elif bot.message.text == 'کدهای تخفیف':
            moshahede_takhfif(bot, update)
            return

        elif bot.message.text[:2] == 'کد':
            afzoodan_code(bot, update)


def creat_db():
    db = {'mahsoolat': {}, 'codeha': {}}
    mahsoolat = {
        'a': {
            'nam': 'Galaxy A51',
            'gheymat': 2000,
            'tedad': 100,
            'berand': 'Samsung'
        },
        'b': {
            'nam': 'Galaxy A21s',
            'gheymat': 1987,
            'tedad': 50,
            'berand': 'Samsung'
        },
        'c': {
            'nam': 'Redmi Note 8',
            'gheymat': 2514,
            'tedad': 144,
            'berand': 'Xiaomi'
        },
        'd': {
            'nam': 'iPhone 11 Pro Max',
            'gheymat': 5420,
            'tedad': 10,
            'berand': 'Apple'
        },
        'e': {
            'nam': 'Galaxy A20s',
            'gheymat': 1400,
            'tedad': 500,
            'berand': 'Samsung'
        }

    }
    db['mahsoolat'] = mahsoolat
    codeha = {
        'test':
        {
            'darsad': 50,
            'tedad': -1
        }
    }
    db['codeha'] = codeha
    write_db(db)


def main():
    creat_db()
    updater = Updater('TOKEN')
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, msg_handler))
    updater.start_polling()
    updater.idle()


main()
