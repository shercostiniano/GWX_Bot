#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters, CallbackQueryHandler
from register import *
from spreadsheet_jobs import *
from account import *
from rewards import *
import logging, threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update, args):
    global referral_code, user_name
    referral_code = getUserReferral(bot, update)
    user_name = storeInformation(bot, update)['user_name']
    try:
        if existing(bot, update):
            update.message.reply_text("Welcome back " + user_name +
                                      "\nReferral Code: " + str(referral_code),
                                      reply_markup=main_keyboard,
                                      resize_keyboard=True)

            return MAIN

        else:
            update.message.reply_text(
                "Thank you for joining the Telegram Group!\n"
                "Press/click on 'Create Profile' to key in your: \n"
                "🔷 Email address,\n"
                "🔔 A total of 50,000 GWX tokens could\n"
                "be yours!\n",
                reply_markup=ReplyKeyboardMarkup([[createButton]], resize_keyboard=True, one_time_keyboard=True))

            return REGISTER
    except NameError or TypeError:
        update.message.reply_text(
            "Thank you for joining the Telegram Group!\n"
            "Press/click on 'Create my AcuToken Bounty\n"
            "Profile' to key in your\n"
            "🔷 Emaill address,\n"
            "🔷 Stellar address,\n"
            "🔷 Twitter handle,\n"
            "and to submit the following:\n"
            "🔷 Facebook screenshot showing you\n"
            "have followed AcuToken's Facebook\n"
            "page\n"

            "🔔 A total of 50,000 ACU tokens could\n"
            "be yours!\n",
            reply_markup=ReplyKeyboardMarkup([[createButton]], resize_keyboard=True, one_time_keyboard=True))

        return REGISTER


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def cancel(bot, update):
    update.message.reply_text("Goodbye! \n Type /start if you want to visit me again 🤖",
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater("")
    dp = updater.dispatcher

    main_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start, pass_args=True)],

        states={
            REGISTER: [RegexHandler('^(' + createButton + ')$', registerAccount)],

            CHOOSING: [RegexHandler('^(' + email + ')$', gettingInformation, pass_user_data=True),
                       RegexHandler('^(' + cryptoAddress + ')$', gettingInformation, pass_user_data=True),
                       RegexHandler('^(' + DONE + ')$', done, pass_user_data=True)
                       ],
            MAIN: [RegexHandler('^(' + balanceButton + ')$', checkBalance),
                   RegexHandler('^(' + joinButton + ')$', joinChannel),
                   RegexHandler('^(' + rewardButton + ')$', getRewards),
                   RegexHandler('^(' + referral + ')$', referralInvite)
                   ],

            REFERRAL: [RegexHandler('^(' + YES + ')$', referralCheck, pass_user_data=True),
                       RegexHandler('^(' + NO + ')$', referralCheck, pass_user_data=True)],

            REWARDS: [RegexHandler('^(' + facebook_task + ')$', facebook),
                      RegexHandler('^(' + twitter_task + ')$', twitter),
                      RegexHandler('^(' + instagram_task + ')$', instagram),
                      RegexHandler('^(' + youtube_task + ')$', youtube),
                      RegexHandler('^(' + completed_task + ')$', completedTasks),
                      RegexHandler('^(' + back + ')$', goBack)],

            TASK: [RegexHandler('^(' + facebook_verify_button + ')$', completeFacebook),
                   RegexHandler('^(' + twitter_verify_button + ')$', completeTwitter),
                   RegexHandler('^(' + instagram_verify_button + ')$', completeInstagram),
                   RegexHandler('^(' + youtube_verify_button + ')$', completeYoutube)],


            TYPING_REPLY: [MessageHandler(Filters.text, receivedInformation, pass_user_data=True)],
            TYPING_REFER: [MessageHandler(Filters.text, receivedRefer, pass_user_data=True)]

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(main_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    # Refresh Token
    gsUpdateThread = threading.Thread(target=gspreadUpdater)
    gsUpdateThread.daemon = True
    gsUpdateThread.start()
    # End of Refresh Token
    updater.idle()


if __name__ == '__main__':
    main()
