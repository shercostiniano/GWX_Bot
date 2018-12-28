import gspread, time
from gspread import CellNotFound
from oauth2client.service_account import ServiceAccountCredentials
from telegram import ReplyKeyboardMarkup

index_balance = 6
index_refer_code = 7
index_referred_user = 8
index_already_referred = 9
index_facebook = 10
index_twitter = 11
index_instagram = 12
index_youtube = 13

joinButton = 'Join Channel'
balanceButton = 'Check Balance'
rewardButton = 'Get More Rewards'
referral = "Referral"

no_refer_keyboard = ReplyKeyboardMarkup([[referral, rewardButton], [joinButton, balanceButton]], resize_keyboard=True)
yes_refer_keyboard = ReplyKeyboardMarkup([[rewardButton], [joinButton, balanceButton]], resize_keyboard=True)


def gspreadUpdater():
    global worksheet
    while True:
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(credentials)
        sheet = client.open("GWX Airdrop")
        worksheet = sheet.worksheet("Telegram")
        time.sleep(3590)


def existing(bot, update):
    global already_referred
    try:
        ID = update.message.from_user.id
        find_id = worksheet.find(str(ID))
        already_referred = worksheet.cell(find_id.row, index_already_referred).value

        result = {'Found_ID': True, 'Already_Referred': already_referred}
        if str(ID) == find_id.value:
            return result

    except CellNotFound:
        return False


def getUserReferral(bot, update):
    global user_referral, find_id, ID
    try:
        ID = update.message.from_user.id
        find_id = worksheet.find(str(ID))
        user_referral = worksheet.cell(find_id.row, index_refer_code)

        return user_referral.value

    except CellNotFound or NameError:
        return None


def checkReferral(bot, update, referrer_code):
    try:
        ID = update.message.from_user.id
        find_id = worksheet.find(str(ID))
        user_referral = worksheet.cell(find_id.row, index_refer_code)
        find_referrer = worksheet.find(referrer_code)
        referrer_users = worksheet.cell(find_referrer.row, index_referred_user).value

        if user_referral.value == find_referrer.value:
            return False

        else:
            worksheet.update_cell(find_referrer.row, index_referred_user, int(referrer_users) + 1)  # Add referred users
            worksheet.update_cell(find_id.row, index_already_referred,
                                  'TRUE')  # Add True to know whether a user has already used a referral code
            addReferrerBalance(find_referrer.row, index_balance, 20)
            return True

    except CellNotFound or ValueError:
        return False


def submitData(timestamp, uid, username, email, wallet, balance, referral_code, referred_user, already_referred,
               facebook_status, twitter_status, instagram_status, youtube_status):
    worksheet.append_row(
        [timestamp, uid, username, email, wallet, balance, referral_code, referred_user, already_referred,
         facebook_status, twitter_status, instagram_status, youtube_status])


def storeInformation(bot, update):
    uid = update.message.from_user.id
    uname = update.message.from_user.username

    info = {'user_id': uid, 'user_name': uname}
    return info


def checkBalance(bot, update):
    ID = update.message.from_user.id
    find_id = worksheet.find(str(ID))

    referred_user = worksheet.cell(find_id.row, index_referred_user).value
    balance = worksheet.cell(find_id.row, index_balance).value
    update.message.reply_text(f"Your current balance: {balance} GWX\n"
                              f"Referred Users: {referred_user}")


def addUserBalance(points):
    balance = worksheet.cell(find_id.row, index_balance).value
    worksheet.update_cell(find_id.row, index_balance, int(balance) + points)


def addReferrerBalance(row, col, points):
    referrer_balance = worksheet.cell(row, col).value
    worksheet.update_cell(row, col, int(referrer_balance) + points)


def changeKeyboard(bot, update):
    if existing(bot, update)['Already_Referred'] == 'TRUE':
        return yes_refer_keyboard
    else:
        return no_refer_keyboard


def taskComplete(task):
    if task == 'facebook':
        worksheet.update_cell(find_id.row, index_facebook, 'COMPLETE')

    elif task == 'twitter':
        worksheet.update_cell(find_id.row, index_twitter, 'COMPLETE')

    elif task == 'instagram':
        worksheet.update_cell(find_id.row, index_instagram, 'COMPLETE')

    elif task == 'youtube':
        worksheet.update_cell(find_id.row, index_youtube, 'COMPLETE')

