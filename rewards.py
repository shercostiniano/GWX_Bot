import time
import webbrowser

from telegram import ReplyKeyboardMarkup

from account import facebook_task, twitter_task, instagram_task, youtube_task, back, completed_task, \
    facebook_verify_button, twitter_verify_button, instagram_verify_button, youtube_verify_button
from register import REWARDS, TASK
from spreadsheet_jobs import addUserBalance, taskComplete, gspreadUpdater, checkStatus
from task_verify import facebook_verify, twitter_verify, instagram_verify, youtube_verify


def facebook(bot, update):
    global fb_current_count

    if checkStatus(bot, update)['Facebook'] != 'COMPLETE':
        update.message.reply_text("🔄  Go to our Facebook Page.... \n https://facebook.com",
                                  disable_web_page_preview=True)

        fb_current_count = facebook_verify()
        update.message.reply_text("Press DONE if you completed the task",
                                  reply_markup=ReplyKeyboardMarkup([[facebook_verify_button]], resize_keyboard=True))

        return TASK

    else:
        update.message.reply_text("Task already completed",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        return REWARDS


def twitter(bot, update):
    global twitter_current_count

    if checkStatus(bot, update)['Twitter'] != 'COMPLETE':
        update.message.reply_text("🔄  Go to our Twitter Page.... \n https://twitter.com",
                                  disable_web_page_preview=True)

        twitter_current_count = twitter_verify()
        update.message.reply_text("Press DONE if you completed the task",
                                  reply_markup=ReplyKeyboardMarkup([[twitter_verify_button]], resize_keyboard=True))

        return TASK

    else:
        update.message.reply_text("Task already completed",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        return REWARDS


def instagram(bot, update):
    global instagram_current_count
    if checkStatus(bot, update)['Instagram'] != 'COMPLETE':
        update.message.reply_text("🔄  Go to our Instagram Page.... \n https://instagram.com",
                                  disable_web_page_preview=True)

        instagram_current_count = instagram_verify()
        update.message.reply_text("Press DONE if you completed the task",
                                  reply_markup=ReplyKeyboardMarkup([[instagram_verify_button]], resize_keyboard=True))

        return TASK

    else:
        update.message.reply_text("Task already completed",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        return REWARDS


def youtube(bot, update):
    global youtube_current_count
    if checkStatus(bot, update)['Youtube'] != 'COMPLETE':
        update.message.reply_text("🔄  Go to our Youtube Channel.... \n https://youtube.com",
                                  disable_web_page_preview=True)

        youtube_current_count = youtube_verify()
        update.message.reply_text("Press DONE if you completed the task",
                                  reply_markup=ReplyKeyboardMarkup([[youtube_verify_button]], resize_keyboard=True))

        return TASK
    else:
        update.message.reply_text("Task already completed",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        return REWARDS


def completeFacebook(bot, update):
    fb_new_count = facebook_verify()
    if fb_new_count > fb_current_count:
        update.message.reply_text("Success you completed facebook task",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        # Write COMPLETE to worksheet
        taskComplete('facebook')
        addUserBalance(bot, update, 600)
        return REWARDS

    else:
        update.message.reply_text("Task not yet complete",
                                  reply_markup=ReplyKeyboardMarkup([[facebook_verify_button]], resize_keyboard=True))

        return TASK


def completeTwitter(bot, update):
    twitter_new_count = twitter_verify()

    if twitter_new_count > twitter_current_count:
        update.message.reply_text("Success you completed twitter task",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        # Write COMPLETE to worksheet
        taskComplete('twitter')
        addUserBalance(bot, update, 600)
        return REWARDS

    else:
        update.message.reply_text("Task not yet complete",
                                  reply_markup=ReplyKeyboardMarkup([[twitter_verify_button]], resize_keyboard=True))

        return TASK


def completeInstagram(bot, update):
    instagram_new_count = instagram_verify()

    if instagram_new_count > instagram_current_count:
        update.message.reply_text("Success you completed instagram task",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        # Write COMPLETE to worksheet
        taskComplete('instagram')
        addUserBalance(bot, update, 600)
        return REWARDS

    else:
        update.message.reply_text("Task not yet complete",
                                  reply_markup=ReplyKeyboardMarkup([[instagram_verify_button]], resize_keyboard=True))

        return TASK


def completeYoutube(bot, update):
    youtube_new_count = youtube_verify()

    if youtube_new_count > youtube_current_count:
        update.message.reply_text("Success you completed youtube task",
                                  reply_markup=ReplyKeyboardMarkup(
                                      [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                       [back]],
                                      resize_keyboard=True))
        # Write COMPLETE to worksheet
        taskComplete('youtube')
        addUserBalance(bot, update, 600)
        return REWARDS

    else:
        update.message.reply_text("Task not yet complete",
                                  reply_markup=ReplyKeyboardMarkup([[youtube_verify_button]], resize_keyboard=True))

        return TASK


def completedTasks(bot, update):
    # Get the COMPLETED tasks in worksheet
    complete = ["✅ " + task for task, value in checkStatus(bot, update).items() if value == "COMPLETE"]
    show = "\n".join(complete)
    update.message.reply_text(f"These are the completed tasks: \n{show}",
                              reply_markup=ReplyKeyboardMarkup(
                                  [[facebook_task, twitter_task], [instagram_task, youtube_task], [completed_task],
                                   [back]],
                                  resize_keyboard=True))
    return REWARDS
