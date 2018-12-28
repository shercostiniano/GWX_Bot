import datetime
import re
import time
import random, string

from telegram import ReplyKeyboardMarkup
from googleRefreshToken import submitData, changeKeyboard

REGISTER, CHOOSING, TYPING_REPLY, MAIN, REWARDS, TYPING_REFER, REFERRAL = range(7)

email = 'Email Address'
cryptoAddress = 'Ethereum/Bitcoin/Stellar Address'
DONE = 'DONE'
createButton = 'Create Profile'

joinButton = 'Join Channel'
balanceButton = 'Check Balance'
rewardButton = 'Get More Rewards'
referral = "Referral"

no_refer_keyboard = ReplyKeyboardMarkup([[referral, rewardButton], [joinButton, balanceButton]], resize_keyboard=True)
yes_refer_keyboard = ReplyKeyboardMarkup([[rewardButton], [joinButton, balanceButton]], resize_keyboard=True)


def registerAccount(bot, update):
    update.message.reply_text("To register you are required to input the following:\n"
                              "📌 Email Addres\n"
                              "📌 Wallet Address",
                              reply_markup=ReplyKeyboardMarkup([[email], [cryptoAddress], [DONE]],
                                                               resize_keyboard=True),
                              disable_web_page_preview=True)
    return CHOOSING


def done(bot, update, user_data):
    userID = update.message.from_user.id
    emailOutput = user_data.get(email)
    cryptoAddressOutput = user_data.get(cryptoAddress)
    username = "@" + update.message.from_user.username.capitalize()
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    balance = 0.00
    referral_code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    referred_users = 0

    if emailOutput is None:
        update.message.reply_text("Please fill up your email address")
        return CHOOSING

    elif cryptoAddressOutput is None:
        update.message.reply_text("Please fill up your wallet address")
        return CHOOSING

    elif not verifyEmail(emailOutput):
        update.message.reply_text("Invalid email, please correct your email to complete the registration")
        return CHOOSING

    elif not verifyWallet(cryptoAddressOutput):
        update.message.reply_text(
            "Invalid wallet address, please correct your wallet address to complete the registration")
        return CHOOSING

    else:
        submitData(timestamp, userID, username, emailOutput, cryptoAddressOutput, balance, referral_code,
                   referred_users, already_referred=False)
        update.message.reply_text("Successfully Registered!\n"
                                  "Referral Code: " + str(referral_code),
                                  reply_markup=changeKeyboard(bot, update))
        return MAIN


def gettingInformation(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    update.message.reply_text('Please type your {}'.format(text.lower()))

    return TYPING_REPLY


def receivedInformation(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    update.message.reply_text("{}".format(listInformation(user_data)),
                              reply_markup=ReplyKeyboardMarkup([[email], [cryptoAddress], [DONE]],
                                                               resize_keyboard=True),
                              disable_web_page_preview=True)
    return CHOOSING


def listInformation(user_data):
    info = list()

    for key, value in user_data.items():
        info.append('{} - {}'.format(key, value))

    return "\n".join(info).join(['\n', '\n'])


def verifyEmail(email):
    try:
        emailVerify = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

        if not re.match(emailVerify, email):
            return False
        else:
            return True

    except TypeError:
        return None


def verifyWallet(wallet):
    try:
        btcVerify = r"^(1|3).{25,34}$"
        ethVerify = r"^0x.{40}$"

        if re.match(btcVerify, wallet):
            return True

        elif re.match(ethVerify, wallet):
            return True

        else:
            return False
    except TypeError:
        return None
