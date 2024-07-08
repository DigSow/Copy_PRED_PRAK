# Импортируем библиотеки
import time
import pandas as pd
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path  # Импортируем путь к chromedriver

# Инициализация сервиса ChromeDriver
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
CommClear = []  # Список для хранения комментариев и оценок

Email = "kirik-novo@bk.ru"
Password = "Ozenib23"

# Открытие начальной страницы с отзывами
driver.get("https://www.ucheba.ru/uz/5904/opinions?")
driver.find_elements(By.XPATH, '//span[contains(text(), "Войти")]/..')[0].click()
time.sleep(2)# Ожидание загрузки страницы

driver.find_elements(By.XPATH, '//span[contains(text(), "У меня есть пароль")]/..')[0].click()
time.sleep(2)# Ожидание загрузки страницы

#Писк элемента Email
elements1 = driver.find_elements(By.XPATH,
                                 '//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/form/div[1]/div/div/input')
if elements1:
    elements1[0].send_keys(str(Email))
else:
    print("Element not found")

#Писк элемента Password
elements2 = driver.find_elements(By.XPATH,
                                 '//*[@id="__next"]/div[2]/div[1]/div[2]/div/div[1]/form/div[3]/div/div/input')
if elements2:
    elements2[0].send_keys(str(Password))
else:
    print("Element not found")
time.sleep(2)# Ожидание загрузки страницы

driver.find_elements(By.XPATH, '//span[contains(text(), "Войти")]/..')[0].click()
time.sleep(1)  # Ожидание загрузки страницы


# Цикл по страницам с отзывами
for p in range(1, 5):
    driver.get(f"https://www.ucheba.ru/uz/5904/opinions?page={p}")
    # Нажатие на кнопку "Показать все отзывы"
    driver.find_elements(By.XPATH, '//span[contains(text(), "Показать все отзывы")]/..')[0].click()
    html = driver.page_source  # Получение HTML-кода страницы
    soup = BS(html, "html.parser")  # Парсинг HTML с помощью BeautifulSoup
    # Поиск элементов с комментариями и оценками
    table1_div = soup.find_all('div', {'class': 'Text-styles__Block-sc-f5d4cf80-0 hoHpZD'})
    table2_div = soup.find_all('div', {'class': 'Text-styles__Block-sc-f5d4cf80-0 kLRwDs'})
    # Создание пар (кортежей) из данных table1_div и table2_div
    combined_data = list(zip([i.text.strip().replace('\n', '') for i in table1_div],
                             [i.text.strip().replace('\n', '') for i in table2_div]))
    # Добавление данных в CommClear
    CommClear.extend(combined_data)
    time.sleep(3)  # Ожидание перед загрузкой следующей страницы

# Закрытие драйвера
driver.quit()

# Создание DataFrame из CommClear
df = pd.DataFrame(CommClear, columns=['Комментарий', 'Оценка'])

# Фильтрация комментариев по длине
df = df[df['Комментарий'].apply(lambda x: len(x) > 23)]

# Сброс индекса DataFrame
df = df.reset_index(drop=True)

# Вывод DataFrame в консоль
print(df)

# Сохранение DataFrame в CSV файл с кодировкой utf-8-sig
df.to_csv('output.csv', encoding='utf-8-sig')
