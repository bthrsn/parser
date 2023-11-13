import os

# URL сайта для поиска
url = 'https://topdeck.ru/apps/toptrade/singles/search'

#  path to credentials file
script_dir = os.path.dirname(__file__)
credentials_path = os.path.join(script_dir, 'credentials/client_secret_330292702592-d0cobi5smnpa7m5c2g00iseis7rtserh.apps.googleusercontent.com.json')

# Имя файла в гугл таблицах
spreadsheet_name = 'Cards'
# Имя листа
worksheet_name = 'Sale'
