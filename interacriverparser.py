import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import json


def on_button_click():
    url = entry.get()
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус-код HTTP
        soup = BeautifulSoup(response.text, 'html.parser')

        # Пример извлечения данных из HTML и преобразования их в JSON
        data = {
            'title': soup.title.string if soup.title else '',
            'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            'links': [{'text': a.get_text().strip(), 'href': a['href']} for a in soup.find_all('a', href=True)],
            'paragraphs': [p.get_text().replace('\n', ' ').strip() for p in soup.find_all('div')],
        }

        # Преобразуем извлеченные данные в JSON
        json_data = json.dumps(data, indent=2, ensure_ascii=False)

        # Очищаем виджет Text перед вставкой новых данных
        data_text.delete(1.0, tk.END)
        data_text.insert(tk.END, json_data)
        success_label.config(text="Данные извлечены!")

    except requests.exceptions.HTTPError as e:
        success_label.config(text=f"HTTP ошибка: {response.status_code}")
        data_text.delete(1.0, tk.END)
    except requests.exceptions.RequestException as e:
        success_label.config(text=f"Ошибка запроса: {e}")
        data_text.delete(1.0, tk.END)
    except Exception as e:
        success_label.config(text=f"Ошибка: {e}")
        data_text.delete(1.0, tk.END)

def clear_entry():
    entry.delete(0, tk.END)

# Создаем главное окно
root = tk.Tk()
root.title("Простое приложение Tkinter")

# Создаем виджеты
label = tk.Label(root, text="Введите URL:", font=("Arial", 16))
entry = tk.Entry(root, font=("Arial", 14))
button = tk.Button(root, text="Нажми меня", command=on_button_click, font=("Arial", 14))
clear_button = tk.Button(root, text="Очистить", command=clear_entry, font=("Arial", 14))
success_label = tk.Label(root, text="", font=("Arial", 16))

# Создаем текстовый виджет с прокруткой
frame = tk.Frame(root)
frame.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

data_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 10))
data_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=data_text.yview)

# Размещаем виджеты с помощью grid
label.grid(row=0, column=0, padx=10, pady=10)
entry.grid(row=1, column=0, padx=10, pady=5)
button.grid(row=2, column=0, padx=10, pady=5)
clear_button.grid(row=2, column=1, padx=10, pady=5)
success_label.grid(row=3, column=0, padx=10, pady=5)
frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Разрешаем изменение размеров для текстового виджета и фрейма
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Запускаем главное окно
root.mainloop()
