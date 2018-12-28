from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError, ReplyKeyboardRemove
from register import REWARDS, MAIN, TYPING_REFER, REFERRAL
from googleRefreshToken import changeKeyboard, checkReferral

fbPhoto = 'Facebook Screenshot'
twitterPhoto = 'Twitter Screenshot'
instagramPhoto = 'Instagram Screenshot'
youtubePhoto = 'Youtube Screenshot'
back = 'Back'

statusFb = InlineKeyboardButton("Facebook", 'https://facebook.com/GWX')
statusTwitter = InlineKeyboardButton("Twitter", 'https://twitter.com/GWX')
statusInstagram = InlineKeyboardButton("Instagram", 'https://instagram.com/GWX')
statusYoutube = InlineKeyboardButton("Youtube", 'https://youtube.com/GWX')

YES = 'YES'
NO = 'NO'


def referralInvite(bot, update):
    update.message.reply_text("Did someone referred you?",
                              reply_markup=ReplyKeyboardMarkup([[YES, NO]], resize_keyboard=True),
                              resize_keyboard=True)
    return REFERRAL


def referralCheck(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text

    if text == YES:
        update.message.reply_text("Please type the referrer's code",
                                  reply_markup=ReplyKeyboardRemove([[YES, NO]]),
                                  resize_keyboard=True)
        return TYPING_REFER
    else:
        update.message.reply_text("Please skip this step",
                                  reply_markup=changeKeyboard(bot, update),
                                  resize_keyboard=True)
        return MAIN


def receivedRefer(bot, update, user_data):
    try:
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text
        del user_data['choice']
        getReferral = user_data.get(YES)

        if checkReferral(bot, update, getReferral):
            update.message.reply_text("🎉 Success! 🎉",
                                      reply_markup=changeKeyboard(bot, update),
                                      resize_keyboard=True)
            return MAIN

        else:
            update.message.reply_text(
                """🔸🔸🔸🔸🔸 ❌ Invalid referral code ❌ 🔸🔸🔸🔸🔸\n\n\
    📌 Make sure you followed the requirements: 📌\n
            ✅ The referral code sent by your referrer
            ✅ Typed the code correctly
            ✅ You did not typed your own referral code""")
            return referralInvite(bot,update)

    except ValueError:
        return referralInvite(bot, update)


def getRewards(bot, update):
    try:
        update.message.reply_text("To be able to get rewards you need to complete the following tasks:\n"
                                  "📌 Like our Facebook Page\n"
                                  "📌 Follow our Twitter Profile\n"
                                  "📌 Follow our Instagram Profile\n"
                                  "📌 Subscribe to our Youtube Channel\n",
                                  reply_markup=InlineKeyboardMarkup(
                                      [[statusFb, statusTwitter], [statusInstagram, statusYoutube]]),
                                  disable_web_page_preview=True)

        update.message.reply_text("📷 Send the screenshots showing that you have completed the task\n",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[fbPhoto, twitterPhoto], [instagramPhoto, youtubePhoto], [back]], resize_keyboard=True))

        return REWARDS

    except TelegramError:
        getRewards(bot, update)


def completeFacebook():
    return False


def completeTwitter():
    return False


def completeInstagram():
    return False


def completeYoutube():
    pass


def completedTasks():
    pass


def joinChannel(bot, update):
    update.message.reply_text("https://t.me/GWXAirdropChannel")
    return MAIN


def goBack(bot, update):
    update.message.reply_text("Back",
                              reply_markup=changeKeyboard(bot, update), resize_keyboard=True)
    return MAIN
