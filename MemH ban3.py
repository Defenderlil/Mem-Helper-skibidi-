import pyautogui
import pytesseract
from PIL import Image, ImageTk
import mss
import time
import threading
import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import keyboard

# Настройка пути к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Глобальные переменные
left, top, width, height = 100, 100, 200, 100
button_x, button_y = 500, 500
threshold_high = 2000  # Верхний порог
threshold_low = 1180   # Нижний порог
running = False  # Флаг для запуска и остановки процесса
show_screen = False  # Флаг для отображения экрана

# Функция для захвата и обновления области экрана
def update_screen_capture():
    with mss.mss() as sct:
        while running:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            img_tk = ImageTk.PhotoImage(img)
            
            if show_screen:
                label_screen.config(image=img_tk)
                label_screen.image = img_tk  # Сохранение ссылки, чтобы изображение отображалось

            # Обработка текста с помощью Tesseract
            text = pytesseract.image_to_string(img, config="--psm 6")
            try:
                cleaned_text = text.replace(",", "")
                number = int(''.join(filter(str.isdigit, cleaned_text)))
                print(f"Число найдено: {number}")
                if number > threshold_high or number < threshold_low:
                    pyautogui.click(button_x, button_y)
                    print(f"Нажата кнопка на ({button_x}, {button_y})!")
            except ValueError:
                print("Число не найдено")

            # Прерывание по сочетанию клавиш
            if keyboard.is_pressed("space") and keyboard.is_pressed("f"):
                stop_checking()
                print("Экстренное прерывание!")

            time.sleep(600)

# Функции для управления процессом и обновления настроек
def start_checking():
    global running
    if not running:
        running = True
        thread = threading.Thread(target=update_screen_capture)
        thread.daemon = True
        thread.start()
        messagebox.showinfo("Запущено", "Процесс запущен!")

def stop_checking():
    global running
    running = False
    messagebox.showinfo("Остановлено", "Процесс остановлен!")

def toggle_screen_view():
    global show_screen
    show_screen = not show_screen
    if not show_screen:
        label_screen.config(image="")  # Очистка изображения, если просмотр выключен
    messagebox.showinfo("Экран", f"Просмотр экрана {'включен' if show_screen else 'выключен'}")

def update_settings():
    global left, top, width, height, button_x, button_y, threshold_high, threshold_low
    try:
        left = int(entry_left.get())
        top = int(entry_top.get())
        width = int(entry_width.get())
        height = int(entry_height.get())
        button_x = int(entry_button_x.get())
        button_y = int(entry_button_y.get())
        threshold_high = int(entry_high.get())
        threshold_low = int(entry_low.get())
        messagebox.showinfo("Обновлено", "Настройки обновлены!")
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числовые значения!")

# Создание интерфейса
root = tk.Tk()
root.title("MemH Ban")
root.configure(bg="#1c1c1c")  # Черный фон

# Цвета
text_color = "#ffffff"
button_color = "#333333"
entry_bg = "#2e2e2e"
entry_fg = "#ffffff"

# Поля для ввода координат и настроек
tk.Label(root, text="Левый верхний угол (X, Y):", bg="#1c1c1c", fg=text_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_left = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_left.grid(row=0, column=1, padx=5, pady=5)
entry_left.insert(0, str(left))

entry_top = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_top.grid(row=0, column=2, padx=5, pady=5)
entry_top.insert(0, str(top))

tk.Label(root, text="Размер области (Ширина, Высота):", bg="#1c1c1c", fg=text_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_width = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_width.grid(row=1, column=1, padx=5, pady=5)
entry_width.insert(0, str(width))

entry_height = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_height.grid(row=1, column=2, padx=5, pady=5)
entry_height.insert(0, str(height))

tk.Label(root, text="Координаты кнопки (X, Y):", bg="#1c1c1c", fg=text_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_button_x = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_button_x.grid(row=2, column=1, padx=5, pady=5)
entry_button_x.insert(0, str(button_x))

entry_button_y = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_button_y.grid(row=2, column=2, padx=5, pady=5)
entry_button_y.insert(0, str(button_y))

tk.Label(root, text="Пороговое значение (Высокое):", bg="#1c1c1c", fg=text_color).grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_high = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_high.grid(row=3, column=1, padx=5, pady=5)
entry_high.insert(0, str(threshold_high))

tk.Label(root, text="Пороговое значение (Низкое):", bg="#1c1c1c", fg=text_color).grid(row=4, column=0, padx=5, pady=5, sticky="w")
entry_low = tk.Entry(root, width=10, bg=entry_bg, fg=entry_fg)
entry_low.grid(row=4, column=1, padx=5, pady=5)
entry_low.insert(0, str(threshold_low))

# Кнопки управления
tk.Button(root, text="Обновить настройки", command=update_settings, bg=button_color, fg=text_color).grid(row=5, column=0, columnspan=3, pady=10)
tk.Button(root, text="Запустить", command=start_checking, bg=button_color, fg=text_color).grid(row=6, column=0, columnspan=3, pady=5)
tk.Button(root, text="Остановить", command=stop_checking, bg=button_color, fg=text_color).grid(row=7, column=0, columnspan=3, pady=5)
tk.Button(root, text="Вкл/Выкл просмотр экрана", command=toggle_screen_view, bg=button_color, fg=text_color).grid(row=8, column=0, columnspan=3, pady=5)

# Отображение захваченной области экрана
label_screen = tk.Label(root, bg="#1c1c1c")
label_screen.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

# Запуск интерфейса
root.mainloop()
