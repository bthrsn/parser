import os
from config import url, credentials_path, spreadsheet_name, worksheet_name
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from bs4 import BeautifulSoup
import gspread

# Установка области видимости для доступа к Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Загружаем учетные данные OAuth 2.0 из файла JSON
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Авторизация в Google Sheets API
gc = gspread.authorize(creds)

# Открываем Google Sheets документ по его названию
sh = gc.open(spreadsheet_name)
worksheet = sh.worksheet(worksheet_name)

# Получаем список карт из Google Sheets
card_list = worksheet.col_values(1)[1:]  # Исключаем заголовок, начинаем со второй строки


# Заголовки для имитации запроса браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Цикл по списку карт
for i, card_name in enumerate(card_list, start=2):  # Начинаем с 2-й строки (после заголовка)
    # Параметры запроса
    params = {'query': card_name}

    # Отправляем GET-запрос на сайт
    response = requests.get(url, params=params, headers=headers)

    # Парсим HTML-код страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим элемент с минимальной ценой
    min_price_element = soup.find('div', class_='price').find('span', class_='low')

    # Получаем текст минимальной цены
    min_price = min_price_element.text.strip() if min_price_element else 'Цена не найдена'

    # Записываем данные в Google Sheets
    worksheet.update_cell(i, 2, min_price)  # Записываем минимальную цену во второй столбец

print('Данные сохранены в Google Sheets.')
