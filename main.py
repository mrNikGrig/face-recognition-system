import os
import requests
from dotenv import load_dotenv


user_id = input("Введите требуемый id ВКонтакте: ")

f = open(".env")
A_TOKEN = f.read()
f.close()

url_VK = f"https://api.vk.ru/method/users.get?user_ids={user_id}&fields=bdate,&access_token={A_TOKEN}&v=5.131"

response_VK = requests.get(url_VK)
if response_VK.status_code == 200:
    data = response_VK.json()

    if 'response' in data:
        user_info = data['response'][0]
        f = open("info.txt", "w")
        f.write(f"Фамилия: {user_info['last_name']}\nИмя: {user_info['first_name']}\nДата рождения: {user_info['bdate']}")
        f.close()
    else:
        print("Ошибка записи в файл")
else:
    print(f"Ошибка: {response_VK.status_code}")