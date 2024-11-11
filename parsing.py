from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json

# Настраиваем ChromeDriver с помощью webdriver-manager
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Запуск драйвера с заданными опциями
driver = webdriver.Chrome(service=service, options=options)
driver.get('http://quotes.toscrape.com')

quotes_data = []

try:
    # Цикл для перехода по страницам и сбора данных
    while True:
        # Ожидаем загрузки цитат на странице
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'quote')))

        # Извлекаем все цитаты на текущей странице
        quotes = driver.find_elements(By.CLASS_NAME, 'quote')

        for quote in quotes:
            # Извлекаем текст цитаты
            quote_text = quote.find_element(By.CLASS_NAME, 'text').text

            # Извлекаем автора
            author = quote.find_element(By.CLASS_NAME, 'author').text

            # Извлекаем теги
            tags_elements = quote.find_elements(By.CLASS_NAME, 'tag')
            tags = [tag.text for tag in tags_elements]

            # Добавляем данные цитаты в список
            quotes_data.append({
                'text': quote_text,
                'author': author,
                'tags': tags
            })

        # Проверяем наличие кнопки "Next" для перехода на следующую страницу
        try:
            next_button = driver.find_element(By.XPATH, '//li[@class="next"]/a')
            next_button.click()
        except:
            # Кнопка "Next" отсутствует, выходим из цикла
            break

finally:
    # Закрываем драйвер
    driver.quit()

# Сохраняем данные в JSON файл
with open('quotes_data.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

print("Сбор данных завершен. Данные сохранены в 'quotes_data.json'")
