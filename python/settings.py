from os import getenv

BotToken = getenv('BOT_TOKEN', None)
if BotToken == '' or BotToken == None:
    with open('telegram.txt', 'r') as fp:
        BotToken = fp.read()

SheetsAccJson = getenv('SHEETS_ACC_JSON', None)
SheetsSecret = './serviceacc.json'
if SheetsAccJson != None and SheetsAccJson != '':
    with open(SheetsSecret, 'w') as fp:
        fp.write(SheetsAccJson)

SheetsName = getenv('SHEETS_NAME', 'Таблица адвент календаря ночного петушка')

SheetTiming = getenv('SHEET_TIMING', 'Время')
SheetGroups = getenv('SHEET_GROUPS', 'Группы')
SheetPivot = getenv('SHEET_PIVOT', 'Уже разосланные сообщения')
SheetPhrases = getenv('SHEET_PHRASES', 'Фразы для поиска')
SheetMainText = getenv('SHEET_MAIN_TEXT', 'Основной текст')
SheetPictures = getenv('SHEET_PICTURES', 'Картинки')

TimingUpdateTime = int(getenv('TIMING_UPDATE_TIME', '10'))