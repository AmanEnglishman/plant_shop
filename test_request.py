import requests

url = 'http://127.0.0.1:8000/api/v1/plant/1/comments/'

# Получаем токен (предположим, что токен сохранен)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyOTA3NzUwLCJpYXQiOjE3NDI5MDc0NTAsImp0aSI6IjQ2MDkzZjdiZjA5YjQzMmQ5MGYxZjQ0ZjAwZjM5OWNjIiwidXNlcl9pZCI6MX0.1B69o34zuS2LaaSLMcUQoxHDG5aqCY5TaboTlIqVqu4"

# Данные для запроса
data = {
    "plant": 1,
    "text": "Очень красивое растение!"
}

# Заголовки с авторизацией
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

# Отправляем POST запрос с аутентификацией
response = requests.post(url, json=data, headers=headers)

# Выводим статус-код и тело ответа
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")

# Если статус-код 200, то пробуем распарсить JSON
if response.status_code == 200:
    print(response.json())
else:
    print("Non-200 response, no JSON to decode.")

